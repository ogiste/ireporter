import router from '../helpers/router.js';
import reqHelpers from '../helpers/request_helpers.js';
import domHelpers from '../helpers/dom_helpers.js';
import authHelpers from '../helpers/auth_helpers.js';
import constants from '../constants.js';

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
        deleteLink.setAttribute('incidentId', id);
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

function addDeleteIncidentEventListener(deleteIncidentCallBack) {
  // Function used to add event listeners to all delete buttons
  const deleteLinks = document.getElementsByClassName('delete-quest');
  const deleteBtns = Array.from(deleteLinks);
  deleteBtns.forEach((element) => {
    element.addEventListener('click', deleteIncidentCallBack);
  });
}

function displayIncidentTableList(incidentsDetailsArray) {
  // Function to append a list of all incidents of a user to the incidents tables
  const incidentTbody = getElById('incidents_tbody');
  let incidentRows = [];
  if (incidentsDetailsArray.length === 1) {
    incidentTbody.appendChild(createIncidentRow(incidentsDetailsArray[0]));
    return;
  }
  if (incidentsDetailsArray.length === 0) {
    incidentRows = createDomElement('td', 'No incidents created.');
    incidentRows.rowSpan = 4;
    incidentTbody.appendChild(incidentRows);
    return;
  }
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

const incidentComponents = {
  displaySingleIncidentDetails,
  displayIncidentTableList,
  addDeleteIncidentEventListener,
};

export default incidentComponents;
