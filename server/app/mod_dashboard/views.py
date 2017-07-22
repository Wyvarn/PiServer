from . import dashboard
from flask import render_template
from flask_login import login_required


@dashboard.route("<username>")
@login_required
def dashboard(username):
    """
    This is the user's dashboard that is accessed only when a user has successfully logged in
    also only accessed after log in.
    :param username: the user's username as they registered it
    :return: template view of the user's dashboard
    """
    return render_template("dashboard/dashboard.html")