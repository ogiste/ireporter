import authHelpers from './helpers/auth_helpers.js';
import incidentServices from './services/incident_services.js';

const { getSingleIncidentRecord } = incidentServices;
const { checkAuthorization } = authHelpers;

function loadIncidentPage() {
// Function that loads create incident page
  checkAuthorization();
  getSingleIncidentRecord();
}

loadIncidentPage();
