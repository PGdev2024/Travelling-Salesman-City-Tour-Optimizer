"""
TSP solver module implementing various algorithms for solving the Travelling Salesman Problem.
Includes greedy nearest neighbor algorithm and 2-opt improvement algorithm.
"""

import random
import math


def greedy_solver(dist_matrix, start_idx):
    """
    Solve the TSP using a greedy nearest neighbor algorithm.
    Start at the given index and always visit the nearest unvisited place next.
    
    Args:
        dist_matrix (list): 2D distance matrix
        start_idx (int): Index of the starting place
        
    Returns:
        list: Ordered list of indices representing the route
    """
    n = len(dist_matrix)
    
    # Initialize variables
    current = start_idx
    unvisited = set(range(n))
    unvisited.remove(current)
    route = [current]
    
    # Greedily select nearest unvisited place until all places are visited
    while unvisited:
        # Find nearest unvisited place
        nearest = min(unvisited, key=lambda i: dist_matrix[current][i])
        
        # Add to route and mark as visited
        route.append(nearest)
        unvisited.remove(nearest)
        current = nearest
        
    return route


def optimize_route(route, dist_matrix):
    """
    Improve a route using the 2-opt algorithm.
    The 2-opt algorithm iteratively replaces two edges with two new ones
    if it reduces the total distance.
    
    Args:
        route (list): Initial route as a list of indices
        dist_matrix (list): 2D distance matrix
        
    Returns:
        list: Improved route
    """
    # Make a copy of the route to avoid modifying the original
    best_route = route.copy()
    improved = True
    
    while improved:
        improved = False
        best_distance = calculate_route_distance(best_route, dist_matrix)
        
        # Try all possible combinations of edge swaps
        for i in range(1, len(best_route) - 2):
            for j in range(i + 1, len(best_route) - 1):
                # Create new route with 2-opt swap
                new_route = best_route.copy()
                # Reverse the portion between i and j
                new_route[i:j+1] = reversed(new_route[i:j+1])
                
                # Calculate new distance
                new_distance = calculate_route_distance(new_route, dist_matrix)
                
                # If the new route is better, keep it
                if new_distance < best_distance:
                    best_distance = new_distance
                    best_route = new_route
                    improved = True
                    # We can break early once we find an improvement
                    break
            
            # If we found an improvement, break out of the outer loop as well
            if improved:
                break
    
    return best_route


def calculate_route_distance(route, dist_matrix):
    """
    Calculate the total distance of a route.
    
    Args:
        route (list): List of indices representing the route
        dist_matrix (list): 2D distance matrix
        
    Returns:
        float: Total distance
    """
    total = 0
    for i in range(len(route) - 1):
        total += dist_matrix[route[i]][route[i+1]]
    return total


def simulated_annealing(route, dist_matrix, temp_start=1000, temp_end=0.01, cooling_rate=0.995):
    """
    Improve a route using simulated annealing algorithm.
    Note: This is an advanced optimization method included as an optional extension.
    
    Args:
        route (list): Initial route as a list of indices
        dist_matrix (list): 2D distance matrix
        temp_start (float): Starting temperature
        temp_end (float): Ending temperature
        cooling_rate (float): Rate at which temperature decreases
        
    Returns:
        list: Improved route
    """
    # Make a copy of the route to avoid modifying the original
    current_route = route.copy()
    best_route = route.copy()
    current_distance = calculate_route_distance(current_route, dist_matrix)
    best_distance = current_distance
    
    # Keep track of the fixed points (usually the first and last if returning to start)
    fixed_points = set()
    if route[0] == route[-1]:  # If returning to start
        fixed_points.add(0)
        fixed_points.add(len(route) - 1)
    
    # Initialize temperature
    temperature = temp_start
    
    # Main simulated annealing loop
    while temperature > temp_end:
        # Create a new candidate route by swapping two cities
        candidate_route = current_route.copy()
        
        # Select two random positions to swap, excluding fixed points
        available_indices = [i for i in range(len(route)) if i not in fixed_points]
        if len(available_indices) < 2:
            break  # Not enough points to swap
        
        i, j = random.sample(available_indices, 2)
        
        # Swap the cities
        candidate_route[i], candidate_route[j] = candidate_route[j], candidate_route[i]
        
        # Calculate the new distance
        candidate_distance = calculate_route_distance(candidate_route, dist_matrix)
        
        # Determine if we should accept the new route
        delta = candidate_distance - current_distance
        
        # Accept if better, or with a probability based on temperature if worse
        if delta < 0 or random.random() < math.exp(-delta / temperature):
            current_route = candidate_route
            current_distance = candidate_distance
            
            # Update best route if this is better
            if current_distance < best_distance:
                best_route = current_route.copy()
                best_distance = current_distance
        
        # Cool down the temperature
        temperature *= cooling_rate
    
    return best_route