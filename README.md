# Flask OAuth2 Boilerplate
Extensive [Flask](http://flask.pocoo.org) boilerplate using best practices with a focus on implementing an OAuth 2.0 client.

## Features
* OAuth 2.0 - Server-side authorization for Google, Facebook.
* [Flask-Login](https://flask-login.readthedocs.io/en/latest/) for local authorization, using [Argon2](https://github.com/P-H-C/phc-winner-argon2) password hashing.
* Flask app design using [Blueprints](http://flask.pocoo.org/docs/0.12/blueprints/) and [Application Factories](http://flask.pocoo.org/docs/0.12/patterns/appfactories/).
* [Bootstrap 4 Beta](https://getbootstrap.com) as frontend.
* [SQLAlchemy](http://www.sqlalchemy.org) ORM using relationships, constraints, joins, labels, ...
* Loading data from JSON into database.
* [Flask-WTF](https://flask-wtf.readthedocs.io/en/stable/) forms with [CSRF Protection](https://flask-wtf.readthedocs.io/en/stable/csrf.html), [Jinja2](http://jinja.pocoo.org) macros and dynamically generated QuerySelectField.
* Using Flasks built-in integration of click [CLI](http://flask.pocoo.org/docs/0.12/cli/) instead of Flask-Script.
* REST API - JSON endpoints.
* Extensive error handling, logging to console and log file.
* Configuration from file.
* Unit Tests with Coverage.
* [Pipenv](https://docs.pipenv.org) as Python packaging tool.

## OAuth 2.0 Client
There are many libraries available for OAuth 2.0 authorization.
Google's [oauth2client](https://oauth2client.readthedocs.io) got [recently deprecated](https://google-auth.readthedocs.io/en/latest/oauth2client-deprecation.html) and now they recommend [google-auth](https://google-auth.readthedocs.io) with [OAuthLib](https://oauthlib.readthedocs.io) but their docs are not yet updated.
[Rauth](https://rauth.readthedocs.io/en/latest/) is unmaintained.
I decided to use [Flask-OAuthlib](https://flask-oauthlib.readthedocs.io), it uses [Requests-OAuthlib](https://requests-oauthlib.readthedocs.io) which is a high-level client library built on [OAuthLib](https://oauthlib.readthedocs.io) & [Requests](http://docs.python-requests.org). Please note that Google has also just released [one-tap sign-up an auto sign-in on websites](https://developers.google.com/identity/one-tap/web/overview).  
Currently supported providers: Google, Facebook.

**Update @ 2018-01-08**: apparently Flask-OAuthlib is now also [deprecated](https://lepture.com/en/2018/announcement-of-authlib) and will be replaced by [Authlib](https://authlib.org)...

## Flask Extensions
Keeping the extensions to a minimum, others can be easily integrated.
* [Flask-OAuthlib](https://flask-oauthlib.readthedocs.io)
* [Flask-Login](https://flask-login.readthedocs.io)
* [Flask-SQLAlchemy](http://flask-sqlalchemy.pocoo.org)
* [Flask-WTF](https://flask-wtf.readthedocs.io)
* [CSRF Protection](https://flask-wtf.readthedocs.io/en/stable/csrf.html)
* [Flask-DebugToolbar](https://flask-debugtoolbar.readthedocs.io)

## User Experience
Have a look in the [Wiki](https://github.com/jsoetens/flask-oauth2-boilerplate/wiki) to see how it looks.

## Getting Started
Before you can integrate sign-in to your websites, set up your app at Google & Facebook.

### Google
Create a [Google API Console](https://developers.google.com/identity/sign-in/web/devconsole-project) project and client ID.  
Authorized JavaScript origins: `http://localhost:5000`  
Authorized redirect URIs: `http://localhost:5000/oauth2/sign-in/google/authorized`  
Add your client_id and client_secret in *myapp/oauth2/google_client_secrets.json*

### Facebook
Create and retrieve a Facebook App ID on the [App Dashboard](https://developers.facebook.com/apps/).  
Open *Products* > *Facebook Login* and enable *Client OAuth Login* and *Web OAuth Login*.  
Valid OAuth redirect URIs: `http://localhost:5000`  
Add your App ID and App Secret to *myapp/oauth2/facebook_client_secrets.json*

### Set your Secret Keys
Generate your own secret keys and add them to files *run_development.sh*, *run_testing.sh*, *run_testing_with_coverage.sh*.

### Run the Development Web Server
Create a virtual environment and start one of the shell scripts, this example uses [Pipenv](https://docs.pipenv.org).  

```
pip3 install --user pipenv
pipenv install #This installs everything from the pipfile.
./run_development.sh
```

## What is next?
Adding multiple ways of sign in for websites, using provider APIs, JavaScript, ...
I really hope that with your contributions, we can keep improving this template.

## License
See the [LICENSE](LICENSE.md) file for license rights and limitations (MIT).
