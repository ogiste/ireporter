"""
Test cases for incident classes
"""
import unittest
import datetime
import json

from app.api.v1.models.incident import IncidentModel, count_id
from app import create_app



class TestIncidents(unittest.TestCase):

    """
    Represents the incident test cases

    """

    def setUp(self):
        """
        Method that is called before all tests
        Defines dummy incident data and sets application configuration.
        """
        self.app = create_app('testing')
        self.client = self.app.test_client

        self.comment = {
            'prop_value': 'Corruption in hiring process'
        }
        self.msg = {
            "deleted": "Incident successfully deleted",
            "created": "Incident successfully created",
            "updated": "Incident successfully updated",
            "read": "Incident(s) successfully retrieved",
            'error': None,
        }
        self.location = {
            'prop_value': '-4.333333,25.333333',
        }

        self.redflag = {
            'type': 'red-flag',
            'title':"Corruption",
            'location': '-2.333333,-13.333333',
            'comment': 'Corruption in tender procurement'
        }

        self.redflag2 = {
            'type': 'red-flag',
            'title':"Corruption",
            'location': '-2.333333,35.333333',
            'status': 'rejected',
            'comment': 'Corruption in employment procurement'
        }


    def test_redflag_create(self):
        """
        Method tests the view endpoint used in creating a new incident.
        """
        count_id = 1
        IncidentModel.count_id = count_id
        res = self.client().post('/api/v1/incidents',
        data=json.dumps(self.redflag),content_type='application/json')
        data=json.loads(res.get_data().decode('utf8'))
        self.assertEqual(res.status_code, 201)
        self.assertEqual(data["data"][0]["type"], self.redflag["type"])
        self.assertEqual(data["data"][0]["title"], self.redflag["title"])
        self.assertEqual(data["data"][0]["location"], self.redflag["location"])
        self.assertEqual(data["data"][0]["comment"], self.redflag["comment"])
        self.assertIn(self.msg['created'],str(data["msg"]))

    def test_get_single_redflag(self):
        """
        Method tests the view endpoint used in get a single incident record.
        """
        count_id = 1
        IncidentModel.count_id = count_id
        res = self.client().post('/api/v1/incidents',
        data=json.dumps(self.redflag),content_type='application/json')
        self.assertEqual(res.status_code, 201)
        res = self.client().get('/api/v1/incidents/1')
        self.assertEqual(res.status_code, 200)
        data=json.loads(res.get_data().decode('utf8'))
        incident_list = data["data"]
        self.assertEqual(incident_list[0]["type"], self.redflag["type"])
        self.assertEqual(incident_list[0]["title"], self.redflag["title"])
        self.assertEqual(data["data"][0]["location"], self.redflag["location"])
        self.assertEqual(incident_list[0]["comment"], self.redflag["comment"])
        self.assertIn(self.msg['read'],str(data["msg"]))

    def test_get_all_redflags(self):
        """
        Method tests the view endpoint used in getting all incident records.
        """
        count_id = 1
        IncidentModel.count_id = count_id
        res = self.client().post('/api/v1/incidents',
        data=json.dumps(self.redflag),content_type='application/json')
        self.assertEqual(res.status_code, 201)
        data=json.loads(res.get_data().decode('utf8'))
        self.assertIn(self.msg['created'],str(data["msg"]))
        res = self.client().post('/api/v1/incidents',
        data=json.dumps(self.redflag2),content_type='application/json')
        self.assertEqual(res.status_code, 201)
        data=json.loads(res.get_data().decode('utf8'))
        self.assertIn(self.msg['created'],str(data["msg"]))
        res = self.client().get('/api/v1/incidents')
        self.assertEqual(res.status_code, 200)
        data=json.loads(res.get_data().decode('utf8'))
        self.assertIn(self.msg['read'],str(data["msg"]))
        self.assertIn(self.redflag["type"], str(data["data"]))
        self.assertIn(self.redflag["title"], str(data["data"]))
        self.assertIn(self.redflag["comment"], str(data["data"]))
        self.assertIn(self.redflag["location"], str(data["data"]))

    def test_update_comment(self):
        """
        Method tests the view endpoint used in updating a single incident
        record comment property.
        """
        count_id = 1
        IncidentModel.count_id = count_id
        res = self.client().post('/api/v1/incidents',
        data=json.dumps(self.redflag),content_type='application/json')
        self.assertEqual(res.status_code, 201)
        res = self.client().patch('/api/v1/incidents/1/comment',
        data=json.dumps(self.comment), content_type='application/json')
        self.assertEqual(res.status_code, 200)
        data=json.loads(res.get_data().decode('utf8'))
        self.assertIn(self.msg['updated'],str(data["msg"]))
        updated_incident = self.client().get('/api/v1/incidents/')
        self.assertEqual(updated_incident.status_code, 200)
        data=json.loads(updated_incident.get_data().decode('utf8'))
        incident_list = data["data"]
        self.assertEqual(self.comment['prop_value'], incident_list[0]["comment"])

    def test_update_location(self):
        """
        Method tests the view endpoint used in creating a new incident
        record location property.
        """
        count_id = 1
        IncidentModel.count_id = count_id
        res = self.client().post('/api/v1/incidents',
        data=json.dumps(self.redflag),content_type='application/json')
        self.assertEqual(res.status_code, 201)
        res = self.client().patch('/api/v1/incidents/1/location',
        data=json.dumps(self.location), content_type='application/json')
        self.assertEqual(res.status_code, 200)
        data=json.loads(res.get_data().decode('utf8'))
        self.assertIn(self.msg['updated'],str(data["msg"]))
        updated_incident = self.client().get('/api/v1/incidents/1')
        self.assertEqual(updated_incident.status_code, 200)
        data=json.loads(updated_incident.get_data().decode('utf8'))
        self.assertIn(self.msg['read'],str(data["msg"]))
        incident_list = data["data"]
        self.assertEqual(self.location['prop_value'], incident_list[0]["location"])

    def test_delete_incident(self):
        """
        Method tests the view endpoint used in deleting a single incident.
        """
        count_id = 1
        IncidentModel.count_id = count_id
        res = self.client().post('/api/v1/incidents',
        data=json.dumps(self.redflag),content_type='application/json')
        self.assertEqual(res.status_code, 201)
        res = self.client().delete('/api/v1/incidents/1', data=None,
        content_type='application/json')
        self.assertEqual(res.status_code, 202)
        data=json.loads(res.get_data().decode('utf8'))
        self.assertIn(self.msg['deleted'],str(data["msg"]))

    def tearDown(self):
        """
        Method is called after all tests and resets the list database
        used in storing the incident records the
        """
        count_id = 1
        IncidentModel.count_id = count_id
        IncidentModel.incident_list = []

if __name__ == '__main__':
    test_incidents = TestIncidents()
    test_incidents.test_get_single_redflag()
    test_incidents.test_get_single_redflag()
