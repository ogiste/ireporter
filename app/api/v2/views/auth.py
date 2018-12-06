import datetime
import types
import os

from flask import Flask, make_response, jsonify,request
from flask_restful import Resource

# Local imports
from errors import parser, get_error
from app.api.v2.models.user import UserModel


auth_parser = parser.copy()

auth_parser.add_argument('username', type=str, required=True,
                             location='json',
                             help='Your username is a required field')

auth_parser.add_argument('password', type=str, required=True,
                             location='json',
                             help='Your password is a required field')


class AuthView(Resource, UserModel):
    """
    AuthView used to sign in a user and return their token and credentials

    Defines a method that defines logic for for :

        -Login a user in
        -Generating a JWT token

    """

    def __init__(self):
        """
        Constructor that sets the AuthView instance.db to the database
        from the User Module class
        """
        db_name = os.getenv("DB_NAME", default="ireporter")
        self.db = UserModel(db_name)
        self.messages = {
            "authenticated": "User successfully signed in",
            "failed":" User failed to authenticate "
        }

    def post(self):
        """
        POST endpoint for user resource that creates a new user

        Returns
        -------
        A JSON response to the user once created
        """

        user_credentials = auth_parser.parse_args()
        user_credentials["username"] = user_credentials["username"].replace(" ",
                                                                            "")
        user_credentials["password"] = user_credentials["password"].lstrip()
        user_credentials["password"] = user_credentials["password"].rstrip()
        non_empty_items = [user_credentials["username"],
                           user_credentials["password"]]
        for user_item in non_empty_items:
            if user_item == "":
                return make_response(jsonify(
                    get_error(" username and password cannot be empty strings",
                          400)), 400)
        authenticated = self.db.verify_pass(user_credentials)
        if isinstance(authenticated, types.BooleanType):
            user_details = self.db.get_single_user_by_username(user_credentials["username"])
            return make_response(jsonify({
                "data": [{
                        "token": "jwt-token",
                        "user": user_details
                        }],
                "msg": self.messages["authenticated"],
                "status_code": 200
            }), 200)

        if isinstance(authenticated, types.StringType):
            return make_response(jsonify(get_error(authenticated, 400))
                                 , 400)
