import datetime

from flask import request, make_response, jsonify
from flask_restful import Resource, abort


# Local imports
from app.api.helpers.auth_validation import (auth_required, access_control,
                                             auth_error_messages)
from app.api.helpers.errors import (parser, get_error,
                                    Validation, error_messages)
from app.api.helpers.incident_validation import (
    validate_incident_post_input,
    validate_incident_put_input,
    incident_parser
)
from app.api.helpers.error_handler_validation import is_valid_json


from app.api.v2.models.incident import IncidentModel

incident_db = IncidentModel()
validator = Validation()


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
        self.messages = {
            "deleted": "Incident successfully deleted",
            "created": "Incident successfully created",
            "updated": "Incident successfully updated",
            "read": "Incident(s) successfully retrieved"
        }

        self.status_types = {
            "DRAFT": "draft",
            "RESOLVED": "resolved",
            "REJECTED": "rejected",
            "UNDER_INVESTIGATION": "under investigation",
        }

    @auth_required
    def post(self, auth, prop=None):
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
        if not is_valid_json(request.get_data()):
            abort(400, message=error_messages["BAD_JSON"], status_code=400)
        new_incident = incident_parser.parse_args(strict=True)
        new_incident["title"] = validator.remove_lr_whitespace(
            new_incident["title"]
        )
        new_incident["type"] = validator.remove_whitespace(
            new_incident["type"]
        )
        new_incident["comment"] = validator.remove_lr_whitespace(
            new_incident["comment"]
        )
        new_incident["location"] = validator.remove_whitespace(
            new_incident["location"]
        )
        non_empty_items = {
            "title": new_incident["title"],
            "type": new_incident["type"],
            "comment": new_incident["comment"],
            "location": new_incident["location"]
            }
        for incident_item in non_empty_items:
            item_val = non_empty_items[incident_item]
            if item_val == "" or item_val is None:
                empty_item_err = "Incident %s cannot be empty" % incident_item
                return make_response(jsonify(
                    get_error(empty_item_err,
                              400)), 400)

        validation_results = validate_incident_post_input(validator,
                                                          new_incident)
        if validation_results is not True:
            return validation_results

        new_incident["createdOn"] = datetime.datetime.today().\
            strftime('%Y/%m/%d')
        new_incident["createdBy"] = auth["id"]
        new_incident["status"] = "draft"
        incident_data = incident_db.save(new_incident)

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

    @auth_required
    def get(self, auth, incident_id=None, prop=None):
        """
        GET method returns all incidents if :param :incident_id is None or a
        single incident if :param :incident_id is an integer
        """
        if prop is not None:
            return make_response(
                jsonify(get_error(
                    error_messages["404"],
                    404)), 404
                )

        if incident_id is None:
            incidents_data = incident_db.get_my_incidents(auth["id"])
            if (isinstance(incidents_data, str)
                    and incident_db.message["NOT_FOUND"] in incidents_data):
                return make_response(jsonify({
                    "msg": incidents_data,
                    "status_code": 404
                }), 404)
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

        incident_owner = access_control.is_incident_owner(incident_id,
                                                          auth["id"])
        admin = access_control.is_admin(auth["id"])
        if (incident_owner["success"] is not True
                and admin["success"] is not True):
            return make_response(jsonify({
                "msg": auth_error_messages["403"],
                "status_code": 403
            }), 403)
        incident_results = incident_db.get_single_incident_by_id(incident_id)
        if isinstance(incident_results, dict):
            return make_response(jsonify({
                "data": [incident_results],
                "msg": self.messages["read"],
                "status_code": 200
            }), 200)

        if isinstance(incident_results, str):
            return make_response(
                jsonify(get_error(incident_results, 404)), 404
                )
        return make_response(
            jsonify(
                get_error(error_messages["404"], 404)), 404
            )

    @auth_required
    def patch(self, auth, incident_id, prop=None):
        """
        PATCH endpoint that updates an incident comment or location
        properties using the :param :incident_id to find the record and :param :prop to
        identify which incident property to update.
        """
        if prop is None:
            return make_response(jsonify(get_error(error_messages["404"],
                                                   404)), 404)
        if not is_valid_json(request.get_data()):
            abort(400, message=error_messages["BAD_JSON"],
                  status_code=400)
        patch_parser = parser.copy()
        patch_parser.add_argument('prop_value', type=str, required=True,
                                  location='json',
                                  help="The new value of the comment"
                                  " or location must be provided")
        new_data = patch_parser.parse_args(strict=True)
        validation_results = validate_incident_put_input(validator,
                                                         new_data,
                                                         prop)
        incident_owner = access_control.is_incident_owner(incident_id, auth["id"])
        if incident_owner["success"] is not True:
            return make_response(jsonify({
                "msg": auth_error_messages["403"],
                "status_code": 403
            }), 403)
        if validation_results is not True:
            return validation_results

        incident_data = incident_db.update_incident(
            incident_id, prop, new_data["prop_value"]
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

    @auth_required
    def delete(self, auth, incident_id, prop=None):
        """
        DELETE endpoint that deletes a single incident using the :param :incident_id
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
        if incident_id is None:
            return make_response(
                jsonify(get_error("Cannot delete incident"
                                  " without a valid id",
                                  400)),
                400)

        incident_owner = access_control.is_incident_owner(incident_id, auth["id"])
        if incident_owner["success"] is not True:
            return make_response(jsonify({
                "msg": auth_error_messages["403"],
                "status_code": 403
            }), 403)
        deleted_incident = incident_db.delete_incident(incident_id)

        if deleted_incident is True:
            return make_response(jsonify({
                "data": [{
                    "id": incident_id
                    }],
                "msg": self.messages["deleted"],
                "status_code": 202
            }), 202)

        if isinstance(deleted_incident, str):
            return make_response(
                jsonify(get_error(deleted_incident, 404)),
                404
                )
        return make_response(jsonify(get_error(error_messages["404"],
                                               404)), 404)
