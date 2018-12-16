"""
Test cases for user classes
"""
import unittest
import os
import json
import datetime

from app import create_app
from app.db_config import create_tables, drop_tables
from app.api.v2.models.user import UserModel
from app.api.v2.models.incident import IncidentModel

user_db = UserModel()


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
            "email": "jtutu@mailinator.com",
            "phone": "+254705093322",
            "username": "jtutu",
            "password": "password1"
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
        self.intervention = {
            'type': 'intervention',
            'title': "Corruption In office",
            'location': '-2.333333,-13.333333',
            'comment': 'Corruption in tender procurement'
        }

        self.redflag2 = {
            'type': 'red-flag',
            'title': "Corruption",
            'location': '-2.333333,35.333333',
            'comment': 'Corruption in employment procurement'
        }

        self.location_patch = {
            'prop_value': '-33.99999,12.444444',
        }

        self.status_patch = {
            'status': 'under investigation',
        }
        self.bad_status_patch = {
            'status': '-33.99999,12.444444',
        }
        self.comment_patch = {
            'prop_value': 'Updated comment',
        }
        self.bad_intervention = {
            'type': 'intervention',
            'title': "   ",
            'location': '-2.333333,35.333333',
            'comment': 'Corruption in employment procurement'
        }

        self.bad_intervention2 = {
            'type': 'intervention',
            'title': "ds",
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

    def test_incident_create(self):
        """
        Method tests the POST endpoint user to create a new user
        """
        # Create an incident
        res = self.client().post(
            '/api/v2/incidents',
            data=json.dumps(self.intervention),
            headers={"Access-token": self.access_token_header},
            content_type='application/json'
        )
        data = json.loads(res.get_data().decode('utf8'))
        self.assertEqual(res.status_code, 201)
        self.assertEqual(data["data"][0]["type"], self.intervention["type"])
        self.assertEqual(data["data"][0]["title"], self.intervention["title"])
        self.assertEqual(data["data"][0]["location"],
                         self.intervention["location"])
        self.assertEqual(data["data"][0]["comment"],
                         self.intervention["comment"])
        self.assertIn(self.msg['created'],
                      str(data["msg"]))
        self.assertEqual(res.status_code, 201)
        # Create an edge case intervention
        res = self.client().post(
            '/api/v2/incidents',
            data=json.dumps(self.bad_intervention),
            headers={"Access-token": self.access_token_header},
            content_type='application/json'
        )
        data = json.loads(res.get_data().decode('utf8'))
        self.assertEqual(res.status_code, 400)
        # Create an edge case intervention 2
        res = self.client().post(
            '/api/v2/incidents',
            headers={"Access-token": self.access_token_header},
            data=json.dumps(self.bad_intervention2),
            content_type='application/json')
        data = json.loads(res.get_data().decode('utf8'))
        self.assertEqual(res.status_code, 400)

    def test_get_all_incidents(self):
        """
        Method tests the GET endpoint to retrieve all to incident records
        """
        # Create an intervention
        res = self.client().post(
            '/api/v2/incidents',
            headers={"Access-token": self.access_token_header},
            data=json.dumps(self.intervention),
            content_type='application/json')
        self.assertEqual(res.status_code, 201)
        data = json.loads(res.get_data().decode('utf8'))
        self.assertIn('success', str(data["msg"]))
        res = self.client().post(
            '/api/v2/incidents',
            headers={"Access-token": self.access_token_header},
            data=json.dumps(self.redflag2),
            content_type='application/json'
        )
        self.assertEqual(res.status_code, 201)
        data = json.loads(res.get_data().decode('utf8'))
        self.assertIn('success', str(data["msg"]))
        res = self.client().get(
            '/api/v2/incidents',
            headers={"Access-token": self.access_token_header}
        )
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.get_data().decode('utf8'))
        self.assertIn(self.intervention["comment"], str(data))

    def test_admin_get_all_incidents(self):
        """
        Method tests the GET endpoint to retrieve all to incident records as
        admin
        """
        res = self.client().post(
            '/api/v2/incidents',
            headers={"Access-token": self.access_token_header},
            data=json.dumps(self.intervention),
            content_type='application/json'
        )
        self.assertEqual(res.status_code, 201)
        data = json.loads(res.get_data().decode('utf8'))
        self.assertIn('success', str(data["msg"]))
        res = self.client().post(
            '/api/v2/incidents',
            headers={"Access-token": self.access_token_header},
            data=json.dumps(self.redflag2),
            content_type='application/json')
        self.assertEqual(res.status_code, 201)
        data = json.loads(res.get_data().decode('utf8'))
        self.assertIn('success', str(data["msg"]))
        res = self.client().get(
            '/api/v2/incidents/all',
            headers={"Access-token": self.access_token_admin}
            )
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.get_data().decode('utf8'))
        self.assertIn(self.intervention["comment"], str(data["data"]))

    def test_get_single_incidents(self):
        """
        Method tests the GET endpoint to retrieve a single to incident record
        """
        res = self.client().post(
            '/api/v2/incidents/',
            headers={"Access-token": self.access_token_header},
            data=json.dumps(self.intervention),
            content_type='application/json')
        self.assertEqual(res.status_code, 201)
        data = json.loads(res.get_data().decode('utf8'))
        self.assertIn('success', str(data["msg"]))
        res = self.client().post(
            '/api/v2/incidents/',
            headers={"Access-token": self.access_token_header},
            data=json.dumps(self.redflag2),
            content_type='application/json'
            )
        self.assertEqual(res.status_code, 201)
        data = json.loads(res.get_data().decode('utf8'))
        self.assertIn('success', str(data["msg"]))
        res = self.client().get(
            '/api/v2/incidents/1',
            headers={"Access-token": self.access_token_header})
        self.assertEqual(res.status_code, 200)
        res = self.client().get(
            '/api/v2/incidents/2',
            headers={"Access-token": self.access_token_header})
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.get_data().decode('utf8'))
        self.assertIn(self.redflag2["comment"], str(data))

    def test_patch_incident(self):
        """
        Method tests the PATCH endpoint to patch a single incident record's
        location or comment
        """
        res = self.client().post(
            '/api/v2/incidents/',
            headers={"Access-token": self.access_token_header},
            data=json.dumps(self.intervention),
            content_type='application/json'
            )
        self.assertEqual(res.status_code, 201)
        data = json.loads(res.get_data().decode('utf8'))
        self.assertIn('success', str(data["msg"]))
        res = self.client().post(
            '/api/v2/incidents/',
            headers={"Access-token": self.access_token_header},
            data=json.dumps(self.redflag2),
            content_type='application/json'
            )
        self.assertEqual(res.status_code, 201)
        data = json.loads(res.get_data().decode('utf8'))
        self.assertIn('success', str(data["msg"]))
        res = self.client().patch(
            '/api/v2/incidents/2/location',
            headers={"Access-token": self.access_token_header},
            data=json.dumps(self.location_patch),
            content_type='application/json')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.get_data().decode('utf8'))
        self.assertIn(self.location_patch["prop_value"], str(data))
        res = self.client().patch(
            '/api/v2/incidents/2/comment',
            headers={"Access-token": self.access_token_header},
            data=json.dumps(self.comment_patch),
            content_type='application/json')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.get_data().decode('utf8'))
        self.assertIn(self.comment_patch["prop_value"], str(data))
        res = self.client().patch(
            '/api/v2/incidents/2/comment',
            headers={"Access-token": self.access_token_admin},
            data=json.dumps(self.comment_patch),
            content_type='application/json')
        self.assertEqual(res.status_code, 403)
        data = json.loads(res.get_data().decode('utf8'))
        res = self.client().patch(
            '/api/v2/incidents/2/dsadsa',
            headers={"Access-token": self.access_token_header},
            data=json.dumps(self.comment_patch),
            content_type='application/json')
        self.assertEqual(res.status_code, 404)

    def test_patch_incident_status(self):
        """
        Method tests the PATCH endpoint to patch status of a single incident
        record
        """
        res = self.client().post(
            '/api/v2/incidents/',
            headers={"Access-token": self.access_token_header},
            data=json.dumps(self.intervention),
            content_type='application/json')
        self.assertEqual(res.status_code, 201)
        data = json.loads(res.get_data().decode('utf8'))
        self.assertIn('success', str(data["msg"]))
        res = self.client().post(
            '/api/v2/incidents/',
            headers={"Access-token": self.access_token_header},
            data=json.dumps(self.redflag2),
            content_type='application/json')
        self.assertEqual(res.status_code, 201)
        data = json.loads(res.get_data().decode('utf8'))
        self.assertIn('success', str(data["msg"]))
        res = self.client().patch(
            '/api/v2/incidents/2/status',
            headers={"Access-token": self.access_token_admin},
            data=json.dumps(self.status_patch),
            content_type='application/json')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.get_data().decode('utf8'))
        self.assertIn(self.status_patch["status"], str(data))
        res = self.client().patch(
            '/api/v2/incidents/2/status',
            headers={"Access-token": self.access_token_admin},
            data=json.dumps(self.bad_status_patch),
            content_type='application/json')
        self.assertEqual(res.status_code, 400)
        res = self.client().patch(
            '/api/v2/incidents/200/status',
            headers={"Access-token": self.access_token_admin},
            data=json.dumps(self.status_patch),
            content_type='application/json')
        self.assertEqual(res.status_code, 404)
        res = self.client().patch(
            '/api/v2/incidents/2/status',
            headers={"Access-token": self.access_token_header},
            data=json.dumps(self.status_patch),
            content_type='application/json')
        self.assertEqual(res.status_code, 403)

    def test_delete_single_incident(self):
        """
        Method tests the DELETE endpoint to remove a single to incident record
        """
        res = self.client().post(
            '/api/v2/incidents/',
            headers={"Access-token": self.access_token_header},
            data=json.dumps(self.intervention),
            content_type='application/json')
        self.assertEqual(res.status_code, 201)
        data = json.loads(res.get_data().decode('utf8'))
        self.assertIn('success', str(data["msg"]))
        res = self.client().post(
            '/api/v2/incidents/',
            headers={"Access-token": self.access_token_header},
            data=json.dumps(self.redflag2),
            content_type='application/json')
        self.assertEqual(res.status_code, 201)
        data = json.loads(res.get_data().decode('utf8'))
        self.assertIn('success', str(data["msg"]))
        res = self.client().delete(
            '/api/v2/incidents/1',
            headers={"Access-token": self.access_token_header})
        self.assertEqual(res.status_code, 202)
        res = self.client().delete(
            '/api/v2/incidents/2',
            headers={"Access-token": self.access_token_header})
        self.assertEqual(res.status_code, 202)
        data = json.loads(res.get_data().decode('utf8'))

    def tearDown(self):
        drop_tables(self.incident_db.conn)
