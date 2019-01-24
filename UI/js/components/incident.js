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

function createIncidentActionLinks(status = '', id = '', parentElement) {
  // Function used to generate links as hypertext link elements based on
  // an incident's status and id
  if (status !== '' && status !== 'null' && (typeof status !== 'undefined')) {
    let viewLink; let editLink; let deleteLink; let actionLinks;
    switch (status) {
      case 'draft':
        viewLink = createDomElement('a', 'View', 'view-quest');
        viewLink.href = `${uiUrlFilepaths.VIEW_INCIDENT}?incident=${id}`;
        editLink = createDomElement('a', 'Edit', 'edit-quest');
        editLink.href = `${uiUrlFilepaths.EDIT_INCIDENT}?incident=${id}`;
        deleteLink = createDomElement('a', 'Delete', 'delete-quest', '');
        deleteLink.setAttribute('incident_id', id);
        actionLinks = [viewLink, editLink, deleteLink];
        break;
      default:
        viewLink = createDomElement('a', 'View', 'view-quest');
        viewLink.href = `${uiUrlFilepaths.VIEW_INCIDENT}?incident=${id}`;
        actionLinks = [viewLink];
        break;
    }
    for (let i = 0; i < actionLinks.length; i++) {
      parentElement.appendChild(actionLinks[i]);
    }
    return parentElement;
  }
  return parentElement;
}

function createIncidentStatusSelectMenu(status = '', id = '') {
  // Function used to generate incident select menu based on
  // an incident's status and id
  const incidentStatusValues = ['draft', 'resolved', 'rejected', 'under investigation'];
  const selectElement = createDomElement('select');
  selectElement.className += ' incident-status-select';
  selectElement.setAttribute('status_menu_incident_id', id);
  for (let i = 0; i < incidentStatusValues.length; i++) {
    let optionTitle = (incidentStatusValues[i].charAt(0).toUpperCase() +
    incidentStatusValues[i].slice(1));
    let selectOption = createDomElement('option', optionTitle);
    selectOption.value = incidentStatusValues[i];
    selectElement.appendChild(selectOption);
  }
  selectElement.value = status;
  return selectElement;
}

function createIncidentRow(incidentDetails) {
  // Function used to create a DOM row for an incident item in an incident list
  const incidentRow = createDomElement('tr');
  const {
    title, type, status, id,
  } = incidentDetails;
  const titleColumn = createDomElement('td', title);
  const typeColumn = createDomElement('td', type);
  const statusColumn = createDomElement('td', status);
  let actionsColumn = createDomElement('td');
  actionsColumn = createIncidentActionLinks(status, id, actionsColumn);
  const columnElements = [titleColumn, typeColumn, statusColumn, actionsColumn];
  for (let i = 0; i < columnElements.length; i++) {
    incidentRow.appendChild(columnElements[i]);
  }
  return incidentRow;
}

function createAdminIncidentRow(incidentDetails) {
  // Function used to create a DOM row for an incident item in an incident list
  const incidentRow = createDomElement('tr');
  const {
    title, type, comment, status, id,
  } = incidentDetails;
  const titleColumn = createDomElement('td', title);
  const typeColumn = createDomElement('td', type);
  const commentColumn = createDomElement('td', comment);
  const statusColumn = createDomElement('td');
  statusColumn.appendChild(createIncidentStatusSelectMenu(status, id));
  const actionsColumn = createDomElement('td');
  const updateStatusLink = createDomElement('a', 'Update Status', 'update-status-quest');
  updateStatusLink.setAttribute('incident_id', id);
  const viewLink = createDomElement('a', 'View', 'view-quest');
  viewLink.href = `${uiUrlFilepaths.VIEW_INCIDENT}?incident=${id}`;
  actionsColumn.appendChild(updateStatusLink);
  actionsColumn.appendChild(viewLink);
  const columnElements = [titleColumn, typeColumn, commentColumn, statusColumn, actionsColumn];
  for (let i = 0; i < columnElements.length; i++) {
    incidentRow.appendChild(columnElements[i]);
  }
  return incidentRow;
}

