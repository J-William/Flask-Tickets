
from flask import(
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from application.auth import login_required, tech_required
from application.db import DBCM
from application.forms import TicketSubmissionForm, TicketForm

bp = Blueprint('ticket', __name__, url_prefix='/ticket')

@bp.route('/<int:ticket_id>', methods=('GET', 'POST'))
def view_ticket(ticket_id):

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

    return render_template('ticket/ticket.html', form=form, message=message)


@bp.route('/submit', methods=('GET', 'POST'))
@login_required
def submit_ticket():
    """ Ticket creation view """
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
        """
    ).fetchmany()
    return render_template('ticket/dashboard.html', data = res)

    
