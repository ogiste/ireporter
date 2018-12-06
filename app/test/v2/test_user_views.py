"""
Test cases for user classes
"""
import unittest
import datetime
import json

from app import create_app
from app.db_config import create_tables, drop_tables
from app.api.v2.models.user import UserModel


class TestUser(unittest.TestCase):

    """
    This class represents the user test cases that test creation of a user
    """

    def setUp(self):
        """
        This method will be called before all tests and sets up the
        test database as well as the dummy data
        """
        self.app = create_app('testing')
        self.client = self.app.test_client
        UserModel(db_name="ireporter_test")
        create_tables()
        self.user = {

            "fname": "Jacob",
            "lname":"Tutu",
            "othername":"Damon",
            "email":"jtutu@gmail.com",
            "phone":"254705093322",
            "username":"jtutu",
            "password":"password"
        }

        self.user2 = {
            "fname": "Kaka",
            "lname":"Abdi",
            "othername":"",
            "email":"Kaka@gmail.com",
            "phone":"254705094322",
            "username":"masu",
            "password":"ssdfa"
        }

        self.messages = {
            "created": "User successfully created"
        }

    def test_user_create(self):

        res = self.client().post('/api/v2/users', data=json.dumps(self.user),content_type='application/json')
        data=json.loads(res.get_data())
        user_details = data["data"][0]
        self.assertEqual(user_details["fname"], self.user["fname"])
        self.assertEqual(user_details["lname"], self.user["lname"])
        self.assertEqual(user_details["email"], self.user["email"])
        self.assertEqual(user_details["othername"], self.user["othername"])
        self.assertEqual(user_details["phone"], self.user["phone"])
        self.assertEqual(res.status_code, 201)
        self.assertIn(self.messages["created"],data["msg"])

    def tearDown(self):
        drop_tables()
