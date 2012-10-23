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

    try:
        dist = radius * math.acos(math.sin(lat1) * math.sin(lat2) + 
                                  math.cos(lat1) * math.cos(lat2) * 
                                  math.cos(lng2 - lng1)
                                 )
        return dist
    except ValueError:
        return 0


def range_of_points(point1, point2, nPoints):
    """ An extended version of the ``linspace`` method in ``numpy``.
    Generates a range of points between two given points.
    """

    lat1, lng1 = point1
    lat2, lng2 = point2

    lat_samples = np.linspace(lat1, lat2, nPoints)
    lng_samples = np.linspace(lng1, lng2, nPoints)

    return zip(lat_samples, lng_samples)


def elevation(p_list):
    """ Calculate the elevation (in mtrs) of a point or a list of points.

    :input: A tuple with latitude and longitude of a point or a list of tuples.
    :output: The elevation as a float or a list of floats correspondingly.

    >>> point = (13.0604, 80.2495) # Chennai, India
    >>> print elevation(point)
    13.6087

    >>> points_lst = [(13.0604, 80.2495), (12.9165167, 79.1324986)]
    >>> print elevation(points_list)
    [13.6087, 218.1465]
    """

    # There is a limit to the no.of locations that can be used in a single
    # URL/request. Hence we break the list into chunks and fetch the elevations
    # of each sub list and finally join them to get the final list
    N_POINTS_SUBLIST = 50

    def elevation_max_points(points_list):
        """ A method defined to work around the URI too large error.
        """

        if type(points_list) != type([]):
            points_list = [points_list]

        latlng_sep = ","
        latlng_list = ["%2.4f%s%2.4f"%(point[0], latlng_sep, point[1]) for point in points_list]

        point_sep = "|"
        point_list = point_sep.join(latlng_list)

        base_url = "http://maps.googleapis.com/maps/api/elevation/json?locations=%s&sensor=true"
        el_url = base_url%point_list
        el_data = loads(urlopen(el_url).read())

        el_results = el_data['results']

        return [r["elevation"] for r in el_results]

    if type(p_list) != type([]):
        p_list = [p_list]

    elev_list = []
    for idx in range(0, len(p_list), N_POINTS_SUBLIST):
        points_sub_list = p_list[idx:idx+N_POINTS_SUBLIST]
        elev_list += elevation_max_points(points_sub_list)

    if len(elev_list) == 1:
        return elev_list[0]
    return elev_list
