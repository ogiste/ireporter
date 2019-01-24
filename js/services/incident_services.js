import alerts from '../components/alerts.js';
import router from '../helpers/router.js';
import reqHelpers from '../helpers/request_helpers.js';
import inputHelpers from '../helpers/input_helpers.js';
import authHelpers from '../helpers/auth_helpers.js';
import constants from '../constants.js';

const { getElTextValue, getSelectedInputOption } = inputHelpers;
const { postData, getValidationErrorMessage } = reqHelpers;
const { ireporterSettings, defaultHeaders, alertIds } = constants;
const { createAlert } = alerts;
const { newUrl, uiUrlFilepaths } = router;
const { setAuth, removeAuth, getAuthToken } = authHelpers;


function createIncidentRecord(e) {
  // Function used to create a new incident record

  e.preventDefault();
  createAlert('loading...', alertIds.loading);
  const newIncidentDetails = {
    title: getElTextValue('new_incident_title'),
    comment: getElTextValue('new_incident_comment'),
    location: `${getElTextValue('incident_lat')}, ${getElTextValue('incident_lng')}`,
    type: getSelectedInputOption('new_incident_type'),
  };

  const newIncidentUrl = `${ireporterSettings.base_api_url}/incidents`;
  defaultHeaders.append('Access-token', `Bearer ${getAuthToken()}`);
  postData(newIncidentUrl, newIncidentDetails, defaultHeaders)
    .then((data) => {
      console.log('new incident function data: ', data);
      if (data.status_code && data.status_code !== 201) {
        if (data.status_code === 403) {
          createAlert(data.msg, alertIds.error);
          newUrl(uiUrlFilepaths.LOGIN);
          return;
        }
        if (data.status_code === 401) {
          createAlert(data.msg, alertIds.error);
          newUrl(uiUrlFilepaths.LOGIN);
          return;
        }
        if (data.msg) createAlert(data.msg, alertIds.error);
        if (data.message) {
          createAlert(getValidationErrorMessage(data),
            alertIds.error);
        }
        return;
      }
      createAlert('You have created the incident successfully',
        alertIds.success);
      newUrl(uiUrlFilepaths.VIEW_ALL_INCIDENTS);
    })
    .catch((error) => {
      if (error && error.msg) createAlert(error.msg, alertIds.error);
    });
}

const incidentServices = {
  createIncidentRecord,
};

export default incidentServices;
