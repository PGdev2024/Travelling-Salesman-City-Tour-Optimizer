"""
Distance calculation module for TSP solver.
Handles distance calculations between geographic coordinates.
"""

import math
from collections import namedtuple


def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calculate the great-circle distance in kilometers between two points 
    on the Earth's surface using the Haversine formula.
    
    Args:
        lat1, lon1: Latitude and longitude of point 1 (in degrees)
        lat2, lon2: Latitude and longitude of point 2 (in degrees)
        
    Returns:
        float: Distance in kilometers
    """
    # Convert latitude and longitude from degrees to radians
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)
    
    # Haversine formula components
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    
    # Haversine formula calculation
    a = math.sin(dlat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    
    # Earth's radius in kilometers
    R = 6371.0
    
    # Calculate distance
    distance = R * c
    
    return distance


def calculate_distance_matrix(places):
    """
    Calculate the distance matrix for a list of places using the Haversine formula.
    
    Args:
        places (list): List of Place namedtuples with 'lat' and 'lon' attributes
        
    Returns:
        list: 2D distance matrix where dist[i][j] is the distance from place i to place j
    """
    # Initialize the distance matrix with zeros
    n = len(places)
    dist_matrix = [[0.0 for _ in range(n)] for _ in range(n)]
    
    # Calculate distances between all pairs of places
    for i in range(n):
        for j in range(i+1, n):  # Only calculate upper triangle (distances are symmetric)
            distance = haversine_distance(
                places[i].lat, places[i].lon,
                places[j].lat, places[j].lon
            )
            # Fill both entries since distance is symmetric
            dist_matrix[i][j] = distance
            dist_matrix[j][i] = distance
    
    return dist_matrix