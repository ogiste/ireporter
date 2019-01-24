import alerts from '../components/alerts.js';
import incidentComponents from '../components/incident.js';
import router from '../helpers/router.js';
import reqHelpers from '../helpers/request_helpers.js';
import inputHelpers from '../helpers/input_helpers.js';
import authHelpers from '../helpers/auth_helpers.js';
import constants from '../constants.js';
import mapsApi from '../maps.js';

const { getElTextValue, setElTextById, getSelectedInputOption } = inputHelpers;
const { postData, getData, getValidationErrorMessage } = reqHelpers;
const { ireporterSettings, defaultHeaders, alertIds } = constants;
const { createAlert } = alerts;
const { newUrl, uiUrlFilepaths } = router;
const { removeAuth, getAuthToken } = authHelpers;
const { displaySingleIncidentDetails } = incidentComponents;
const { geocodeLatLng, geocoder, infowindow } = mapsApi;

function addIncidentCoordinatesToMaps(incidentLocation) {
// Function to add the google maps coordinates of an incident
  const latLngArray = incidentLocation.split(',', 2);
  const lat = parseFloat(latLngArray[0]);
  const lng = parseFloat(latLngArray[1]);
  function initMap() {
    const myLatLng = {
      lat,
      lng,
    };
    const map = new google.maps.Map(document.getElementById('map'), {
      zoom: 10,
      center: myLatLng
    });
    geocodeLatLng(geocoder, map, infowindow, myLatLng.lat, myLatLng.lng);
  }
  setElTextById('incident_lat', lat);
  setElTextById('incident_lng', lng);
  initMap();
}

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

const incidentServices = {
  createIncidentRecord,
  getSingleIncidentRecord,
};

export default incidentServices;
