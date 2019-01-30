"""
Provides functions to implement and manage access control
"""
import os
import jwt
import datetime

from functools import wraps
from flask import request, make_response, jsonify
from app.db_config import connect
from psycopg2 import IntegrityError
from .errors import get_error

SECRET_KEY = os.getenv("SECRET_KEY")
auth_error_messages = {}
auth_error_messages["401"] = ("You are not authorize to access"
                              " this resource. Please sign in and try again")
auth_error_messages["403"] = ("You do not have permissions to access"
                              " this resource")

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


def auth_required(func):
    """
    Decorator function that returns the authetication details for a protected
    routes
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        access_token = request.headers.get("Access-token")
        if access_token is None or access_token == "":
            return make_response(jsonify({
                    "msg": auth_error_messages["401"],
                    "status_code": 401
                }), 401)

        access_token = access_token.split(" ")[1]
        access_token = access_token.replace(" ", "")
        if access_token is None or access_token == "":
            return make_response(jsonify({
                    "msg": auth_error_messages["401"],
                    "status_code": 401
                }), 401)
        auth_results = decode_token(access_token)
        if auth_results["success"]:
            return func(auth=auth_results["user"], *args, **kwargs)
        return make_response(jsonify({
                "msg": auth_error_messages["401"],
                "status_code": 401
            }), 401)
    return wrapper


def generate_token(username, id, isAdmin):
    """
    function that generates an authentication token with the username,user's id
    and isAdmin details of the user as the payload.

    Returns
    --------
     A dict with the JWT token and a success bool value of True  if successful
     or a dict with an error string and success bool value of false otherwise
    """
    user_credentials = {
        "username": username,
        "id": id,
        "isAdmin": isAdmin
    }

    message = {
        'sub': user_credentials,
        'iat': datetime.datetime.utcnow(),
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
    }

    try:
        access_token = jwt.encode(
            message,
            SECRET_KEY,
            algorithm='HS256'
        )

        results = {"access_token": access_token, "success": True}
        return results

    except Exception as e:
        results = {"error": str(e), "success": False}
        return results


def decode_token(access_token):
    """
    Function that decodes the JWT token used by a user for authentication.abs

    Returns
    -------
     A dict with the decoded token payload and a success bool value of True or
     a dict with an error string and a success bool value of false
    """
    try:
        decoded = jwt.decode(access_token, SECRET_KEY, algorithm='HS256')
        return {"user": decoded['sub'], "success": True}

    except jwt.ExpiredSignatureError as e:
        # Signature has expired
        return {"error": str(e), "success": False}

    except jwt.InvalidIssuedAtError as e:
        # Issued at date is not valid
        return {"error": str(e), "success": False}
    except jwt.InvalidTokenError as e:
        # Token is invalid
        return {"error": str(e), "success": False}
    except Exception as e:
        # any other exception
        return {"error": str(e), "success": False}


class AccessControl(object):
    """
    This class defines methods to verify the access levels for a user based on
    whether they are the owners of a resource or an administator.

    Methods
    --------
    is_user_profile_owner(user_id,auth_user_id) - Checks if current user can
    change user profile details

    is_incident_owner(created_by_id, auth_user_id) - Checks if current user has
    access to update, or delete an incident's user_details

    is_admin(auth_id) - checks to see if current user is an administrator
    """

    def __init__(self):
        self.conn = connect()
        self.cursor = self.conn.cursor()
        self.messages = {}
        self.messages["NOT_FOUND"] = "The resource was not found with id: "

    def is_user_profile_owner(self, user_id, auth_user_id):
        """
        Method that verifies current user as the owner of a record to be
        updated
        or viewed

        Returns
        --------
        dictionary
            dictionary containing a is_owner bool value that is True if
            the current user is the owner  and success status bool
            value. Both return false otherwise
        """

        select_user_statement = """
        SELECT id FROM users WHERE id={};
        """.format(auth_user_id)
        try:
            self.cursor.execute(select_user_statement)
            result = self.cursor.fetchone()
            if result is not None:
                return {"is_owner": True, "success": True}
            error = (self.messages["NOT_FOUND"] + str(id) +\
                     "Record could not be found or doesnot exist")
            return {"error": error, "status": 404, "success": False}
        except IntegrityError as e:
            error = (self.messages["NOT_FOUND"] + str(id) +\
                     "Record could not be found or doesnot exist")
            return {"error": error, "success": False}
        except Exception as e:
            return {"error": str(e), "success": False}

    def is_incident_owner(self, incident_id, auth_user_id):
        """
        Method that verifies current user as the owner of an incident record
        to be updated, viewed or deleted

        Returns
        --------
        dictionary
            dictionary containing a is_owner bool value that is True if
            the current user is the owner  and success status bool
            value. Both return false otherwise
        """

        select_user_statement = """
        SELECT id,createdBy FROM incidents WHERE createdBy={} AND id={};
        """.format(auth_user_id, incident_id)
        try:
            self.cursor.execute(select_user_statement)
            result = self.cursor.fetchone()
            if result is not None:
                return {"is_owner": True, "success": True}
            error = (self.messages["NOT_FOUND"] + str(id) +\
                     "Record could not be found or doesnot exist")
            return {"error": error, "success": False}
        except IntegrityError as e:
            error = (self.messages["NOT_FOUND"] + str(id) +\
                     "Record could not be found or doesnot exist")
            return {"error": error, "success": False}
        except Exception as e:
            return {"error": str(e), "success": False}

    def is_admin(self, auth_user_id):
        """
        Verifies current user as the owner of a record to be updated
        or viewed

        Returns
        --------
        dictionary
            dictionary containing a is_owner bool value that is True if
            the current user is the owner  and success status bool
            value. Both return false otherwise
        """

        select_user_statement = """
        SELECT id,isAdmin FROM users WHERE id={} AND isAdmin=True;
        """.format(auth_user_id)

        try:
            self.cursor.execute(select_user_statement)
            result = self.cursor.fetchone()
            if result is not None:
                return {"is_owner": True, "success": True}
            error = (self.messages["NOT_FOUND"] + str(id)
                     + " Record could not be found or doesnot exist")
            return {"error": error, "success": False}
        except IntegrityError as e:
            error = (self.messages["NOT_FOUND"] + str(id)
                     + " Record could not be found or doesnot exist")
            return {"error": error, "success": False}
        except Exception as e:
            return {"error": str(e), "success": False}


access_control = AccessControl()
