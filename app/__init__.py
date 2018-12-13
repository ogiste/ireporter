# -*- coding: utf-8 -*-
"""
    app
    ~~~~~~~~~~~~~~

    A module containing the function that creates the Flask application

"""

from flask import Flask, make_response, jsonify
from instance.config import app_config
from .api.v1 import v1 as version_one
from .api.v2 import v2 as version_two
from app.db_config import connect, create_tables


def create_app(config_name="development"):
    """
    Function used to create the Flask application.
    Takes a string defining the configuration name as a parameter to use when
    setting application
    configuration variables such as debugging and database selection.

    Returns
    --------
    flask application object with settings configured
    """
    app = Flask(__name__)
    app.url_map.strict_slashes = False
    app.config.from_object(app_config[config_name])
    app.config['BUNDLE_ERRORS'] = True
    conn = connect(app.config['DB_NAME'])
    create_tables(conn)
    app.register_blueprint(version_one)
    app.register_blueprint(version_two)

    @app.errorhandler(403)
    def forbidden(error):
        return make_response(jsonify({
            "status_code": 403,
            "msg": ("You do not have sufficient permission to access"
                    " this resource")
        }), 403)

    @app.errorhandler(500)
    def internal_server_error(error):
        app.logger.error('Server Error: %s', (error))
        return make_response(jsonify({
            "status": 500,
            "message": ("Whoops. The server encountered an error :("
                        " Administrators have been notified.")
        }), 500)
    return app
