import datetime
import types
import os
import json

from flask import Flask, make_response, jsonify
from flask_restful import Resource, request, abort

# Local imports
from app.api.helpers.auth_validation import (
    auth_required, access_control,
    auth_error_messages
)
from app.api.helpers.errors import(
    parser, get_error,
    Validation, error_messages
)
from app.api.helpers.user_validation import (
    validate_user_post_input,
    validate_user_put_input)

from app.api.helpers.error_handler_validation import (
    is_valid_json
    )
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
user_db = UserModel()

class UserView(Resource, UserModel):
    """
    UserView used to view, edit and delete user records

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
        self.messages = {
            "deleted": "Account was successfully deleted",
            "created": "Your account was successfully created",
            "updated": "Your account was successfully updated",
            "read": "Account details successfully retrieved"
        }

    @auth_required
    def get(self, auth, id=None):
        """
        Method used to return a single user's details or all user details if
        the current user is an administrator.

        Returns
        --------
        A JSON response object with user details
        """
        if id is None:
            admin = access_control.is_admin(auth["id"])
            if admin["success"] is not True:
                return make_response(jsonify({
                    "msg": auth_error_messages["403"],
                    "status_code": 403
                }), 403)
            user_data = user_db.get_users()
            if (isinstance(user_data, str) and user_db.message["NOT_FOUND"]
                in user_data):
                return make_response(jsonify({
                    "msg": user_data,
                    "status_code": 404
                }), 404)
            if isinstance(user_data, str):
                return make_response(jsonify({
                    "msg": user_data,
                    "status_code": 404
                }), 404)
            return make_response(jsonify({
                "data": user_data,
                "msg": self.messages["read"],
                "status_code": 200
            }), 200)
        if(auth["id"] == id):
            user_results = user_db.get_single_user_by_id(id)
            if isinstance(user_results, dict):
                return make_response(jsonify({
                    "data": [user_results],
                    "msg": self.messages["read"],
                    "status_code": 200
                }), 200)

            if isinstance(user_results, str):
                return make_response(
                    jsonify(get_error(user_results, 404)), 404
                    )
            return make_response(
                jsonify(
                    get_error(error_messages["404"], 404)), 404
                )
        return make_response(jsonify({
            "msg": auth_error_messages["403"],
            "status_code": 403
        }), 403)

    def post(self):
        """
        POST endpoint for user resource that creates a new user

        Returns
        -------
        A JSON response to the user once created
        """
        if not is_valid_json(request.get_data()):
            abort(400, message=error_messages["BAD_JSON"], status_code=400)
        new_user = user_parser.parse_args(strict=True)
        new_user["fname"] = validator.remove_whitespace(new_user["fname"])
        new_user["lname"] = validator.remove_whitespace(new_user["lname"])
        new_user["othername"] = validator.remove_whitespace(
            new_user["othername"]
            )
        new_user["email"] = validator.remove_whitespace(new_user["email"])
        new_user["username"] = validator.remove_whitespace(
            new_user["username"].lower()
            )
        new_user["phone"] = validator.remove_whitespace(new_user["phone"])
        non_empty_items = {
            "first name": new_user["fname"],
            "last name": new_user["lname"],
            "email": new_user["email"],
            "username": new_user["username"],
            "phone number": new_user["phone"],
            "password": new_user["password"]
            }
        for user_item in non_empty_items:
            item_val = non_empty_items[user_item]
            if item_val == "" or item_val is None:
                empty_item_err = "Your %s cannot be empty" % user_item
                return make_response(jsonify(
                    get_error(empty_item_err,
                              400)), 400)
        validation_results = validate_user_post_input(validator,
                                                      new_user)
        if validation_results is not True:
            return validation_results
        new_user["createdOn"] = datetime.datetime.today().strftime('%Y/%m/%d')
        new_user["isAdmin"] = False
        create_results = user_db.save(new_user)
        if isinstance(create_results, dict):
            return make_response(jsonify({
                "data": [create_results],
                "msg": self.messages["created"],
                "status_code": 201
            }), 201)
        duplicate = user_db.message["DUPLICATE"]

        if isinstance(create_results, str) and duplicate in create_results:
            abort(409, msg=create_results, status_code=409)
        if isinstance(create_results, str):
            return make_response(jsonify(get_error(create_results, 400)),
                                 400)
