"""
Test cases for user classes
"""
import unittest
import os
import json
from pprint import pprint

from app import create_app
from app.db_config import connect, create_tables, drop_tables
from app.api.v2.models.user import UserModel


class TestIncident(unittest.TestCase):

    """
    This class represents the incident test cases that test
    manipulation of an incident
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
            "email": "jtutu@gmail.com",
            "phone": "+254705093322",
            "username": "jtutu",
            "password": "password1"
        }

        self.redflag = {
            'type': 'red-flag',
            'title':"Corruption",
            'location': '-2.333333,-13.333333',
            'comment': 'Corruption in tender procurement'
        }

        self.redflag2 = {
            'type': 'red-flag',
            'title': "Corruption",
            'location': '-2.333333,35.333333',
            'comment': 'Corruption in employment procurement'
        }

        self.msg = {
            "deleted": "Incident successfully deleted",
            "created": "Incident successfully created",
            "updated": "Incident successfully updated",
            "read": "Incident(s) successfully retrieved",
            'error': None,
        }

    def test_incident_create(self):
        """
        Method tests the POST endpoint user to create a new user
        """

        res = self.client().post('/api/v2/users', data=json.dumps(self.user),content_type='application/json')
        data= json.loads(res.get_data().decode('utf8'))
        user_details = data["data"][0]
        self.assertEqual(res.status_code, 201)
        res = self.client().post('/api/v2/incidents',
        data=json.dumps(self.redflag),content_type='application/json')
        data=json.loads(res.get_data().decode('utf8'))
        print(res.get_data().decode('utf8'))
        print(data)
        self.assertEqual(res.status_code, 201)
        self.assertEqual(data["data"][0]["type"], self.redflag["type"])
        self.assertEqual(data["data"][0]["title"], self.redflag["title"])
        self.assertEqual(data["data"][0]["location"], self.redflag["location"])
        self.assertEqual(data["data"][0]["comment"], self.redflag["comment"])
        self.assertIn(self.msg['created'],str(data["msg"]))

    def tearDown(self):
        drop_tables(self.user_db.conn)
