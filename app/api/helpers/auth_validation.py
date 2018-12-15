"""
Provides functions to implement and manage access control
"""
import os
import jwt
import datetime

from functools import wraps
from flask import request, make_response, jsonify

SECRET_KEY = os.getenv("SECRET_KEY")
auth_error_messages = {}
auth_error_messages["401"] = ("You are not authorize to access"
                              " this resource. Please sign in and try again")
auth_error_messages["403"] = ("You do not have permissions to access"
                              " this resource. Please sign in ")


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
