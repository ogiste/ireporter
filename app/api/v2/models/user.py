
from app.db_config import connect
from psycopg2 import IntegrityError
from passlib.hash import sha256_crypt
from app.api.helpers.user_model_errors import get_duplicate_message


def get_all_users(user_tuples, get_formated_user_dict):
    """
    Function used to get all users in database as a list of dictionary
    items

    Returns
    -------
    List of dictionary items that represent users
    """

    users_all = []
    for user in user_tuples:
        user_details = get_formated_user_dict(user)
        users_all.append(user_details)
    return users_all

class UserModel():
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

    def __init__(self, db_name=None):
        """
        Constructor that initializes the user records database object
        """

        self.conn = connect(db_name)
        self.cursor = self.conn.cursor()
        self.message = {}
        self.message["NOT_FOUND"] = "The user was not found with username - "
        self.message["NOT_CREATED"] = ("The user was not created."
                                       " Please try again ")
        self.message["NONE_EXIST"] = "No users could be found "
        self.message["DUPLICATE"] = (
            "username,email or phone number is already taken."
            " Please provide alternative details")

    def verify_pass(self, user_credentials):
        """
        A method that compares a candidate password to a users password

        Returns
        -------
            True if the verification was successful
            False if the verification failed
        """
        username = user_credentials["username"]
        candidate_pass = user_credentials["password"]
        select_credentials_statement = """
        SELECT username,password FROM users WHERE username='{username}'
        """.format(username=username)
        try:
            self.cursor.execute(select_credentials_statement)
            result = self.cursor.fetchone()
            if result is not None:
                username = result[0]
                pw_hash = result[1]
                authenticated = sha256_crypt.verify(candidate_pass, pw_hash)
                return authenticated
            return None
        except Exception as e:
            if hasattr(e, 'message'):
                return None
            return self.message["NOT_FOUND"] + str(username) \
                + " Record could not be found , doesnot exist"

    def get_users(self):
        """
        Method that retrieves a single user from the user records database

        Returns
        --------
        dictionary
            dictionary containing all user details
        """

        select_user_statement = """
        SELECT id,username,fname,lname,othername,email,createdOn,isAdmin,phone
        FROM users;
        """
        try:
            self.cursor.execute(select_user_statement)
            result = self.cursor.fetchall()
            if (len(result) > 0):
                all_users = get_all_users(result, self.get_formated_user_dict)
                return all_users
            return (self.message["NONE_EXIST"] )
        except IntegrityError as e:
            return self.message["NOT_FOUND"] +\
             " Record could not be found or doesnot exist"

    def get_formated_user_dict(self, user_tuple, allInfo=True):
        """
        Method takes a single tuple from a database query and returns the user
        details in an easily readable dictionary

        Returns
        -------
            Dictionary with key,value pairs of user data
        """
        user_details = dict(enumerate(user_tuple))
        user_details[6] = user_details[6].strftime('%Y/%m/%d')
        user_details = {
            "id": user_details[0],
            "username": user_details[1],
            "fname": user_details[2],
            "lname": user_details[3],
            "othername": user_details[4],
            "email": user_details[5],
            "createdOn": user_details[6],
            "isAdmin": user_details[7],
            "phone": user_details[8]
        }
        if allInfo is True:
            return user_details

        del user_details["isAdmin"]
        return user_details

    def get_single_user_by_id(self, id):
        """
        Method that retrieves a single user from the user records database

        Returns
        --------
        dictionary
            dictionary containing all user details
        """

        select_user_statement = """
        SELECT id,username,fname,lname,othername,email,createdOn,isAdmin,phone
        FROM users WHERE id={id};
        """.format(id=id)
        try:
            self.cursor.execute(select_user_statement)
            result = self.cursor.fetchone()
            if result is not None:
                user_details = self.get_formated_user_dict(result)
                return user_details
            return (self.message["NOT_FOUND"] + str(id) +\
                    "Record could not be found or doesnot exist")
        except IntegrityError as e:
            return self.message["NOT_FOUND"] + str(id) \
             + " Record could not be found or doesnot exist"

    def get_single_user_by_username(self, username):
        """
        Method that retrieves a single user from the user records database

        Returns
        --------
        dictionary
            dictionary containing all user details
        """

        select_user_statement = """
        SELECT id,username,fname,lname,othername,email,createdOn,isAdmin,phone
        FROM users WHERE username='{username}';
        """.format(username=username)
        try:
            self.cursor.execute(select_user_statement)
            result = self.cursor.fetchone()
            if result is not None:
                user_details = self.get_formated_user_dict(result)
                return user_details
            return (self.message["NOT_FOUND"] + str(username) +\
                    "Record could not be found or doesnot exist")
        except IntegrityError as e:
            return self.message["NOT_FOUND"] + str(username) \
             + " Record could not be found or doesnot exist"

    def save(self, new_user, isAdmin=None):
        """
        Creates a new user record
        by taking in a :new_user arg of type dictionary
        with all needed user details.

        Returns
        --------
        dictionary
            dictionary containing all newly created user details
        """
        new_user = {
            "fname": new_user["fname"],
            "lname": new_user["lname"],
            "othername": new_user["othername"],
            "email": new_user["email"],
            "phone": new_user["phone"],
            "username": new_user["username"],
            "password": new_user["password"],
            "createdOn": new_user["createdOn"],
            "isAdmin": new_user["isAdmin"]
        }
        if isAdmin is True:
            new_user["isAdmin"] = True
        pw_hash = sha256_crypt.hash(new_user["password"])
        insert_user_statement = """INSERT INTO users(
        fname,lname,othername,username,email,phone,password,createdOn,isAdmin)
        VALUES ('{fname}','{lname}','{othername}','{username}','{email}',
        '{phone}','{password}','{createdOn}',
        '{isAdmin}');""".format(fname=new_user["fname"],
                                lname=new_user["lname"],
                                othername=new_user["othername"],
                                username=new_user["username"],
                                email=new_user["email"],
                                phone=new_user["phone"],
                                password=pw_hash,
                                createdOn=new_user["createdOn"],
                                isAdmin=new_user["isAdmin"])
        try:
            self.cursor.execute(insert_user_statement)
            return self.get_single_user_by_username(new_user["username"])
        except IntegrityError as e:
            return get_duplicate_message(e.pgerror)
        except Exception as e:
            return self.message["NOT_CREATED"]
