import unittest
from flask import url_for

from myapp import create_app
from myapp.models.db_orm import db


class TestStoresBlueprint(unittest.TestCase):

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

    def test_route_stores(self):
        """
        Verify route /stores
        http://localhost:5000/stores
        """
        response = self.client.get(url_for('stores.index'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(b'Stores Overview' in response.data)
