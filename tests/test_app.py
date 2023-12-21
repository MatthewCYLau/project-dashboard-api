from api import app
import unittest

class AppTestCase(unittest.TestCase):

    def setUp(self):
        app.testing = True
        self.app = app.test_client()
        
    def test_health_check(self):
        response = self.app.get('/ping')
        self.assertEqual(response.status_code, 200)

    def test_no_resources(self):
        response = self.app.get('/foo')
        self.assertEqual(response.status_code, 404)