import domHelpers from '../helpers/dom_helpers.js';
import constants from '../constants.js';

const { getElById } = domHelpers;
const { alertIds } = constants;
let alertTimeoutDefault = 6000;

function removeAlert(alertId) {
  // Remove any element with id - alertId
  const element = document.getElementById(alertId);
  if (element !== null && element !== undefined) {
    element.parentNode.removeChild(element);
  }
}

function removeAllAlerts() {
  // Function to clear all alerts on screen
  const propKeys = Object.keys(alertIds);
  for (let alertId = 0; alertId < propKeys.length; alertId++) {
    removeAlert(alertIds[propKeys[alertId]]);
  }
}

function setRemoveAlertTimeout(alertId, alertTimeout) {
  // Function used to remove an alert after alertTimeout number of seconds

  setTimeout(() => { removeAlert(alertId); }, alertTimeout);
}

function createAlert(msg = '', alertId = 'alert_error') {
  // This function is user to create error alert by taking in an error message
  if (msg === '') return;
  removeAllAlerts();
  const alertElement = document.createElement('div');
  const cancelBtn = document.createElement('span');
  cancelBtn.id = 'cancel_btn';
  cancelBtn.innerHTML = 'X';
  alertElement.id = alertId;
  const alertMsg = document.createTextNode(msg);
  alertElement.appendChild(alertMsg);
  alertElement.appendChild(cancelBtn);
  document.body.appendChild(alertElement);
  if (alertId === alertIds.loading) alertTimeoutDefault = 30000;
  if (alertId !== alertIds.loading) {
    cancelBtn.addEventListener('click', removeAllAlerts);
  }
  setRemoveAlertTimeout(alertId, alertTimeoutDefault);
}

const alerts = {
  createAlert,
};

export default alerts;
