
from app.db_config import connect
from pprint import pprint
from psycopg2 import IntegrityError


def get_all_incidents(incident_tuples, get_formated_incident_dict):
    """
    Function used to get all incidents in database as a list of dictionary
    items

    Returns
    -------
    List of dictionary items that represent incidents
    """

    incidents_all = []
    for incident in incident_tuples:
        incident_details = get_formated_incident_dict(incident)
        incidents_all.append(incident_details)
    return incidents_all


class IncidentModel():
    """
    IncidentModel used to view, edit and delete incident records

    Defines methods that define logic for for :

        -Create an incident record
        -Get all incident records
        -Get a single incident record
        -Update an incident record
        -Delete an incident record

        Incident Record : {
            "id": Integer,
            "createdOn": String, # Datetime string
            "createdBy": Integer,
            # Integer ID of the user who created the incident
            "title": String ,
            "type": String,
            "location": String, # Lat Long Coordinates
            "status": String,
            # Either draft,resolved,rejected or under investigation
            "images": List, # List of image urls
            "videos": List,# List of video urls
            "comment": String
        }

    """

    def __init__(self, db_name=None):
        """
        Constructor that initializes the Incident records database property
        """
        self.conn = connect(db_name)
        self.cursor = self.conn.cursor()
        self.message = {}
        self.message["NOT_FOUND"] = "The incident was not found with id: "
        self.message["NONE_EXIST"] = "No incidents could be found "
        self.message["NOT_CREATED"] = ("The incident was not created."
                                       " Please try again ")
        self.message["INTEGRITY"] = ("Could not create the incident")
        self.message["STATUS_CHANGE"] = ("Cannot edit an incident that is not"
                                         " in draft status")

    def get_formated_incident_dict(self, incident_tuple):
        """
        Method takes a single tuple from a database query and returns the
        incident details in an easily readable dictionary

        Returns
        -------
            Dictionary with key,value pairs of user data
        """
        incident_details = dict(enumerate(incident_tuple))
        incident_details[7] = incident_details[7].strftime('%Y/%m/%d')
        incident_details = {
            "id": incident_details[0],
            "createdBy": incident_details[1],
            "title": incident_details[2],
            "type": incident_details[3],
            "comment": incident_details[4],
            "status": incident_details[5],
            "location": incident_details[6],
            "createdOn": incident_details[7]
        }
        return incident_details

    def get_single_incident_by_id(self, id):
        """
        Method that retrieves a single incident from the incident
        records database

        Returns
        --------
        dictionary
            dictionary containing all incident details
        """

        select_incident_statement = """
        SELECT id,createdBy,title,type,comment,status,location,createdOn
        FROM incidents WHERE id={id};
        """.format(id=id)
        try:
            self.cursor.execute(select_incident_statement)
            result = self.cursor.fetchone()
            if result is not None:
                incident_details = self.get_formated_incident_dict(result)
                return incident_details
            return (self.message["NOT_FOUND"] + str(id) +\
                    " Record could not be found or doesnot exist")
        except IntegrityError as e:
            return self.message["NOT_FOUND"] + str(id) \
             + "Record could not be found or doesnot exist"

    def get_incidents(self):
        """
        Method that retrieves a single incident from the incident records database

        Returns
        --------
        dictionary
            dictionary containing all incident details
        """

        select_incidents_statement = """
        SELECT id,createdBy,title,type,comment,status,location,createdOn
        FROM incidents;
        """
        try:
            self.cursor.execute(select_incidents_statement)
            result = self.cursor.fetchall()
            if(len(result) > 0):
                incidents_all = get_all_incidents(
                    result, self.get_formated_incident_dict
                )
                return incidents_all
            return self.message["NONE_EXIST"]
        except IntegrityError as e:
            return self.message["NOT_FOUND"] + str(id) \
             + "Record could not be found or doesnot exist"

    def update_incident(self, id, prop, prop_value, isAdmin=False):
        """
        Update a property of an incident
        by taking the :id arg to find the incident record,
        :prop arg to identify the key of the property of the record to update,
        :prop_value arg to store the new property value

        Returns
        --------
        dictionary
            dictionary containing all details of found incident and a success message
            OR
        String containing an error message and the success status of the update.
        """
        incident = self.get_single_incident_by_id(id)
        if not isinstance(incident, dict):
            return self.message["NOT_FOUND"] + str(id) \
             + " Record could not be found or doesnot exist"

        if incident['status'] != "draft" and isAdmin is False:
            return self.message["STATUS_CHANGE"]
        update_incident_statement = """
        UPDATE incidents SET {prop} = $${prop_value}$$ WHERE id ={id};
        """.format(prop=prop, prop_value=prop_value, id=id)

        try:

            result = self.cursor.execute(update_incident_statement)
            if result is None:
                incident_details = self.get_single_incident_by_id(id)
                return incident_details
            return (self.message["NOT_FOUND"] + str(id) +\
                    " Record could not be found or doesnot exist")
        except IntegrityError as e:
            return self.message["NOT_FOUND"] + str(id) \
             + "Record could not be found or doesnot exist"
        except Exception as e:
            return str(e)

    def get_my_incidents(self, user_id):
        """
        Method used to retrieve all incidents created by the current user

        Returns
        --------
        dictionary
            dictionary containing all incident details

            OR
        String with an error message
        """
        select_incidents_statement = """
        SELECT id,createdBy,title,type,comment,status,location,createdOn
        FROM incidents WHERE createdBy={};
        """.format(int(user_id))
        try:
            self.cursor.execute(select_incidents_statement)
            result = self.cursor.fetchall()
            if(len(result) > 0):
                incidents_all = get_all_incidents(
                    result, self.get_formated_incident_dict
                )
                return incidents_all
            return self.message["NONE_EXIST"]
        except IntegrityError as e:
            return self.message["NOT_FOUND"] + str(id) \
             + "Record could not be found or doesnot exist"

    def save(self, new_incident):
        """
        Creates a new incident record
        by taking in a :new_incident arg of type dictionary
        with all need incident details.

        Returns
        --------
        dictionary
            dictionary containing all newly created incident details
        """

        data = {
            "createdOn": new_incident["createdOn"],
            "createdBy": new_incident["createdBy"],
            "title": new_incident["title"],
            "type": new_incident["type"],
            "location": new_incident["location"],
            "status": new_incident["status"],
            "comment": new_incident["comment"]
        }
        insert_incident_statement = """
        INSERT INTO incidents(
        createdBy,title,type,comment,status,location,createdOn)
        VALUES ({createdBy},$${title}$$,'{type}',$${comment}$$,'{status}',
        '{location}','{createdOn}') RETURNING id ;
        """.format(
            createdBy=new_incident["createdBy"],  # A a value from auth'd user
            title=new_incident["title"],
            type=new_incident["type"],
            comment=new_incident["comment"],
            status='draft',
            location=new_incident["location"],
            createdOn=new_incident["createdOn"]
        )
        try:
            self.cursor.execute(insert_incident_statement)
            incident_results = self.cursor.fetchone()
            return self.get_single_incident_by_id(incident_results[0])
        except IntegrityError as e:
            return self.message["INTEGRITY"]
        except IntegrityError as e:
            return self.message["NOT_CREATED"]
        return data

    def delete_incident(self, id):
        """
        Find a single incident record and delete it.

        Returns
        --------
        bool
            bool value of True if incident was deleted
        string
            string defining an error message
        """

        delete_incidents_statement = """
        DELETE FROM incidents WHERE id={};
        """.format(id)
        incident = self.get_single_incident_by_id(id)
        if not isinstance(incident, dict):
            return self.message["NOT_FOUND"] + str(id) \
             + " Record could not be found or doesnot exist"
        try:
            result = self.cursor.execute(delete_incidents_statement)
            if result is None:
                return True
        except IntegrityError as e:
            return self.message["NOT_FOUND"] + str(id) \
             + "Record could not be found or doesnot exist"
        except Exception as e:
            return str(e)
