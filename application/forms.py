from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, Email

class TicketForm(FlaskForm):
    """ The ticket form"""
    subject = StringField(
        'Subject',
        [DataRequired()]
    )
    description = TextAreaField(
        'Description',
        [DataRequired()]
    )
    submit = SubmitField('Submit')

