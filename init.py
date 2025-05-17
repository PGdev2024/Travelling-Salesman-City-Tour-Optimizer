"""
__init__.py file to make the directory a proper Python package.
This allows for clean imports between modules.
"""

# Import key functions so they can be imported directly from the package
from distance import calculate_distance_matrix, haversine_distance
from tsp_solver import greedy_solver, optimize_route, calculate_route_distance, simulated_annealing

# Define what gets imported with "from package import *"
__all__ = [
    'calculate_distance_matrix',
    'haversine_distance',
    'greedy_solver',
    'optimize_route',
    'calculate_route_distance',
    'simulated_annealing'
]