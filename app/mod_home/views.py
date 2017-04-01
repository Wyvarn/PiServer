"""
Home route, entry point of application
"""
from getpass import getuser
from . import home
from flask import render_template, redirect, flash, request
import os


@home.route("")
@home.route("index")
@home.route("home")
def index():
    """
    Main view, or home page of the application
    Will get the username of the current logged in user. This will be used to get the folders that 
    this user can access. WIll be used specifically to access the media directory that the user can
    access
    :return: renders home page template
    """
    media = os.listdir("/media/{}/".format(getuser()))
    return render_template("home/index.html", media=media)


@home.route("contact")
def contact():
    """
    Contact page
    :return: renders the contact page template
    """
    return render_template("home/contact.html")


@home.route("about")
def about():
    """
    About page
    :return: renders template for the about page
    """
    return render_template("home/about.html")
