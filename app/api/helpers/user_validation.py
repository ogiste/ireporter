"""
Describes helper functions used in providing validation logic for:

user GET methods
user PUT method
user POST method
"""
from flask import make_response, jsonify
from .errors import get_error, Validation

FL_NAME_MAX = 30  # First name, Last name max value
FL_NAME_MIN = 2  # First name, Last name min value
EMAIL_MAX = 60
EMAIL_MIN = 10
PHONE_MAX = 13
PHONE_MIN = 12
PASSWORD_MAX = 30
PASSWORD_MIN = 6

validator = Validation()


def prop_is_in_proplist(prop, proplist):
    """
    Search for an item within a property list
    Takes the item and list as parameters

    Returns
    -------
    Boolean value of True if found , false otherwise
    """
    is_in_list = None
    for idx, item in enumerate(proplist):
        if prop == item:
            is_in_list = True
            break
        elif idx == (len(proplist)-1):
            is_in_list = False
            break
    return is_in_list


def validate_single_name(name):
    """
    function to validate the name of a use
    Takes the name string as the parameter

    Returns
    -------
    True if validated or response object otherwise
    """
    if not validator.is_in_limit(name,
                                 FL_NAME_MAX, FL_NAME_MIN):
        msg = validator.create_limit_message("Your name", FL_NAME_MAX,
                                             FL_NAME_MIN)
        return make_response(jsonify(
            get_error(
                msg,
                400)), 400)
    if not name.isalpha():
        return make_response(jsonify(
            get_error(
                validator.validation_messages["alphabetic"],
                400)), 400)
    return True


def validate_single_othername(othername):
    """
    function to validate the other name of a user
    Takes the other name string as the parameter

    Returns
    -------
    True if validated or response object otherwise
    """
    if not validator.is_in_limit(othername,
                                 FL_NAME_MAX, 0):
        msg = validator.create_limit_message("Your other name", FL_NAME_MAX, 0)
        return make_response(jsonify(
            get_error(msg,
                      400)), 400)
    if othername != "" and not othername.isalpha():
        return make_response(jsonify(
            get_error(
                validator.validation_messages["alphabetic"],
                400)), 400)
    return True


def validate_single_email(email):
    """
    function to validate the email of a user
    Takes the email string as the parameter

    Returns
    -------
    True if validated or response object otherwise
    """
    if not validator.is_in_limit(email,
                                 EMAIL_MAX, EMAIL_MIN):
        msg = validator.create_limit_message("Your email",
                                             EMAIL_MAX, EMAIL_MIN)
        return make_response(jsonify(
            get_error(msg,
                      400)), 400)
    if not validator.is_valid_email(email):
        return make_response(jsonify(
            get_error(validator.
                      validation_messages["valid_user_email"],
                      400)), 400)
    return True


def validate_single_phone(phone):
    """
    function to validate the phome number of a user
    Takes the phone number string as the parameter

    Returns
    -------
    True if validated or response object otherwise
    """
    if not validator.is_valid_phone(phone):
        return make_response(jsonify(
            get_error(validator.
                      validation_messages["valid_user_phone"],
                      400)), 400)
    return True


validator_functions = {
    "fname": validate_single_name,
    "lname": validate_single_name,
    "othername": validate_single_othername,
    "email": validate_single_email,
    "phone": validate_single_phone
}


def validate_user_post_input(validator, new_user):
    """
    Function that validates the username,firstname ,lastname,othername,
    phone, email, password properties of a new user

    Returns
    -------
    make_response object if validation Failed
    True Boolean if validation Succeeded
    """
    names = [new_user["fname"], new_user["othername"],
             new_user["lname"]]
    for name in names:
        if name != "" and not name.isalpha():
            return make_response(jsonify(
                get_error(
                    validator.validation_messages["alphabetic"],
                    400)), 400)
    if not validator.is_in_limit(new_user["username"]):
        return make_response(jsonify(
            get_error(validator.validation_messages["lim_user_username"],
                      400)), 400)
    if not validator.is_valid_username(new_user["username"]):
        return make_response(jsonify(
            get_error(validator.validation_messages["valid_username"],
                      400)), 400)
    if not validator.is_in_limit(new_user["fname"],
                                 FL_NAME_MAX, FL_NAME_MIN):
        return make_response(jsonify(
            get_error(validator.
                      create_limit_message("Your first name", FL_NAME_MAX,
                                           FL_NAME_MIN),
                      400)), 400)

    if not validator.is_in_limit(new_user["lname"],
                                 FL_NAME_MAX, FL_NAME_MIN):
        return make_response(jsonify(
            get_error(validator.
                      create_limit_message("Your last name", FL_NAME_MAX,
                                           FL_NAME_MIN),
                      400)), 400)
    if not validator.is_in_limit(new_user["othername"],
                                 FL_NAME_MAX, 0):
        return make_response(jsonify(
            get_error(validator.
                      create_limit_message("Your other name", FL_NAME_MAX,
                                           0),
                      400)), 400)
    if not validator.is_in_limit(new_user["email"],
                                 EMAIL_MAX, EMAIL_MIN):
        return make_response(jsonify(
            get_error(validator.
                      create_limit_message("Your email", EMAIL_MAX,
                                           EMAIL_MIN),
                      400)), 400)
    if not validator.is_valid_email(new_user["email"]):
        return make_response(jsonify(
            get_error(validator.
                      validation_messages["valid_user_email"],
                      400)), 400)
    if not validator.is_valid_phone(new_user["phone"]):
        return make_response(jsonify(
            get_error(validator.
                      validation_messages["valid_user_phone"],
                      400)), 400)
    if not validator.is_in_limit(new_user["password"],
                                 PASSWORD_MAX, PASSWORD_MIN):
        return make_response(jsonify(
            get_error(validator.
                      create_limit_message("Your password", PASSWORD_MAX,
                                           PASSWORD_MIN),
                      400)), 400)
    if not validator.is_valid_password(new_user["password"]):
        return make_response(jsonify(
            get_error(validator.
                      validation_messages["valid_user_password"],
                      400)), 400)
    return True


def validate_user_put_input(validator, update_data):
    """
    Function that validates the value of user details for update
    takes in a validator object, update_data dictionary from the request body

    Returns
    -------
    make_response object if validation Failed
    True Boolean object if validation Succeeded
    """
    if isinstance(update_data, dict):
        user_prop_names = list(update_data.keys())
        validator_functions_names = list(validator_functions.keys())
        validation_results = None
        for user_prop_name in user_prop_names:
            if(prop_is_in_proplist(user_prop_name, validator_functions_names)):
                validation_results = validator_functions[user_prop_name](
                    update_data[user_prop_name]
                    )
                if validation_results is True:
                    continue
                else:
                    break
            continue
        return validation_results
    else:
        return make_response(jsonify(
            get_error("Update details provided are in an invalid format",
                      400)), 400)
    return True
