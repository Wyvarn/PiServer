"""
Home route, entry point of application
"""
from getpass import getuser
from . import home
from flask import render_template, redirect, flash, request, current_app, jsonify
import os


# noinspection PyUnresolvedReferences
@home.route("")
@home.route("index")
@home.route("home")
def index():
    """
    Main view, or home page of the application
    Will get the username of the current logged in user. This will be used to get the folders
     that this user can access. WIll be used specifically to access the media directory that
     the user can access
    :return: renders home page template
    """
    context = dict()

    # check which current config we are running and mount to that file system
    if os.environ.get("FLASK_CONFIG") == "develop":
        media = os.listdir(current_app.config.get("LOCAL_MEDIA_PATH"))
        # todo:
        # classify the drives and files in the media/username directory into either files
        # or directories, then group them into directories list or file list
        # response should be something like
        # {
        #   dirs : [...]
        #   files : [...]
        # }
        context = dict(medias=media)
        return jsonify(**context)

    elif os.environ.get("FLASK_CONFIG") == "production":
        media = os.listdir(current_app.config.get("SERVER_MEDIA_PATH"))
        context = dict(medias=media)
        return jsonify(**context)

    return render_template("home.index.html", **context)


@home.route("contact")
def contact():
    """
    Contact page
    :return: renders the contact page template
    """
    return render_template("home.contact.html")


@home.route("about")
def about():
    """
    About page
    :return: renders template for the about page
    """
    return render_template("home.about.html")
