from flask import render_template, Flask
from config import config
from flask_login import LoginManager

login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.login_view = "auth.login"


def create_app(config_name):
    """
    This defines a new application Web Site Gateway Interface
    Will be used to create a new application instance based on the configurations it is given
    All configurations for the application will come here, whenever a new application is registered,
    These configurations will be set and used.
    :param config_name: The configuration to use, either Testing, Production, Development, found in config.py
    :return: A new application WSGI
    """
    app = Flask(__name__, template_folder="templates", static_folder="static")

    # app configurations, considering config is a dictionary, we pass in the key that we will receive
    app.config.from_object(config[config_name])

    # initialize the application with the login manager
    login_manager.init_app(app)

    # register error pages and blueprints
    error_handlers(app)
    register_blueprints(app)

    # finally return the new flask application
    return app


def error_handlers(app):
    """
    Function that will handle the erros encountered in the application
    :param app: Application object
    """

    # Error handler for page not found
    @app.errorhandler(404)
    def not_found():
        return render_template('errorpages/404.html')

    @app.errorhandler(403)
    def error_403():
        return render_template("errorpages/403.html")

    @app.errorhandler(403)
    def error_500():
        return render_template("errorpages/500.html")

    @app.errorhandler(400)
    def not_found():
        return render_template('errorpages/400.html')


def register_blueprints(app):
    """
    Registers all the blueprints in the application
    Whenever a new module is created, ensure that it is registered here for it to work
    :param app: Current flask application object
    """
    from app.mod_auth import auth

    app.register_blueprint(auth)
