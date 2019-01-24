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

function createIncidentRecord(e) {
  // Function used to create a new incident record

  e.preventDefault();
  createAlert('loading...', alertIds.loading);
  const newIncidentDetails = {
    username: getElTextValue('sign_up_username'),
    password: getElTextValue('sign_up_password'),
    fname: getElTextValue('sign_up_fname'),
    lname: getElTextValue('sign_up_lname'),
    othername: getElTextValue('sign_up_othername'),
    email: getElTextValue('sign_up_email'),
    phone: getElTextValue('sign_up_phone'),
  };

  const newIncidentUrl = `${ireporterSettings.base_api_url}/incident`;
  postData(newIncidentUrl, newIncidentDetails, defaultHeaders)
    .then((data) => {
      console.log('new incident function data: ', data);
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
      console.log('new incident function error', error);
    });
}
