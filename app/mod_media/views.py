"""
This will handle media files that are in the media directory if the Pi
"""
from . import media
from getpass import getuser
from flask import render_template, redirect, url_for, current_app
import os


@media.route("<drive>")
def view_media(drive):
    """
    View media files that are in the drive folder
    :param drive: the drive to display
    :return: view template for files in the media file
    """
    drive_folders = os.listdir("/media/{}/{}".format(getuser(), drive))
    context = {
        "drive_folders": drive_folders,
        "drive_name": drive
    }

    return render_template("media/media.html", **context)


@media.route("<drive_name>/<folder_or_file>")
def view_folder_in_drive(drive_name, folder_or_file):
    """
    Enables viewing a particular folder in the drive or the file
    :param folder_or_file: the folder to open or the file to view
    :param drive_name: the name of the connected drive
    :return: view of the folder or the file 
    """
    root_path = "media/{}/{}/{}".format(getuser(), drive_name, folder_or_file)

    # perform a check to determine if the folder is a folder or a file
    if os.path.isdir(root_path):
        # view the directory
        folders = os.listdir(root_path)
        return render_template("media/media_dir.html", drive_name=drive_name, drive=folders)

    # if not a folder then it is obviously a file :D
    return redirect(url_for("media.view_file_in_drive", drive_name=drive_name, file=folder_or_file))


@media.route("<drive_name>/<file>")
def view_file_in_drive(drive_name, file):
    """
    Views files in the drive
    :return: 
    """
    return "file"
