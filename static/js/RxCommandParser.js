

window._last_rover_update = Date.now();

followRoverElem = document.getElementById('followRover');

function parse_message(msg) {

    if ('cmd' in msg) {
        console.log('command is:', msg.cmd);

        if (msg.cmd === 'reload mission') {
            get_mission();
        }
    }

    if ('lat' in msg && 'lon' in msg && 'hdg' in msg) {
        //var ts = Date.now();
        //if ((ts - window._last_rover_update) > 500) {
            //window._last_rover_update = ts;
            //console.log(msg.lat, msg.lon);
            window._rover.setLatLng([msg.lat, msg.lon]);
            window._rover.setRotationAngle(msg.hdg);

            if (followRoverElem.checked) {
                var zoom = map.getZoom();
                map.setView([msg.lat, msg.lon], zoom, {animate: false});
            }
        //}
    }
}

