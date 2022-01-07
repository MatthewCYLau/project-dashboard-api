from api import app
import unittest
from api.db.setup import db
from unittest.mock import patch
from mongomock import MongoClient


class PyMongoMock(MongoClient):
    def init_app(self, app):
        return super().__init__()


class TestUsers(unittest.TestCase):
    def test_get_users(self):
        with patch.object(db, "mongo", PyMongoMock()):
            mock_app = app.test_client()
            response = mock_app.get("/api/users")
            self.assertEqual(response.status_code, 200)
