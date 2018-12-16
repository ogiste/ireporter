import datetime

from flask import make_response, jsonify
from flask_restful import Resource


# Local imports
from app.api.helpers.errors import parser, get_error, Validation, error_messages
from app.api.helpers.incident_validation import (
    validate_incident_post_input,
    validate_incident_put_input)


from app.api.v1.models.incident import IncidentModel

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
        self.db = IncidentModel()
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
        new_incident["comment"] = new_incident["comment"].lstrip()
        new_incident["comment"] = new_incident["comment"].rstrip()
        new_incident["location"] = \
            self.validator.remove_whitespace(new_incident["location"])
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
        new_incident["createdBy"] = (len(self.db.get_incidents())+1)
        new_incident["status"] = "draft"
        new_incident["images"] = ["/url/image1", "url/image2"]
        new_incident["videos"] = ["/url/video1", "url/video2"]
        incident_data = self.db.save(new_incident)

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

    def get(self, id=None, prop=None):
        """
        GET method returns all incidents if :param :id is None or a single
        incident if :param :id is an integer
        """
        if prop is not None:
            return make_response(
                jsonify(get_error(
                    error_messages["404"],
                    404)),
                404
                )

        if id is None:
            incidents_data = self.db.get_incidents()
            if isinstance(incidents_data, str):
                return make_response(jsonify({
                    "msg": incidents_data,
                    "status_code": 404
                }), 404)
            return make_response(jsonify({
                "data": incidents_data,
                "msg": self.messages["read"],
                "status_code": 200
            }), 200)

        incident_results = self.db.get_single_incident(id)
        if isinstance(incident_results, dict):
            return make_response(jsonify({
                "data": [incident_results],
                "msg": self.messages["read"],
                "status_code": 200
            }), 200)

        if isinstance(incident_results, str):
            return make_response(
                jsonify(get_error(incident_results, 400)), 400
                )
        return make_response(
            jsonify(
                get_error(error_messages["404"], 404)), 404
            )

    def patch(self, id, prop=None):
        """
        PATCH endpoint that updates an incident comment or location
        properties using the :param :id to find the record and :param :prop to
        identify which incident property to update.
        """
        if prop is None:
            return make_response(jsonify(get_error(error_messages["404"],
                                                   404)), 404)
        if prop == "comment" or prop == "location":
            patch_parser = parser.copy()
            patch_parser.add_argument('prop_value', type=str, required=True,
                                      location='json',
                                      help="The new value of the comment"
                                      " or location must be provided")
            new_data = patch_parser.parse_args()
        validation_results = validate_incident_put_input(self.validator,
                                                         new_data,
                                                         prop)
        if validation_results is not True:
            return validation_results

        incident_data = self.db.update_incident(
            id, prop, new_data["prop_value"]
        )
        if isinstance(incident_data, dict):
            return make_response(jsonify({
                "data": [incident_data],
                "msg": self.messages["updated"],
                "status_code": 200
            }), 200)
        if isinstance(incident_data, str):
            return make_response(jsonify({
                "msg": incident_data,
                "status_code": 400
            }), 400)
        return make_response(
            jsonify(get_error(error_messages["400"], 400)), 400)

        return make_response(
            jsonify(get_error("Cannot update "
                              " attributes other than incident"
                              " location and comment "
                              , 404)), 404)

    def delete(self, id, prop=None):
        """
        DELETE endpoint that deletes a single incident using the :param :id
        to identify which incident to delete
        """
        delete_parser = parser.copy()
        delete_incident_parsed = delete_parser.parse_args()

        if prop is not None:
            return make_response(
                jsonify(get_error("Cannot load the"
                                  " requested page."
                                  "Check your URL"
                                  " and parameters provided",
                                  404)), 404)
        if id is None:
            return make_response(
                jsonify(get_error("Cannot delete incident"
                                  " without a valid id"
                                  , 400))
                , 400)

        deleted_incident = self.db.delete_incident(id)

        if deleted_incident is True:
            return make_response(jsonify({
                "msg": self.messages["deleted"],
                "status_code": 202
            }), 202)

        if isinstance(deleted_incident, str):
            return make_response(
                jsonify(get_error(deleted_incident, 400)),
                400
                )

        return make_response(jsonify(get_error(error_messages["404"],
                                               404)), 404)
