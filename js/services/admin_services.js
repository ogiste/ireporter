import alerts from '../components/alerts.js';
import router from '../helpers/router.js';
import reqHelpers from '../helpers/request_helpers.js';
import domHelpers from '../helpers/dom_helpers.js';
import authHelpers from '../helpers/auth_helpers.js';
import incidentComponents from '../components/incident.js';
import constants from '../constants.js';

const { displayAdminIncidentTableList } = incidentComponents;
const { getElTextValue, setElTextById, getSelectedInputOption, addElementClassEventListener } = domHelpers;
const { postData, patchData, getData, deleteData, getValidationErrorMessage } = reqHelpers;
const { ireporterSettings, defaultHeaders, alertIds } = constants;
const { createAlert } = alerts;
const { newUrl, uiUrlFilepaths } = router;
const { removeAuth, getAuthToken } = authHelpers;


function adminGetAllIncidentRecords() {
  // Function to fetch details of a single incident record
  createAlert('loading...', alertIds.loading);
  const allIncidentsUrl = `${ireporterSettings.base_api_url}/incidents/all`;
  defaultHeaders.set('Access-token', `Bearer ${getAuthToken()}`);
  getData(allIncidentsUrl, defaultHeaders)
    .then((data) => {
      if (data.status_code && data.status_code !== 200) {
        if (data.status_code === 403) {
          createAlert(data.msg, alertIds.error);
          removeAuth();
          newUrl(uiUrlFilepaths.LOGIN);
          return;
        }
        if (data.status_code === 401) {
          createAlert(data.msg, alertIds.error);
          removeAuth();
          newUrl(uiUrlFilepaths.LOGIN);
          return;
        }
        if (data.msg) createAlert(data.msg, alertIds.error);
        if (data.message) {
          createAlert(getValidationErrorMessage(data),
            alertIds.error);
        }
        return;
      }
      const incidents = data.data;
      console.log('adminGetAllIncidentRecords displayAdminIncidentTableList: ', displayAdminIncidentTableList);
      displayAdminIncidentTableList(incidents);
      createAlert(data.msg,
        alertIds.success);
    })
    .catch((error) => {
      if (error && error.msg) createAlert(error.msg, alertIds.error);
    });
}

const adminServices = {
  adminGetAllIncidentRecords,
};

export default adminServices;
