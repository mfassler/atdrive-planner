#!/usr/bin/env python3

import sys
if sys.version_info[0] < 3:
    raise Exception("Must be using Python 3")

import os
import signal
import psutil


def killall_geofenced_hup(debug=False):
    """
    Send a SIGHUP to geofenced, which will trigger it to reload
    any config files, etc.
    """

    processes = []

    for proc in psutil.process_iter():
        if proc.name().startswith('python'):
            for item in proc.cmdline():
                if item == 'geofenced.py':
                    processes.append(proc)
                    break

    if debug:
        print("Found %d processes" % (len(processes)))
        for oneProc in processes:
            print("  ", oneProc.pid, oneProc.cmdline())

    for oneProc in processes:
        os.kill(oneProc.pid, signal.SIGHUP)



if __name__ == "__main__":
    killall_geofenced_hup(debug=True)

