from flask import Flask

from config import config

from .extensions import debug_toolbar, csrf, login_manager, oauth
from .models.db_orm import db


# We are using application factory functions to create the application.
# http://flask.pocoo.org/docs/0.12/patterns/appfactories
# Flask extensions can use an app specific
# initialization inside the factory function via the init_app() method
# - no more global app/app.route decorator so all endpoints need to be moved to
# blueprints
# - use current_app context variable to access application


def create_app(config_name):
    # The configuration check is handled in autoapp.py

    # Flask uses the name argument to determine the root path of
    # the application so that it later can find resource files
    # relative to the location of the application.
    app = Flask(__name__)

    # Read the configuration
    app.config.from_object(config[config_name])

    # Initialize Flask extensions
    # Initialize extension SQLAlchemy
    db.init_app(app)

    # Initialize extension Flask-DebugToolbar
    # By default, it's only enabled in debug mode but we will only Initialize
    # it in development mode
    if config_name == 'development':
        debug_toolbar.init_app(app)

    # Initialize extension CSRF Protection (Flask-WTF)
    csrf.init_app(app)

    # Initialize extension Flask-Login
    login_manager.init_app(app)

    # Initialize extension Flask-OAuthlib
    oauth.init_app(app)

    # Client endpoints
    # Register web application routes
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # Register OAuth 2.0 routes
    from .oauth2 import oauth2 as oauth2_blueprint
    app.register_blueprint(oauth2_blueprint, url_prefix='/oauth2')

    # Register Stores routes
    from .stores import stores as stores_blueprint
    app.register_blueprint(stores_blueprint, url_prefix='/stores')

    # Register API routes
    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')

    return app
