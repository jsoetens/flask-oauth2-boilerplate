import os
import hashlib

from flask import current_app, flash, redirect, session, url_for

from myapp import oauth


# A great introduction to OAuth 2.0 can be found at https://www.oauth.com

# Thanks for the inspirational book and blog posts of Miguel Grinberg
# https://blog.miguelgrinberg.com/post/oauth-authentication-with-flask


# TODO: make sure it handles next_url! You can test it from an Add Store button

class OAuth2Client(object):

    """
    The OAuth2Client base class defines the structure that subclasses that
    implement each provider must follow.
    """

    providers = None

    def __init__(self, provider_name):
        """
        Create an OAuth2Client provider, get the client_id and client_secret
        from configuration.
        """
        self.provider_name = provider_name
        credentials = current_app.config['OAUTH2_PROVIDERS'][provider_name]
        self.client_id = credentials['client_id']
        self.client_secret = credentials['client_secret']

    def authorization(self):
        """
        The client will direct a user’s browser to the authorization server
        to begin the OAuth process. We are using the authorization code grant
        type. The response_type will be set to code, indicating that the
        application expects to receive an authorization code if successful.
        The redirect_uri is optional and depends on authorization server.
        """
        pass

    def get_redirect_uri(self):
        """
        The get_redirect_uri() method builds the redirect_uri based on
        the provider name. It is meant to be provided to the authorize()
        method. We add the argument _external=True to method url_for()
        so it will return us an absolute url.
        Atm not using next=request.args.get('next') or request.referrer or None

        Returns:
            Absolute path for redirect_uri
        """
        return url_for(
            '.authorized',
            provider=self.provider_name,
            _external=True)

    @classmethod
    def signout(self):
        """
        Remove the oauth2_token.
        """
        session.pop('oauth2_token', None)

    @classmethod
    def get_provider(self, provider_name):
        """
        Get the correct OAuth2Client instance by provider_name. This method
        uses introspection to find all subclasses and saves an instance
        of each in a dictionary.
        """
        if self.providers is None:
            self.providers = {}
            for provider_class in self.__subclasses__():
                provider = provider_class()
                self.providers[provider.provider_name] = provider
        return self.providers[provider_name]


# These are all the possible values for flask_oauthlib.client.OAuthRemoteApp.
# We currently only add required and non default settings for each provider.

# name – the name of the remote app.
# base_url – the base url for every request.
# request_token_url – the url for requesting new tokens. OAuth 2 requires that
#   the request_token_url is None.
# access_token_url – the url for token exchange (redirect_uri)
# authorize_url – the url for authorization.
# consumer_key – the app specific consumer key, public identifier (client_id).
# consumer_secret – the app specific consumer secret (client_secret).
# request_token_params – an optional dictionary of parameters to forward to
#   the request token url or authorize url depending on oauth version.
#   Usually contains scope and state.


class OAuth2Google(OAuth2Client):

    """
    OAuth2Google sets details for OAuth2Client provider Google.
    In Google API Console add the authorized redirect URI:
    http://localhost:5000/oauth2/sign-in/google/authorized

    We're using the same names as used by Flask-OAuthlib. Where needed
    there's a reference to general OAuth 2.0 definitions.

    https://flask-oauthlib.readthedocs.io/en/latest/api.html#

    """

    def __init__(self):
        super(OAuth2Google, self).__init__('google')
        self.google_remote_app = oauth.remote_app(
            name='google',
            base_url='https://www.googleapis.com/oauth2/v2',
            request_token_url=None,
            access_token_url='https://accounts.google.com/o/oauth2/token',
            authorize_url='https://accounts.google.com/o/oauth2/auth',
            consumer_key=self.client_id,
            consumer_secret=self.client_secret,
            request_token_params={
                'scope': 'https://www.googleapis.com/auth/userinfo.email',
                'state': lambda: hashlib.sha256(os.urandom(1024)).hexdigest()
            },
        )
        self.google_remote_app.tokengetter(self.get_oauth2_token)

    def authorization(self):
        """
        Building the authorization request url is done using Flask-OAuthlib's
        authorize(). To sign in with Google, we will call into authorize()
        and pass it the URL that the user should be redirected back to.
        It returns a redirect response to the remote authorization URL with
        the signed callback given.
        The response_type=code argument tells the OAuth provider
        that the application is a web application. Finally, the redirect_uri
        argument is set to the application route that the provider needs
        to invoke after it completes the authentication.
        This Google redirect_uri should not have a next appended to it.
        """
        return self.google_remote_app.authorize(
            callback=self.get_redirect_uri())

    def authorized(self):
        """
        If the application redirects back, the remote application can fetch
        all relevant information in the oauth_authorized function with
        authorized_response(). Google returns an access_token like this:
        {'access_token': 'x', 'expires_in': 3600, 'id_token': 'x',
        'token_type': 'Bearer'}

        Returns:
            provider, social_id, email_address, username
        """
        resp = self.google_remote_app.authorized_response()
        # resp = {'access_token': 'x', 'expires_in': 3600, 'id_token': 'x',
        #   'token_type': 'Bearer'}
        if resp is None or resp.get('access_token') is None:
            flash('Authentication failed!', 'error')
            return redirect(url_for('main.index'))
        session['oauth2_token'] = (resp['access_token'], '')
        # https://developers.google.com/oauthplayground
        userinfo = self.google_remote_app.request(
            'https://www.googleapis.com/userinfo/v2/me')
        # userinfo.data = {'name': 'Johan Soetens', 'id': 'x', 'email': 'x'}
        email_address, username = None, None
        provider = self.google_remote_app.name
        social_id = userinfo.data.get('id')
        if userinfo.data.get('email'):
            email_address = userinfo.data.get('email')
        if userinfo.data.get('name'):
            username = userinfo.data.get('name')
        return provider, social_id, email_address, username

    def get_oauth2_token(self, token=None):
        """
        Register a function as token getter.
        OAuth uses a token and a secret to figure out who is connecting to the
        remote application. After authentication/authorization this information
        is passed to a function on our side and we need to remember it.
        If the token does not exist, the function must return None, and
        otherwise return a tuple in the form (token, secret). The function
        might also be passed a token parameter. This is user defined and can
        be used to indicate another token.
        The name of the token can be passed to to the request() function.
        """
        return session.get('oauth2_token')


