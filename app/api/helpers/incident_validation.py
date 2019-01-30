"""
Describes helper functions used in providing validation logic for:

Incident GET methods
Incident PUT method
Incident POST method
Incident DELETE method

"""
from flask import make_response, jsonify
from .errors import get_error, parser

COMMENT_MAX = 100
COMMENT_MIN = 3

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
    help='The Latitude and Longitude location coordinates of the incident'
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


def validate_incident_post_input(validator, new_incident):
    """
    Function that validates the title,comment,and location properties of a new
    incident

    Returns
    -------
    make_response object if validation Failed
    None object if validation Succeeded
    """
    if not validator.is_in_limit(new_incident["title"]):
        return make_response(jsonify(
            get_error(validator.validation_messages["lim_incident_title"],
                      400)), 400)
    if not validator.is_in_limit(new_incident["comment"],
                                 COMMENT_MAX, COMMENT_MIN):
        return make_response(jsonify(
            get_error(validator.
                      create_limit_message("Incident comment", COMMENT_MAX,
                                           COMMENT_MIN),
                      400)), 400)
    if not validator.is_valid_location(new_incident["location"]):
        return make_response(jsonify(
            get_error(validator.
                      validation_messages["valid_incident_location"],
                      400)), 400)
    return True


def validate_incident_put_input(validator, new_data, prop):
    """
    Function that validates the location or comment value for update
    takes in a validator object, new_data from the request body
    and a prop which should only be location or comment
    Returns
    -------
    make_response object if validation Failed
    True object if validation Succeeded
    """
    if prop != "comment" and prop != "location":
        return make_response(
            jsonify(get_error("Cannot update "
                              " attributes other than incident"
                              " location and comment ",
                              404)), 404)
    if prop == "location":
        new_data["prop_value"] = validator.\
            remove_whitespace(new_data["prop_value"])
    if prop == "comment":
        new_data["prop_value"] = validator.\
            remove_lr_whitespace(new_data["prop_value"])
    if prop is not None and new_data["prop_value"] != "":
        is_valid_location = validator.is_valid_location(new_data["prop_value"])
        if prop == "location" and not is_valid_location:
            return make_response(jsonify(
                get_error(validator.
                          validation_messages["valid_incident_location"],
                          400)), 400)
        is_valid_comment = validator.is_in_limit(new_data["prop_value"],
                                                 COMMENT_MAX, COMMENT_MIN)
        if prop == "comment" and not is_valid_comment:
            return make_response(jsonify(
                get_error(validator.
                          create_limit_message("Incident comment", COMMENT_MAX,
                                               COMMENT_MIN),
                          400)), 400)
    else:
        empty_loc_or_comment = validator.\
            validation_messages["empty_loc_or_comment"]
        return make_response(jsonify(get_error(empty_loc_or_comment, 400)),
                             400)
    return True


def validate_admin_put_input(validator, new_data):
    """
    Function that validates the status value for update
    takes in a validator object and new_data dictionary from the request body
    Returns
    -------
    make_response object if validation Failed
    True object if validation Succeeded
    """
    new_data["status"] = validator.\
        remove_lr_whitespace(new_data["status"])
    if new_data["status"] != "":
        is_valid_status = validator.\
            is_valid_incident_status(new_data["status"])
        if is_valid_status is not True:
            valid_status = validator.\
                validation_messages["valid_status"]
            return make_response(jsonify(get_error(valid_status, 400)), 400)
    else:
        empty_status = validator.\
            validation_messages["empty_status"]
        return make_response(jsonify(get_error(empty_status, 400)), 400)
    return True
