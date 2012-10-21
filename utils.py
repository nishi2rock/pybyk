#!/usr/bin/python

from urllib2 import urlopen
from json import loads

import math

import numpy as np

def gc_dist(point1, point2):
    """ Calculates the great-circle distance between two points on earth.

    >>> point1 = (13.060422, 80.249583)
    >>> point2 = (12.9165167, 79.1324986)

    >>> gc_dist(point1, point2)
    122.089163396
    """

    radius = 6371
    lat1, lng1 = point1
    lat2, lng2 = point2

    lat1 = lat1 * math.pi / 180
    lng1 = lng1 * math.pi / 180
    lat2 = lat2 * math.pi / 180
    lng2 = lng2 * math.pi / 180

    return radius * math.acos(math.sin(lat1) * math.sin(lat2) + 
                              math.cos(lat1) * math.cos(lat2) * math.cos(lng2 - lng1)
                             )


def range_of_points(point1, point2, nPoints):
    """ An extended version of the ``linspace`` method in ``numpy``.
    Generates a range of points between two given points.
    """

    x1, y1 = point1
    x2, y2 = point2

    x_range = np.linspace(x1, x2, nPoints)
    y_range = np.linspace(y1, y2, nPoints)

    return zip(x_range, y_range)


def elevation(point):
    """ Returns the elevation (in mtrs) of the given point.
    Ex:
    >>> point = (13.0604, 80.2495) # Chennai, India
    >>> print elevation(point)
    13.6087
    """

    base_url = "http://maps.googleapis.com/maps/api/elevation/json?locations=%f,%f&sensor=true"

    p_url = base_url%point
    el_data = loads(urlopen(p_url).read())
    return el_data['results'][0]['elevation']
