
from datetime import datetime
from flask import(
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from application.auth import login_required, tech_required
from application.db import DBCM
from application.forms import TicketSubmissionForm, TicketForm

bp = Blueprint('ticket', __name__, url_prefix='/ticket')


@bp.route('/<int:ticket_id>', methods=('GET', 'POST'))
@tech_required
def edit_ticket(ticket_id):
    """ Form for a TECH user to view/edit a ticket."""
    form = TicketForm()
    message = None
    if form.validate_on_submit():
        conn = DBCM.get_conn()
        cur = conn.cursor()
        cur.execute(
            """
            UPDATE ticket 
            SET notes = :1
            WHERE ticket_id = :2
            """,
            [ form.notes.data, form.ticket_id.data ]
        )
        conn.commit()
        cur.close()
        message = "Notes updated."
    else:
        res = DBCM.get_result(
            """
                SELECT subject, description, created_at, started_at, finished_at, notes,
                    (SELECT username FROM app_user WHERE user_id = assigned_to) assigned_to,
                    (SELECT username FROM app_user WHERE user_id = submitted_by) submitted_by
                FROM ticket WHERE ticket_id = :1
            """,
            [ ticket_id ]
            ).fetchone()

        form.ticket_id.data = ticket_id
        form.subject.data = res['SUBJECT']
        form.submitted_by.data = res['SUBMITTED_BY']
        form.description.data = res['DESCRIPTION']
        form.created_at.data = res['CREATED_AT']
        form.started_at.data = res['STARTED_AT']
        form.finished_at.data = res['FINISHED_AT']
        form.notes.data = res['NOTES']

    if form.errors:
        print(form.errors)

    return render_template('ticket/ticket.html', form=form, message=message)


@bp.route('/submit', methods=('GET', 'POST'))
@login_required
def submit_ticket():
    """ Ticket submission view """
    form = TicketSubmissionForm()
    
    if form.validate_on_submit():
        conn = DBCM.get_conn()
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO ticket ( subject, submitted_by, description, created_at)
            VALUES (:1, :2, :3, systimestamp)
            """,
            [ form.subject.data, g.user['USER_ID'], form.description.data ]
        )
        conn.commit()
        cur.close()
        flash("Thanks for your ticket we're on it.", 'success')
        return render_template('base.html')
        
    return render_template('ticket/submit.html', form=form)


@bp.route('/dashboard')
@tech_required
def ticket_dashboard():
    """ Return the dashboard view."""
    res = DBCM.get_result(
        """
            SELECT ticket_id, subject, description, created_at, started_at, finished_at, notes,
                (SELECT username FROM app_user WHERE user_id = assigned_to) assigned_to,
                (SELECT username FROM app_user WHERE user_id = submitted_by) submitted_by
            FROM ticket
            ORDER BY ticket_id DESC
        """
    ).fetchmany()
    return render_template('ticket/dashboard.html', data = res)

    
@bp.route('/<int:ticket_id>/start', methods=('POST',))
@tech_required
def start_ticket(ticket_id):
    """ Start work on a ticket."""
    conn = DBCM.get_conn()
    cur = conn.cursor()
    stamp = cur.var(datetime)
    userid = g.user['USER_ID']
    
    cur.execute(
        """ 
            UPDATE ticket
            SET started_at = nvl(started_at, systimestamp), 
                assigned_to = nvl(assigned_to, :1)
            WHERE ticket_id = :2
            RETURNING started_at INTO :3
        """,
        [ userid, ticket_id, stamp ]
    )
    conn.commit()
    cur.close()
    stamp = stamp.getvalue()[0]
    return str(stamp)


@bp.route('/<int:ticket_id>/finish', methods=('POST',))
@tech_required
def finish_ticket(ticket_id):
    """ Finish work on a ticket."""
    conn = DBCM.get_conn()
    cur = conn.cursor()
    stamp = cur.var(datetime)

    cur.execute(
        """ 
            UPDATE ticket
            SET finished_at = nvl(finished_at, systimestamp)
            WHERE ticket_id = :1
            RETURNING finished_at INTO :2        
        """,
        [ ticket_id, stamp ]
    )
    conn.commit()
    cur.close()
    stamp = stamp.getvalue()[0]
    if str(stamp) is None:
        raise Exception('fatal error')
    return str(stamp)
