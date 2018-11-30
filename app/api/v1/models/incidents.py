incident_list = []

class IncidentModel():
    """docstring for IncidentModel."""
    def __init__(self):
        self.db = incident_list

    def save(self,new_incident):
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
        return self.db

    def get_incidents(self):
        return self.db
