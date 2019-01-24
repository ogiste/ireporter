import alerts from './components/alerts.js';
import router from './helpers/router.js';
import reqHelpers from './helpers/request_helpers.js';
import inputHelpers from './helpers/input_helpers.js';
import authHelpers from './helpers/auth_helpers.js';
import incidentServices from './services/incident_services.js';
import constants from './constants.js';

const { createIncidentRecord } = incidentServices;
const { getElById } = inputHelpers;
const { postData, getValidationErrorMessage } = reqHelpers;
const { ireporterSettings, defaultHeaders, alertIds } = constants;
const { createAlert } = alerts;
const { newUrl, uiUrlFilepaths } = router;
const { setAuth, removeAuth, isAuth } = authHelpers;

function loadIncidentPage() {
// Function that loads create incident page
  createAlert('loading...', alertIds.loading);
  if (isAuth()) {
    createAlert('Page successfully loaded', alertIds.success);
    return;
  }
  createAlert('You are not signed in. Please sign in to view this page',
    alertIds.error);
  newUrl(uiUrlFilepaths.LOGIN);
}

loadIncidentPage();
if (getElById('new_incident_submit')) {
  getElById('new_incident_submit').addEventListener('click',
    createIncidentRecord);
}
