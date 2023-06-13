
var map = new L.Map('map', {
    center: new L.LatLng(51.505, 0.0),
    zoom: 18,
    zoomAnimation: false,
    fadeAnimation: false,
    markerZoomAnimation: false,
    inertia: false,
    panAnimation: false,
    worldCopyJump: true,
});


/*
var osm = L.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 21,
    attribution: '&copy; <a href="http://openstreetmap.org/copyright">OpenStreetMap</a> contributors',
});
*/

//osm.addTo(map);

/*
var myPublicToken = 'nothingtoseeheremovealong';

var mapbox = L.tileLayer(
    'https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}',
    {
        attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
        maxZoom: 21,
        id: 'mapbox/streets-v11',
        tileSize: 512,
        zoomOffset: -1,
        accessToken: myPublicToken
    }
);
*/
//mapbox.addTo(map);



var google = L.tileLayer('http://www.google.cn/maps/vt?lyrs=s@189&gl=cn&x={x}&y={y}&z={z}', {
    attribution: 'google',
    maxNativeZoom: 21,
    maxZoom: 24,
});

google.addTo(map);


var geofence_layer = L.featureGroup().addTo(map);
//geofence_layer.addTo(map);


L.control.layers({}, {
    Geofence: geofence_layer
}, {
    position: 'topleft',
    collapsed: false
}).addTo(map);



map.addControl(new L.Control.Draw({
    edit: {
        featureGroup: geofence_layer,
        polygon: {
            allowIntersection: false,
            showArea: true
        },
    },
    draw: {
        polygon: {
            allowIntersection: false,
            showArea: true
        },

        // TODO:  implement these later:
        marker: false,
        circlemarker: false,
        rectangle: false,
        polyline: false
    }
}));



window._missionLayer = L.featureGroup().addTo(map);
window._markersLayer = L.featureGroup().addTo(map);

map.on(L.Draw.Event.CREATED, function (evt) {
    geofence_layer.addLayer(evt.layer);
});


var roverIcon = L.icon({
    iconUrl: '/static/roverIcon.png',
    iconSize: [21,21],
    iconAnchor: [10, 20]
});


window._rover = L.marker([0.0, 0.0], {
    icon: roverIcon,
    rotationAngle: 0.0,
}).addTo(map);


