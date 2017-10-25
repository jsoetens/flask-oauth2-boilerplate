from flask import jsonify, render_template, request
from flask_wtf.csrf import CSRFError

from . import main


# Using app_errorhandler, it is like Flask.errorhandler() but for a blueprint.
# This handler is used for all requests, even if outside of the blueprint.
# http://flask.pocoo.org/docs/0.12/api/#flask.Blueprint.app_errorhandler


# CSRF Error
@main.app_errorhandler(CSRFError)
def handle_csrf_error(e):
    return render_template('errors/csrf_error.html', reason=e.description), 400


# 403 Forbidden
@main.app_errorhandler(400)
def bad_request(error):
    return render_template('errors/400.html'), 400


# 401 Unauthorized
@main.app_errorhandler(401)
def unauthorized(error):
    return render_template('errors/401.html'), 401


# 403 Forbidden
@main.app_errorhandler(403)
def forbidden(error):
    return render_template('errors/403.html'), 403


# 404 Not Found
@main.app_errorhandler(404)
def not_found(error):
    if request.accept_mimetypes.accept_json and \
            not request.accept_mimetypes.accept_html:
        response = jsonify({'error': 'not found'})
        response.status_code = 404
        return response
    return render_template('errors/404.html'), 404


# 405 Method Not Allowed
@main.app_errorhandler(405)
def method_not_allowed(error):
    return render_template('errors/405.html'), 405


# 500 Internal Server Error
@main.app_errorhandler(500)
def internal_server_error(error):
    if request.accept_mimetypes.accept_json and \
            not request.accept_mimetypes.accept_html:
        response = jsonify({'error': 'internal server error'})
        response.status_code = 500
        return response
    return render_template('errors/500.html'), 500
