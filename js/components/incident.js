import router from '../helpers/router.js';
import reqHelpers from '../helpers/request_helpers.js';
import inputHelpers from '../helpers/input_helpers.js';
import authHelpers from '../helpers/auth_helpers.js';
import constants from '../constants.js';

const { getElTextValue, setElTextById, getSelectedInputOption } = inputHelpers;

function displaySingleIncidentDetails(incidentDetails) {
// Function to display a single incident's details on the UI Page
  // Display the incident title
  setElTextById('incident_title', incidentDetails.title);
  // Display incident type
  setElTextById('incident_type', incidentDetails.type);
  // Display incident status
  setElTextById('incident_status', incidentDetails.status);
  // Display incident creation date
  setElTextById('incident_createdOn', incidentDetails.createdOn);
  // Display incident comment
  setElTextById('incident_comment', incidentDetails.comment);
}

const incidentComponents = {
  displaySingleIncidentDetails,
};

export default incidentComponents;
