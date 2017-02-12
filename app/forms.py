from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from app.models import PiCloudUserAccount


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


class RegisterForm(FlaskForm):
    """
    Register form for new users
    """
    first_name = StringField(validators=[DataRequired()])
    last_name = StringField(validators=[DataRequired()])
    email = StringField(validators=[DataRequired(), Email()])
    password = PasswordField(validators=[DataRequired(),
                                         EqualTo("verify_password", message="Passwords must match"),
                                         Length(min=8, max=15)])
    verify_password = PasswordField(validators=[DataRequired()])
    register_button = SubmitField("REGISTER")

    def validate_form(self):
        """
        Validates the form by checking the database for the email submitted
        This way the register form will communicate directly with the Database before
        submitting data
        :return: True or false based on the response from the db
        :rtype: bool
        """
        initial_validation = super(RegisterForm, self).validate()
        if not initial_validation:
            return False
        user = PiCloudUserAccount.query.filter_by(email=self.email.data).first()
        if user:
            self.email.errors.append("Email already exists")
            return False
        return True


class RecoverPasswordForm(FlaskForm):
    """
    Recover password form, or forgot password form
    """
    email = StringField(validators=[DataRequired(), Email()])
    send_mail_btn = SubmitField("RECOVER PASSWORD")

# todo: add contact form