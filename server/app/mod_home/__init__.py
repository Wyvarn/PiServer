from flask import Blueprint

home = Blueprint(name="home", url_prefix="/", template_folder="templates",
                 static_folder="static",import_name=__name__)

from . import views
