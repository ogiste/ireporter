import alerts from '../components/alerts.js';
import router from '../helpers/router.js';
import reqHelpers from '../helpers/request_helpers.js';
import userInputHelpers from '../helpers/user_input_helpers.js';
import constants from '../constants.js';

const { getElById } = userInputHelpers;
const { postData } = reqHelpers;
const { ireporterSettings, defaultHeaders, alertIds } = constants;
const { createAlert } = alerts;
const { newUrl } = router;

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

function login(e) {
  // Function used to sign in user based on username and password
  e.preventDefault();
  createAlert('loading...', alertIds.loading);
  const username = getElById('login_username').value;
  const password = getElById('login_password').value;
  const loginUrl = `${ireporterSettings.base_api_url}/auth`;
  postData(loginUrl, { username, password }, defaultHeaders)
    .then((data) => {
      console.log('login function data', data);
      if (data.status_code && data.status_code !== 200) {
        if (data.msg) createAlert(data.msg, alertIds.error);
        return;
      }
      createAlert(data.msg, alertIds.success);
      const userData = data.data[0];
      localStorage.setItem('ireporter_auth', userData.token);
      localStorage.setItem('ireporter_username', userData.user.username);
      newUrl('profile.html');
    })
    .catch(((error) => {
      if (error && error.msg) createAlert(error.msg, alertIds.error);
      console.log('login function error', error);
    }));
}

function logout(e) {
  // Function used to sign in user based on username and password
  e.preventDefault();
  createAlert('loading...', alertIds.loading);
  localStorage.removeItem('ireporter_auth');
  localStorage.removeItem('ireporter_username');
  createAlert('User logged out', alertIds.success);
  newUrl('index.html');
}

const loginSubmit = getElById('login_submit');
loginSubmit.addEventListener('click', login);
getElById('logout').addEventListener('click', logout);

const userServices = {
  User,
  login,
};

export default userServices;
