# -*- coding: utf-8 -*-
"""
    app.api.v2
    ~~~~~~~~~~~~~~

    A module for setting the resources and blueprint configuration
    for version 2 of the application

"""
from flask import Blueprint
from flask_restful import Api


# Local imports
from .views.user import UserView
from .views.auth import AuthView
from .views.incident import IncidentView

v2 = Blueprint("v2", __name__, url_prefix="/api/v2")

api_v2 = Api(v2)
api_v2.add_resource(UserView, '/users')
api_v2.add_resource(AuthView, '/auth')
api_v2.add_resource(IncidentView, '/incidents')
