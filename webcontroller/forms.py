import quart.flask_patch

from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField, BooleanField, StringField
from wtforms.validators import DataRequired, Length

class LoginForm(FlaskForm):
    token = PasswordField('Token', validators=[DataRequired()])

    remember = BooleanField('Remember me')
    submit = SubmitField('Login')


class PresenceForm(FlaskForm):
    new_pr = StringField("New Presence", validators=[Length(max=100)])

    submit = SubmitField('change')
