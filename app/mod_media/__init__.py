from flask import Blueprint
from getpass import getuser

media = Blueprint(name="media", url_prefix="/media/" + getuser() + "/", import_name=__name__)

from . import views
