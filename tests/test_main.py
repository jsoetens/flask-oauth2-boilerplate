import unittest

from myapp import create_app
from myapp.models.db_orm import db


class TestMainBlueprint(unittest.TestCase):

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

    # http://localhost:5000/
    def test_index(self):
        # Ensure Flask is setup.
        # response = self.client.get(
        #     url_for('main.index'), follow_redirects=True)
        response = self.client.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Welcome to MYAPP', response.data)

    # def test_main_404(self):
    #     # Ensure 404 error is handled for main
    #     response = self.client.get('/404')
    #     self.assert404(response)
    #     self.assertTemplateUsed('errors/404.html')
