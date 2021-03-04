# AT Drive Planner

Edit a geofence.  Read and write using the GeoJSON format.


## Software Requirements

This software requires the aiortc Python library.  

To build aiortc, you'll need ffmpeg 4.x and python >= 3.6


### To install aiortc in Fedora:

```bash
sudo dnf install ffmpeg-devel  # (from RPM Fusion, not Fedora)
sudo dnf install python3-aiohttp
pip3 install --user aiortc
```

Also required:

```bash
sudo dnf install python3-psutil
```

## To run:

This program expects to find a "CURRENT_MISSION.txt" in the current directory.
Typically, what I do is this:

```bash
ln -s /location/to/mission_file.txt ./CURRENT_MISSION.txt
```

Start the server with:

```bash
python3 main.py
```

Then use a web browser to connect to localhost:8080

