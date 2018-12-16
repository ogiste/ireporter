"""
Test cases for user classes
"""
import unittest
import os
import json
from pprint import pprint

from app import create_app
from app.db_config import connect, create_tables, drop_tables
from app.api.helpers.errors import Validation
from app.api.helpers.user_validation import (validate_user_post_input,
                                             validate_user_put_input)


class TestUserAuthentication(unittest.TestCase):

    """
    This class represents the user test cases that test validation of a user
    """

    def setUp(self):
        """
        This method will be called before all tests and sets up the dummy data
        """
        self.app = create_app("testing")

        self.user = {

            "fname": "Jacob",
            "lname": "Tutu",
            "othername": "Damon",
            "email": "jtutu@gmail.com",
            "phone": "+254705093322",
            "username": "jtutu",
            "password": "password1"
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

        self.user3 = {
            "username":"masu",
            "password":"ssdfa"
        }

        self.validator = Validation()

    def test_user_post_validation(self):
        """
        Method tests the POST endpoint user validation
        """
        with self.app.test_request_context('/api/v2/users'):
            self.assertTrue(validate_user_post_input(self.validator,
                                                     self.user))
            self.assertIsNot(validate_user_post_input(self.validator,
                                                      self.user2),
                             True)

    def test_user_put_validation(self):
        """
        Method tests the PUT endpoint user validation
        """
        with self.app.test_request_context('/api/v2/users'):
            self.assertTrue(
                validate_user_put_input(self.validator, self.user))
            self.assertIsNot(
                validate_user_put_input(self.validator, self.user3),
                True)

    def tearDown(self):
        pass
