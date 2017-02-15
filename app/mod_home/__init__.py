from flask import Blueprint

home = Blueprint(name="home", url_prefix="/", template_folder="home", import_name=__name__)

from app.mod_home import views
