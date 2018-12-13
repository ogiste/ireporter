import datetime

from flask import make_response, jsonify
from flask_restful import Resource


# Local imports
from .errors import parser, get_error, Validation, error_messages
from .helpers.incident_validation import (validate_incident_post_input,
                                          validate_incident_put_input)


from app.api.v2.models.incident import IncidentModel

IncidentDB = IncidentModel()
incident_parser = parser.copy()

incident_parser.add_argument(
    'title', type=str,
    required=True, location='json',
    help='The title of the incident is a required field'
    )

incident_parser.add_argument(
    'type', type=str, required=True,
    choices=('red-flag', 'intervention'), location='json',
    help='The type of the incident is a required field'
    '- must be red-flag or intervention'
    )

incident_parser.add_argument(
    'location',
    type=str, required=True, location='json',
    help='The Latitude and Longitude of the incident'
    ' is a required field'
    )

incident_parser.add_argument(
    'comment',
    type=str, required=True, location='json',
    help='The descriptive comment of the incident'
    ' is a required field'
    )

incident_parser.add_argument(
    'status',
    type=str, choices=('draft', 'resolved', 'rejected', 'under investigation'),
    location='json',
    help='The status of the incident - can either be draft, resolved,'
    'rejected or under investigation'
    )

incident_parser.add_argument(
    'images', action='append', location='json',
    help="A list of image urls related to the incident and is not required"
    )

incident_parser.add_argument(
    'videos', action='append', location='json',
    help="A list of video urls related to the incident and is not required"
    )


class IncidentView(Resource, IncidentModel):
    """
    Views that establish endpoints for :

        -Create an incident
        -Get all incidents
        -Get a single incident
        -Update an incident
        -Delete an incident

        Incident Record : {
            "id": Integer,
            "createdOn": String, # Datetime string
            "createdBy": Integer,
            # Integer ID of the user who created the incident
            "title": String ,
            "type": String,
            "location": String, # Lat Long Coordinates
            "status": String,
            # Either draft,resolved,rejected or under investigation
            "images": List, # List of image urls
            "videos": List,# List of video urls
            "comment": String
        }

    """

    def __init__(self):
        """
        Constructor sets the IncidentView instance.db to the database
        from the Incident Module class
        """
        self.validator = Validation()
        self.messages = {
            "deleted": "Incident successfully deleted",
            "created": "Incident successfully created",
            "updated": "Incident successfully updated",
            "read": "Incident(s) successfully retrieved"
        }

    def post(self, prop=None):
        """
        POST endpoint for incident resource that creates a new instance
        and returns the incident once created
        """
        if prop is not None:
            return make_response(
                jsonify(
                    get_error(error_messages["404"], 404)),
                404
                )

        new_incident = incident_parser.parse_args()
        new_incident["title"] = self.validator.remove_whitespace(
            new_incident["title"]
        )
        new_incident["type"] = self.validator.remove_whitespace(
            new_incident["type"]
        )
        new_incident["comment"] = self.validator.remove_lr_whitespace(
            new_incident["comment"]
        )
        new_incident["location"] = self.validator.remove_whitespace(
            new_incident["location"]
        )
        non_empty_items = [new_incident["title"], new_incident["type"],
                           new_incident["comment"], new_incident["location"]]
        for incident_item in non_empty_items:
            if incident_item == "" or incident_item is None:
                return make_response(jsonify(
                    get_error("Incident title,type,"
                              " comment and location cannot be empty strings",
                              400)), 400)

        validation_results = validate_incident_post_input(self.validator,
                                                          new_incident)
        if validation_results is not True:
            return validation_results

        new_incident["createdOn"] = datetime.datetime.today().\
            strftime('%Y/%m/%d')
        new_incident["createdBy"] = 1
        new_incident["status"] = "draft"
        new_incident["images"] = ["/url/image1", "url/image2"]
        new_incident["videos"] = ["/url/video1", "url/video2"]
        incident_data = IncidentDB.save(new_incident)

        if isinstance(incident_data, dict) or isinstance(incident_data, list):
            return make_response(jsonify({
                "data": [incident_data],
                "msg": self.messages["created"],
                "status_code": 201
            }), 201)
        if isinstance(incident_data, str):
            return make_response(jsonify({
                "msg": incident_data,
                "status_code": 400
            }), 400)
        return make_response(jsonify(get_error("Failed to create new incident",
                                               400)), 400)
