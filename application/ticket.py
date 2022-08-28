
from flask import(
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from application.db import DBCM
from application.forms import TicketForm

bp = Blueprint('ticket', __name__, url_prefix='/ticket')

@bp.route('/')
def get_tickets():
    return 'Coming Soon'

@bp.route('/submit', methods=('GET', 'POST'))
def submit_ticket():
    form = TicketForm()
    if form.validate_on_submit():
        subject = form.subject.data
        description = form.description.data

        conn = DBCM.get_conn()
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO ticket ( subject, submitted_by, description, created_at)
            VALUES (?, ?, ?, systimestamp)
            """,
            [subject, g.user['USER_ID'], description]
        )
        conn.commit()
        cur.close()
    return render_template('ticket/submit.html', form=form)