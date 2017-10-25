import unittest
from flask import url_for

from myapp import create_app
from myapp.models.db_orm import db
from myapp.models.db_models import User


class TestOAuth2Blueprint(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        # self.client = self.app.test_client(use_cookies=True)
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_signin(self):
        """
        Verify route /sign-in
        http://localhost:5000/oauth2/sign-in
        """
        # Add an existing user so we can test the sign in
        user = User(
            provider='myapp',
            social_id='1',
            email_address='admin@myapp.com',
            password='only4admins'
            )
        db.session.add(user)
        db.session.commit()
        response = self.client.post(url_for('oauth2.signin'), data={
            'email_address': 'admin@myapp.com',
            'password': 'only4admins'
            }, follow_redirects=True)
        # self.assertTrue(response.status_code == 302)
        self.assertTrue(b'Signed in successfully' in response.data)
