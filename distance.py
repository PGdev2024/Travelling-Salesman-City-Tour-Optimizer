# Check the distance calculation implementation in distance.py
def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    
    Returns distance in kilometers
    """
    from math import radians, sin, cos, sqrt, atan2
    
    # Convert decimal degrees to radians
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    
    # Haversine formula
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a)) 
    
    # Radius of earth in kilometers
    r = 6371
    
    # Distance in km
    return r * c

def calculate_distance_matrix(places):
    """
    Calculate distance matrix between all places.
    
    Args:
        places (list): List of Place namedtuples
        
    Returns:
        list: 2D distance matrix
    """
    n = len(places)
    dist_matrix = [[0.0 for _ in range(n)] for _ in range(n)]
    
    for i in range(n):
        for j in range(i+1, n):
            dist = haversine_distance(
                places[i].lat, places[i].lon,
                places[j].lat, places[j].lon
            )
            # Store distance in both directions
            dist_matrix[i][j] = dist
            dist_matrix[j][i] = dist
            
    return dist_matrix
