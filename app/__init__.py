# -*- coding: utf-8 -*-
"""
    app
    ~~~~~~~~~~~~~~

    A module containing the function that creates the Flask application

"""

from flask import Flask, make_response, jsonify
from instance.config import app_config
from .api.v2 import v2 as version_two
from app.db_config import connect, create_tables
from app.api.helpers.error_handler_validation import status_error_messages
from flask_cors import CORS


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
    CORS(app)
    app.url_map.strict_slashes = False
    app.config.from_object(app_config[config_name])
    conn = connect(app.config['DB_NAME'])
    create_tables(conn)
    app.register_blueprint(version_two)

    @app.errorhandler(400)
    def handle_bad_request(error):
        return make_response(jsonify({
            "status_code": 400,
            "msg": status_error_messages["400"]
        }), 400)

    @app.errorhandler(401)
    def no_auth_credentials(error):
        return make_response(jsonify({
            "status_code": 401,
            "msg": status_error_messages["401"]
        }), 401)

    @app.errorhandler(403)
    def forbidden(error):
        return make_response(jsonify({
            "status_code": 403,
            "msg": status_error_messages["403"]
        }), 403)

    @app.errorhandler(404)
    def page_not_found(error):
        return make_response(jsonify({
            "status_code": 404,
            "msg": status_error_messages["404"]
        }), 404)

    @app.errorhandler(409)
    def conflict(error):
        return make_response(jsonify({
            "status_code": 409,
            "msg": status_error_messages["409"]
        }), 409)

    @app.errorhandler(500)
    def internal_server_error(error):
        app.logger.error('Server Error: %s', (error))
        return make_response(jsonify({
            "status_code": 500,
            "msg": status_error_messages["500"]
        }), 500)
    return app
