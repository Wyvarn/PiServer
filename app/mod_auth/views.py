from . import auth
from flask import render_template, redirect, url_for, current_app, session, request, flash
from datetime import datetime
from app import db
from flask_login import login_user, login_required, current_user, logout_user
from app.models import PiCloudUserAccount, PiCloudUserProfile
from app.forms import LoginForm, RegisterForm, RecoverPasswordForm, ChangePasswordForm
from app.mod_auth.tokens import generate_token, confirm_token
from app.mod_auth.email import send_mail


@auth.route('/login', methods=["POST", "GET"])
def login():
    """
    Login route/view to be accessed at auth/login route
    :return: a login view
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
                                                          email=register_form.email.data,
                                                          username=register_form.email.data,
                                                          registered_on=datetime.now(),
                                                          confirmed=False)
                # add to db session and commit
                db.session.add(picloud_user_account)
                db.session.add(picloud_user_profile)
                db.session.commit()

                # build token and send an email for user confirmation
                token = generate_token(picloud_user_profile.email)

                # _external adds the full url that includes the hostname and port
                confirm_url = url_for("auth.confirm_email", token=token, _external=True)

                # build the message
                html = render_template("auth/confirm_email.html", confirm_url=confirm_url)
                subject = "Please confirm you email"

                # send the user an email
                send_mail(picloud_user_profile.email, subject, html)

                # login the user
                login_user(picloud_user_account)

                # flash the message
                flash(message="A confirmation email has been sent to {}".format(picloud_user_account.email),
                      category="success")

                # todo: redirect unconfirmed users to the unconfirmed view
                # return redirect(url_for("dashboard.unconfirmed"))

    return render_template("auth/register.html", register_form=register_form)


# todo: forgot password view and add tests
@auth.route("/recover_password", methods=["POST", "GET"])
def forgot_password():
    """
    View function for recovery passwords. This is accessed when a user clicks on forgot password
    and is redirected to a form to allow them to change their passwords based on the email provided
    will check if the email exists in the database and send a token for recover of password
    :return: forgot password view
    """
    recover_password_form = RecoverPasswordForm(request.form)
    # if request is post
    if request.method == "POST":
        # if the form is valid on submission and the user email exists in the db
        if recover_password_form.validate_on_submit() and recover_password_form.validate_form():
            # get their email address
            email = recover_password_form.email.data

            # create token
            token = generate_token(email)

            # create a recover password url
            recover_pass_url = url_for("auth.recover_password", token=token, _external=True)

            # build the message
            html = render_template("auth/recover_pass_msg.html", recover_pass_url=recover_pass_url)
            subject = "PiCloud password recovery"

            # send the user an email
            send_mail(to=email, subject=subject, template=html)

            # flash a message that the message has been sent to their email
            flash(message="A recovery password link has been sent to {}".format(email),
                  category="success")

            # redirect to home page
            return redirect(url_for("home.index"))
    return render_template("auth/recover_password.html", recover_password_form=recover_password_form)


@auth.route("/recover-password/<token>", methods=["POST", "GET"])
def recover_password(token):
    """
    Recover password route which will allow user to change their password. will perform a check on the
     token to confirm that the email is indeed correct, then proceed to allow changing of their password
    :param token: token from the email sent when user recovered password, will contain the email
    :return: a redirect to login page once password has been reset
    """

    change_password_form = ChangePasswordForm(request.form)

    # extract the email from the token
    email = confirm_token(token)

    # if email is not valid
    if not email:
        # flash a message and redirect to login
        flash(message="The confirmation link has expired or is invalid", category="error")
        return redirect(url_for("auth.login"))

    else:
        if request.method == "POST":

            if change_password_form.validate_on_submit():
                # get the user
                picloud_user = PiCloudUserAccount.query.filter_by(email=email).first()

                # change the password
                picloud_user.password_hash = change_password_form.password_field_1.data

                db.session.add(picloud_user)
                db.session.commit()

                flash(message="Password has been reset", category="success")
                return render_template("auth/change_password.html",
                                       change_password_form=change_password_form)

    return render_template("auth/change_password.html", change_password_form=change_password_form)


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


@auth.route("/logout")
@login_required
def logout():
    """
    Logout view which logs out the user from the application and redirects to home page
    :return: redirect to home page
    """
    logout_user()
    return redirect(url_for("home.index"))
