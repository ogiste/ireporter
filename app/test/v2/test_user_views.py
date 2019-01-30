"""
Test cases for user classes
"""
import unittest
import os
import json
import datetime

from app import create_app
from app.db_config import connect, create_tables, drop_tables
from app.api.v2.models.user import UserModel

user_db = UserModel()
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
        db_name = os.getenv("DB_NAME", default="tester")

        create_tables(user_db.conn)
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
            "lname":"Abdi",
            "othername":"",
            "email":"kaka@mailinator.com",
            "phone":"+254705094322",
            "username":"masu",
            "password":"1ssdfa"
        }

        self.admin = {

            "fname": "Admin",
            "lname": "iReporter",
            "othername": "Damon",
            "email": "admin@mailinator.com",
            "phone": "+254703093322",
            "username": "admin",
            "password": "password1",
            "createdOn": datetime.datetime.today().strftime('%Y/%m/%d'),
            "isAdmin": True
        }
        self.user_credentials = {
            "username": "jtutu",
            "password": "password1"
        }

        self.admin_credentials = {
            "username": "admin",
            "password": "password1"
        }

        self.messages = {
            "deleted": "Account was successfully deleted",
            "created": "Your account was successfully created",
            "updated": "Your account was successfully updated",
            "read": "Account details successfully retrieved"
        }

        # Create user
        res = self.client().post(
            '/api/v2/users',
            data=json.dumps(self.user),
            content_type='application/json')
        data = json.loads(res.get_data().decode('utf8'))
        # Sign in user
        res = self.client().post('/api/v2/auth',
                                 data=json.dumps(self.user_credentials),
                                 content_type='application/json')
        data = json.loads(res.get_data().decode('utf8'))
        token = data["data"][0]["token"]
        self.access_token_header = "Bearer {token}".format(token=token)

        # create admin user
        user_db.save(self.admin, isAdmin=True)
        # Sign in admin
        res = self.client().post('/api/v2/auth',
                                 data=json.dumps(self.admin_credentials),
                                 content_type='application/json')
        admin_data = json.loads(res.get_data().decode('utf8'))
        admin_token = admin_data["data"][0]["token"]
        self.access_token_admin = "Bearer {token}".format(token=admin_token)

    def test_user_create(self):
        """
        Method tests the POST endpoint user to create a new user
        """

        res = self.client().post(
            '/api/v2/users',
            data=json.dumps(self.user2),
            content_type='application/json')
        data= json.loads(res.get_data().decode('utf8'))
        user_details = data["data"][0]
        self.assertEqual(user_details["fname"], self.user2["fname"])
        self.assertEqual(user_details["lname"], self.user2["lname"])
        self.assertEqual(user_details["email"], self.user2["email"])
        self.assertEqual(user_details["othername"], self.user2["othername"])
        self.assertEqual(user_details["phone"], self.user2["phone"])
        self.assertEqual(res.status_code, 201)
        self.assertIn(self.messages["created"],data["msg"])

    def test_user_get(self):
        """
        Method tests the GET endpoint used to fetch a single user's record
        """

        res = self.client().get(
            '/api/v2/users/1',
            headers={"Access-token": self.access_token_header})
        data = json.loads(res.get_data().decode('utf8'))
        self.assertEqual(res.status_code, 200)
        user_details = data["data"][0]
        self.assertEqual(user_details["fname"], self.user["fname"])
        self.assertEqual(user_details["lname"], self.user["lname"])
        self.assertEqual(user_details["email"], self.user["email"])
        self.assertEqual(user_details["othername"], self.user["othername"])
        self.assertEqual(user_details["phone"], self.user["phone"])

        res = self.client().get(
            '/api/v2/users/1',
            headers={"Access-token": self.access_token_admin})
        data = json.loads(res.get_data().decode('utf8'))
        self.assertEqual(res.status_code, 403)

        res = self.client().get(
            '/api/v2/users/',
            headers={"Access-token": self.access_token_admin})
        data = json.loads(res.get_data().decode('utf8'))
        self.assertEqual(res.status_code, 200)

        res = self.client().get(
            '/api/v2/users/dsds',
            headers={"Access-token": self.access_token_admin})
        self.assertEqual(res.status_code, 404)

        res = self.client().get(
            '/api/v2/users',
            headers={"Access-token": self.access_token_header})
        self.assertEqual(res.status_code, 403)

    def tearDown(self):
        drop_tables(user_db.conn)
