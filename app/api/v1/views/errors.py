
"""
Create the default reqparse object to be used by all resources

"""

from flask_restful import reqparse


parser = reqparse.RequestParser()

parser.add_argument('id', type=int, help='id must be a valid integer',location='args')

def get_error(error_message,status_code):
    """
    Take and error message and status_code of a response

    Returns
    -------
    dictionary
        dictionary containing the error message and status code to be used in a
        response
    """
    return {
        "msg":error_message,
        "status_code":status_code
    }
