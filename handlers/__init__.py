import os
import sys
import pprint
import json
from aiohttp import web

import config

from .FileMonitor import setup as file_monitor_setup
from .FileMonitor import get_mission
from .WebRTCs import WebRTCs

from .killall_geofenced_hup import killall_geofenced_hup

ROOT = os.path.join(os.path.dirname(__file__), '../')


async def get_index(request):
    content = open(os.path.join(ROOT, 'static', "index.html"), "r").read()
    return web.Response(content_type="text/html", text=content)


async def get_geofence(request):
    try:
        #content = open(os.path.join(ROOT, 'geofence.json'), "r").read()
        content = open(os.path.join(ROOT, config.GEOFENCE_FILENAME), "r").read()
        _nothing = json.loads(content)
    except:
        print('Failed to parse geofence from file')
        sys.stdout.flush()
        # empty GeoJSON object:
        content = '{"type": "FeatureCollection", "features": []}'

    return web.Response(content_type="application/json", text=content)


async def post_geofence(request):
    geofence = await request.json()
    print('RX geofence:')
    pprint.pprint(geofence)
    sys.stdout.flush()

    f = open(os.path.join(ROOT, config.GEOFENCE_FILENAME), 'w')
    f.write(json.dumps(geofence))
    f.close()

    # Send a SIGHUP to geofenced, causing it to reload the geofence file:
    killall_geofenced_hup()

    return web.json_response({'nothing': 'ho hum'})

