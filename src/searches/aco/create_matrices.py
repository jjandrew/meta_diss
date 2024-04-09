"""
Creates distance and pheromone matrices for the problem
"""
import random
from typing import List, Dict
from TNRP_model.depot import Depot


def create_dist_matrix(model: Dict[int, Depot]) -> List[List[float]]:
    """
    Creates the distance matrix from the model passed in

    Params
        model - The TNRP model as a dictionary of depot name: DepotObj

    Returns:
        List where dist_matrix[i][j] is the distance on edge i-j
    """

    # Create a distance matrix with all values equalling 0 and of length and width len(model)
    dist_matrix = [[0] * len(model) for _ in range(len(model))]

    # Add the connections into the dist_matrix
    for dep_name in model:
        dep = model[dep_name]
        # Get the name and connections of the dept
        name = dep.get_name()
        connections = dep.get_connections()

        # Add each connection to its corresponding position
        for key in connections:
            # From name -> key
            dist_matrix[name][key] = connections[key]

    return dist_matrix


def create_pher_matrix(model: Dict[int, Depot], dist_matrix: List[List[float]], p_min=0, p_max=1) -> List[List[float]]:
    """
    Params:
        model - The depots in the model as a {name: DepotObj} dictionary
        dist_matrix - the corresponding distance matrix showing distances between depots
        p_min - the minimum level of pheromone created - defaults to 0
        p_max - the maximum level of pheromone created - defaults to 1

    Returns:
        Pheremone matrix, with positions the same as the dist_matrix
    """
    pher_matrix = []
    # For each depot in the distance matrix
    for start_dep in range(len(dist_matrix)):
        row = []

        # If the start_dep is in deficit, add 0 to every pheromone value (as nothing to move)
        if model[start_dep].get_s() < 0:
            pher_matrix.append([0] * len(dist_matrix))
            # Continue to the next depot
            continue

        # For each edge from that surplus depot
        for edge in range(len(dist_matrix)):
            # If is an edge to itself, set pheremone to 0 so never selected
            if edge == start_dep:
                row.append(0)
                continue
            # Generate a random number between p_min and p_max and round to 2dp
            rand = round(random.uniform(p_min, p_max), 2)
            # Add to pheremone matrix
            row.append(rand)
        pher_matrix.append(row)

    return pher_matrix


def create_heur_matrix(dist_matrix: List[List[float]]) -> List[List[float]]:
    """
    Creates the heuristic matrix

    Params:
        dist_matrix - the corresponding distance matrix

    returns:
        A heuristic matrix containing inverse values to the distance matrix
    """
    # Get the size of the distance matrix
    size = len(dist_matrix)

    # Create the heuristic matrix using 1/distance for each edge
    heur_matrix = [[round(1/dist_matrix[i][j], 4) if i != j else 0
                    for j in range(size)] for i in range(size)]

    return heur_matrix
