"""
Test cases for user classes
"""
import unittest
import datetime
import json
import os

from pprint import pprint
from app import create_app
from app.db_config import connect, create_tables, drop_tables,delete_all_rows
from app.api.v2.models.user import UserModel


class TestUser(unittest.TestCase):

    """
    This class represents the authentication test cases that test login of a user
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

        self.user_credentials1 = {
            "username":"jtutu",
            "password":"password"
        }

        self.user_credentials2 = {
            "username":"masu",
            "password":"ssdfa"
        }
        self.messages = {
            "created": "User successfully created",
            "authenticated": "User successfully signed in"
        }

    def test_user_login(self):
        """
        Method tests the POST endpoint of user authentication
        """
        # Create user 1
        res = self.client().post('/api/v2/users',
                                 data=json.dumps(self.user),
                                 content_type='application/json')
        data = json.loads(res.get_data().decode('utf8'))
        user_details = data["data"][0]
        self.assertEqual(user_details["fname"], self.user["fname"])
        self.assertEqual(user_details["lname"], self.user["lname"])
        self.assertEqual(user_details["email"], self.user["email"])
        self.assertEqual(user_details["othername"], self.user["othername"])
        self.assertEqual(user_details["phone"], self.user["phone"])
        self.assertEqual(res.status_code, 201)
        self.assertIn(self.messages["created"],data["msg"])

        # Create user 2
        res = self.client().post('/api/v2/users',
                                 data=json.dumps(self.user2),
                                 content_type='application/json')
        data = json.loads(res.get_data().decode('utf8'))
        user_details = data["data"][0]
        self.assertEqual(user_details["fname"], self.user2["fname"])
        self.assertEqual(user_details["lname"], self.user2["lname"])
        self.assertEqual(user_details["email"], self.user2["email"])
        self.assertEqual(user_details["othername"], self.user2["othername"])
        self.assertEqual(user_details["phone"], self.user2["phone"])
        self.assertEqual(res.status_code, 201)
        self.assertIn(self.messages["created"], data["msg"])

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
        print("""data["data"]: """, data["data"])
        user_details = data["data"][0]["user"]
        self.assertEqual(user_details["fname"], self.user2["fname"])
        self.assertEqual(user_details["lname"], self.user2["lname"])
        self.assertEqual(user_details["email"], self.user2["email"])
        self.assertEqual(user_details["othername"], self.user2["othername"])
        self.assertEqual(user_details["phone"], self.user2["phone"])
        self.assertEqual(res.status_code, 200)
        self.assertIn(self.messages["authenticated"], data["msg"])

    def tearDown(self):
        drop_tables(self.user_db.conn)
