# -*- coding: utf-8 -*-
"""
    app
    ~~~~~~~~~~~~~~

    A module containing the function that creates the Flask application

"""

from flask import Flask
from instance.config import app_config, DevelopmentConfig, TestingConfig, ProductionConfig
from .api.v1 import v1 as version_one

def create_app(config_name="development"):
    app = Flask(__name__,instance_relative_config=True)
    app.url_map.strict_slashes = False
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile("config.py", silent=False)
    app.register_blueprint(version_one)
    return app
