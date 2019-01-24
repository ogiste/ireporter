import constants from '../constants.js';

const { alertIds } = constants;
let alertTimeoutDefault = 6000;

function removeAlert(alertId) {
  // Remove any element with id - alertId
  const element = document.getElementById(alertId);
  if (element !== null && element !== undefined) {
    element.parentNode.removeChild(element);
  }
}

function removeAllAlerts(allAlertIds) {
  // Function to clear all alerts on screen
  const propKeys = Object.keys(allAlertIds);
  for (let alertId = 0; alertId < propKeys.length; alertId++) {
    removeAlert(allAlertIds[propKeys[alertId]]);
  }
}

function setRemoveAlertTimeout(alertId, alertTimeout) {
  // Function used to remove an alert after alertTimeout number of seconds

  setTimeout(() => { removeAlert(alertId); }, alertTimeout);
}

function createAlert(msg = '', alertId = 'alert_error') {
  // This function is user to create error alert by taking in an error message
  if (msg === '') return;
  removeAllAlerts(alertIds);
  const alertElement = document.createElement('div');
  alertElement.id = alertId;
  const alertMsg = document.createTextNode(msg);
  alertElement.appendChild(alertMsg);
  document.body.appendChild(alertElement);
  if (alertId === alertIds.loading) alertTimeoutDefault = 30000;
  setRemoveAlertTimeout(alertId, alertTimeoutDefault);
}

const alerts = {
  createAlert,
};

export default alerts;
