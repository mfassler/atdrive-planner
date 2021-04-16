

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


        // ES6 (2015)
        for (const item of mission) {
            const cmd = item[0];
            const params = item[1];

            switch (cmd) {
            case 'home':

                var waypoint = new L.LatLng(params.lat, params.lon);
                pointList.push(waypoint);

                var circle = L.circle(waypoint, {
                    color: 'orange',
                    //fillColor: '#f03',
                    fillOpacity: 0.1,
                    weight: 1,
                    radius: params.radius
                }).addTo(window._missionLayer);

                if (origin === null) {
                    origin = waypoint;
                    window._mapOrigin = origin;
                }
                break;

            case 'waypoint':

                var waypoint = new L.LatLng(params.lat, params.lon);
                pointList.push(waypoint);

                var circle = L.circle(waypoint, {
                    color: 'yellow',
                    //fillColor: '#f03',
                    fillOpacity: 0.1,
                    weight: 1,
                    radius: params.radius
                }).addTo(window._missionLayer);

                if (origin === null) {
                    origin = [lat, lon];
                    window._mapOrigin = origin;
                }

                break;

            default:
                console.log('Unknown mission item:', cmd);
                break;
            }
        }

        if (origin != null) {
            map.setView(origin, 19, {animate: false});
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


