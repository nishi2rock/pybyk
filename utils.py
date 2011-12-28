#!/usr/bin/python

from urllib2 import urlopen
from json import loads

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