function displayIncidentStatusStats(incidentsDetailsArray) {
  // Function used to count statistics for incidents based on the status of an incident
  const statsResolvedElement = getElById('stats_resolved');
  const statsRejectedElement = getElById('stats_rejected');
  const statsUnderInvestigationElement = getElById('stats_under_investigation');
  const statsDraftElement = getElById('stats_resolved');

  const resolvedCount = incidentsDetailsArray.filter(incident => incident.status === 'resolved').length;
  const rejectedCount = incidentsDetailsArray.filter(incident => incident.status === 'rejected').length;
  const underInvestigationCount = incidentsDetailsArray.filter(incident => incident.status === 'under investigation').length;
  const draftCount = incidentsDetailsArray.filter(incident => incident.status === 'draft').length;

  statsResolvedElement.innerHTML = resolvedCount;
  statsRejectedElement.innerHTML = rejectedCount;
  statsUnderInvestigationElement.innerHTML = underInvestigationCount;
  statsDraftElement.innerHTML = draftCount;
}

function displayAdminIncidentTableList(incidentsDetailsArray) {
  // Function to append a list of all incidents of a user to the incidents tables
  const incidentTbody = getElById('incidents_admin_tbody');
  let incidentRows = [];
  if (incidentsDetailsArray.length === 1) {
    incidentTbody.appendChild(createAdminIncidentRow(incidentsDetailsArray[0]));
    displayIncidentStatusStats(incidentsDetailsArray);
    return;
  }
  if (incidentsDetailsArray.length === 0) {
    incidentRows = createDomElement('td', 'No incidents created.');
    incidentRows.rowSpan = 5;
    incidentTbody.appendChild(incidentRows);
    return;
  }
  displayIncidentStatusStats(incidentsDetailsArray);
  for (let i = 0; i < incidentsDetailsArray.length; i++) {
    incidentRows.push(createAdminIncidentRow(incidentsDetailsArray[i]));
  }
  for (let i = 0; i < incidentRows.length; i++) {
    incidentTbody.appendChild(incidentRows[i]);
  }
}

function displayIncidentTableList(incidentsDetailsArray) {
  // Function to append a list of all incidents of a user to the incidents tables
  const incidentTbody = getElById('incidents_tbody');
  let incidentRows = [];
  if (incidentsDetailsArray.length === 1) {
    incidentTbody.appendChild(createIncidentRow(incidentsDetailsArray[0]));
    displayIncidentStatusStats(incidentsDetailsArray);
    return;
  }
  if (incidentsDetailsArray.length === 0) {
    incidentRows = createDomElement('td', 'No incidents created.');
    incidentRows.rowSpan = 4;
    incidentTbody.appendChild(incidentRows);
    return;
  }
  displayIncidentStatusStats(incidentsDetailsArray);
  for (let i = 0; i < incidentsDetailsArray.length; i++) {
    incidentRows.push(createIncidentRow(incidentsDetailsArray[i]));
  }
  for (let i = 0; i < incidentRows.length; i++) {
    incidentTbody.appendChild(incidentRows[i]);
  }
}

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

function addIncidentCoordinatesToMaps(incidentLocation) {
// Function to add the google maps coordinates of an incident
  const latLngArray = incidentLocation.split(',', 2);
  const lat = parseFloat(latLngArray[0]);
  const lng = parseFloat(latLngArray[1]);
  function initNewMap() {
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
  initNewMap();
}

function addIncidentEditableMap(incidentLocation) {
// Function to add the google maps coordinates of an incident for editing
  const latLngArray = incidentLocation.split(',', 2);
  const lat = parseFloat(latLngArray[0]);
  const lng = parseFloat(latLngArray[1]);
  setElTextById('incident_lat', lat);
  setElTextById('incident_lng', lng);
  initMap(lat, lng);
}

const incidentComponents = {
  displaySingleIncidentDetails,
  displayIncidentTableList,
  displayIncidentStatusStats,
  displayAdminIncidentTableList,
  addIncidentCoordinatesToMaps,
  addIncidentEditableMap,
};

export default incidentComponents;
