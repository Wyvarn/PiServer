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
