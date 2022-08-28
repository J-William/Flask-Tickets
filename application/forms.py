from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, Email

class TicketForm(FlaskForm):
    """ The login form"""
    subject = StringField(
        'Username',
        [DataRequired()]
    )
    description = TextAreaField(
        'Description',
        [DataRequired()]
    )
    submit = SubmitField('Submit')

