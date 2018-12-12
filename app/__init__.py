# -*- coding: utf-8 -*-
"""
    app
    ~~~~~~~~~~~~~~

    A module containing the function that creates the Flask application

"""

from flask import Flask
from instance.config import app_config
from .api.v1 import v1 as version_one
from .api.v2 import v2 as version_two
from app.db_config import connect, create_tables

def create_app(config_name="development"):
    app = Flask(__name__)
    app.url_map.strict_slashes = False
    app.config.from_object(app_config[config_name])
    app.config['BUNDLE_ERRORS'] = True
    conn=connect(app.config['DB_NAME'])
    create_tables(conn)
    app.register_blueprint(version_one)
    app.register_blueprint(version_two)
    return app
