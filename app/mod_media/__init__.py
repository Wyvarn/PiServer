from flask import Blueprint

media = Blueprint(name="media", url_prefix="/media/", import_name=__name__)

from . import views
