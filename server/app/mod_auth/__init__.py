from flask import Blueprint

# register this blueprint, giving it a name and prefix, template folder
auth = Blueprint("auth", url_prefix="/auth", template_folder="auth", import_name=__name__)

# made as a last import to avoid circular imports
from . import views
