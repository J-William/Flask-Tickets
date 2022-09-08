from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, DateTimeField
from wtforms.validators import DataRequired

class TicketSubmissionForm(FlaskForm):
    """ The ticket submission form."""
    subject = StringField(
        'Subject',
        [DataRequired()]
    )
    description = TextAreaField(
        'Description',
        [DataRequired()]
    )
    submit = SubmitField('Submit')

class TicketForm(FlaskForm):
    """ The full ticket form."""
    ticket_id = StringField(
        'ID'
    )
    assigned_to = StringField(
        'Assigned To:'
    )
    submitted_by = StringField(
        'Submitted By:'
    )
    subject = StringField(
        'Subject'
    )
    description = TextAreaField(
        'Description'
    )

    created_at = StringField(
        'Created:'
    )
    started_at = StringField(
        'Started:'
    )
    finished_at = StringField(
        'Finished:'
    )
    notes = TextAreaField(
        'Notes'
    )
    submit = SubmitField('Update')
    start = SubmitField('Start')
