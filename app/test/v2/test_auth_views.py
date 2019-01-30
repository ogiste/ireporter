"""
Test cases for user classes
"""
import unittest
import json
import os

from app import create_app
from app.db_config import create_tables, drop_tables
from app.api.v2.models.user import UserModel


class TestAuth(unittest.TestCase):

    """
    This class represents the authentication test cases that test login of a
    user
    """

    def setUp(self):
        """
        This method will be called before all tests and sets up the
        test database as well as the dummy data
        """
        self.app = create_app('testing')
        self.client = self.app.test_client
        db_name = os.getenv("DB_NAME", default="tester")
        self.user_db = UserModel(db_name)
        create_tables(self.user_db.conn)
        self.user = {

            "fname": "Jacob",
            "lname": "Tutu",
            "othername": "Damon",
            "email": "jtutu@mailinator.com",
            "phone": "+254705093322",
            "username": "jtutu",
            "password": "password1"
        }

        self.user2 = {
            "fname": "Kaka",
            "lname": "Abdi",
            "othername": "",
            "email": "kaka@mailinator.com",
            "phone": "+254705094322",
            "username": "masu",
            "password": "11ssdfa"
        }

        self.user_credentials1 = {
            "username": "jtutu",
            "password": "password1"
        }

        self.bad_user_credentials = {
            "username": "jtutu",
            "password": "passwor1"
        }

        self.user_credentials2 = {
            "username": "masu",
            "password": "11ssdfa"
        }
        self.messages = {
            "created": "Your account was successfully created",
            "read": "Account details successfully retrieved",
            "authenticated": "Successfully signed in!",
            "failed": ("Could not sign you in,"
                       "ensure you have the right entered"
                       " the right username and password"),
            "not_found": ("User doesnot exist, "
                          "please check the username spelling.")
        }

        # Create user 1
        res = self.client().post('/api/v2/users',
                                 data=json.dumps(self.user),
                                 content_type='application/json')
        data = json.loads(res.get_data().decode('utf8'))
        self.user_details = data["data"][0]
        # Create user 2
        res = self.client().post('/api/v2/users',
                                 data=json.dumps(self.user2),
                                 content_type='application/json')
        data = json.loads(res.get_data().decode('utf8'))
        self.user_details2 = data["data"][0]

    def test_user_login(self):
        """
        Method tests the POST endpoint of user authentication
        """
        # Test first user login
        res = self.client().post('/api/v2/auth',
                                 data=json.dumps(self.user_credentials1),
                                 content_type='application/json')
        data = json.loads(res.get_data().decode('utf8'))
        user_details = data["data"][0]["user"]
        self.assertEqual(user_details["fname"], self.user["fname"])
        self.assertEqual(user_details["lname"], self.user["lname"])
        self.assertEqual(user_details["email"], self.user["email"])
        self.assertEqual(user_details["othername"], self.user["othername"])
        self.assertEqual(user_details["phone"], self.user["phone"])
        self.assertEqual(res.status_code, 200)
        self.assertIn(self.messages["authenticated"], data["msg"])

        # Test second user login
        res = self.client().post('/api/v2/auth',
                                 data=json.dumps(self.user_credentials2),
                                 content_type='application/json')
        data = json.loads(res.get_data().decode('utf8'))
        user_details = data["data"][0]["user"]
        self.assertEqual(user_details["fname"], self.user2["fname"])
        self.assertEqual(user_details["lname"], self.user2["lname"])
        self.assertEqual(user_details["email"], self.user2["email"])
        self.assertEqual(user_details["othername"], self.user2["othername"])
        self.assertEqual(user_details["phone"], self.user2["phone"])
        self.assertEqual(res.status_code, 200)
        self.assertIn(self.messages["authenticated"], data["msg"])

        # Test edge case user login
        res = self.client().post('/api/v2/auth',
                                 data=json.dumps(self.bad_user_credentials),
                                 content_type='application/json')
        self.assertEqual(res.status_code, 400)

    def tearDown(self):
        drop_tables(self.user_db.conn)
