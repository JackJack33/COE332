#!/usr/bin/env python3

from math import radians, cos, sin, asin, sqrt

earth_radius = 6378.14

def greatCircleDistance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Computes the great circle distance between two points on the Earth's surface

    Args:
        lat1 (float): Latitude of the first point in degrees
        lon1 (float): Longitude of the first point in degrees
        lat2 (float): Latitude of the second point in degrees
        lon2 (float): Longitude of the second point in degrees

    Returns:
        float: The great circle distance between the two points in kilometers
    """

    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    # Haversine formula
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))

    return c * earth_radius
