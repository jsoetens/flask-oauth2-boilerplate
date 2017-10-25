from flask_debugtoolbar import DebugToolbarExtension
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager
from flask_oauthlib.client import OAuth

from myapp.models.db_models import User


# Flask-DebugToolbar
# https://flask-debugtoolbar.readthedocs.io
debug_toolbar = DebugToolbarExtension()

# CSRF Protection
# http://flask-wtf.readthedocs.io/en/stable/csrf.html
csrf = CSRFProtect()

# Flask-Login
# https://flask-login.readthedocs.io
login_manager = LoginManager()
# When a user attempts to access a login_required view without being logged in,
# Flask-Login will flash a message and redirect them to the log in view.
# This endpoint is set with attribute login_view.
login_manager.login_view = 'oauth2.signin'
# Custom default message flashed.
login_manager.login_message = u'Please sign in to access this page.'
# The session_protection attribute will help to protect the users' sessions
# from being stolen. When active, each request generates an identifier for the
# user's computer (secure hash of IP and user agent). If the newly generated
# and stored identifiers do not match for a non-permanent session, the entire
# session (including remember me token) is deleted.
# It can also be set in the application config with SESSION_PROTECTION
login_manager.session_protection = 'strong'


@login_manager.user_loader
def load_user(id):
    """
    Flask-Login user_loader callback is used to reload the user object from
    the user ID stored in the session. It takes the unicode ID of a user,
    and returns the corresponding user object.

    Args:
        id: user identifier as Unicode string

    Returns:
        User object if available or None otherwise.
    """
    return User.query.get(int(id))


# Flask-OAuthlib
# http://flask-oauthlib.readthedocs.io
oauth = OAuth()
