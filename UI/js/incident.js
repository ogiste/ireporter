import domHelpers from './helpers/dom_helpers.js';
import authHelpers from './helpers/auth_helpers.js';
import incidentServices from './services/incident_services.js';
import mapsApi from './maps.js';

const { initMap } = mapsApi;
const { createIncidentRecord } = incidentServices;
const { getElById } = domHelpers;
const { checkAuthorization } = authHelpers;

function loadIncidentPage() {
// Function that loads create incident page
  checkAuthorization();
  initMap();
  if (getElById('new_incident_submit')) {
    getElById('new_incident_submit').addEventListener('click',
      createIncidentRecord);
  }
}

loadIncidentPage();
