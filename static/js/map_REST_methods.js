

window._mission = [];

function get_mission() {
    fetch('mission.json')
    .then((response) => response.json())
    .then((mission) => {
        console.log(mission);
        window._mission = mission;


        var origin = null;
        var pointList = [];

        try {
            window._missionLayer.clearLayers();
        } catch (error) {
        }

        for (var i=0; i<mission.length; ++i) {
            var item = mission[i];
            if (item.length >1) {
                var cmd = item[0];
                //console.log(' ---- mission cmd:', cmd);
                if (cmd == 'waypoint' && item[1].length === 5) {
                    var lat = item[1][0];
                    var lon = item[1][1];
                    var minSpeed = item[1][2];
                    var maxSpeed = item[1][3];
                    var radius = item[1][4];

                    if (origin === null) {
                        origin = [lat, lon];
                    }

                    var waypoint = new L.LatLng(lat, lon);
                    pointList.push(waypoint);

                    var circle = L.circle([lat, lon], {
                        color: 'yellow',
                        //fillColor: '#f03',
                        fillOpacity: 0.1,
                        weight: 1,
                        radius: radius
                    }).addTo(window._missionLayer);

                }
            }
        }

        if (pointList.length > 1) {
            window.firstpolyline = new L.Polyline(pointList, {
                color: 'red',
                weight: 3,
                opacity: 0.5,
                smoothFactor: 1
            });
            window.firstpolyline.addTo(window._missionLayer);
        }

        if (origin != null) {
            map.setView(origin, 19, {animate: false});
        }
    });
}



function diy_json() {
    // GeoJSON doesn't support radius of points, therefore
    // Leaflest doesn't support radius of points.  So we
    // have to JSON-ize our own geofence maps for now.

    var jso = {
        type: 'FeatureCollection',
        features: []
    };

    var layers = geofence_layer.getLayers();

    for (var i=0; i<layers.length; ++i) {
        var o = layers[i].toGeoJSON();

        // This seems to be the standard work-around that ppl are using:
        if ('_mRadius' in layers[i]) {
            o.properties.radius = layers[i]._mRadius;
        }

        jso.features.push(o)
    }

    return jso;
}



function post_geofence(tshoot) {
    console.log('this is post_geofence()');

    var myBody = {};
    if (tshoot===1) {
        // This is purely so that I can compare, back-to-back, the
        // toGeoJSON() method compared to my own diy_json() function:
        myBody = JSON.stringify(geofence_layer.toGeoJSON());
    } else {
        myBody = JSON.stringify(diy_json());
    }

    fetch('/geofence.json', {
        body: myBody,
        headers: {
            'Content-Type': 'application/json'
        },
        method: 'POST'
    }).then((response) => response.json())
    .then((resp) => {
        console.log(' yo...');
        console.log('server said:', resp);
        alert("saved");
    });
}



function get_geofence() {
    fetch('/geofence.json')
    .then((response) => response.json())
    .then((geofenceJSON) => {
        window._geofenceJSON = geofenceJSON;
        console.log('geofence from server:', geofenceJSON);

        // ... trying to add the "radius" back into our circles...
        // see also:  https://medium.com/geoman-blog/how-to-handle-circles-in-geojson-d04dcd6cb2e6

        var aa = L.geoJSON(geofenceJSON, {
            pointToLayer: (feature, latlng) => {
                if (feature.properties.radius) {
                    return new L.Circle(latlng, feature.properties.radius);
                } else {
                    return new L.Marker(latlng);
                }
            }
        });

        var layers = aa.getLayers();
        geofence_layer.clearLayers();
        for (var i=0; i<layers.length; ++i) {
            geofence_layer.addLayer(layers[i]);
        }
    });
}


