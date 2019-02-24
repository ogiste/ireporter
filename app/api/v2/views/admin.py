import smtplib
import os
from flask import make_response, jsonify, request
from flask_restful import Resource, abort
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
# Local imports
from app.api.helpers.auth_validation import (auth_required, access_control,
                                             auth_error_messages)
from app.api.helpers.errors import parser, get_error, Validation, error_messages
from app.api.helpers.incident_validation import (validate_admin_put_input)
from app.api.v2.models.incident import IncidentModel
from app.api.v2.models.user import UserModel
from app.api.helpers.error_handler_validation import (
    is_valid_json
    )

incident_db = IncidentModel()
user_db = UserModel()
validator = Validation()
EMAIL_ADDRESS = os.getenv("ADMIN_EMAIL", default="ireporterkenya@gmail.com")
EMAIL_PASSWORD = os.getenv("ADMIN_EMAIL_PASSWORD")


def send_email_notification(user_data, incident_data):
    email_msg = MIMEMultipart()
    email_msg['From'] = EMAIL_ADDRESS
    email_msg['To'] = user_data["email"]
    email_msg['Subject'] = "Incident: {} status updated to {}".format(
        incident_data["title"],
        incident_data["status"]
    )

    body_text = """\
    Hello, {}.
    Your incident ( {} ) status was updated to {} by the administrators.
    For more information contact ireporterkenya@gmail.com.
    """.format(
        user_data["fname"],
        incident_data["title"],
        incident_data["status"]
    )
    body_html = """\
    <html>
      <head></head>
      <body>
        <p>Hello, {}<br>
    Your incident <b> {} </b> status was updated to {} by the administrators.
           <br>
           <small>
           For more information contact ireporterkenya@gmail.com.
           </small>
        </p>
      </body>
    </html>
    """.format(
        user_data["fname"],
        incident_data["title"],
        incident_data["status"]
    )
    email_msg.attach(MIMEText(body_text, 'plain'))
    email_msg.attach(MIMEText(body_html, 'html'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(email_msg)
        server.quit()
    except Exception as e:
        str(e)


class AdminView(Resource):
    """
    AdminView used to update incident status and retrieve all incident records

    Defines methods that define logic for for :

        -Get all incidents
        -Update an incident's status

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
        Constructor sets the AdminView initializes the validator and sets The
        messages used in responses
        """
        self.messages = {
            "updated": "Incident status successfully updated",
            "read": "Incident(s) successfully retrieved"
        }

        self.status_types = {
            "DRAFT": "draft",
            "RESOLVED": "resolved",
            "REJECTED": "rejected",
            "UNDER_INVESTIGATION": "under investigation",
        }

    @auth_required
    def get(self, auth):
        """
        GET method returns all incidents records
        """
        admin = access_control.is_admin(auth["id"])
        if admin["success"] is not True:
            return make_response(jsonify({
                "msg": auth_error_messages["403"],
                "status_code": 403
            }), 403)
        incidents_data = incident_db.get_incidents()
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

    @auth_required
    def patch(self, auth, id):
        """
        PATCH endpoint that updates an incident status
        properties using the :param :id to find the record
        """
        if not is_valid_json(request.get_data()):
            abort(400, message=error_messages["BAD_JSON"], status_code=400)
        admin = access_control.is_admin(auth["id"])
        if admin["success"] is not True:
            return make_response(jsonify({
                "msg": auth_error_messages["403"],
                "status_code": 403
            }), 403)
        patch_parser = parser.copy()
        patch_parser.add_argument(
            'status', required=True, type=str,
            choices=('draft', 'resolved', 'rejected',
                     'under investigation'),
            location='json',
            help='The status of the incident - '
            'can either be draft, resolved,'
            'rejected or under investigation'
        )
        new_data = patch_parser.parse_args(strict=True)
        validation_results = validate_admin_put_input(validator, new_data)
        if validation_results is not True:
            return validation_results

        incident_data = incident_db.update_incident(
            id, "status", new_data["status"], isAdmin=True
        )
        if isinstance(incident_data, dict):
            user_data = user_db.get_single_user_by_id(
                incident_data["createdBy"]
            )
            if isinstance(user_data, dict):
                send_email_notification(user_data, incident_data)
            return make_response(jsonify({
                "data": [incident_data],
                "msg": self.messages["updated"],
                "status_code": 200
            }), 200)

        if (isinstance(incident_data, str)
            and incident_db.message["NOT_FOUND"] in incident_data):
            return make_response(jsonify({
                "msg": incident_data,
                "status_code": 404
            }), 404)
        if isinstance(incident_data, str):
            return make_response(jsonify({
                "msg": incident_data,
                "status_code": 400
            }), 400)
        return make_response(
            jsonify(get_error(error_messages["400"], 400)), 400)
