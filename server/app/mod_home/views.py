"""
Home route, entry point of application
"""
from . import home
from flask import redirect, request, current_app, jsonify
import os
from collections import defaultdict


@home.route("")
@home.route("index")
@home.route("home")
def index():
    """
    Will get the username of the current logged in user. This will be used to get the folders
    and files that this user can access in the media directory. The media directory may have
    files and folders/directories, thus this will draw a tree structure as a JSON and return
    response back to client
    :return: json response of files in /media/username path
    :rtype: dict
    """
    # obtain the path to walk down
    media_path_tree = current_app.config.get("MEDIA_PATH")

    # we can create the response we send out
    context = defaultdict(list)

    # sanity check to determine if there are any files/directories to begin with
    # if the path has nothing, then return message to user
    if len(os.listdir(media_path_tree)) == 0:
        return jsonify(dict(message="No media mounted", success=False, files=0,
                            directories=0))

    # at this point we can ascertain that this path has directories and/or files
    # we start by getting the number of files and directories
    context["directories"], context["files"] = get_total_dirs_and_files(media_path_tree)

    # this is because the root path will be counted as a directory
    # to avoid that we start the count from -1

    # the root path
    context["root_path"] = media_path_tree
    context["directory_tree"] = defaultdict(dict)

    # get the media names mounted, these will be the root directories in the media/username
    # root path
    # this will also add the path to the directory tree key as its own object
    # which will be populated later
    for path in os.listdir(media_path_tree):
        path_full_name = os.path.join(media_path_tree, path)
        if os.path.isdir(path_full_name):
            context["media"].append(path)
            context["directory_tree"][path] = {}
            context["directory_tree"][path]["files"] = 0
            context["directory_tree"][path]["dirs"] = 0

    # we walk down this key and retrieve the directories and add the directories
    # as keys and their files as objects
    for key in context["directory_tree"].keys():

        # this will return /media/username/key/
        full_path = os.path.join(media_path_tree, key)

        for dirpath, dirnames, filenames in os.walk(full_path):
            # count the number of files and directories we have
            # and state the root directories

            context["directory_tree"][key]["files"] += len(filenames)
            context["directory_tree"][key]["dirs"] += len(dirnames)

            # under each directory we list the files and sub directories available

            directories = create_create_full_paths(dirpath, dirnames)
            files = create_create_full_paths(dirpath, filenames)

            # update the response dictionary
            if len(directories) > 0:
                context["dir"].append(directories)
            if len(files) > 0:
                context["f"].append(files)

    # return the unpacked dictionary response
    return jsonify(message="Media(s) mounted", success=True, **context)


def create_create_full_paths(root_path, path_list):
    """
    Create paths to the given directories and file names of the given
    :param root_path to the directory or file
    :param path_list list of file names/directories
    :return: List with the full path to the file or directory
    :rtype: list
    """
    return list(map(lambda x: os.path.join(root_path, x), path_list))


def list_files(startpath):
    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * level
        print('{}{}/'.format(indent, os.path.basename(root)))
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            print('{}{}'.format(subindent, f))


def get_total_dirs_and_files(root_path):
    """
    Returns the number of directories and files in the media root path
    :param root_path: media root path
    :return: tuple with the number of directories and files
    :rtype: tuple
    """
    # we start the dir num with -1 to exclude the root path
    dir_num, file_num = -1, 0
    for dirpath, directories, filenames in os.walk(root_path):
        dir_num += len(directories)
        file_num += len(filenames)

    return dir_num, file_num
