import router from '../helpers/router.js';
import reqHelpers from '../helpers/request_helpers.js';
import domHelpers from '../helpers/dom_helpers.js';
import authHelpers from '../helpers/auth_helpers.js';
import constants from '../constants.js';
import mapsApi from '../maps.js';

const { geocodeLatLng, geocoder, infowindow, initMap } = mapsApi;
const { uiUrlFilepaths } = router;
const {
  getElTextValue,
  getElById,
  setElTextById,
  getSelectedInputOption,
  createDomElement
} = domHelpers;


function createAdminUserRow(userDetails) {
  // Function used to create a DOM row for an incident item in an incident list
  const userRow = createDomElement('tr');
  const {
    username, email, fname, lname, phone, createdOn
  } = userDetails;
  const usernameColumn = createDomElement('td', username);
  const emailColumn = createDomElement('td', email);
  const fnameColumn = createDomElement('td', fname);
  const lnameColumn = createDomElement('td', lname);
  const phoneColumn = createDomElement('td', phone);
  const createdOnColumn = createDomElement('td', createdOn);
  const columnElements = [
    usernameColumn,
    emailColumn,
    fnameColumn,
    lnameColumn,
    phoneColumn,
    createdOnColumn,
  ];
  for (let i = 0; i < columnElements.length; i++) {
    userRow.appendChild(columnElements[i]);
  }
  return userRow;
}

function displayAdminUsersTableList(incidentsDetailsArray) {
  // Function to append a list of all incidents of a user to the incidents tables
  const incidentTbody = getElById('users_admin_tbody');
  let userRows = [];
  if (incidentsDetailsArray.length === 1) {
    incidentTbody.appendChild(createAdminUserRow(incidentsDetailsArray[0]));
    return;
  }
  if (incidentsDetailsArray.length === 0) {
    userRows = createDomElement('td', 'No incidents created.');
    userRows.rowSpan = 5;
    incidentTbody.appendChild(userRows);
    return;
  }
  for (let i = 0; i < incidentsDetailsArray.length; i++) {
    userRows.push(createAdminUserRow(incidentsDetailsArray[i]));
  }
  for (let i = 0; i < userRows.length; i++) {
    incidentTbody.appendChild(userRows[i]);
  }
}

const usersComponents = {
  displayAdminUsersTableList,
};

export default usersComponents;
