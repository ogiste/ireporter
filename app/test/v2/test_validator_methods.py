"""
Test cases for user classes
"""
import unittest
from app import create_app
from app.api.helpers.errors import Validation
from app.api.helpers.auth_validation import validate_auth_post_input


class TestValidatorMethods(unittest.TestCase):

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

        self.redflag = {
            'type': 'red-flag',
            'title': "Corruption",
            'location': '-2.333333,-13.333333',
            'comment': 'Corruption in tender procurement'
        }

        self.usercredentials = {
            "username": "masu",
            "password": "ssdfa12"
        }

        self.bad_usercredentials = {
            "username": "masu",
            "password": "ssd2"
        }

        self.validator = Validation()

    def test_all_user_property_validators(self):
        """
        Method tests the validator methods used in testing
        user properties
        """
        self.assertTrue(self.validator.is_string('string'))
        self.assertTrue(self.validator.is_in_limit('string'))
        self.assertFalse(self.validator.is_in_limit('s'))
        self.assertEqual(self.validator.remove_whitespace(12), None)
        self.assertEqual(self.validator.remove_lr_whitespace(" dsad "), "dsad")
        self.assertTrue(self.validator.is_valid_email(self.user["email"]))
        self.assertTrue(self.validator.is_valid_phone(self.user["phone"]))
        self.assertTrue(self.validator.is_valid_password(
            self.user["password"])
        )

    def test_all_incident_property_validators(self):
        """
        Method tests the validator methods used in testing
        incidents properties
        """
        self.assertTrue(self.validator.is_valid_location(
            self.redflag["location"])
        )

    def test_all_auth_property_validators(self):
        """
        Method tests the validator methods used in testing
        authentication properties
        """
        with self.app.test_request_context('/api/v2/auth'):

            self.assertTrue(
                validate_auth_post_input(
                    self.validator, self.usercredentials
                )
            )
            res = validate_auth_post_input(
                self.validator, self.bad_usercredentials
            )
            self.assertEqual(
                res.status_code,
                400
            )

    def tearDown(self):
        pass
