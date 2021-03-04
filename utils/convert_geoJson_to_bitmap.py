#!/usr/bin/env python3

import sys
if sys.version_info[0] < 3:
    raise Exception("Must be using Python 3")

import os
import time
import json
import pprint
import numpy as np
import cv2

earthRadiusMeters = 6371.0 * 1000.0


class ConverterThing:
    def __init__(self):
        self._reset()

    def _reset(self):
        self.min_lat = None
        self.min_lon = None
        self.max_lat = None
        self.max_lon = None
        self.max_radius = 0.0

    def check_lat_lon_r(self, lat, lon, r):
        ## TODO:  intelligently handle large radiuses overflowing the bounding-box
        if self.min_lat is None:
            self.min_lat = lat
        if self.min_lon is None:
            self.min_lon = lon
        if self.max_lat is None:
            self.max_lat = lat
        if self.max_lon is None:
            self.max_lon = lon

        if self.min_lat > lat:
            self.min_lat = lat

        if self.min_lon > lon:
            self.min_lon = lon

        if self.max_lat < lat:
            self.max_lat = lat

        if self.max_lon < lon:
            self.max_lon = lon

        if self.max_radius < r:
            self.max_radius = r

_myimg = None
_mycoords = None

def convert_geoJson_to_bitmap(filename, pixels_per_meter):
    f = open(filename, 'r')
    geoJson = json.load(f)
    f.close()
    global _myimg
    global _mycoords

    checker = ConverterThing()

    # Right now, we only support Polygons and Points-with-radius

    # find the mins,maxes lats/lons to find a GPS bounding box
    for item in geoJson['features']:
        if 'geometry' in item:
            if 'type' in item['geometry']:
                print(item['geometry']['type'])
                if item['geometry']['type'] == 'Polygon':
                    for subShape in item['geometry']['coordinates']:
                        for pt in subShape:
                            lon, lat = pt
                            r = 0.0
                            print('   ', lat, lon, r)
                            checker.check_lat_lon_r(lat, lon, r)

                elif item['geometry']['type'] == 'Point':
                    lon, lat = item['geometry']['coordinates']
                    r = 0.0
                    if 'properties' in item:
                        if 'radius' in item['properties']:
                            r = item['properties']['radius']
                    print('   ', lat, lon, r)
                    checker.check_lat_lon_r(lat, lon, r)


    min_lat = checker.min_lat
    min_lon = checker.min_lon
    max_lat = checker.max_lat
    max_lon = checker.max_lon
    max_radius = checker.max_radius

    print(min_lat, min_lon, max_lat, max_lon, max_radius)

    mid_lat = (max_lat + min_lat) / 2.0

    ## Skipping sin() because of the small-angle approximation
    delta_Y = np.radians(max_lat - min_lat) * earthRadiusMeters
    delta_X = np.radians(max_lon - min_lon) * earthRadiusMeters * np.cos(np.radians(mid_lat))

    print("Width x Height:", delta_X, delta_Y)

    map_height_meters = delta_Y + 2 * max_radius  # include a margin for the circles
    map_width_meters = delta_X + 2 * max_radius  # include a margin for the circles

    map_height_pixels = int(np.ceil(map_height_meters * pixels_per_meter))
    map_width_pixels = int(np.ceil(map_width_meters * pixels_per_meter))

    img = np.zeros((map_height_pixels, map_width_pixels), np.uint8)

    vScale = np.pi / 180.0 * earthRadiusMeters
    hScale = np.pi / 180.0 * earthRadiusMeters * np.cos(np.radians(mid_lat))

    for item in geoJson['features']:
        if 'geometry' in item:
            if 'type' in item['geometry']:
                print(item['geometry']['type'])
                if item['geometry']['type'] == 'Polygon':
                    for subShape in item['geometry']['coordinates']:
                        coords = []
                        for pt in subShape:
                            lon, lat = pt
                            offset = max_radius  # leave enough room for the circles
                            y = (max_lat - lat) * vScale + offset
                            x = (lon - min_lon) * hScale + offset

                            x_px = int(round(x * pixels_per_meter))
                            y_px = int(round(y * pixels_per_meter))
                            coords.append( [x_px, y_px] )

                        _myimg = img
                        _mycoords = coords
                        cv2.fillPoly(img, [np.array(coords, np.int32)], (255, 255,255))

                elif item['geometry']['type'] == 'Point':
                    lon, lat = item['geometry']['coordinates']
                    r = 0.0
                    if 'properties' in item:
                        if 'radius' in item['properties']:
                            r = item['properties']['radius']
                    #print('   ', lat, lon, r)
                    #checker.check_lat_lon_r(lat, lon, r)
                    offset = max_radius  # leave enough room for the circles
                    y = (max_lat - lat) * vScale + offset
                    x = (lon - min_lon) * hScale + offset

                    x_px = int(round(x * pixels_per_meter))
                    y_px = int(round(y * pixels_per_meter))
                    r_px = int(round(r * pixels_per_meter))

                    cv2.circle(img, (x_px, y_px), r_px, 255, -1)

    ## get the Lat, Lon of the top-left corner of the source image
    # top is max_lat
    # left is min_lon
    #  we added "max_radius" to the border of the map
    TOP_LAT = max_lat + np.degrees(max_radius / earthRadiusMeters)
    LEFT_LON = min_lon - np.degrees(max_radius / (earthRadiusMeters * np.cos(np.radians(mid_lat))))

    return img, TOP_LAT, LEFT_LON



def ResizeWithAspectRatio(image, width=None, height=None, inter=cv2.INTER_AREA):
    dim = None
    (h, w) = image.shape[:2]

    if width is None and height is None:
        return image
    if width is None:
        r = height / float(h)
        dim = (int(w * r), height)
    else:
        r = width / float(w)
        dim = (width, int(h * r))

    return cv2.resize(image, dim, interpolation=inter)



if __name__ == "__main__":
    prev_mtime = 0.0

    while True:
        mtime = os.path.getmtime(sys.argv[1])
        if mtime > prev_mtime:
            prev_mtime = mtime
            img, top_lat, left_lon = convert_geoJson_to_bitmap(sys.argv[1], 100)
            print(img.shape, top_lat, left_lon)
            im2 = ResizeWithAspectRatio(img, width=1000)
            cv2.imshow('asdf', im2)
            #cv2.moveWindow('asdf', 20,20)
            cv2.waitKey(1)
        else:
            time.sleep(1)
            cv2.imshow('asdf', im2)
            cv2.waitKey(1)


