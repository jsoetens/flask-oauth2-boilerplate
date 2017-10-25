import unittest
from flask import current_app

from myapp import create_app


class TestBaseConfig(unittest.TestCase):
    def setUp(self):
        self.app = create_app('default')
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    def test_app_config_is_base(self):

        self.assertTrue(current_app.config['DEBUG'] is False)
        self.assertTrue(current_app.config['TESTING'] is False)
        self.assertTrue(current_app.config['SECRET_KEY'])
        self.assertTrue(current_app.config['WTF_CSRF_SECRET_KEY'])
        self.assertTrue(current_app.config[
            'SQLALCHEMY_TRACK_MODIFICATIONS'] is False)
        self.assertTrue(current_app.config[
            'OAUTH2_PROVIDERS']['google']['client_id'])
        self.assertTrue(current_app.config[
            'OAUTH2_PROVIDERS']['google']['client_secret'])
        self.assertTrue(current_app.config[
            'OAUTH2_PROVIDERS']['facebook']['client_id'])
        self.assertTrue(current_app.config[
            'OAUTH2_PROVIDERS']['facebook']['client_secret'])


class TestDevelopmentConfig(unittest.TestCase):

    def setUp(self):
        self.app = create_app('development')
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    def test_app_config_is_development(self):
        self.assertFalse(current_app.config['TESTING'])
        self.assertTrue(current_app.config['DEBUG'] is True)
        self.assertTrue(current_app.config[
            'DEBUG_TB_INTERCEPT_REDIRECTS'] is False)
        self.assertIn(
            'dev_myapp.db', current_app.config['SQLALCHEMY_DATABASE_URI'])


class TestProductionConfig(unittest.TestCase):

    def setUp(self):
        self.app = create_app('production')
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    def test_app_config_is_production(self):
        self.assertFalse(current_app.config['TESTING'])
        self.assertTrue(current_app.config['SESSION_PROTECTION'] == 'strong')
        self.assertTrue(current_app.config['HOST'] == '0.0.0.0')
        self.assertTrue(current_app.config['PORT'] == '5001')


class TestTestingConfig(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    def test_app_config_is_testing(self):
        self.assertTrue(current_app.config['TESTING'])
        self.assertTrue(current_app.config['TESTING'] is True)
        self.assertTrue(current_app.config['SERVER_NAME'] == 'localhost:5000')
        self.assertTrue(current_app.config['FLASK_COVERAGE'] is True)
        self.assertTrue(current_app.config['WTF_CSRF_ENABLED'] is False)
        self.assertTrue(
            current_app.config['SQLALCHEMY_DATABASE_URI'] == 'sqlite://')
