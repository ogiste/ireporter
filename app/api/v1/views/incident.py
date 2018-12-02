import datetime

from flask import Flask, make_response,jsonify,request
from flask_restful import Resource

#Local imports

from app.api.v1.models import IncidentModel


class IncidentView(Resource, IncidentModel):
    """docstring for IncidentView."""

    def __init__(self):
        self.db = IncidentModel()

    def post(self):
        new_incident = request.get_json()
        new_incident["createdOn"] = datetime.datetime.today().strftime('%Y-%m-%d')
        new_incident["createdBy"] = (len(self.db.get_incidents())+1)
        new_incident["status"] = "draft"
        new_incident["images"] = ["/url/image1","url/image2"]
        new_incident["videos"] = ["/url/video1","url/video2"]

        incidents_data = self.db.save(new_incident)
        return make_response(jsonify({
            "data":incidents_data,
            "msg":"success",
            "status_code":201
        }),201)

    def get(self,id=None):
        if id is None:
            incidents_data = self.db.get_incidents()
            return make_response(jsonify({
                "data":incidents_data,
                "msg":"success",
                "status_code":200
            }),200)
        else:
            incident = self.db.get_incident(id)
            return make_response(jsonify({
                "data":[incident],
                "msg":"success",
                "status_code":200
            }),200)

    def patch(self,id,prop):
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
        if id != None:
            deleted_incident =  self.db.delete_incident(id)
            return make_response(jsonify({
                "data":[deleted_incident],
                "msg":"success",
                "status_code":202
            }),202)