

def parse_mission(filename, maxSpeed=6.5):
    '''
    Read and parse a plain-text mission file
    (this is the type of file exported by APM_Planner2, for example)

    https://mavlink.io/en/file_formats/#mission_plain_text_file
    '''

    items = []
    f = open(filename)

    first_line = f.readline()
    assert first_line.startswith('QGC WPL'), "unknown file format"

    for oneLine in f:
        pieces = oneLine.split()
        if len(pieces) < 12:
            print(' ******* ERROR PARSING MISSION ******')
            return
        cmd = int(pieces[3], 10)
        print("CMD:", cmd)
        if cmd == 16:  # waypoint
            #minSpeed = float(pieces[4])
            radius = float(pieces[5])
            lat = float(pieces[8])
            lon = float(pieces[9])
            # First line is "HOME", which we can't seem to do much with...
            if len(items) == 0:
                items.append( ('home', {'lat': lat, 'lon': lon, 'radius': radius}))
            else:
                items.append( ('waypoint', {'lat': lat, 'lon': lon, 'radius': radius}))
        elif cmd == 19:  # loiter time
            tWait = float(pieces[4])
            items.append( ('stop', tWait))
        elif cmd == 21:  # land -> next mission
            items.append( ('wait_for_button', (None)))
        elif cmd == 115:  # condition yaw (set heading)
            hdg = float(pieces[4])
            items.append( ('set_heading', hdg))
        elif cmd == 178:  # change speed
            maxSpeed = float(pieces[5])
        elif cmd == 181:  # set relay
            val = int(pieces[4], 10)
            items.append( ('set_relay', (val)))
        elif cmd == 203:  # digicam -- switch to follow mode
            items.append( ('follow_mode', (None)))
        else:
            print("Unknown command in mission:", cmd)

    f.close()

    return items


if __name__ == "__main__":
    import sys
    import pprint
    import shutil
    fname = sys.argv[1]
    items = parse_mission(fname)

    cols = shutil.get_terminal_size().columns
    pprint.pprint(items, width=(cols-5))

