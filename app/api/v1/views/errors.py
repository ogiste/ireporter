
"""
Create the default reqparse object to be used by all resources
Define the Validation class used in validation of user input

"""
import types
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
LOCATION_REGEX = re.compile(r"^[-+]?([1-8]?\d(\.\d+)?|90(\.0+)?),[-+]?(180(\.0+)?|((1[0-7]\d)|([1-9]?\d))(\.\d+)?)$")
PHONE_REGEX = re.compile(r"((\+254)){1}(\d{9,9})")
PW_REGEX = re.compile(r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{6,}$")
NAME_MAX = 30
NAME_MIN = 4

error_messages = {
    "404": "Requested URL is invalid and no resource could be found :O ",
    "400": "Bad request. Ensure all inputs and parameters are valid. ",
    "401": "Unauthorized request was made."+\
    " Please sign in before making this request",
    "403": "The request made is forbidden."+\
    " You do not have the necessary permissions",
    "500": "An error occured while"+\
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
        self.validation_messages["lim_incident_title"] = "Incident title\
         cannot be greater than 30 characters and less than 4"
        self.validation_messages["valid_incident_location"] = "Incident location"+\
            " must be a valid string of lat and long coordinates"

    def is_string(self, var):
        """
        Method used to check if var is of a string instance

        Returns
        --------
         Boolean value - true if var is a string false otherwise
        """
        if isinstance(var, types.StringType):
            return True
        print "var is not a string"
        print "var is of instance: ", type(var)
        return False

    def is_in_limit(self, strvar, max=NAME_MAX, min=NAME_MIN):
        """
        Method used to check if strvar is within the max and min value

        Returns
        --------
         Boolean value - true if strvar is a within the max and min values
         false otherwise
        """

        if self.is_string(strvar):
            if len(strvar) <= max and len(strvar) >= min:
                return True
            print (strvar, " is not within string limits of max: ", max,
                   " min: ", min)
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
            print (strvar, " is not a valid email address ")
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
            print (strvar, " is not a valid lat long location ")
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
            if PHONE_REGEX.match(strvar):
                return True
            print (strvar, " is not a valid phone number with +254 extension.")
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
            print (strvar, " is not a valid password string.")
            return False
        return False

    def create_limit_message(self, property,max,min):
        """
        Method used to generate a limit message string when a strvar is not
        within the string requirements

        Returns
        --------
         String message describing the limits of property
        """
        return "{} cannot be greater than {} characters and less than {}".\
            format(property, str(max), str(min))
