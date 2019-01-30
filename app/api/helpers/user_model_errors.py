unique_column_items = {
    "username": "username",
    "phone number": "phone",
    "email address": "email"
}


def get_duplicate_message(model_error):
    """
    Function used to return the duplicate resource error message
    Take the exception error of an IntegrityError and returns the
    valid error message for a database column

    Returns
    ------------
    String providing duplicate error message
    """
    print("get dup message")
    print("model_error")
    print(model_error)
    for user_column_item in unique_column_items:
        col_val = unique_column_items[user_column_item]
        if col_val in model_error:
            dup_col_error = (
                "The {user_col}".format(user_col=user_column_item)
                + " provided is already taken. Please provide another.")
            return dup_col_error
