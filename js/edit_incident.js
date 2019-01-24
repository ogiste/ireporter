import domHelpers from './helpers/dom_helpers.js';
import authHelpers from './helpers/auth_helpers.js';
import incidentServices from './services/incident_services.js';

const { getEditableIncidentRecord, updateIncidentDetail } = incidentServices;
const { checkAuthorization } = authHelpers;
const { getElById } = domHelpers;

function loadEditIncidentPage() {
// Function that loads create incident page
  checkAuthorization();
  getEditableIncidentRecord();
  if (getElById('edit_incident_location')) {
    getElById('edit_incident_location').addEventListener('click',
      updateIncidentDetail);
  }
  if (getElById('edit_incident_comment')) {
    getElById('edit_incident_comment').addEventListener('click',
      updateIncidentDetail);
  }
}

loadEditIncidentPage();
