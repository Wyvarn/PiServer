"""
This will handle media files that are in the media directory if the Pi
"""
from . import media
from getpass import getuser
from flask import render_template, redirect, url_for
import os


@media.route("<drive>")
def view_media(drive):
    """
    View media files that are in the drive folder
    :param drive: the drive to display
    :return: view template for files in the media file
    """
    drive_folders = os.listdir("/media/{}/{}".format(getuser(), drive))
    return render_template("media/media.html", drive_name=drive, drive=drive_folders)


@media.route("<drive_name>/<folder>")
def view_folder_in_drive(drive_name, folder):
    """
    
    :param drive: 
    :return: 
    """
