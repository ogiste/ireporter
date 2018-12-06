import datetime
import types

from flask import Flask, make_response,jsonify,request
from flask_restful import Resource


#Local imports
from errors import parser,get_error



from app.api.v1.models.incident import IncidentModel

incident_parser = parser.copy()

incident_parser.add_argument('title',type = str,required = True,
    location = 'json',
    help = 'The title of the incident is a required field')

incident_parser.add_argument('type',type = str,required = True,
    choices = ('red-flag','intervention'),location = 'json',
    help = 'The type of the incident is a required field'+\
    '- must be red-flag or intervention')

incident_parser.add_argument('location',
    type = str,required = True,location = 'json',
    help = 'The Latitude and Longitude of the incident'+\
    ' is a required field')

incident_parser.add_argument('comment',
    type = str,required = True,location = 'json',
    help = 'The descriptive comment of the incident'+\
    ' is a required field')

incident_parser.add_argument('status',
    type = str,choices = ('draft','resolved','rejected','under investigation'),
    location = 'json',
    help = 'The status of the incident - can either be resolved,'+\
    'rejected or under investigation')

incident_parser.add_argument('images',action = 'append',location = 'json',
    help = "A list of image urls related to the incident and is not required")

incident_parser.add_argument('videos',action = 'append',location = 'json',
    help = "A list of video urls related to the incident and is not required")

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
        self.messages = {
            "deleted":"Incident successfully deleted",
            "created":"Incident successfully created",
            "updated":"Incident successfully updated",
            "read":"Incident(s) successfully retrieved"
        }

    def post(self):
        """
        POST endpoint for incident resource that creates a new instance
        and returns the incident once created
        """

        # new_incident = request.get_json()
        new_incident  = incident_parser.parse_args()
        new_incident["title"] = new_incident["title"].replace(" ", "")
        new_incident["type"] = new_incident["type"].replace(" ", "")
        new_incident["comment"] = new_incident["comment"].lstrip()
        new_incident["comment"] = new_incident["comment"].rstrip()
        new_incident["location"] = new_incident["location"].replace(" ", "")
        non_empty_items=[new_incident["title"],new_incident["type"],
        new_incident["comment"],new_incident["location"]]
        for incident_item in non_empty_items:
            if incident_item=="":
                return make_response(jsonify(
                get_error("Incident title,type,"+\
                " comment and location cannot be empty strings", 400)),400)


        new_incident["createdOn"] = datetime.datetime.today().strftime('%Y/%m/%d')
        new_incident["createdBy"] = (len(self.db.get_incidents())+1)
        new_incident["status"] = "draft"
        new_incident["images"] = ["/url/image1","url/image2"]
        new_incident["videos"] = ["/url/video1","url/video2"]
        incident_data = self.db.save(new_incident)

        return make_response(jsonify({
            "data":incident_data,
            "msg":self.messages["created"],
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
                "msg":self.messages["read"],
                "status_code":200
            }),200)
        incident_results = self.db.get_single_incident(id)
        if isinstance(incident_results,types.DictType):
            return make_response(jsonify({
                "data":[incident_results],
                "msg":self.messages["read"],
                "status_code":200
            }),200)

        if isinstance(incident_results,types.StringType):
            return make_response(jsonify(get_error(incident_results,400))
            ,400)


    def patch(self,id,prop):
        """
        PATCH endpoint that updates an incident comment or location
        properties using the :param :id to find the record and :param :prop to
        identify which incident property to update.
        """
        if prop=="comment" or prop=="location":
            patch_parser = parser.copy()
            patch_parser.add_argument('prop_value',type = str,required = True,
                location = 'json',
                help = "The new value of the {} of the incident and is a required field".format(prop)+\
                "- must be red-flag or intervention")
            new_data = patch_parser.parse_args()
            new_data["prop_value"].replace(" ","")
            if id != None and prop != None and new_data["prop_value"] != "":
                incident_data = self.db.update_incident(id,prop, new_data["prop_value"])
                return make_response(jsonify({
                    "data":[incident_data],
                    "msg":self.messages["updated"],
                    "status_code":200
                }),200)
            else:
                return make_response(jsonify(get_error("Cannot location"+
                "and comments can only be updated with a new valid string",400))
                ,400)

        return make_response(jsonify(get_error("Cannot find the page requested",
            404)),404)


    def delete(self, id):
        """
        DELETE endpoint that deletes a single incident using the :param :id
        to identify which incident to delete
        """
        delete_parser = parser.copy()
        delete_incident_parsed = delete_parser.parse_args()

        if id == None:
            return make_response(jsonify(get_error("Cannot delete"+
            "incident without a valid id",400))
            ,400)

        deleted_incident =  self.db.delete_incident(id)

        if deleted_incident==True:
            return make_response(jsonify({
                "msg":self.messages["deleted"],
                "status_code":202
            }),202)

        return make_response(jsonify(get_error(deleted_incident,400))
        ,400)
