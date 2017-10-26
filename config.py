import os
import json


basedir = os.path.abspath(os.path.dirname(__file__))


def get_secrets_from_json(provider_name, filename):
    """
    Reads the providers client_secrets.json file

    Args:
        provider_name: string, OAuth2 provider (Google, Facebook)
        filename: string, File name of client secrets.
    Returns:
        id, secret: string
    """
    id, secret = None, None
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            json_object = json.load(f)
            # print(json_object)
            if provider_name == 'google':
                id = json_object['web'].get('client_id')
                secret = json_object['web'].get('client_secret')
            elif provider_name == 'facebook':
                id = json_object['web'].get('app_id')
                secret = json_object['web'].get('app_secret')
            else:
                print('Unknown provider for get_secrets_from_json')
    except FileNotFoundError:
        print('Unknown client_secrets.json file')

    return id, secret


class BaseConfig(object):

    """
    BaseConfig holds the default configuration for myapp
    Use environmental variables, consider autoenv
    export APP_SETTINGS="config.DevConfig"
    app.config.from_object(os.environ['APP_SETTINGS'])
    http://flask.pocoo.org/docs/0.12/config/
    """

    # Flask debug mode
    DEBUG = False
    TESTING = False

    # Secret key needs to be randomly generated (you can use os.urandom(24))
    SECRET_KEY = os.environ.get(
        'SECRET_KEY',
        '\xa6TQ5\xc9\xf942\x9cx\x9b\xed\xa4\xc7\x95\xcc\xfd\xb8Q\xa1\x80\x99Z%')  # noqa
    # Separate token for CSRF protection (by default it uses secret key)
    # Random data for generating secure tokens.
    WTF_CSRF_SECRET_KEY = os.environ.get(
        'WTF_CSRF_SECRET_KEY',
        '\xc9\xcc\x91{\xd9\x9a\x18\x92\xaa\xb4\x9e\x80\x07\x13\x92-\x1ciH\x86\xecz:[')  # noqa

    # Turn off Flask-SQLAlchemy event system
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # SQLAlchemy database location
    # PostgreSQL - postgresql://username:password@hostname/database
    # MySQL - mysql://username:password@hostname/database
    # SQLite - sqlite:////absolute/path/to/database
    # Create the default db/sqlite directory if it doesn't exist
    # Avoid sqlalchemy.exc.OperationalError: (sqlite3.OperationalError)
    if not os.path.isdir('db/sqlite'):
        os.makedirs('db/sqlite')
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        'sqlite:///' + os.path.join(basedir, 'db/sqlite/myapp.db'))

    # Flask-OAuthlib - OAuth 2.0 Credentials
    # https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
    google_client_id, google_client_secret = get_secrets_from_json(
        provider_name='google',
        filename=os.path.join(
            basedir, 'myapp/oauth2/google_client_secrets.json'))
    facebook_app_id, facebook_app_secret = get_secrets_from_json(
        provider_name='facebook',
        filename=os.path.join(
            basedir, 'myapp/oauth2/facebook_client_secrets.json'))
    # We use the same names for our OAUTH2_PROVIDERS as used by Flask-OAuthlib
    # http://flask-oauthlib.readthedocs.io/en/latest/api.html
    OAUTH2_PROVIDERS = {
        'google': {
            'client_id': google_client_id,
            'client_secret': google_client_secret
        },
        'facebook': {
            'client_id': facebook_app_id,
            'client_secret': facebook_app_secret
        }
    }
    # print(OAUTH2_PROVIDERS)


class DevelopmentConfig(BaseConfig):
    """
    DevelopmentConfig holds development configuration for myapp
    """
    # Flask debug mode
    DEBUG = True
    # Flask-DebugToolbar - Disable intercept redirects
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    # SQLAlchemy database location
    # PostgreSQL - postgresql://username:password@hostname/database
    # MySQL - mysql://username:password@hostname/database
    # SQLite - sqlite:////absolute/path/to/database
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_DEV_URL',
        'sqlite:///' + os.path.join(basedir, 'db/sqlite/dev_myapp.db'))
    # OAuth 2.0 - OpenID connect
    # OAuthLib will raise an InsecureTransportError if you attempt to use
    # OAuth2 over HTTP, rather than HTTPS. This is mostly useful for local
    # testing, or automated tests. Never set this variable in production.
    # Prevent OAuth 2 MUST utilize https on Development / Test server
    # OAUTHLIB_INSECURE_TRANSPORT = '1'
    # OAUTHLIB_RELAX_TOKEN_SCOPE = '1'
    # DEBUG = '1'
    # os.environ['DEBUG'] = '1'


class ProductionConfig(BaseConfig):
    """
    ProdConfig holds production configuration for myapp
    """
    # SQLAlchemy database location: keep the default sqlite
    # Flask-Login - Session Protection
    SESSION_PROTECTION = 'strong'
    # Run publicly - app.run(host='0.0.0.0')
    HOST = '0.0.0.0'
    # Change the listening port - app.run(port=5001)
    PORT = '5001'


class TestingConfig(BaseConfig):
    """
    TestingConfig holds the testing configuration for myapp
    """
    TESTING = True
    # Code Coverage Reports
    FLASK_COVERAGE = True
    # Setting a SERVER_NAME also by default enables URL generation without
    # a request context but with an application context.
    SERVER_NAME = 'localhost:5000'
    # Disable CSRF protection in the testing configuration
    WTF_CSRF_ENABLED = False
    # For testing we can use an in memory database
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    # OAuth 2.0 - OpenID connect
    # OAuthLib will raise an InsecureTransportError if you attempt to use
    # OAuth2 over HTTP, rather than HTTPS. This is mostly useful for local
    # testing, or automated tests. Never set these in production!
    # Prevent OAuth 2 MUST utilize https on Development / Test server
    # OAUTHLIB_INSECURE_TRANSPORT = '1'
    # OAUTHLIB_RELAX_TOKEN_SCOPE = '1'
    # DEBUG = '1'
    # os.environ['DEBUG'] = '1'


config = {
    'default': BaseConfig,
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}
