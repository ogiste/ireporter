var quest_marker=undefined;
var address_name = '';
var lat,lng;
  function initMap() {

    var map = new google.maps.Map(document.getElementById('map'), {
      zoom: 4,
      center: {lat: -1.3118799370815788, lng: 36.81155887155501}
    });

    var geocoder = new google.maps.Geocoder;
    var infowindow = new google.maps.InfoWindow;

    map.addListener('click', function(e) {
      if (quest_marker) {
        quest_marker.setMap(null);
      }
      //quest_marker = placeMarkerAndPanTo(e.latLng, map);
      geocodeLatLng(geocoder, map, infowindow,e.latLng.lat(),e.latLng.lng());
    });
  }

  function geocodeLatLng(geocoder, map, infowindow,lat,lng) {
    var latlng = {lat: lat, lng: lng};
    console.log("geocodeLatLng latlng:",latlng);
    geocoder.geocode({'location': latlng}, function(results, status) {
      if (status === 'OK') {
        if (results[0]) {
          //map.setZoom(11);
          map.panTo(latlng);
          quest_marker = new google.maps.Marker({
            position: latlng,
            map: map
          });
          infowindow.setContent(results[0].formatted_address);
          infowindow.open(map, quest_marker);
          document.getElementById('lat').value = latlng.lat;
          document.getElementById('lng').value = latlng.lng;
          document.getElementById('loc').value = results[0].formatted_address;
        } else {
          window.alert('No results found');
        }
      } else {
        window.alert('Geocoder failed due to: ' + status);
      }
    });
  }

  function placeMarkerAndPanTo(latLng, map) {
    map.panTo(latLng);
     return new google.maps.Marker({
      position: latLng,
      map: map
    });

  }
