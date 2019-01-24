import alerts from '../components/alerts.js';
import router from '../helpers/router.js';
import reqHelpers from '../helpers/request_helpers.js';
import inputHelpers from '../helpers/input_helpers.js';
import authHelpers from '../helpers/auth_helpers.js';
import constants from '../constants.js';

const { getElTextValue } = inputHelpers;
const { postData, getValidationErrorMessage } = reqHelpers;
const { ireporterSettings, defaultHeaders, alertIds } = constants;
const { createAlert } = alerts;
const { newUrl, uiUrlFilepaths } = router;
const { setAuth, removeAuth } = authHelpers;

function login(e) {
  // Function used to sign in user based on username and password
  e.preventDefault();
  createAlert('loading...', alertIds.loading);
  const username = getElTextValue('login_username');
  const password = getElTextValue('login_password');
  removeAuth();
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
      setAuth(userData);
      newUrl(uiUrlFilepaths.PROFILE);
    })
    .catch(((error) => {
      if (error && error.msg) createAlert(error.msg, alertIds.error);
      console.log('login function error', error);
    }));
}

function logout(e) {
  // Function used to sign out user
  e.preventDefault();
  createAlert('loading...', alertIds.loading);
  removeAuth();
  createAlert('User logged out', alertIds.success);
  newUrl(uiUrlFilepaths.HOME);
}

function register(e) {
  // Function used to sign up new user
  e.preventDefault();
  createAlert('loading...', alertIds.loading);
  const newUserDetails = {
    username: getElTextValue('sign_up_username'),
    password: getElTextValue('sign_up_password'),
    fname: getElTextValue('sign_up_fname'),
    lname: getElTextValue('sign_up_lname'),
    othername: getElTextValue('sign_up_othername'),
    email: getElTextValue('sign_up_email'),
    phone: getElTextValue('sign_up_phone'),
  };
  const registerUrl = `${ireporterSettings.base_api_url}/users`;
  postData(registerUrl, newUserDetails, defaultHeaders)
    .then((data) => {
      console.log('sign up function data: ', data);
      if (data.status_code && data.status_code !== 201) {
        if (data.msg) createAlert(data.msg, alertIds.error);
        if (data.message) {
          createAlert(getValidationErrorMessage(data), alertIds.error);
        }
        return;
      }
      createAlert('You have registered successfully', alertIds.success);
      newUrl(uiUrlFilepaths.LOGIN);
    })
    .catch((error) => {
      if (error && error.msg) createAlert(error.msg, alertIds.error);
      console.log('sign in function error', error);
    });
}

const userServices = {
  login,
  logout,
  register,
};

export default userServices;
