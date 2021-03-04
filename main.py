#!/usr/bin/env python3

import logging
import ssl
import asyncio
from aiohttp import web
import handlers

import config

# One object to manage all WebRTC connections:
webrtcs = handlers.WebRTCs()


if __name__ == "__main__":

    if hasattr(config, 'LOGLEVEL'):
        logging.basicConfig(level=config.LOGLEVEL)

    if hasattr(config, 'SSL_CERT_FILE') and hasattr(config, 'SSL_KEY_FILE'):
        ssl_context = ssl.SSLContext()
        ssl_context.load_cert_chain(config.SSL_CERT_FILE, config.SSL_KEY_FILE)
    else:
        ssl_context = None


    app = web.Application()


    # Static web pages:
    app.router.add_get("/", handlers.get_index)
    app.router.add_static('/static/', path='static')

    # Read/write the mission and/or geofence:
    app.router.add_get("/mission.json", handlers.get_mission)
    #app.router.add_post("/mission.json", handlers.post_mission)
    app.router.add_get("/geofence.json", handlers.get_geofence)
    app.router.add_post("/geofence.json", handlers.post_geofence)

    # This is to create the WebRTC channel:
    app.router.add_get("/offer", webrtcs.get_offer)
    app.router.add_post("/answer", webrtcs.post_answer)
    app.router.add_post("/ice_candidate", webrtcs.post_ice_candidate)
    app.on_shutdown.append(webrtcs.on_shutdown)

    # These can push live messages to the web browser via the WebRTC DataChannel:
    handlers.file_monitor_setup(app, webrtcs)

    loop = asyncio.get_event_loop()
    loop.create_task(webrtcs.check_nav_packets())

    web.run_app(app, port=config.HTTP_LISTEN_PORT, ssl_context=ssl_context)


