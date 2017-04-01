"""
This will handle media files that are in the media directory if the Pi
"""
from . import media
from flask import render_template, redirect, url_for
import os


@media.route("<drive>")
def view_media(drive):
    """
    View media files that are in the drive folder
    :param drive: 
    :return: view template for files in the media file
    """
    drive_folders = os.listdir("/media/" + drive)
    return render_template("media/media.html", drive_name=drive, folders=drive_folders)