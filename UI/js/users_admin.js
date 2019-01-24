import authHelpers from './helpers/auth_helpers.js';
import adminServices from './services/admin_services.js';

const { adminGetAllUserRecords } = adminServices;
const { checkAdminAuthorization } = authHelpers;

function loadAdminGetAllUsersPage() {
// Function that loads create incident page
  checkAdminAuthorization();
  adminGetAllUserRecords();
}

loadAdminGetAllUsersPage();
