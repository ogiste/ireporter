import alerts from '../components/alerts.js';
import incidentComponents from '../components/incident.js';
import router from '../helpers/router.js';
import reqHelpers from '../helpers/request_helpers.js';
import domHelpers from '../helpers/dom_helpers.js';
import authHelpers from '../helpers/auth_helpers.js';
import constants from '../constants.js';


const { getElTextValue, setElTextById, getSelectedInputOption } = domHelpers;
const { postData, patchData, getData, deleteData, getValidationErrorMessage } = reqHelpers;
const { ireporterSettings, defaultHeaders, alertIds } = constants;
const { createAlert } = alerts;
const { newUrl, uiUrlFilepaths } = router;
const { removeAuth, getAuthToken, isAdmin } = authHelpers;
const {
  addIncidentCoordinatesToMaps,
  addIncidentEditableMap,
  displaySingleIncidentDetails,
  displayIncidentTableList,
  addDeleteIncidentEventListener,
} = incidentComponents;

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
  defaultHeaders.set('Access-token', `Bearer ${getAuthToken()}`);
  postData(newIncidentUrl, newIncidentDetails, defaultHeaders)
    .then((data) => {
      console.log('new incident function data: ', data);
      if (data.status_code && data.status_code !== 201) {
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
      createAlert('You have created the incident successfully',
        alertIds.success);
      const { id } = data.data[0]; // Get the id of the newly created incident
      newUrl(`${uiUrlFilepaths.VIEW_INCIDENT}?incident=${id}`);
    })
    .catch((error) => {
      if (error && error.msg) createAlert(error.msg, alertIds.error);
    });
}

function updateIncidentDetail(e) {
  // Function used to update an incident's Comment
  e.preventDefault();
  const incidentDetail = e.target.getAttribute('incidentDetail');
  console.log('e.target: ', e.target);
  const viewIncidentUrl = new URL(window.location.href);
  const id = viewIncidentUrl.searchParams.get('incident');
  createAlert('loading...', alertIds.loading);
  let updatedIncidentDetails; let updateIncidentUrl;
  if (incidentDetail === 'comment') {
    updateIncidentUrl = `${ireporterSettings.base_api_url}/incidents/${id}/comment`;
    console.log('prop_value: ', getElTextValue('incident_comment'));
    updatedIncidentDetails = {
      prop_value: getElTextValue('incident_comment'),
    };
  } else if (incidentDetail === 'location') {
    updateIncidentUrl = `${ireporterSettings.base_api_url}/incidents/${id}/location`;
    updatedIncidentDetails = {
      prop_value: `${getElTextValue('incident_lat')}, ${getElTextValue('incident_lng')}`,
    };
  } else {
    return;
  }
  defaultHeaders.set('Access-token', `Bearer ${getAuthToken()}`);
  patchData(updateIncidentUrl, updatedIncidentDetails, defaultHeaders)
    .then((data) => {
      console.log('update incident function data: ', data);
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
      newUrl(`${uiUrlFilepaths.VIEW_INCIDENT}?incident=${id}`);
    })
    .catch((error) => {
      if (error && error.msg) createAlert(error.msg, alertIds.error);
    });
}

function getSingleIncidentRecord() {
  // Function to fetch details of a single incident record
  const viewIncidentUrl = new URL(window.location.href);
  const id = viewIncidentUrl.searchParams.get('incident');
  createAlert('loading...', alertIds.loading);
  const singleIncidentUrl = `${ireporterSettings.base_api_url}/incidents/${id}`;
  defaultHeaders.set('Access-token', `Bearer ${getAuthToken()}`);
  getData(singleIncidentUrl, defaultHeaders)
    .then((data) => {
      console.log('get single incident function data: ', data);
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
      const incidentDetails = data.data[0];
      const { location } = incidentDetails;
      displaySingleIncidentDetails(incidentDetails);
      addIncidentCoordinatesToMaps(location);
      createAlert('Incident details loaded successfully',
        alertIds.success);
    })
    .catch((error) => {
      if (error && error.msg) createAlert(error.msg, alertIds.error);
    });
}

function getEditableIncidentRecord() {
  // Function to fetch details of a single incident record for editing
  const viewIncidentUrl = new URL(window.location.href);
  const id = viewIncidentUrl.searchParams.get('incident');
  createAlert('loading...', alertIds.loading);
  const singleIncidentUrl = `${ireporterSettings.base_api_url}/incidents/${id}`;
  defaultHeaders.set('Access-token', `Bearer ${getAuthToken()}`);
  getData(singleIncidentUrl, defaultHeaders)
    .then((data) => {
      console.log('edit single incident function data: ', data);
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
      const incidentDetails = data.data[0];
      const { location } = incidentDetails;
      displaySingleIncidentDetails(incidentDetails);
      addIncidentEditableMap(location);
      createAlert('Incident details loaded successfully',
        alertIds.success);
    })
    .catch((error) => {
      if (error && error.msg) createAlert(error.msg, alertIds.error);
    });
}

function deleteSingleIncidentRecord(e) {
  // // Function used to delete a single incident record
  // e.preventDefault();
  console.log('delete e: ', e);
  e.preventDefault();
  const deleteLink = e.target;
  const deletionConfirmationMessage = 'Are you sure you want to DELETE this incident?';
  if (window.confirm(deletionConfirmationMessage)) {
    createAlert('loading...', alertIds.loading);
    const id = deleteLink.getAttribute('incidentId');
    console.log('deleteSingleIncidentRecord id: ', id);
    const deleteIncidentUrl = `${ireporterSettings.base_api_url}/incidents/${id}`;
    defaultHeaders.set('Access-token', `Bearer ${getAuthToken()}`);
    deleteData(deleteIncidentUrl, defaultHeaders)
      .then((data) => {
        if (data.status_code && data.status_code !== 202) {
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
        newUrl(uiUrlFilepaths.VIEW_ALL_INCIDENTS);
      })
      .catch((error) => {
        if (error && error.msg) createAlert(error.msg, alertIds.error);
      });
  }
}

function getAllIncidentRecords() {
  // Function to fetch details of a single incident record
  createAlert('loading...', alertIds.loading);
  const allIncidentsUrl = `${ireporterSettings.base_api_url}/incidents/`;
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
      displayIncidentTableList(incidents);
      addDeleteIncidentEventListener(deleteSingleIncidentRecord);
      createAlert(data.msg,
        alertIds.success);
    })
    .catch((error) => {
      if (error && error.msg) createAlert(error.msg, alertIds.error);
    });
}

const incidentServices = {
  createIncidentRecord,
  getSingleIncidentRecord,
  getEditableIncidentRecord,
  getAllIncidentRecords,
  updateIncidentDetail,
  deleteSingleIncidentRecord,
};

export default incidentServices;
