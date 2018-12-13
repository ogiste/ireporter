"""
Describes helper functions used in providing validation logic for:

Auth POST method
"""
from flask import make_response, jsonify
from app.api.v2.views.errors import get_error

PASSWORD_MAX = 30
PASSWORD_MIN = 6


def validate_auth_post_input(validator, user_credentials):
    """
    Function that validates the username and password properties of a user

    Returns
    -------
    make_response object if validation Failed
    True Boolean if validation Succeeded
    """
    if not validator.is_in_limit(user_credentials["username"]):
        return make_response(jsonify(
            get_error(validator.validation_messages["lim_user_username"],
                      400)), 400)
    if not validator.is_in_limit(user_credentials["password"],
                                 PASSWORD_MAX, PASSWORD_MIN):
        return make_response(jsonify(
            get_error(validator.
                      create_limit_message("Your password", PASSWORD_MAX,
                                           PASSWORD_MIN),
                      400)), 400)
    return True
