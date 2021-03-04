#!/usr/bin/env python3

import sys
if sys.version_info[0] < 3:
    raise Exception("Must be using Python 3")

import time
import signal
import json
import pprint



def load_geofence():
    f = open('../geofence.json', 'r')
    geofence = json.load(f)
    f.close()
    pprint.pprint(geofence)


def rx_signal_HUP(signum, stack):
    '''A SIGHUP will trigger us to reload the geofence file'''
    print('got a signal:', signum, stack)
    try:
        load_geofence()
    except Exception as ee:
        print('failed to load geofence:', ee)


signal.signal(signal.SIGHUP, rx_signal_HUP)


while True:
    time.sleep(1)
    print('.')
    sys.stdout.flush()


