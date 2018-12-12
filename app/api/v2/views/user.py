import datetime
import types
import os

from flask import Flask, make_response, jsonify,request
from flask_restful import Resource

# Local imports
from .errors import parser, get_error, Validation
from .helpers.user_validation import (validate_user_post_input,
                                      validate_user_put_input)
from app.api.v2.models.user import UserModel


user_parser = parser.copy()

user_parser.add_argument('fname', type=str, required=True,
                             location='json',
                             help='Your first name is a required field')

user_parser.add_argument('lname', type=str, required=True,
                             location='json',
                             help='Your last name is a required field')

user_parser.add_argument('username', type=str, required=True,
                             location='json',
                             help='Your username is a required field')

user_parser.add_argument('othername', type=str,
                             location='json', default="",
                             help='Your other name is an optional field')

user_parser.add_argument('email', type=str, required=True,
                             location='json',
                             help='Your email is a required field')

user_parser.add_argument('phone', type=str, required=True,
                             location='json',
                             help='Your phone number is a required field')

user_parser.add_argument('password', type=str, required=True,
                             location='json',
                             help='A password is a required field')

validator = Validation()


class UserView(Resource, UserModel):
    """
    UserModel used to view, edit and delete user records

    Defines methods that define logic for for :

        -Create a user record
        -Get all user records
        -Get a single user record
        -Update a user record
        -Delete a user record

        User Record : {
            "id": Integer,
            "createdOn": String, # Date string
            "fname": String ,
            "lname": String,
            "username":String,
            "password": String,
            "othername": String,
            "email": String,
            "phone": String, # Digit string e.g 254712333444
            "isAdmin": Bool
        }

    """

    def __init__(self):
        """
        Constructor that sets the UserView instance.db to the database
        from the User Module class
        """
        db_name = os.getenv("DB_NAME", default="ireporter")
        self.db = UserModel(db_name)
        self.messages = {
            "deleted": "User successfully deleted",
            "created": "User successfully created",
            "updated": "User successfully updated",
            "read": "User(s) successfully retrieved"
        }

    def post(self):
        """
        POST endpoint for user resource that creates a new user

        Returns
        -------
        A JSON response to the user once created
        """

        new_user = user_parser.parse_args()
        new_user["fname"] = validator.remove_whitespace(new_user["fname"])
        new_user["lname"] = validator.remove_whitespace(new_user["lname"])
        new_user["othername"] = validator.remove_whitespace(new_user["othername"])
        new_user["email"] = validator.remove_whitespace(new_user["email"])
        new_user["username"] = validator.remove_whitespace(new_user["username"])
        new_user["phone"] = validator.remove_whitespace(new_user["phone"])
        non_empty_items = [new_user["fname"], new_user["lname"],
                           new_user["email"],
                           new_user["username"], new_user["phone"],
                           new_user["password"]]
        for user_item in non_empty_items:
            if user_item == "":
                return make_response(jsonify(
                    get_error("user first and last name  email,"
                              " username,phone and password cannot"
                              " be empty strings",
                              400)), 400)
        validation_results = validate_user_post_input(validator,
                                                     new_user)
        if validation_results is not True:
            return validation_results
        new_user["createdOn"] = datetime.datetime.today().strftime('%Y/%m/%d')
        new_user["isAdmin"] = False
        create_results = self.db.save(new_user)
        if isinstance(create_results, dict):
            return make_response(jsonify({
                "data": [create_results],
                "msg": self.messages["created"],
                "status_code": 201
            }), 201)

        if isinstance(create_results, str):
            return make_response(jsonify(get_error(create_results, 400)),
                                 400)
