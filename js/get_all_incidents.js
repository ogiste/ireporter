import authHelpers from './helpers/auth_helpers.js';
import incidentServices from './services/incident_services.js';

const { getAllIncidentRecords } = incidentServices;
const { checkAuthorization } = authHelpers;

function loadGetAllIncidentsPage() {
// Function that loads create incident page
  checkAuthorization();
  getAllIncidentRecords();
}

loadGetAllIncidentsPage();
