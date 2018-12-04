# -*- coding: utf-8 -*-
"""
    app.api.v1
    ~~~~~~~~~~~~~~

    A module for setting the resources and blueprint configuration
    for version 1 of the application

"""
from flask import Blueprint
from flask_restful import Api


# Local imports
from .views.incident import  IncidentView

v1 = Blueprint ("v1", __name__,url_prefix="/api/v1")

api = Api(v1)
api.add_resource(IncidentView, '/incidents','/incidents/<int:id>',
'/incidents/<int:id>/<prop>')
