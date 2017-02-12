from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from app.models import PiCloudUserAccount, PiCloudUserProfile


class LoginForm(FlaskForm):
    """
    Login form for user login
    :cvar email: user email
    :cvar password: user password
    :cvar login_button: login button
    :cvar remember_me: checkbox to remember user once they are logged in
    """
    email = StringField(validators=[DataRequired(), Email()])
    password = PasswordField(validators=[DataRequired()])
    login_button = SubmitField("LOG IN")
    remember_me = BooleanField()

    # def __init__(self, email, password, login_button, remember_me):
    #     self.email = email
    #     self.password = password
    #     self.login_button = login_button
    #     self.remember_me = remember_me


class RegisterForm(FlaskForm):
    """
    Register form for new users
    """


class RecoverPasswordForm(FlaskForm):
    """
    Recover password form, or forgot password form
    """
