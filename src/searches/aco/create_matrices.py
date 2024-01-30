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


def create_pher_matrix(model: Dict[int, Hub], dist_matrix: List[List[float]], p_min=0, p_max=1) -> List[List[float]]:
    """
    Params:
        model - The hubs in the model as a {name: Hub} dictionary
        dist_matrix - the corresponding distance matrix showing distances between nodes
        p_min - the minimum level of pheromone created - defaults to 0
        p_max - the maximum level of pheromone created - defaults to 1

    Returns:
        Pheremone matrix, with positions corresponding to dist_matrix
    """
    pher_matrix = []
    # For each hub in the distance matrix
    for start_hub in range(len(dist_matrix)):
        row = []

        # If the start_hub is in deficit, add 0 to every pheromone value (as nothing to move)
        if model[start_hub].get_s() < 0:
            pher_matrix.append([0] * len(dist_matrix))
            continue

        # For each edge from that surplus hub
        for e in range(len(dist_matrix)):
            # If is an edge to itself, set pheremone to 0 so never selected
            if e == start_hub:
                row.append(0)
                continue
            # Generate a random number between p_min and p_max and round to 2dp
            rand = round(random.uniform(p_min, p_max), 2)
            # Add to pheremone matrix
            row.append(rand)
        pher_matrix.append(row)

    return pher_matrix


def create_heur_matrix(dist_matrix: List[List[float]], Q=1) -> List[List[float]]:
    """
    Creates the heuristic matrix

    Params:
        dist_matrix - the corresponding distance matrix
        Q - the scaling factor for Q/distance, default = 1

    returns:
        Corresponding heuristic matrix to distance matrix
    """
    # Get the size of the disrance matrix
    size = len(dist_matrix)
    # Create the heuristic matrix using Q/distance for each edge
    heur_matrix = [[round(Q/dist_matrix[i][j], 4) if i != j else 0
                    for j in range(size)] for i in range(size)]
    return heur_matrix
