"""
This will handle media files that are in the media directory if the Pi
"""
from . import media
from getpass import getuser
from flask import render_template, redirect, url_for, current_app
import os


@media.route("<drive_name>")
def view_media(drive_name):
    """
    View media files that are in the drive folder
    :param drive_name: the drive to display
    :return: view template for files in the media file
    """
    try:
        context = {
            "drive": os.listdir("/media/{}/{}".format(getuser(), drive_name)),
            "drive_name": drive_name
        }
        return render_template("media.media.html", **context)
    except FileNotFoundError:
        context = {
            "drive_name": drive_name
        }
        return render_template("media.media.html", **context)

        # for root, dirs, files in os.walk("/media/{}/{}".format(getuser(), drive)):
        #     level = root.replace(drive, '').count(os.sep)
        #     indent = ' ' * 4 * (level)
        #     print('{}{}/'.format(indent, os.path.basename(root)))
        #     subindent = ' ' * 4 * (level + 1)
        #     for f in files:
        #         print('{}{}'.format(subindent, f))


@media.route("<drive_name>/<folder_or_file>")
def view_folder_in_drive(drive_name, folder_or_file):
    """
    Enables viewing a particular folder in the drive or the file
    :param folder_or_file: the folder to open or the file to view
    :param drive_name: the name of the connected drive
    :return: view of the folder or the file 
    """
    root_path = "/media/{}/{}/{}".format(getuser(), drive_name, folder_or_file)

    # perform a check to determine if the folder is a folder or a file
    if os.path.isdir(root_path):
        context = dict(
            folders=os.listdir(root_path),
            drive_name=drive_name
        )
        return render_template("media.media_dir.html", **context)
    # if not a folder then it is obviously a file :D
    # return redirect(url_for("media.view_file_in_drive", drive_name=drive_name, file=folder_or_file))


@media.route("<drive_name>/<file>")
def view_file_in_drive(drive_name, file):
    """
    Views files in the drive
    :return: 
    """
    return render_template("media.media_file.html", file=file)
