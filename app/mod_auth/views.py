from . import auth
from flask import render_template, redirect, url_for, current_app, session, request, flash
from datetime import datetime
from app import db
from flask_login import login_user, login_required, current_user, logout_user
from app.models import PiCloudUserAccount, PiCloudUserProfile
from app.forms import LoginForm, RegisterForm, RecoverPasswordForm


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
                                                          registered_on=datetime.now())

                db.session.add(picloud_user_account)
                db.session.add(picloud_user_profile)
                db.session.commit()

                # todo
                # build token and send an email for user confirmation
    pass


@auth.route("/recover_password", methods=["POST", "GET"])
def forgot_password():
    pass
