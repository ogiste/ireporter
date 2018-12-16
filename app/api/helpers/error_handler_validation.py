
import json


def is_valid_json(str):
    """
    Function that checks if a string is a valid JSON object

    Returns
    --------
     Bool value true if the str is a valid JSON object, False otherwise
    """
    try:
        json.loads(str.decode("utf8"))
        return True
    except json.decoder.JSONDecodeError:
        return False
    except ValueError:
        return False


status_error_messages = {
    "400": ("Request could not be applied"
            " because of a client error e.g"
            " malformed request syntax or invalid request message "),
    "401": ("Request could not be applied"
            " because you lack authentication credentials"
            "for the target resource allow acces"),
    "403": ("You do not have sufficient credentials to access"
            " this resource"),
    "404": "The resource requested could not be found",
    "409": ("The request could not be completed due to a"
            " conflict with the current state of the target resource"),
    "500": ("The server encountered an error :("
            " Administrators have been notified.")

}
