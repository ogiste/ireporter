#from app.api.v1.models import user.model,incident.model
from flask import Blueprint
from flask_restful import Api


# Local imports
from .views import  IncidentView

v1 = Blueprint ("v1", __name__,url_prefix="/api/v1")

api = Api(v1)
api.add_resource(IncidentView, '/incidents','/incidents/<int:id>','/incidents/<int:id>/<prop>')
