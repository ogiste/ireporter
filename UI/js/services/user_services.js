import alerts from '../components/alerts.js';
import router from '../helpers/router.js';
import reqHelpers from '../helpers/request_helpers.js';
import inputHelpers from '../helpers/input_helpers.js';
import authHelpers from '../helpers/auth_helpers.js';
import constants from '../constants.js';

const { getElById } = inputHelpers;
const { postData } = reqHelpers;
const { ireporterSettings, defaultHeaders, alertIds } = constants;
const { createAlert } = alerts;
const { newUrl, uiUrlFilepaths } = router;
const { setAuth, removeAuth } = authHelpers;

function login() {
  // Function used to sign in user based on username and password
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
      setAuth(userData);
      newUrl(uiUrlFilepaths.PROFILE);
    })
    .catch(((error) => {
      if (error && error.msg) createAlert(error.msg, alertIds.error);
      console.log('login function error', error);
    }));
}

function logout() {
  // Function used to sign in user based on username and password
  console.log('logout called..');
  createAlert('loading...', alertIds.loading);
  removeAuth();
  createAlert('User logged out', alertIds.success);
  newUrl(uiUrlFilepaths.HOME);
}

const userServices = {
  login,
  logout,
};

export default userServices;
