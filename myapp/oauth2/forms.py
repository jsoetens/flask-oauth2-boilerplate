from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Email


class SignInForm(FlaskForm):

    email_address = StringField(validators=[InputRequired(), Email()])
    password = PasswordField(validators=[InputRequired()])
