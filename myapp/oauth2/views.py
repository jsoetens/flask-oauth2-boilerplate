from flask import flash, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user

from . import oauth2
from .forms import SignInForm
from .oauth2client import OAuth2Client


from myapp.models.db_orm import db
from myapp.models.db_models import User


# http://localhost:5000/oauth2/sign-in
@oauth2.route('/sign-in', methods=['GET', 'POST'])
def signin():
    """ Default route that allows you to sign in to your account. """

    form = SignInForm()

    # HTTP POST
    if form.validate_on_submit():
        # # Validate and sign in the user.
        user = User.query.filter_by(
            email_address=form.email_address.data).first()
        if (user is not None and user.verify_password(form.password.data)):
            # Flask-Login login_user() function to record the user is logged in
            # for the user session.
            login_user(user)
            flash('Signed in successfully.', 'info')
            # Post/Redirect/Get pattern, so a redirect but two possible
            # destinations. The next query string argument is used when
            # the login form was used to prevent unauthorized access.
            return redirect(request.args.get('next') or url_for('main.index'))

        flash('Invalid username or password.', 'error')
        # Return back to homepage

    # HTTP GET
    return render_template(
        'oauth2/oauth2.html',
        title='Sign in to continue - MYAPP',
        form=form)


# http://localhost:5000/oauth2/sign-in/<provider>
@oauth2.route('/sign-in/<provider>')
def oauth2_signin(provider):
    remote_app = OAuth2Client.get_provider(provider)
    return remote_app.authorization()


# http://localhost:5000/oauth2/<provider>/authorized
@oauth2.route('/sign-in/<provider>/authorized')
def authorized(provider):
    remote_app = OAuth2Client.get_provider(provider)
    provider, social_id, email_address, username = remote_app.authorized()
    if provider is not None and social_id is not None:
        # If the social user is not known, add to our database.
        user = User.query.filter_by(provider=provider).filter_by(
            social_id=social_id).first()
        if user is None:
            user = User(
                provider=provider,
                social_id=social_id,
                email_address=email_address,
                username=username
                )
            db.session.add(user)
            db.session.commit()
        # Flask-Login login_user() function to record the user is logged in
        # for the user session.
        login_user(user)
        flash('Signed in successfully.', 'info')
        return redirect(url_for('main.index'))

    else:
        flash('Authentication failed!', 'error')
        return redirect(url_for('main.index'))


# http://localhost:5000/oauth2/sign-out
@oauth2.route('/sign-out')
@login_required
def signout():
    # Remove oauth2_token from session
    OAuth2Client.signout()
    # Flask-Login logout_user() function to remove and reset user session.
    logout_user()
    flash('Signed out successfully.', 'info')
    return redirect(url_for('main.index'))
