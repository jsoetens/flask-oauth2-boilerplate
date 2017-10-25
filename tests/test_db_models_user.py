import unittest

from myapp import create_app
from myapp.models.db_orm import db
from myapp.models.db_models import User


class TestModelUser(unittest.TestCase):

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

    def test_password_setter(self):
        user = User(password='Password!')
        self.assertTrue(user.password_hash is not None)

    def test_no_password_getter(self):
        user = User(password='Password!')
        with self.assertRaises(AttributeError):
            user.password

    def test_password_verification(self):
        user = User(password='Password!')
        self.assertTrue(user.verify_password('Password!'))
        self.assertFalse(user.verify_password('WrongPassword!'))

    def test_password_salts_are_random(self):
        user1 = User(password='Password!')
        user2 = User(password='Password!')
        self.assertTrue(user1.password_hash != user2.password_hash)
