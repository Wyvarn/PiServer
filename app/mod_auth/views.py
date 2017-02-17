from . import auth
from flask import render_template, redirect, url_for, current_app, session, request, flash
from datetime import datetime
from app import db
from flask_login import login_user, login_required, current_user, logout_user
from app.models import PiCloudUserAccount, PiCloudUserProfile
from app.forms import LoginForm, RegisterForm, RecoverPasswordForm
from app.mod_auth.tokens import generate_confirmation_token, confirm_token


@auth.route('/login', methods=["POST", "GET"])
def login():
    """
    Login route/view to be accessed at auth/login route
    :return:
    """
    login_form = LoginForm(request.form)
    if request.method == "POST":
        if login_form.validate_on_submit():
            # find the user from the database
            picloud_user = PiCloudUserAccount.query.filter_by(email=login_form.email.data).first()

            # if the user is valid and their password checks out, log them in
            if picloud_user is not None and picloud_user.verify_password(login_form.password.data):
                # login user
                login_user(picloud_user, login_form.remember_me.data)

                # display a message
                flash(message="Welcome back {}!".format(picloud_user.username), category="success")

                # todo: dashboard redirect
                # redirect to dashboard
                # return redirect(url_for("", username=picloud_user.username))
                print("Login success")
            # flash error message
            flash(message="Invalid email or password", category="error")
    return render_template("auth/login.html", login_form=login_form)


@auth.route("/register", methods=["POST", "GET"])
def register():
    """
    Register route/view for registering new users
    Will build both the user account and user profile add them to the database and send an email verification
    This will then login the user to their dashboard. The login will be to the unconfirmed section of their
    dashboard, this will allow the user to then either resend an email verification or check their mail
    :return: render register form or redirect to login view once there is successful register
    """
    register_form = RegisterForm(request.form)

    if request.method == "POST":
        if register_form.validate_on_submit():
            # check if the user credentials already exist
            picloud_user = PiCloudUserAccount.query.filter_by(email=register_form.email.data).first()

            # if they do no exist, create this user
            if picloud_user is None:
                picloud_user_profile = PiCloudUserProfile(first_name=register_form.first_name.data,
                                                          last_name=register_form.last_name.data,
                                                          email=register_form.email.data,
                                                          accept_terms=register_form.accept_terms.data)
                picloud_user_account = PiCloudUserAccount(password_hash=register_form.password.data,
                                                          registered_on=datetime.now(),
                                                          confirmed=False)

                db.session.add(picloud_user_account)
                db.session.add(picloud_user_profile)
                db.session.commit()


                # build token and send an email for user confirmation
                token = generate_confirmation_token(picloud_user_profile.email)

                # login the user
                login_user(picloud_user_account)

                # flash the message
                flash(message="A confirmation email has been sent to {}".format(picloud_user_account.email),
                      category="success")

                # redirect unconfirmed users to the unconfirmed view
                # return redirect(url_for(""))

    return render_template("auth/register.html", register_form=register_form)


@auth.route("/recover_password", methods=["POST", "GET"])
def forgot_password():

    pass


@auth.route("/confirm/<token>")
@login_required
def confirm_email(token):
    """
    Route to confirm user email. Checks if the user's token is valid and their account is valid.
    If the user is already confirmed, redirect them to login to their account
    If the token checks out and the email is extracted from the token successfully, we get the user details
    from the database and update the confirmed column to True and set the date the confirmation took place

    :param token: token generated in user registration
    :return: a redirect to login.
    """

    # if the current user is already confirmed, redirect them to login
    if current_user.confirmed:
        flash(message="Account already confirmed. Please login", category="success")
        return redirect(url_for("auth.login"))

    # extract the email from the token, this will either bring back false or the email address
    email = confirm_token(token)

    # get the user by their email
    picloud_user = PiCloudUserProfile.query.filter_by(email=current_user.email).first_or_404()

    # if the email is not valid
    if not email:
        flash(message="The confirmation link has expired or is invalid", category="error")
    # if the email matches the current user's email
    elif picloud_user.email == email:
        picloud_user.confirmed = True
        picloud_user.confirmed_on = datetime.now()

        db.session.add(picloud_user)
        db.session.commit()

        flash(message="You have confirmed your account, thank you", category="success")

        return redirect(url_for("auth.login"))
    return redirect(url_for("auth.login"))




