from geopy import Point
from geopy.distance import geodesic

def get_coords(lat, lon, distKm):
    max_lat = geodesic(kilometers=distKm).destination(Point(lat, lon), 0).latitude # north
    max_lon = geodesic(kilometers=distKm).destination(Point(lat, lon), 90).longitude # east
    min_lat = geodesic(kilometers=distKm).destination(Point(lat, lon), 180).latitude # south
    min_lon = geodesic(kilometers=distKm).destination(Point(lat, lon), 270).longitude # west
    return (min_lat, max_lat, min_lon, max_lon)
