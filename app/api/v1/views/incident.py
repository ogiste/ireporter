import datetime

from flask import Flask, make_response,jsonify,request
from flask_restful import Resource

#Local imports

from app.api.v1.models.incident import IncidentModel


class IncidentView(Resource, IncidentModel):
    """
    Views that establish endpoints for :

        -Create an incident
        -Get all incidents
        -Get a single incident
        -Update an incident
        -Delete an incident

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
        Constructor sets the IncidentView instance.db to the database
        from the Incident Module class
        """

        self.db = IncidentModel()

    def post(self):
        """
        POST endpoint for incident resource that creates a new instance
        and returns the incident once created
        """

        new_incident = request.get_json()
        new_incident["createdOn"] = datetime.datetime.today().strftime('%Y-%m-%d')
        new_incident["createdBy"] = (len(self.db.get_incidents())+1)
        new_incident["status"] = "draft"
        new_incident["images"] = ["/url/image1","url/image2"]
        new_incident["videos"] = ["/url/video1","url/video2"]

        incident_data = self.db.save(new_incident)
        return make_response(jsonify({
            "data":incident_data,
            "msg":"success",
            "status_code":201
        }),201)

    def get(self,id=None):
        """
        GET method returns all incidents if :param :id is None or a single
        incident if :param :id is an integer
        """

        if id is None:
            incidents_data = self.db.get_incidents()
            return make_response(jsonify({
                "data":incidents_data,
                "msg":"success",
                "status_code":200
            }),200)
        else:
            incident = self.db.get_single_incident(id)
            return make_response(jsonify({
                "data":[incident],
                "msg":"success",
                "status_code":200
            }),200)

    def patch(self,id,prop):
        """
        PATCH endpoint that updates an incident comment or location
        properties using the :param :id to find the record and :param :prop to
        identify which incident property to update.
        """

        new_data = request.get_json()
        if id != None and prop != None:
            incident_data = self.db.update_incident(id,prop, new_data["prop_value"])
            return make_response(jsonify({
                "data":[incident_data],
                "msg":"success",
                "status_code":200
            }),200)
        else:
            return make_response(jsonify({
                "error":"Bad request",
                "msg":"fail",
            }),400)

    def delete(self, id):
        """
        DELETE endpoint that deletes a single incident using the :param :id
        to identify which incident to delete
        """

        if id != None:
            deleted_incident =  self.db.delete_incident(id)
            return make_response(jsonify({
                "msg":"success",
                "status_code":202
            }),202)
