let baseUiUrl;
const baseUrl = `${window.location.protocol}//${window.location.hostname}`;
console.log(`port --- ${window.location.port}`);
if (window.location.port) {
  baseUiUrl = `${baseUrl}:${window.location.port}/UI`;
} else {
  baseUiUrl = `${baseUrl}/UI`;
}

const ireporterSettings = {
  base_api_url: 'https://ireporter-ao.herokuapp.com/api/v2',
  base_api_local: 'http://127.0.0.1:5000/api/v2',
  baseUiUrl: `${baseUiUrl}`,
};

// export ireporterSettings;
const defaultHeaders = new Headers({
  Accept: 'application/json',
  'Content-Type': 'application/json',
});

const constants = {
  ireporterSettings,
  defaultHeaders,
  alertIds: {
    error: 'alert_error',
    success: 'alert_success',
    loading: 'alert_loading',
  },
};

export default constants;
