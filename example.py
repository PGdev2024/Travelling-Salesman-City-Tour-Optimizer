"""
Example usage script for the TSP solver.
This script demonstrates how to use the TSP solver with a sample dataset.
"""

import os
import sys
from collections import namedtuple

# Import modules from the same directory
import sys
import os

# Add the current directory to the path if not already there
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import modules from the TSP solver package
from distance import calculate_distance_matrix
from tsp_solver import greedy_solver, optimize_route, calculate_route_distance
from visualization import plot_route, compare_routes

# Sample data: Famous landmarks in Paris
sample_data = [
    ("Eiffel Tower", 48.8584, 2.2945),
    ("Louvre Museum", 48.8606, 2.3376),
    ("Notre-Dame", 48.8530, 2.3499),
    ("Arc de Triomphe", 48.8738, 2.2950),
    ("Sacré-Cœur", 48.8867, 2.3431),
    ("Panthéon", 48.8462, 2.3464),
    ("Musée d'Orsay", 48.8600, 2.3266),
    ("Centre Pompidou", 48.8606, 2.3522),
]

def create_sample_csv(filename="sample_places.csv"):
    """Create a sample CSV file with Paris landmarks."""
    with open(filename, 'w') as f:
        f.write("Name,Lat,Lon\n")  # Header
        for name, lat, lon in sample_data:
            f.write(f"{name},{lat},{lon}\n")
    return filename

def run_example():
    """Run a complete example of the TSP solver workflow."""
    print("TSP Solver Example")
    print("=================")
    
    # Create a Place namedtuple to store data
    Place = namedtuple('Place', ['name', 'lat', 'lon'])
    
    # Convert sample data to Place objects
    places = [Place(name=name, lat=lat, lon=lon) for name, lat, lon in sample_data]
    
    print(f"Loaded {len(places)} places")
    for i, place in enumerate(places):
        print(f"{i+1}. {place.name} ({place.lat}, {place.lon})")
    
    # Calculate distance matrix
    print("\nCalculating distance matrix...")
    dist_matrix = calculate_distance_matrix(places)
    
    # Print distance matrix (truncated for readability)
    print("\nDistance Matrix (km):")
    print("    " + " ".join(f"{place.name[:7]:>10}" for place in places))
    for i, row in enumerate(dist_matrix):
        print(f"{places[i].name[:7]:>7}", end="")
        for dist in row:
            print(f"{dist:>10.2f}", end="")
        print()
    
    # Set starting point (Eiffel Tower)
    start_idx = 0
    print(f"\nStarting point: {places[start_idx].name}")
    
    # Solve using greedy algorithm
    print("\nSolving using greedy algorithm...")
    route = greedy_solver(dist_matrix, start_idx)
    
    # Add return to start
    return_route = route.copy() + [start_idx]
    
    # Calculate initial route distance
    initial_distance = calculate_route_distance(return_route, dist_matrix)
    print(f"Initial route distance: {initial_distance:.2f} km")
    
    # Print initial route
    print("\nInitial route:")
    for i, idx in enumerate(return_route):
        print(f"{i+1}. {places[idx].name}")
    
    # Optimize using 2-opt
    print("\nOptimizing route using 2-opt algorithm...")
    optimized_route = optimize_route(return_route, dist_matrix)
    
    # Calculate optimized route distance
    optimized_distance = calculate_route_distance(optimized_route, dist_matrix)
    print(f"Optimized route distance: {optimized_distance:.2f} km")
    improvement = ((initial_distance - optimized_distance) / initial_distance) * 100
    print(f"Improvement: {improvement:.2f}%")
    
    # Print optimized route
    print("\nOptimized route:")
    for i, idx in enumerate(optimized_route):
        print(f"{i+1}. {places[idx].name}")
    
    # Visualize the routes
    try:
        import matplotlib.pyplot as plt
        
        # Save the visualizations if matplotlib is available
        print("\nGenerating visualizations...")
        
        # Plot original route
        original_fig = plot_route(places, return_route, "Original Route")
        original_fig.savefig("original_route.png")
        
        # Plot optimized route
        optimized_fig = plot_route(places, optimized_route, "Optimized Route")
        optimized_fig.savefig("optimized_route.png")
        
        # Plot comparison
        comparison_fig = compare_routes(
            places, return_route, optimized_route, 
            initial_distance, optimized_distance
        )
        comparison_fig.savefig("route_comparison.png")
        
        print("Visualizations saved as PNG files")
        
    except ImportError:
        print("\nNote: matplotlib not available, skipping visualizations")
    
    print("\nExample completed successfully!")


if __name__ == "__main__":
    run_example()