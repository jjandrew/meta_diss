"""
Creates distance and pheromone matrices for the problem
"""
from typing import List, Dict
from model.hub import Hub
import random


def create_dist_matrix(model: Dict[int, Hub]) -> List[List[float]]:
    """
    Creates the distance matrix from the model passed in

    Params
        model - A list of hubs that is passed in

    Returns:
        List where dist_matrix[i][j] is the distance on edge i-j
    """

    # Create a distance matrix with all values equalling 0 and of length and width len(model)
    dist_matrix = [[0] * len(model) for _ in range(len(model))]

    # Add the connections into the dist_matrix
    for hub_name in model:
        hub = model[hub_name]
        # Get the name and connections of the hub
        name = hub.get_name()
        connections = hub.get_connections()

        # Add each connection
        for key in connections:
            # From name -> key
            dist_matrix[name][key] = connections[key]

    return dist_matrix


def create_pher_matrix(dist_matrix: List[List[float]], p_min=0, p_max=1) -> List[List[float]]:
    """
    Params:
        dist_matrix - the corresponding distance matrix showing distances between nodes
        p_min - the minimum level of pheromone created - defaults to 0
        p_max - the maximum level of pheromone created - defaults to 1

    Returns:
        Pheremone matrix, with positions corresponding to dist_matrix
    """
    pher_matrix = []
    # For each vertex in the distance matrix
    for v in range(len(dist_matrix)):
        row = []
        # For each edge from that vertex
        for e in range(len(dist_matrix)):
            # If is an edge to itself, set pheremone to 0 so never selected
            if e == v:
                row.append(0)
                continue
            # Generate a random number between p_min and p_max and round to 2dp
            rand = round(random.uniform(p_min, p_max), 2)
            # Add to pheremone matrix
            row.append(rand)
        pher_matrix.append(row)

    return pher_matrix


def create_pher_matrix(dist_matrix: List[List[float]], p_min=0, p_max=1) -> List[List[float]]:
    """
    Params:
        dist_matrix - the corresponding distance matrix showing distances between hubs
        p_min - the minimum level of pheromone created - defaults to 0
        p_max - the maximum level of pheromone created - defaults to 1

    Returns:
        Pheremone matrix, with positions corresponding to dist_matrix
    """
    pher_matrix = []
    # For each vertex in the distance matrix
    for v in range(len(dist_matrix)):
        row = []
        # For each edge from that vertex
        for e in range(len(dist_matrix)):
            # If is an edge to itself, set pheremone to 0 so never selected
            if e == v:
                row.append(0)
                continue
            # Generate a random number between p_min and p_max and round to 2dp
            rand = round(random.uniform(p_min, p_max), 2)
            # Make sure pheromone value is never 0 so a joruney is never selected
            while rand == 0:
                rand = round(random.uniform(p_min, p_max), 2)
            # Add to pheremone matrix
            row.append(rand)
        pher_matrix.append(row)

    return pher_matrix
