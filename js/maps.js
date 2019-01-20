let questMarker=undefined;
let address_name = '';
let lat,lng;
let map = '';

function geocodeLatLng(geocoder, curMap, infowindow, latVal, lngVal) {
  const latlng = { lat: latVal, lng: lngVal };
  console.log('geocodeLatLng latlng:', latlng);
  geocoder.geocode({ location: latlng }, (results, status) => {
    if (status === 'OK') {
      if (results[0]) {
        map.setZoom(11);
        curMap.panTo(latlng);
        questMarker = new google.maps.Marker({
          position: latlng,
          map: curMap,
        });
        infowindow.setContent(results[0].formatted_address);
        infowindow.open(curMap, questMarker);
        document.getElementById('incident_lat').value = latlng.lat;
        document.getElementById('incident_lng').value = latlng.lng;
        document.getElementById('incident_loc').value = results[0].formatted_address;
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
