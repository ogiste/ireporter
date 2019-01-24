import alerts from '../components/alerts.js';
import router from '../helpers/router.js';
import reqHelpers from '../helpers/request_helpers.js';
import domHelpers from '../helpers/dom_helpers.js';
import authHelpers from '../helpers/auth_helpers.js';
import incidentComponents from '../components/incident.js';
import usersComponents from '../components/user.js';
import constants from '../constants.js';

const { displayAdminIncidentTableList } = incidentComponents;
const { displayAdminUsersTableList } = usersComponents;
const { getElementByAttribute, setElTextById, getSelectedInputOption, addElementClassEventListener } = domHelpers;
const { patchData, getData, getValidationErrorMessage } = reqHelpers;
const { ireporterSettings, defaultHeaders, alertIds } = constants;
const { createAlert } = alerts;
const { newUrl, uiUrlFilepaths } = router;
const { removeAuth, getAuthToken } = authHelpers;

function updateIncidentStatus(e) {
  // Function used to update an incident's status
  e.preventDefault();
  const id = e.target.getAttribute('incident_id');
  console.log('e target incident_id', e.target.getAttribute('incident_id'));
  const statusMenuElement = getElementByAttribute('status_menu_incident_id', id);
  const newStatusDetails = { status: statusMenuElement.value };
  createAlert('loading...', alertIds.loading);
  const updateIncidentStatusUrl = `${ireporterSettings.base_api_url}/incidents/${id}/status`;
  defaultHeaders.set('Access-token', `Bearer ${getAuthToken()}`);
  patchData(updateIncidentStatusUrl, newStatusDetails, defaultHeaders)
    .then((data) => {
      if (data.status_code && data.status_code !== 200) {
        if (data.status_code === 403) {
          createAlert(data.msg, alertIds.error);
          removeAuth();
          newUrl(uiUrlFilepaths.LOGIN);
          return;
        }
        if (data.status_code === 401) {
          createAlert(data.msg, alertIds.error);
          removeAuth();
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
      createAlert(data.msg,
        alertIds.success);
      newUrl(uiUrlFilepaths.ADMIN);
    })
    .catch((error) => {
      if (error && error.msg) createAlert(error.msg, alertIds.error);
    });
}

function adminGetAllIncidentRecords() {
  // Function to fetch details of a single incident record
  createAlert('loading...', alertIds.loading);
  const allIncidentsUrl = `${ireporterSettings.base_api_url}/incidents/all`;
  defaultHeaders.set('Access-token', `Bearer ${getAuthToken()}`);
  getData(allIncidentsUrl, defaultHeaders)
    .then((data) => {
      if (data.status_code && data.status_code !== 200) {
        if (data.status_code === 403) {
          createAlert(data.msg, alertIds.error);
          removeAuth();
          newUrl(uiUrlFilepaths.LOGIN);
          return;
        }
        if (data.status_code === 401) {
          createAlert(data.msg, alertIds.error);
          removeAuth();
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
      const incidents = data.data;
      displayAdminIncidentTableList(incidents);
      addElementClassEventListener(updateIncidentStatus, 'update-status-quest');
      createAlert(data.msg,
        alertIds.success);
    })
    .catch((error) => {
      if (error && error.msg) createAlert(error.msg, alertIds.error);
    });
}

function adminGetAllUserRecords() {
  // Function to fetch details of a single incident record
  createAlert('loading...', alertIds.loading);
  const allIncidentsUrl = `${ireporterSettings.base_api_url}/users`;
  defaultHeaders.set('Access-token', `Bearer ${getAuthToken()}`);
  getData(allIncidentsUrl, defaultHeaders)
    .then((data) => {
      if (data.status_code && data.status_code !== 200) {
        if (data.status_code === 403) {
          createAlert(data.msg, alertIds.error);
          removeAuth();
          newUrl(uiUrlFilepaths.LOGIN);
          return;
        }
        if (data.status_code === 401) {
          createAlert(data.msg, alertIds.error);
          removeAuth();
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
      const incidents = data.data;
      displayAdminUsersTableList(incidents);
      createAlert(data.msg,
        alertIds.success);
    })
    .catch((error) => {
      if (error && error.msg) createAlert(error.msg, alertIds.error);
    });
}

const adminServices = {
  adminGetAllIncidentRecords,
  adminGetAllUserRecords,
  updateIncidentStatus,
};

export default adminServices;