class OAuth2Facebook(OAuth2Client):

    """
    OAuth2Facebook sets details for OAuth2Client provider Facebook.
    We're using the same names as used by Flask-OAuthlib. Where needed
    there's a reference to general OAuth 2.0 definitions.

    https://flask-oauthlib.readthedocs.io/en/latest/api.html#
    https://developers.facebook.com/docs/facebook-login/manually-build-a-login-flow
    https://developers.facebook.com/docs/graph-api/securing-requests
    https://developers.facebook.com/docs/facebook-login/security/
    """

    def __init__(self):
        super(OAuth2Facebook, self).__init__('facebook')
        self.facebook_remote_app = oauth.remote_app(
            name='facebook',
            base_url='https://graph.facebook.com',
            request_token_url=None,
            access_token_url='/oauth/access_token',
            authorize_url='https://www.facebook.com/dialog/oauth',
            consumer_key=self.client_id,
            consumer_secret=self.client_secret,
            request_token_params={
                'scope': 'email',
                'state': lambda: hashlib.sha256(os.urandom(1024)).hexdigest()
            }
        )
        self.facebook_remote_app.tokengetter(self.get_oauth2_token)

    def authorization(self):
        """
        Building the authorization request url is done using Flask-OAuthlib's
        authorize(). To sign in with Facebook, we will call into authorize()
        and pass it the URL that the user should be redirected back to.
        It returns a redirect response to the remote authorization URL with
        the signed callback given.
        The response_type=code argument tells the OAuth provider
        that the application is a web application. Finally, the redirect_uri
        argument is set to the application route that the provider needs
        to invoke after it completes the authentication.
        """
        return self.facebook_remote_app.authorize(
            callback=self.get_redirect_uri())

    def authorized(self):
        """
        If the application redirects back, the remote application can fetch
        all relevant information in the oauth_authorized function with
        authorized_response(). Facebook returns an access_token like this:
        {'access_token': 'x', 'token_type': 'bearer', 'expires_in': x}

        Returns:
            provider, social_id, email_address, username
        """
        resp = self.facebook_remote_app.authorized_response()
        # resp = {'access_token': 'x', 'token_type': 'bearer', 'expires_in': x}
        # When the user clicks on Not Now, resp will be None.
        # The returned url will contain error=access_denied, error_code=x,
        # error_description=x, error_reason=
        if resp is None or resp.get('access_token') is None:
            flash('Authentication failed!', 'error')
            return redirect(url_for('main.index'))
        session['oauth2_token'] = (resp['access_token'], '')
        me = self.facebook_remote_app.get('/me')
        # me.data = {'name': 'Johan Soetens', 'id': 'x'}
        email_address, username = None, None
        provider = self.facebook_remote_app.name
        social_id = me.data.get('id')
        if me.data.get('name'):
            username = me.data.get('name')
        return provider, social_id, email_address, username

    def get_oauth2_token(self, token=None):
        """
        Register a function as token getter.
        OAuth uses a token and a secret to figure out who is connecting to the
        remote application. After authentication/authorization this information
        is passed to a function on our side and we need to remember it.
        If the token does not exist, the function must return None, and
        otherwise return a tuple in the form (token, secret). The function
        might also be passed a token parameter. This is user defined and can
        be used to indicate another token.
        The name of the token can be passed to to the request() function.
        """
        return session.get('oauth2_token')
