import sys
from app.api.v2.models.user import UserModel
import datetime

user_db = UserModel()


def create_admin():
    """
    This function uses cli arguments to create an admin user

    cli arguments must be in this order
    --------------
    1.first name
    2.last name
    3.othername
    4.username
    5.email
    6.phone
    7.password
    """

    if len(sys.argv) == 8:
        new_user = {
            "fname": sys.argv[1],
            "lname": sys.argv[2],
            "othername": sys.argv[3],
            "username": sys.argv[4],
            "email": sys.argv[5],
            "phone": sys.argv[6],
            "password": sys.argv[7],
            "isAdmin": True,
            "createdOn": datetime.datetime.today().strftime('%Y/%m/%d')
        }
        create_results = user_db.save(new_user, isAdmin=True)
        if isinstance(create_results, dict):
            print("Admin created")

if __name__ == '__main__':
    create_admin()
