"""
Generates a path for an ant
"""
from model.hub import Hub
from typing import List, Dict
from utils import fitness
import random


def perform_journey(sur_hub: Hub, def_hub: Hub, max_journey_size: int) -> List[int]:
    """
    Performs a jouurney of maximum quanitity from surplus to deficit hub

    params
        sur_hub - The surplus hub
        def_hub - The deficit hub
        max_journey_size - The maximum size of hourney allowed per journey

    returns
        List of any hub that have reach equilibrium as a result
    """
    # Calculate the movement size
    move_size = min(sur_hub.get_s(), abs(def_hub.get_s()), max_journey_size)

    # Perform the movement
    Hub.move_s(start=sur_hub, end=def_hub, s=move_size)

    # Check if any of the hubs have reach equilibrium
    equilibrium_hubs = []
    if sur_hub.get_s() == 0:
        equilibrium_hubs.append(sur_hub.get_name())

    if def_hub.get_s() == 0:
        equilibrium_hubs.append(def_hub.get_name())

    return equilibrium_hubs


def generate_path(sur_hubs: Dict[int, Hub], def_hubs: Dict[int, Hub],
                  d=List[List[float]], h=[List[List[float]]], p=List[List[float]]) -> (List[Dict[str, int]], float):
    """
    Generates a path from surplus to deficit hubs using distance and pheromone matrices

    params:
        sur_hubs - The surplus hubs in the model
        def_hubs - The deficit hubs in the model
        d - distance matrix
        h - heuristic matrix
        p - pheromone matrix

    returns 
        A tuple of (path list as [{from, to, s}], cost)
    """
    # Define alpha and beta
    # Alpha is the exponent used to scale the pheromone matrix
    alpha = 1
    # Beta is the exponent used to scale the heuristic matrix
    beta = 2

    # Calculate the total number of hubs
    network_size = len(sur_hubs) + len(def_hubs)

    # Calculate a random surplus hub to be in the first journey

    # Set the current surplus hub to be this random surplus hub

    # TODO think i Can remove
    # Create a set of hubs in equilibrium
    visited = set()
    # Add the start node to visited nodes
    visited.add(start_node)

    # Continue until all hub are in equilibrium
    while len(sur_hubs) != 0:
        # Create a list of the distances to neighbours of a hub
        neighbours = d[current_hub]

        opts = []
        cum_probs = []
        total_prob = 0
        hubs = []
        # Calculate transition probabilities
        # For each of the neighbours
        for i in range(len(neighbours)):
            # Check hub not in surplus
            if i in def_hubs or sur_hubs:  # TODO do I want this to be surplus hubs or just deficit hubs?
                # Calculate pher^alpha * heur^beta
                pher = p[current_node][i]
                heur = h[current_node][i]
                n = pher**alpha * heur**beta
                # Add n to the calculated options
                opts.append(n)
                hubs.append(i)
                # Keep track of the total probabilities
                total_prob += n

        # If there are no choices with any pheromone choose a random vertex next
        if total_prob == 0:
            rand = random.randint(0, len(nodes)-1)
            path.append(nodes[rand])
            visited.add(nodes[rand])
        else:
            # Calculate each of the cumulative probabilities for the options
            for opt in opts:
                # Check if probability is the first
                if len(cum_probs) > 0:
                    # Add the probabilities to a cumulative probabilities list
                    cum_probs.append((opt / total_prob)+cum_probs[-1])
                else:
                    cum_probs.append(opt / total_prob)
            # Use final value in cumulative probabilities as max to allow for floating point errors
            rand_choice = random.uniform(0, cum_probs[-1])
            # Loop through probabilities until find one that is higher than the random probability
            for i in range(len(cum_probs)):
                if cum_probs[i] > rand_choice:
                    # If node is selected add it to the path and visited set and add its cost
                    path.append(nodes[i])
                    # print(d[current_node][nodes[i]])
                    visited.add(nodes[i])
                    break
        current_node = path[-1]
    # Add the final node to complete the tour
    path.append(0)
    # Calculate path cost
    cost = get_path_cost(path, d)
    return path, cost
