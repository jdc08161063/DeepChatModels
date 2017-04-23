"""apps/forms.py: """

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, InputRequired
from wtforms.validators import ValidationError


def bad_chars(form, string_field):
    for c in r";'`":
        if c in string_field.data:
            raise ValidationError('DONT TYPE DAT')


class ChatForm(FlaskForm):
    """Creates a chat_form for users to enter input."""
    message = StringField('message', validators=[DataRequired()])


class UserForm(FlaskForm):
    """Form for creating/editing a user."""
    name = StringField('name', validators=[DataRequired(), bad_chars])
    submit = SubmitField('Submit')


