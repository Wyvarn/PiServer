from . import home
from flask import render_template, redirect, flash, request
import os


@home.route("")
@home.route("index")
@home.route("home")
def index():
    """
    Main view, or home page of the application
    :return: renders home page template
    """
    media = os.listdir("/media/")
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
