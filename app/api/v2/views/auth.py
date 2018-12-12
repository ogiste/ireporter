import datetime
import types
import os

from flask import make_response, jsonify
from flask_restful import Resource

# Local imports
from .errors import parser, get_error
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
            "failed": "Could not sign you in,ensure you have the right entered the right username and password",
            "not_found": "User doesnot exist, please check the username spelling."
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
        if isinstance(authenticated, bool) and authenticated is True:
            user_details = self.db.get_single_user_by_username(user_credentials["username"])
            return make_response(jsonify({
                "data": [{
                        "token": "jwt-token",
                        "user": user_details
                        }],
                "msg": self.messages["authenticated"],
                "status_code": 200
            }), 200)

        if authenticated is False:
            return make_response(jsonify(get_error(self.messages["failed"],
                                                    400))
                                 , 400)

        if authenticated is None:
            return make_response(jsonify(get_error(self.messages["not_found"],
                                                    400))
                                 , 400)

        if isinstance(authenticated, bytes):
            return make_response(jsonify(get_error(authenticated, 400))
                                 , 400)
