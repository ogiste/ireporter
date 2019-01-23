let questMarker=undefined;
let address_name = '';
let lat,lng;
let map = '';
const geocoder = new google.maps.Geocoder();
const infowindow = new google.maps.InfoWindow();

function geocodeLatLng(geocoder, curMap, infowindow, latVal, lngVal) {
  const latlng = { lat: latVal, lng: lngVal };
  geocoder.geocode({ location: latlng }, (results, status) => {
    if (status === 'OK') {
      if (results[0]) {
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

function initMap(defaultLat = '', defaultLng = '') {
  // Function used to integrate google maps api for latitude and Longitude
  // coordinates

  if (defaultLat !== '' && defaultLng !== '') {
    map = new google.maps.Map(document.getElementById('map'), {
      zoom: 14,
      center: { lat: defaultLat, lng: defaultLng },
    });
    geocodeLatLng(geocoder, map, infowindow, defaultLat, defaultLng);
  } else {
    map = new google.maps.Map(document.getElementById('map'), {
      zoom: 4,
      center: { lat: -1.3118799370815788, lng: 36.81155887155501}
    });
  }

  // Create the search box and link it to the UI element.
  let input = document.getElementById('pac-input');
  let searchBox = new google.maps.places.SearchBox(input);
  map.controls[google.maps.ControlPosition.TOP_LEFT].push(input);

  // Bias the SearchBox results towards current map's viewport.
  map.addListener('bounds_changed', (() => {
    searchBox.setBounds(map.getBounds());
  }));
  let markers = [];

  searchBox.addListener('places_changed', () => {
    let places = searchBox.getPlaces();
    if (places.length === 0) {
      return;
    }
    // Clear out the old markers.
    markers.forEach((marker) => {
      marker.setMap(null);
    });
    markers = [];
    // For each place, get the icon, name and location
    let bounds = new google.maps.LatLngBounds();
    places.forEach((place) => {
      if (!place.geometry) {
        console.log('Returned place contains no geometry');
        return;
      }
      let icon = {
        url: place.icon,
        size: new google.maps.Size(71, 71),
        origin: new google.maps.Point(0, 0),
        anchor: new google.maps.Point(17, 34),
        scaledSize: new google.maps.Size(25, 25)
      };
      // Create a marker for each place.
      markers.push(new google.maps.Marker({
        map: map,
        icon: icon,
        title: place.name,
        position: place.geometry.location
      }));

      if (place.geometry.viewport) {
        // Only geocodes have viewport.
        bounds.union(place.geometry.viewport);
      } else {
        bounds.extend(place.geometry.location);
      }
    });
    map.fitBounds(bounds);
  });

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

const mapsApi = {
  initMap,
  geocodeLatLng,
  geocoder,
  infowindow,
  placeMarkerAndPanTo,
};

export default mapsApi;
