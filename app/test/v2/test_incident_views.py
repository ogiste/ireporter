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
from app.api.v2.models.incident import IncidentModel

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
        self.incident_db = IncidentModel(db_name)
        create_tables(self.incident_db.conn)
        self.user = {

            "fname": "Jacob",
            "lname": "Tutu",
            "othername": "Damon",
            "email": "jtutu@gmail.com",
            "phone": "+254705093322",
            "username": "jtutu",
            "password": "password1"
        }

        self.intervention = {
            'type': 'intervention',
            'title':"Corruption In office",
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
        data=json.dumps(self.intervention),content_type='application/json')
        data=json.loads(res.get_data().decode('utf8'))
        print(res.get_data().decode('utf8'))
        print(data)
        self.assertEqual(res.status_code, 201)
        self.assertEqual(data["data"][0]["type"], self.intervention["type"])
        self.assertEqual(data["data"][0]["title"], self.intervention["title"])
        self.assertEqual(data["data"][0]["location"], self.intervention["location"])
        self.assertEqual(data["data"][0]["comment"], self.intervention["comment"])
        self.assertIn(self.msg['created'],str(data["msg"]))

    def test_get_all_incidents(self):
        """
        Method tests the GET endpoint to retrieve all to incident records
        """
        res = self.client().post('/api/v2/users', data=json.dumps(self.user),content_type='application/json')
        data= json.loads(res.get_data().decode('utf8'))
        user_details = data["data"][0]
        self.assertEqual(res.status_code, 201)
        res = self.client().post('/api/v2/incidents', data=json.dumps(self.intervention),content_type='application/json')
        self.assertEqual(res.status_code, 201)
        data=json.loads(res.get_data().decode('utf8'))
        self.assertIn('success',str(data["msg"]))
        res = self.client().post('/api/v2/incidents', data=json.dumps(self.redflag2),content_type='application/json')
        self.assertEqual(res.status_code, 201)
        data=json.loads(res.get_data().decode('utf8'))
        self.assertIn('success',str(data["msg"]))
        res = self.client().get('/api/v2/incidents')
        self.assertEqual(res.status_code, 200)
        data=json.loads(res.get_data().decode('utf8'))
        self.assertIn('Corruption in tender procurement', str(data))

    def tearDown(self):
        drop_tables(self.incident_db.conn)
