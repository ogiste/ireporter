import authHelpers from './helpers/auth_helpers.js';
import adminServices from './services/admin_services.js';

const { adminGetAllIncidentRecords } = adminServices;
const { checkAdminAuthorization } = authHelpers;

function loadAdminGetAllIncidentsPage() {
// Function that loads create incident page
  checkAdminAuthorization();
  adminGetAllIncidentRecords();
}

loadAdminGetAllIncidentsPage();
