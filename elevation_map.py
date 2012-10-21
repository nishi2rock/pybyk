# coding: utf-8
from sys import argv
from BeautifulSoup import BeautifulStoneSoup
from matplotlib import pyplot
from utils import gc_dist, elevation

gpx_file = argv[1]
data = open(gpx_file).read()
soup = BeautifulStoneSoup(data)

points = soup.findAll("trkpt")
route = [(float(p.attrs[0][1]), float(p.attrs[1][1])) for p in points]

dist_diffs = [0] + [gc_dist(route[i], route[i + 1]) for i in range(1, len(route) - 1)]
dist_from_src = [0]

for d in dist_diffs:
    dist_from_src.append(dist_from_src[-1] + d)

elevs = elevation(route)

pyplot.plot(dist_from_src, elevs)
pyplot.show()
