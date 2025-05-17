"""
Travelling Salesman Problem (TSP) City-Tour Optimizer
Main program file that handles command-line arguments and executes the overall flow.

Usage:
    python tsp.py --csv <csv_file> --start "<starting_point>" [--return] [--algo simulated-annealing]

Example:
    python tsp.py --csv places.csv --start "Eiffel Tower" --return
"""

import argparse
import json
import os
import sys
from collections import namedtuple

# Import modules from the same directory
import sys
import os

# Add the current directory to the path if not already there
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from distance import calculate_distance_matrix
from tsp_solver import greedy_solver, optimize_route


def parse_arguments():
    """
    Parse command line arguments.
    
    Returns:
        argparse.Namespace: Parsed command line arguments
    """
    parser = argparse.ArgumentParser(description='Travelling Salesman Problem Solver')
    parser.add_argument('--csv', required=True, help='CSV file with places (Name,Lat,Lon)')
    parser.add_argument('--start', required=True, help='Name of the starting point')
    parser.add_argument('--return', dest='return_to_start', action='store_true', 
                        help='Return to the starting point')
    parser.add_argument('--algo', choices=['greedy', 'simulated-annealing'], 
                        default='greedy', help='Algorithm to use')
    return parser.parse_args()


def read_csv(filename):
    """
    Read places from CSV file.
    
    Args:
        filename (str): Path to the CSV file
        
    Returns:
        list: List of Place namedtuples (name, lat, lon)
    """
    places = []
    Place = namedtuple('Place', ['name', 'lat', 'lon'])
    
    try:
        with open(filename, 'r') as f:
            # Skip header if it exists
            first_line = f.readline().strip()
            if not first_line.replace(',', '').replace('.', '').isdigit():
                # Reset file pointer if we detected and skipped a header
                f.seek(0)
                next(f)  # Skip header
                
            # Read places from file
            for line in f:
                parts = line.strip().split(',')
                if len(parts) >= 3:
                    name = parts[0]
                    try:
                        lat = float(parts[1])
                        lon = float(parts[2])
                        places.append(Place(name=name, lat=lat, lon=lon))
                    except ValueError:
                        print(f"Warning: Skipping invalid line: {line.strip()}")
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        sys.exit(1)
        
    if not places:
        print("Error: No valid places found in the CSV file")
        sys.exit(1)
        
    return places


def find_starting_index(places, start_name):
    """
    Find the index of the starting place.
    
    Args:
        places (list): List of Place namedtuples
        start_name (str): Name of the starting place
        
    Returns:
        int: Index of the starting place or -1 if not found
    """
    for i, place in enumerate(places):
        if place.name.lower() == start_name.lower():
            return i
            
    # Try partial matching if exact match fails
    for i, place in enumerate(places):
        if start_name.lower() in place.name.lower():
            print(f"Using '{place.name}' as it partially matches '{start_name}'")
            return i
    
    return -1


def calculate_total_distance(route, dist_matrix):
    """
    Calculate the total distance of a route.
    
    Args:
        route (list): List of indices representing the route
        dist_matrix (list): 2D distance matrix
        
    Returns:
        float: Total distance in kilometers
    """
    total = 0
    for i in range(len(route) - 1):
        total += dist_matrix[route[i]][route[i+1]]
    return total


def create_geojson(places, route, output_file="route.geojson"):
    """
    Create a GeoJSON file for the route that can be imported into mapping software.
    
    Args:
        places (list): List of Place namedtuples
        route (list): List of indices representing the route
        output_file (str): Output file name
    """
    # Create a LineString feature for the route
    coordinates = [[places[i].lon, places[i].lat] for i in route]
    
    geojson = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {},
                "geometry": {
                    "type": "LineString",
                    "coordinates": coordinates
                }
            }
        ]
    }
    
    # Add point features for each place
    for i, idx in enumerate(route):
        place = places[idx]
        geojson["features"].append({
            "type": "Feature",
            "properties": {
                "name": place.name,
                "order": i + 1
            },
            "geometry": {
                "type": "Point",
                "coordinates": [place.lon, place.lat]
            }
        })
    
    # Write GeoJSON to file
    with open(output_file, 'w') as f:
        json.dump(geojson, f, indent=2)


def main():
    """
    Main function that orchestrates the TSP solving process.
    """
    # Parse command-line arguments
    args = parse_arguments()
    
    # Read places from CSV
    places = read_csv(args.csv)
    print(f"Read {len(places)} places from {args.csv}")
    
    # Find starting index
    start_idx = find_starting_index(places, args.start)
    if start_idx == -1:
        print(f"Error: Starting place '{args.start}' not found in the CSV file")
        sys.exit(1)
    
    # Calculate distance matrix
    dist_matrix = calculate_distance_matrix(places)
    
    # Solve TSP using greedy algorithm
    route = greedy_solver(dist_matrix, start_idx)
    
    # If return flag is set, add the starting point to the end
    if args.return_to_start:
        route.append(start_idx)
    
    # Optimize the route using 2-opt
    if len(route) > 3:  # Only optimize if there are enough points
        print("Optimizing route using 2-opt algorithm...")
        optimized_route = optimize_route(route, dist_matrix)
    else:
        optimized_route = route
    
    # Calculate total distance
    total_distance = calculate_total_distance(optimized_route, dist_matrix)
    
    # Print the results
    print("\nOptimal tour" + (" (returns to start)" if args.return_to_start else "") + ":")
    for i, idx in enumerate(optimized_route):
        print(f"{i+1}) {places[idx].name}")
    
    print(f"\nTotal distance: {total_distance:.1f} km")
    
    # Create GeoJSON file
    output_file = "route.geojson"
    create_geojson(places, optimized_route, output_file)
    print(f"Route written to {output_file}")


if __name__ == "__main__":
    main()