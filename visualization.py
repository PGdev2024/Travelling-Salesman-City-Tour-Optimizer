"""
Visualization module for the TSP solver.
Creates matplotlib visualizations of routes and optimizations.
This is an optional extension that can be imported when visualization is needed.
"""

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch


def plot_route(places, route, title="TSP Route"):
    """
    Create a scatter plot with arrows showing the TSP route.
    
    Args:
        places (list): List of Place namedtuples with 'name', 'lat', and 'lon' attributes
        route (list): List of indices representing the route
        title (str): Title for the plot
    """
    # Extract coordinates for plotting
    lats = [places[i].lat for i in route]
    lons = [places[i].lon for i in route]
    names = [places[i].name for i in route]
    
    # Create figure and axis
    plt.figure(figsize=(10, 8))
    
    # Plot points (cities)
    plt.scatter(lons, lats, c='blue', s=100, zorder=2)
    
    # Plot route as lines with arrows
    for i in range(len(route)-1):
        plt.arrow(lons[i], lats[i], 
                 lons[i+1] - lons[i], lats[i+1] - lats[i],
                 head_width=0.01, head_length=0.02, 
                 fc='red', ec='red', zorder=1,
                 length_includes_head=True)
    
    # Add city labels
    for i, txt in enumerate(names):
        plt.annotate(txt, (lons[i], lats[i]), 
                    xytext=(5, 5), textcoords='offset points')
    
    # Add index numbers to show order
    for i in range(len(route)):
        plt.annotate(f"{i+1}", (lons[i], lats[i]), 
                    xytext=(-15, -15), textcoords='offset points',
                    bbox=dict(boxstyle="circle,pad=0.3", fc="yellow", ec="black", alpha=0.8))
    
    # Set plot properties
    plt.title(title)
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.grid(True)
    
    # Adjust axis limits to add some padding
    x_margin = (max(lons) - min(lons)) * 0.1
    y_margin = (max(lats) - min(lats)) * 0.1
    plt.xlim(min(lons) - x_margin, max(lons) + x_margin)
    plt.ylim(min(lats) - y_margin, max(lats) + y_margin)
    
    # Make the plot aspect ratio equal
    plt.gca().set_aspect('equal', adjustable='box')
    
    # Add distance information if available
    plt.tight_layout()
    
    return plt.gcf()  # Return the figure


def compare_routes(places, original_route, improved_route, original_distance, improved_distance):
    """
    Create a side-by-side comparison of original and improved routes.
    
    Args:
        places (list): List of Place namedtuples
        original_route (list): Original route indices
        improved_route (list): Improved route indices
        original_distance (float): Distance of original route
        improved_distance (float): Distance of improved route
    """
    # Create a figure with two subplots side by side
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 7))
    
    # Plot original route on the left
    _plot_route_on_axis(ax1, places, original_route, 
                       f"Original Route\nDistance: {original_distance:.2f} km")
    
    # Plot improved route on the right
    _plot_route_on_axis(ax2, places, improved_route, 
                       f"Improved Route\nDistance: {improved_distance:.2f} km")
    
    # Add information about improvement
    improvement = ((original_distance - improved_distance) / original_distance) * 100
    fig.suptitle(f"Route Optimization: {improvement:.2f}% improvement", fontsize=16)
    
    plt.tight_layout()
    
    return fig


def _plot_route_on_axis(ax, places, route, title):
    """
    Helper function to plot a route on a given matplotlib axis.
    
    Args:
        ax (matplotlib.axes.Axes): The axis to plot on
        places (list): List of Place namedtuples
        route (list): List of indices representing the route
        title (str): Title for the plot
    """
    # Extract coordinates for plotting
    lats = [places[i].lat for i in route]
    lons = [places[i].lon for i in route]
    names = [places[i].name for i in route]
    
    # Plot points (cities)
    ax.scatter(lons, lats, c='blue', s=80, zorder=2)
    
    # Plot route as lines with arrows
    for i in range(len(route)-1):
        ax.arrow(lons[i], lats[i], 
                lons[i+1] - lons[i], lats[i+1] - lats[i],
                head_width=0.01, head_length=0.02, 
                fc='red', ec='red', zorder=1,
                length_includes_head=True)
    
    # Add city labels
    for i, txt in enumerate(names):
        ax.annotate(txt, (lons[i], lats[i]), 
                   xytext=(5, 5), textcoords='offset points')
    
    # Add index numbers to show order
    for i in range(len(route)):
        ax.annotate(f"{i+1}", (lons[i], lats[i]), 
                   xytext=(-15, -15), textcoords='offset points',
                   bbox=dict(boxstyle="circle,pad=0.3", fc="yellow", ec="black", alpha=0.8))
    
    # Set plot properties
    ax.set_title(title)
    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')
    ax.grid(True)
    
    # Adjust axis limits to add some padding
    x_margin = (max(lons) - min(lons)) * 0.1
    y_margin = (max(lats) - min(lats)) * 0.1
    ax.set_xlim(min(lons) - x_margin, max(lons) + x_margin)
    ax.set_ylim(min(lats) - y_margin, max(lats) + y_margin)
    
    # Make the plot aspect ratio equal
    ax.set_aspect('equal', adjustable='box')