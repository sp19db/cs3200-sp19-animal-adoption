var map;
var markers = [];
var infoWindow;
var locationSelect;

function initMap() {
    var boston = {lat: 42.368254, lng: -71.062585};
    map = new google.maps.Map(document.getElementById('map'), {
        center: boston,
        zoom: 12,
        mapTypeId: 'roadmap',
        mapTypeControlOptions: {style: google.maps.MapTypeControlStyle.DROPDOWN_MENU}
    });
    infoWindow = new google.maps.InfoWindow();

    searchButton = document.getElementById("searchButton").onclick = searchLocations;

    locationSelect = document.getElementById("locationSelect");
    locationSelect.onchange = function () {
        var markerNum = locationSelect.options[locationSelect.selectedIndex].value;
        if (markerNum != "none") {
            google.maps.event.trigger(markers[markerNum], 'click');
        }
    };

    document.getElementById("addressInput").value = "02115";
}

function searchLocations() {
    var address = document.getElementById("addressInput").value;
    var geocoder = new google.maps.Geocoder();
    geocoder.geocode({address: address}, function (results, status) {
        if (status == google.maps.GeocoderStatus.OK) {
            searchLocationsNear(results[0].geometry.location);
            document.getElementById("addressInput").value = '';
        } else {
            if (address === '') {
                alert('please enter a zip code or location');
            } else {
                alert('location: ' + address + ' not found');
            }
        }
    });
}

function clearLocations() {
    infoWindow.close();
    for (var i = 0; i < markers.length; i++) {
        markers[i].setMap(null);
    }
    markers.length = 0;

    locationSelect.innerHTML = "";
    var option = document.createElement("option");
    option.value = "none";
    option.innerHTML = "See all results:";
    locationSelect.appendChild(option);
}

function searchLocationsNear(center) {
    clearLocations();

    var radius = document.getElementById('radiusSelect').value;
    var searchUrl = 'http://127.0.0.1:8000/map?lat=' + center.lat() + "&lng=" + center.lng()
        + "&radius=" + radius + "&" + getAnimalFilterUrl();
    console.log(searchUrl);
    downloadUrl(searchUrl, function (data) {
        var xml = parseXml(data);
        var markerNodes = xml.documentElement.getElementsByTagName("marker");
        var bounds = new google.maps.LatLngBounds();
        for (var i = 0; i < markerNodes.length; i++) {
            var id = markerNodes[i].getAttribute("id");
            var name = markerNodes[i].getAttribute("name");
            var address = markerNodes[i].getAttribute("address");
            var distance = parseFloat(markerNodes[i].getAttribute("distance"));
            var latlng = new google.maps.LatLng(
                parseFloat(markerNodes[i].getAttribute("lat")),
                parseFloat(markerNodes[i].getAttribute("lng")));

            createOption(name, distance, i);
            createMarker(latlng, name, address);
            bounds.extend(latlng);
        }
        map.fitBounds(bounds);
        locationSelect.style.visibility = "visible";
        locationSelect.onchange = function () {
            var markerNum = locationSelect.options[locationSelect.selectedIndex].value;
            google.maps.event.trigger(markers[markerNum], 'click');
        };
    });
}

function createMarker(latlng, name, address) {
    var html = "<b>" + name + "</b> <br/>" + address;
    var marker = new google.maps.Marker({
        map: map,
        position: latlng
    });
    google.maps.event.addListener(marker, 'click', function () {
        infoWindow.setContent(html);
        infoWindow.open(map, marker);
    });
    markers.push(marker);
}

function createOption(name, distance, num) {
    var option = document.createElement("option");
    option.value = num;
    option.innerHTML = name;
    locationSelect.appendChild(option);
}

function downloadUrl(url, callback) {
    fetch(url)
        .then(function (response) {
            return response.json();
        })
        .then(function (locationMap) {
            console.log(locationMap["location"]);
            callback(locationMap["location"]);
        });
}

function parseXml(str) {
    if (window.ActiveXObject) {
        var doc = new ActiveXObject('Microsoft.XMLDOM');
        doc.loadXML(str);
        return doc;
    } else if (window.DOMParser) {
        return (new DOMParser).parseFromString(str, 'text/xml');
    }
}

