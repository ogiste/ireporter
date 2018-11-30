"""
Test cases for redflag classes
"""
import unittest
import datetime
import json

from app import create_app
from app.api.v1.models import IncidentModel


class TestIncidents(unittest.TestCase):

    """
    This class represents the redflag test cases
    """

    def setUp(self):
        """
        This method will be called before all tests
        """
        self.app = create_app('testing')
        self.client = self.app.test_client

        self.comment = {
            'prop_value': 'Corruption in hiring process'
        }

        self.location = {
            'prop_value': '-4.333333, 25.333333',
        }

        self.redflag = {
            'type': 'red-flag',
            'title':"Corruption",
            'createdBy': 0,
            'createdOn':datetime.datetime.today().strftime('%Y-%m-%d'),
            'location': '-2.333333, 35.333333',
            'status': 'resolved',
            'images': ['/new.jpg'],
            'videos': ['/new.mp4'],
            'comment': 'Corruption in tender procurement'
        }

        self.redflag2 = {
            'type': 'red-flag',
            'title':"Corruption",
            'createdBy': 0,
            'createdOn':datetime.datetime.today().strftime('%Y-%m-%d'),
            'location': '-2.333333, 35.333333',
            'status': 'rejected',
            'images': ['/new2.jpg'],
            'videos': ['/new2.mp4'],
            'comment': 'Corruption in employment procurement'
        }


    def test_redflag_create(self):

        res = self.client().post('/api/v1/incidents', data=json.dumps(self.redflag),content_type='application/json')
        data=json.loads(res.get_data())
        self.assertEqual(res.status_code, 201)
        self.assertIn('success',data["msg"])

    def test_get_single_redflag(self):
        res = self.client().post('/api/v1/incidents',data=json.dumps(self.redflag),content_type='application/json')
        self.assertEqual(res.status_code, 201)
        res = self.client().get('/api/v1/incidents/1')
        self.assertEqual(res.status_code, 200)
        data=json.loads(res.get_data())
        self.assertIn('success',str(data["msg"]))

    def test_get_all_redflags(self):
        res = self.client().post('/api/v1/incidents', data=json.dumps(self.redflag),content_type='application/json')
        self.assertEqual(res.status_code, 201)
        data=json.loads(res.get_data())
        self.assertIn('success',str(data["msg"]))
        res = self.client().post('/api/v1/incidents', data=json.dumps(self.redflag2),content_type='application/json')
        self.assertEqual(res.status_code, 201)
        data=json.loads(res.get_data())
        self.assertIn('success',str(data["msg"]))
        res = self.client().get('/api/v1/incidents')
        self.assertEqual(res.status_code, 200)
        data=json.loads(res.get_data())
        self.assertIn('Corruption in tender procurement', str(data))

    def test_update_comment(self):
        res = self.client().post('/api/v1/incidents', data=json.dumps(self.redflag),content_type='application/json')
        self.assertEqual(res.status_code, 201)
        res = self.client().patch('/api/v1/incidents/1/comment', data=json.dumps(self.comment), content_type='application/json')
        self.assertEqual(res.status_code, 200)
        data=json.loads(res.get_data())
        self.assertIn('success',str(data["msg"]))
        updated_incident = self.client().get('/api/v1/incidents/1')
        self.assertEqual(updated_incident.status_code, 200)
        data=json.loads(updated_incident.get_data())
        self.assertIn('Corruption in hiring process', str(data))

    def test_update_location(self):
        res = self.client().post('/api/v1/incidents', data=json.dumps(self.redflag),content_type='application/json')
        self.assertEqual(res.status_code, 201)
        res = self.client().patch('/api/v1/incidents/1/location', data=json.dumps(self.location), content_type='application/json')
        self.assertEqual(res.status_code, 200)
        data=json.loads(res.get_data())
        self.assertIn('success',str(data["msg"]))
        updated_incident = self.client().get('/api/v1/incidents/1')
        self.assertEqual(updated_incident.status_code, 200)
        data=json.loads(updated_incident.get_data())
        self.assertIn('-4.333333, 25.333333', str(data))

    def test_delete_incident(self):
        res = self.client().post('/api/v1/incidents', data=json.dumps(self.redflag),content_type='application/json')
        self.assertEqual(res.status_code, 201)
        res = self.client().delete('/api/v1/incidents/1', data=None, content_type='application/json')
        self.assertEqual(res.status_code, 202)
        data=json.loads(res.get_data())
        self.assertIn('success',str(data["msg"]))

    def tearDown(self):
        IncidentModel.red_flag_list = []
