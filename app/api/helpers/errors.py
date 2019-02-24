
"""
Create the default reqparse object to be used by all resources
Define the Validation class used in validation of user input

"""
import re
from flask_restful import reqparse


parser = reqparse.RequestParser()

parser.add_argument('id', type=int, help='id must be a valid integer',
                    location='args')


def get_error(error_message, status_code):
    """
    Take and error message and status_code of a response

    Returns
    -------
    dictionary
        dictionary containing the error message and status code to be used in a
        response
    """
    return {
        "msg": error_message,
        "status_code": status_code
    }


EMAIL_REGEX = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")
USERNAME_REGEX = re.compile(r"^(?=.{4,30}$)(?![_.])(?!.*[_.]{2})[a-zA-Z0-9_]"
                            r"+(?<![_.])$")

LOCATION_REGEX = re.compile(
    r"^[-+]?([1-8]?\d(\.\d+)?|90(\.0+)?),[-+]?(180(\.0+)?|((1[0-7]\d)|"
    r"([1-9]?\d))(\.\d+)?)$"
)
PHONE_REGEX = re.compile(r"((\+254)){1}(\d{9,9})")
PW_REGEX = re.compile(r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{6,}$")
NAME_MAX = 30
NAME_MIN = 4

error_messages = {
    "BAD_JSON": "Bad request. Request object was not a valid json object. ",
    "404": "Requested URL is invalid and no resource could be found. ",
    "400": "Bad request. Ensure all inputs and parameters are valid. ",
    "401": "Unauthorized request was made."
    " Please sign in before making this request",
    "403": "The request made is forbidden."
    " You do not have the necessary permissions",
    "500": "An error occured while"
    " executing your request :/ Admin has been notified"
}


class Validation():
    """
    Creates an object with methods used in validation of user input parameters

    Returns
    --------
    Validation object with methods for validating user input data

    Methods
    --------
    is_string(var)
    is_in_limit(strvar,max,min)
    remove_whitespace(strvar)
    remove_lr_whitespace(strvar)
    is_valid_email(strvar)
    is_valid_location(strvar)
    is_valid_phone(strvar)
    is_valid_password(strvar)
    is_valid_incident_status(strvar)
    is_valid_incident_type(strvar)
    """

    def __init__(self):
        """
        Constructor function for Validation class used in validation of user
        input
        """
        self.validation_messages = {}
        self.valid_incident_status = ('draft', 'resolved', 'rejected',
                                      'under investigation')
        self.validation_messages["lim_incident_title"] = "Incident title\
         cannot be greater than 30 characters and less than 4"
        self.validation_messages["lim_user_username"] = (
            "Usernames cannot be greater than 30 characters and less than 4"
        )
        valid_loc = ("Incident location"
                     " must be a valid string of lat and long coordinates")
        empty_loc_or_comment = ("Cannot update empty location"
                                " or comment provide a valid string")
        self.validation_messages["valid_incident_location"] = valid_loc
        self.validation_messages["valid_user_email"] = (
            "Your email must be a valid email address e.g abc@gmail.com"
        )
        self.validation_messages["valid_user_phone"] = (
            "Your phone number must be in the form of +245700111222"
        )
        self.validation_messages["valid_user_password"] = (
            "Your password must be a minimum of six characters,"
            " and have at least one letter and one number"
        )
        self.validation_messages["empty_loc_or_comment"] = empty_loc_or_comment
        self.validation_messages["empty_status"] = ("Status of your incident"
                                                    " cannot be empty")
        self.validation_messages["valid_status"] = ("Status of an incident"
                                                    " can only be - draft,"
                                                    " resolved, rejected or"
                                                    " under investigation")
        self.validation_messages["alphabetic"] = (
            "Your first name, last name can only be"
            " alphabetic characters")
        self.validation_messages["valid_username"] = (
            "Your username can only consist of numbers letters"
            " and underscore characters")

    def is_string(self, var):
        """
        Method used to check if var is of a string instance

        Returns
        --------
         Boolean value - true if var is a string false otherwise
        """
        if isinstance(var, str):
            return True
        return False

    def is_in_valid_status(self, strvar):
        """
        Method used to check if strvar is in list of incident statuses

        Returns
        --------
         Boolean value - true if var is in the tuple of valid statuses false
         otherwise
        """
        is_valid = None
        for status in self.valid_incident_status:
            if status == strvar:
                is_valid = True
                break
            else:
                is_valid = False
        return is_valid

    def is_in_limit(self, strvar, strmax=NAME_MAX, strmin=NAME_MIN):
        """
        Method used to check if strvar is within the strmax and strmin value

        Returns
        --------
         Boolean value - true if strvar is a within the strmax and strmin
         values
         false otherwise
        """

        if self.is_string(strvar):
            if len(strvar) <= strmax and len(strvar) >= strmin:
                return True
            return False
        return False

    def remove_whitespace(self, strvar):
        """
        Method used to remove whitespace from a strvar

        Returns
        --------
         String without whitespaces if successfully removed or None otherwise
        """
        if self.is_string(strvar):
            strvar = strvar.replace(" ", "")
            return strvar
        return None

    def remove_lr_whitespace(self, strvar):
        """
        Method used to remove leadin and trailing whitespace from a strvar

        Returns
        --------
         String without leading and trailing whitespaces if successfully
         removed or None otherwise
        """
        if self.is_string(strvar):
            strvar = strvar.lstrip()
            strvar = strvar.rstrip()
            return strvar
        return None

    def is_valid_username(self, strvar):
        """
        Method used check if strvar is a valid username string

        Returns
        --------
         Boolean value - true if strvar is a valid email
         false otherwise
        """

        if self.is_string(strvar):
            if USERNAME_REGEX.match(strvar):
                return True
            return False
        return False

    def is_valid_email(self, strvar):
        """
        Method used check if strvar is a valid email string

        Returns
        --------
         Boolean value - true if strvar is a valid email
         false otherwise
        """

        if self.is_string(strvar):
            if EMAIL_REGEX.match(strvar):
                return True
            return False
        return False

    def is_valid_location(self, strvar):
        """
        Method used check if strvar has valid location coordinates

        Returns
        --------
         Boolean value - true if strvar is a valid lat long string
         false otherwise
        """
        if self.is_string(strvar):
            if LOCATION_REGEX.match(strvar):
                return True
            return False
        return False

    def is_valid_phone(self, strvar):
        """
        Method used check if strvar is a valid phone number

        Returns
        --------
         Boolean value - true if strvar is a valid phone number string
         false otherwise
        """
        if self.is_string(strvar):
            if PHONE_REGEX.match(strvar) and len(strvar) == 13:
                return True
            return False
        return False

    def is_valid_password(self, strvar):
        """
        Method used check if strvar is a valid password

        Returns
        --------
         Boolean value - true if  is a valid password string
         false otherwise
        """
        if self.is_string(strvar):
            if PW_REGEX.match(strvar):
                return True
            return False
        return False

    def is_valid_incident_status(self, strvar):
        """
        Method used check if strvar is a valid incident status

        Returns
        --------
         Boolean value - true if  is a valid incident status string
         false otherwise
        """
        if self.is_string(strvar):
            if self.is_in_valid_status(strvar):
                return True
            return False
        return False

    def create_limit_message(self, resource_property, strmax, strmin):
        """
        Method used to generate a limit message string when a strvar is not
        within the string requirements

        Returns
        --------
         String message describing the limits of resource_property
        """
        return "{} cannot be greater than {} characters and less than {}".\
            format(resource_property, str(strmax), str(strmin))
