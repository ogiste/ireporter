
incident_list = []

def is_in_db(id,db):
    if(id <= len(db) and len(db) > 0):
        print "Item does not exist in incident db"
        return False
    return True

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
    def __init__(self):
        """
        Constructor that initializes the Incident records database property
        """
        self.db = incident_list
        self.NOT_FOUND = "The incident was not found with id: "

    def save(self,new_incident):
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
            "id":(len(self.db)+1),
            "createdOn": new_incident["createdOn"],
            "createdBy":new_incident["createdBy"],
            "title":new_incident["title"],
            "type":new_incident["type"],
            "location":new_incident["location"],
            "status":new_incident["status"],
            "images":new_incident["images"],
            "videos":new_incident["videos"],
            "comment":new_incident["comment"]
        }

        self.db.append(data)
        return data

    def get_incidents(self):
        """
        Method gets all created incidents

        Returns
        --------
        list
            list of all created incident records
        """

        return self.db

    def get_single_incident(self, id):
        """
        Finds a single incident record
        in the database and returns it in dictionary format once
        found otherwise returns an error message

        Returns
        --------
        dictionary
            dictionary containing all detals of found incident
        string
            string describing error if incident was not found
        """
        if is_in_db(id,self.db):
            return None
        for indx,incident in enumerate(self.db):
            if incident["id"]==id:
                return incident
            elif indx==(len(self.db)-1):
                return self.NOT_FOUND + str(id) \
                 + " Could not get a non-existent record"

    def delete_incident(self,id):
        """
        Find a single incident record and delete it.

        Returns
        --------
        bool
            bool value of True if incident was deleted
        string
            string defining an error message
        """
        if is_in_db(id,self.db):
            return None
        (id,self.db)
        if len(self.db) == 0:
             return self.NOT_FOUND + str(id) \
             + " Could not delete a non-existent record"

        for indx,incident in enumerate(self.db):
            if incident["id"]==id:
                 self.db.remove(incident)
                 return True
            elif indx==(len(self.db)-1):
                return self.NOT_FOUND + str(id) \
                + " Could not delete a non-existent record"

    def update_incident(self,id,prop, prop_value):
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

        dictionary
            dictionary contaiing an error message and the success status of the update.
        """
        if is_in_db(id,self.db):
            return None
        update_incident_list = [incident for incident in self.db if incident["id"]==id ]
        print update_incident_list
        update_incident = update_incident_list[0]
        if (len(update_incident_list)>=1):
            update_incident = update_incident_list[0]
            update_incident[prop]=prop_value
            return update_incident

        error_msg=self.NOT_FOUND + str(id) \
             + "Could not update a non-existent record"
        return error_msg
