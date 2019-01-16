
// import * as reqHelpers from './helpers/request_helpers';
// import * as inputHelpers from './helpers/user_input_helpers';
import userServices from './services/user_services.js';

const { login } = userServices;
let questMarker;
const addressName = '';
let lat; let lng;
function initMap() {
  const map = new google.maps.Map(document.getElementById('map'), {
    zoom: 4,
    center: { lat: -1.3118799370815788, lng: 36.81155887155501 },
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

function geocodeLatLng(geocoder, map, infowindow, lat, lng) {
  const latlng = { lat, lng };
  console.log('geocodeLatLng latlng:', latlng);
  geocoder.geocode({ location: latlng }, (results, status) => {
    if (status === 'OK') {
      if (results[0]) {
        // map.setZoom(11);
        map.panTo(latlng);
        questMarker = new google.maps.Marker({
          position: latlng,
          map,
        });
        infowindow.setContent(results[0].formatted_address);
        infowindow.open(map, questMarker);
        document.getElementById('lat').value = latlng.lat;
        document.getElementById('lng').value = latlng.lng;
        document.getElementById('loc').value = results[0].formatted_address;
      } else {
        window.alert('No results found');
      }
    } else {
      window.alert(`Geocoder failed due to: ${status}`);
    }
  });
}

function placeMarkerAndPanTo(latLng, map) {
  map.panTo(latLng);
  return new google.maps.Marker({
    position: latLng,
    map,
  });
}
