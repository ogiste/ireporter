
import postData from '../helpers/request_helpers';
import getElById from '../helpers/user_input_helpers';
import { ireporterSettings, defaultHeaders } from '../constants';

class User {
  // User class defining properties of a user object and class methods
  // User properties:
  //     fname: First Name (String)
  //     lname: Second Name (String)
  //     othername: Other Name (String)
  //     username: Username (String)
  //     email: Email (String)
  //     phone: Phone (String)
  //     isAdmin: is Administrator (Boolean)
  //     createdOn: Created On (Datetime)

  constructor(userData) {
    // constructor to initialize user details
    this.fname = userData.fname;
    this.lname = userData.lname;
    this.othername = userData.othername;
    this.username = userData.username;
    this.email = userData.email;
    this.phone = userData.phone;
    this.isAdmin = userData.isAdmin;
    this.createdOn = userData.createdOn;
  }
}

function login() {
  // Function used to sign in user based on username and password
  const username = getElById('login_username');
  const password = getElById('login_password');
  const loginUrl = `${ireporterSettings.base_url}/auth`;
  postData(loginUrl, { username, password }, defaultHeaders)
    .then(data => console.log('login function data', data))
    .catch(error => console.log('login function error', error));
}

const userServices = {
  User,
  login,
};

export default userServices;
