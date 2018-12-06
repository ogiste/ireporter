
from app.db_config import connect
from pprint import pprint
from psycopg2 import IntegrityError


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

    def __init__(self,db_name="ireporter"):
        """
        Constructor that initializes the user records database object
        """
        print db_name
        self.conn = connect(db_name)
        self.cursor = self.conn.cursor()
        self.NOT_FOUND = "The user was not found with username - "
        self.NOT_CREATED = "The user was not created. Please try again "

    def get_formated_user_dict(self, user_tuple, allInfo=False):
        """
        Method takes a single tuple from a database query and returns the user
        details in an easily readable dictionary

        Returns
        -------
            Dictionary with key,value pairs of user data
        """
        print(len(user_tuple))
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
            user_details = self.get_formated_user_dict(result)
            return user_details
        except IntegrityError as e:
            pprint("Raised exception: ")
            if hasattr(e, 'message'):
                print(e.message)
            else:
                print(e)
            return self.NOT_FOUND + str(username) \
             + "Record could not be found or doesnot exist"

    def save(self, new_user):
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
                                password=new_user["password"],
                                createdOn=new_user["createdOn"],
                                isAdmin=new_user["isAdmin"])
        try:
            self.cursor.execute(insert_user_statement)
            print "User created"
            return self.get_single_user_by_username(new_user["username"])
        except IntegrityError as e:
            pprint("Raised exception: ")
            if hasattr(e, 'message'):
                print(e.message)
            else:
                print(e)
            return "username,email or phone number is already taken."+\
                " Please provide alternative details"
        except IntegrityError as e:
            pprint("Raised exception: ")
            if hasattr(e, 'message'):
                print(e.message)
            else:
                print(e)
            return self.NOT_CREATED
