"""
General utilities for use throughout the project
"""
from typing import Dict, List
from src.classes.hub import Hub


def calc_distance(path: List[Dict[str, int]], hubs: List[Hub]) -> int:
    """
    Function for calculating fitness (distance) of a solution

    params:
        path - List of {from, to, s} dictionaries
        hubs - The hubs in the solution

    returns
        Total distance of the solution
    """
    # Convert list of hubs into a dictionary to make it easier (and faster) to search
    hub_dict = {}
    for hub in hubs:
        hub_dict[hub.get_name()] = hub

    # Counter for total distance
    total_dist = 0

    # For each of the journeys
    for j in path:
        # Assign hub1 to the relative hubs in the model
        hub1: Hub = hub_dict[j['from']]

        # Get the distance to the 'to' hub in the journey
        dist = hub1.get_connections()[j['to']]

        # sum the distance with total distance
        total_dist += dist

    return total_dist
