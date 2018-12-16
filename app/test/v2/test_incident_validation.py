"""
Test cases for user classes
"""
import unittest
from app import create_app
from app.api.helpers.errors import Validation
from app.api.helpers.incident_validation import (
    validate_incident_post_input
)


class TestIncidentValidation(unittest.TestCase):

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

        self.redflag2 = {
            'type': 'red-flag',
            'title': "Corruption",
            'location': '-2.333333,35.333333',
            'comment': 'Corruption in employment procurement'
        }

        self.validator = Validation()

    def test_incident_post_validation(self):
        """
        Method tests the POST endpoint user validation
        """
        with self.app.test_request_context('/api/v2/incidents'):
            self.assertTrue(validate_incident_post_input(
                self.validator, self.redflag))

    def tearDown(self):
        pass
