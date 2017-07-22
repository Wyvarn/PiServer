import jinja2
import os
from celery import Celery
from flask import render_template, Flask
from flask_login import LoginManager
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from config import config

login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.login_view = "auth.login"
db = SQLAlchemy()
mail = Mail()

# create global instance of celery and delay its configuration until create_app is initialized
celery = Celery(__name__, broker=os.environ.get("CELERY_BROKER_URL"))


class PiCloudApp(Flask):
    """
    This allows us to separate templates and static files by blueprints
    also allows for a much cleaner design, even though we can still separate the template
    and resource files by blueprints without this pattern, this servers as an easier
     approach when designing the application
    """

    def __init__(self):
        """
        jinja_loader object (a FileSystemLoader pointing to the global templates folder)
        is being replaced with a ChoiceLoader object that will first search the normal
        FileSystemLoader and then check a PrefixLoader that we create
        """
        Flask.__init__(self, __name__, template_folder="templates", static_folder="static")
        self.jinja_loader = jinja2.ChoiceLoader([
            self.jinja_loader,
            jinja2.PrefixLoader({}, delimiter=".")
        ])

    def create_global_jinja_loader(self):
        return self.jinja_loader

    def register_blueprint(self, blueprint, **options):
        Flask.register_blueprint(self, blueprint, **options)
        self.jinja_loader.loaders[1].mapping[blueprint.name] = blueprint.jinja_loader


def create_app(config_name):
    """
    This defines a new application Web Site Gateway Interface
    Will be used to create a new application instance based on the configurations it is given
    All configurations for the application will come here, whenever a new application is registered,
    These configurations will be set and used.
    :param config_name: The configuration to use, either Testing, Production, Development, found in config.py
    :return: A new application WSGI
    """
    app = PiCloudApp()

    # app configurations, considering config is a dictionary, we pass in the key that we will receive
    app.config.from_object(config[config_name])

    # CONFIGURE celery
    celery.conf.update(app.config)

    # initialize the application with the login manager
    login_manager.init_app(app)

    # initialize the db
    db.init_app(app)

    # initialize flask mail
    mail.init_app(app)

    request_handlers(app, db)

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
    def page_not_found(e):
        return render_template('errorpages/404.html'), 404

    @app.errorhandler(403)
    def forbidden_403(e):
        return render_template("errorpages/403.html"), 403

    @app.errorhandler(410)
    def resource_gone(e):
        return render_template("errorpages/410.html"), 410

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template("errorpages/500.html"), 500


def request_handlers(picloud_app, picloud_db):
    """
    Handles requests sent to the application, Requests will mostly be first request sent
    and before request sent
    :param picloud_app: the api cloud application
    :param picloud_db: the pi cloud database
    """

    @picloud_app.before_first_request
    def before_first_request():
        """
        we initialize Rollbar before first request
        :return:
        """
        pass


def register_blueprints(app_):
    """
    Registers all the blueprints in the application
    Whenever a new module is created, ensure that it is registered here for it to work
    :param app: Current flask application object
    """
    from app.mod_auth import auth
    from app.mod_home import home
    from app.mod_dashboard import dashboard
    from app.mod_api import api
    from app.mod_media import media

    app_.register_blueprint(media)
    app_.register_blueprint(auth)
    app_.register_blueprint(home)
    app_.register_blueprint(dashboard)
    app_.register_blueprint(api)


def set_logger(app, config_name):
    """
    Sets logging of error messages in case they occur in the application. This will send an email to
    any of the administrators, or all of the administrators.
    This should work when the application is in production
    Will also record any errors to a log file
    RotatingFileHandler is used to limit the number of logs to 1MB and limit the backup to 10 files
    logging.formatter will enable us to format the log messages and get the line number that brought up the issue as
    well as the stack trace.
    :param app: current Flask app
    :param config_name: the configuration to use this, normally in Production
    """
    import logging
    from logging.handlers import SMTPHandler, RotatingFileHandler
    MAIL_SERVER = app.config.get("MAIL_SERVER")

    if config_name == "production":
        if not app.debug and MAIL_SERVER != "":
            credentials = None

            MAIL_USERNAME = app.config.get("MAIL_USERNAME")
            MAIL_PASSWORD = app.config.get("MAIL_PASSWORD")

            if MAIL_USERNAME or MAIL_PASSWORD:
                credentials = (MAIL_USERNAME, MAIL_PASSWORD)

            mail_handler = SMTPHandler(mailhost=(MAIL_SERVER, app.config.get("MAIL_HOST")),
                                       fromaddr="no-reply@" + MAIL_SERVER,
                                       toaddrs=app.config.get("ADMINS"),
                                       subject="PiCloud app failure",
                                       credentials=credentials)
            mail_handler.setLevel(logging.ERROR)
            app.logger.addHandler(mail_handler)

        if not app.debug and os.environ.get("HEROKU") is None:
            # log file will be saved in the tmp directory
            file_handler = RotatingFileHandler(filename="tmp/picloud.log", mode="a", maxBytes=1 * 1024 * 1024,
                                               backupCount=10)
            file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%('
                                                        'lineno)d]'))
            app.logger.setLevel(logging.INFO)
            file_handler.setLevel(logging.INFO)
            app.logger.addHandler(file_handler)
            app.logger.info("PiCloud")
