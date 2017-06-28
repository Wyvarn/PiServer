"""
Home route, entry point of application
"""
from . import home
from flask import redirect, request, current_app, jsonify
import os


@home.route("")
@home.route("index")
@home.route("home")
def index():
    """
    Main view, or home page of the application
    Will get the username of the current logged in user. This will be used to get the folders
     that this user can access. WIll be used specifically to access the media directory that
     the user can access
    :return: json response of files in /media/username path
    :rtype: dict
    """
    # obtain the path to walk down
    media_path_tree = current_app.config.get("MEDIA_PATH")

    # this will be the dict response we send out
    context = {}

    # walk down the tree and retrieve files and directories
    for dirpath, dirnames, filenames in os.walk(media_path_tree):
        directories = create_create_full_paths(dirpath, dirnames)
        files = create_create_full_paths(dirpath, filenames)

        # update the response dictionary
        context["directories"] = directories
        context["filenames"] = files

    # return the unpacked dictionary response
    return jsonify(**context)


def create_create_full_paths(root_path, path_list):
    """
    Create paths to the given directories and filenames of the given
    :param root_path to the directory or file
    :param path_list list of filenames/directories
    :return: List with the full path to the file or directory
    :rtype: list
    """
    return list(map(lambda x: os.path.join(root_path, x), path_list))
