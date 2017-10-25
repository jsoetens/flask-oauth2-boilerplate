import os
import click

from config import config
from myapp import create_app
from myapp.logger import setup_logging
from myapp.models.db_orm import db
from myapp.models.db_data import load_users_from_json
from myapp.models.db_data import load_countries_from_json
from myapp.models.db_data import load_distribution_centers_from_json
from myapp.models.db_data import load_stores_status_from_json
from myapp.models.db_data import load_stores_from_json
from myapp.models.db_data import load_store_components_from_json


# Flask - Command Line Interface
# As Flask-Script is no longer maintained, we'll use Flasks built-in CLI tool
# http://flask.pocoo.org/docs/0.12/cli/

# We are using factory functions to create the application, so the flask
# command cannot work with them directly. The application gets instantiated
# by this separate file 'autoapp.py' (alternative is using custom scripts).
# http://flask.pocoo.org/docs/0.12/cli/

# Use the flask command as follows:
# export MYAPP_CONFIG=/path/to/config.py
# export FLASK_APP=`pwd`/autoapp.py


# Determine config settings from environment variables.
config_name = os.environ.get('MYAPP_CONFIG')

# If none given, we'll set it to development
if config_name not in config:
    config_name = 'development'

# Setup logging levels
setup_logging(config_name=config_name)


# Create the application object
app = create_app(config_name=config_name)


# CLI Commands

@app.cli.command()
def test():
    """
    Run Unit Tests.
    """
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


@app.cli.command()
def test_with_coverage():
    """ Runs the Unit Tests with Coverage. """
    # Configure Code Coverage Reports
    if app.config.get('FLASK_COVERAGE'):
        from coverage import Coverage
        # Start coverage engine, enable branch coverage analytics
        # Limit analysis to files inside application package.
        cov = Coverage(branch=True, include='myapp/*')
        cov.start()
        import unittest
        tests = unittest.TestLoader().discover('tests')
        unittest.TextTestRunner(verbosity=2).run(tests)
        cov.stop()
        cov.save()
        print('Coverage Summary')
        cov.report()
        cov.html_report(directory='covhtml')
        cov.erase()


@app.cli.command()
def db_create(drop_first=True):
    """ Creating database. """
    click.echo('Starting db_create')
    if drop_first:
        db.drop_all()
    db.create_all()


@app.cli.command()
def db_load_users():
    """ Importing JSON data to table users. """
    click.echo('Starting db_load_users')
    load_users_from_json()


@app.cli.command()
def db_load_countries():
    """ Importing JSON data to table countries. """
    click.echo('Starting db_load_countries')
    load_countries_from_json()


@app.cli.command()
def db_load_distribution_centers():
    """ Importing JSON data to table distribution_centers. """
    click.echo('Starting db_load_distribution_centers')
    load_distribution_centers_from_json()


@app.cli.command()
def db_load_store_status():
    """ Importing JSON data to table store_status. """
    click.echo('Starting db_load_store_status')
    load_stores_status_from_json()


@app.cli.command()
def db_load_stores():
    """ Importing JSON data to table stores. """
    click.echo('Starting db_load_stores')
    load_stores_from_json()


@app.cli.command()
def db_load_store_components():
    """ Importing JSON data to table store_components. """
    click.echo('Starting db_load_store_components')
    load_store_components_from_json()
