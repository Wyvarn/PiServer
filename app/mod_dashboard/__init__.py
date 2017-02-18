from flask import Blueprint

dashboard = Blueprint(name="dashboard", url_prefix="dashboard/", template_folder="dashboard", import_name=__name__)

from app.mod_dashboard import views