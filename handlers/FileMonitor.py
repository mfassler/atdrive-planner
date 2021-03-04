
import os
import sys
import time
import logging
import json
import asyncio
import config
import pprint

from aiohttp import web
from .parse_mission import parse_mission


_daMainThing = None
_last_mtime = 0
_mission = []

async def get_mission(request):
    global _mission
    print("hello   .... this is mission.json")
    pprint.pprint(_mission)
    sys.stdout.flush()
    return web.json_response(_mission)


async def myBgTask():
    global _daMainThing
    global _last_mtime
    global _mission
    while True:
        try:
            mtime = os.path.getmtime(config.MISSION_FILENAME)
        except Exception as ee:
            print('failed to find MISSION file:', ee)
            sys.stdout.flush()
            await asyncio.sleep(1)
        else:
            if _last_mtime != mtime:
                _last_mtime = mtime
                print('file has changed')
                try:
                    _mission = parse_mission(config.MISSION_FILENAME)
                except Exception as ee:
                    print('failed to parse mission:', ee)
                    sys.stdout.flush()
                else:
                    _daMainThing.send_to_all('{"cmd": "reload mission"}')
            else:
                await asyncio.sleep(1)



async def start_background_tasks(app):
    loop = asyncio.get_event_loop()
    #loop = asyncio.get_running_loop()  # <-- hmm, what's the difference?
    app['file_monitor'] = loop.create_task(myBgTask())


async def cleanup_background_tasks(app):
    app['file_monitor'].cancel()
    await app['file_monitor']


def setup(app, daMainThing):
    print('FileMonitor setup.  daMainThing:', daMainThing)
    global _daMainThing
    _daMainThing = daMainThing

    print('hello from file monitor')
    app.on_startup.append(start_background_tasks)
    app.on_cleanup.append(cleanup_background_tasks)

