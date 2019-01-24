import alerts from './components/alerts.js';
import router from './helpers/router.js';
import reqHelpers from './helpers/request_helpers.js';
import inputHelpers from './helpers/input_helpers.js';
import authHelpers from './helpers/auth_helpers.js';
import constants from './constants.js';

const { getElTextValue, getElById } = inputHelpers;
const { postData, getValidationErrorMessage } = reqHelpers;
const { ireporterSettings, defaultHeaders, alertIds } = constants;
const { createAlert } = alerts;
const { newUrl, uiUrlFilepaths } = router;
const { setAuth, removeAuth } = authHelpers;

let questMarker=undefined;
let address_name = '';
let lat,lng;
let map = '';

function geocodeLatLng(geocoder, curMap, infowindow, latVal, lngVal) {
  const latlng = { latVal, lngVal };
  console.log('geocodeLatLng latlng:', latlng);
  geocoder.geocode({ location: latlng }, (results, status) => {
    if (status === 'OK') {
      if (results[0]) {
        // map.setZoom(11);
        curMap.panTo(latlng);
        questMarker = new google.maps.Marker({
          position: latlng,
          map: curMap,
        });
        infowindow.setContent(results[0].formatted_address);
        infowindow.open(curMap, questMarker);
        getElById('incident_lat').value = latlng.lat;
        getElById('incident_lng').value = latlng.lng;
        getElById('incident_loc').value = results[0].formatted_address;
      } else {
        window.alert('No results found');
      }
    } else {
      window.alert(`Geocoder failed due to: ${status}`);
    }
  });
}

function initMap() {
  // Function used to integrate google maps api for latitude and Longitude
  // coordinates
  map = new google.maps.Map(document.getElementById('map'), {
    zoom: 4,
    center: { lat: -1.3118799370815788, lng: 36.81155887155501}
  });

  const geocoder = new google.maps.Geocoder();
  const infowindow = new google.maps.InfoWindow();

  map.addListener('click', (e) => {
    if (questMarker) {
      questMarker.setMap(null);
    }
    // questMarker = placeMarkerAndPanTo(e.latLng, map);
    geocodeLatLng(geocoder, map, infowindow, e.latLng.lat(), e.latLng.lng());
  });
}

function placeMarkerAndPanTo(latLng, curMap) {
  map.panTo(latLng);
  return new google.maps.Marker({
    position: latLng,
    map: curMap
  });

}

export default initMap;
