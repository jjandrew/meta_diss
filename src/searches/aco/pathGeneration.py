"""
Generates a path for an ant
"""
from model.hub import Hub
from typing import List, Dict
from utils import fitness
import random


def perform_journey(sur_hub: Hub, def_hub: Hub, max_journey_size: int) -> (Dict[str, int], List[int]):
    """
    Performs a jouurney of maximum quanitity from surplus to deficit hub

    params
        sur_hub - The surplus hub
        def_hub - The deficit hub
        max_journey_size - The maximum size of hourney allowed per journey

    returns
        Tuple of journey as {from, to, s} and List of any hub that have reach equilibrium as a result
    """
    # Calculate the movement size
    move_size = min(sur_hub.get_s(), abs(def_hub.get_s()), max_journey_size)

    # Perform the movement
    Hub.move_s(start=sur_hub, end=def_hub, s=move_size)

    # Put the journey in a dictionary
    journey = {'from': sur_hub.get_name(), 'to': def_hub.get_name(),
               's': move_size}

    # Check if any of the hubs have reach equilibrium
    equilibrium_hubs = []
    if sur_hub.get_s() == 0:
        equilibrium_hubs.append(sur_hub.get_name())

    if def_hub.get_s() == 0:
        equilibrium_hubs.append(def_hub.get_name())

    return journey, equilibrium_hubs


def generate_path(sur_hubs: Dict[int, Hub], def_hubs: Dict[int, Hub],
                  d: List[List[float]], h: List[List[float]], p: List[List[float]], max_journey_size: int) -> List[Dict[str, int]]:
    """
    Generates a path from surplus to deficit hubs using distance and pheromone matrices

    params:
        sur_hubs - The surplus hubs in the model
        def_hubs - The deficit hubs in the model
        d - distance matrix
        h - heuristic matrix
        p - pheromone matrix
        max_journey_size - Maximum journey size

    returns 
        Path as list of journeys as dictionaries {from, to, s}
    """
    # Define alpha and beta
    # Alpha is the exponent used to scale the pheromone matrix
    alpha = 1
    # Beta is the exponent used to scale the heuristic matrix
    beta = 2

    # Store the path
    path = []

    # Continue until all hub are in equilibrium
    while len(sur_hubs) != 0:
        # Pick the current hub as a random surplus hub
        current_hub = random.choice(list(sur_hubs.keys()))

        # Create a list of the distances to neighbours of a hub
        neighbours = d[current_hub]

        opts = []
        hubs = []
        total_prob = 0
        # Calculate transition probabilities
        # For each of the neighbours
        for i in range(len(neighbours)):
            # Check hub still to be resolved
            if i in def_hubs and i in sur_hubs:  # TODO do I want this to be surplus hubs or just deficit hubs?
                # Calculate pher^alpha * heur^beta
                pher = p[current_hub][i]
                heur = h[current_hub][i]
                n = pher**alpha * heur**beta
                # Add n to the calculated options
                opts.append(n)

                # Add name of hub to hubs
                hubs.append(i)

                # Keen track of the total probabilities
                total_prob += n

        # If there are no choices with any pheromone choose a random deficit hub next
        if total_prob == 0:
            # Pick a random deficit hub
            rand_def_hub = random.choice(list(def_hubs.keys()))
            # Perform a journey to the random deficit hub
            journey, resolved_hubs = perform_journey(
                sur_hub=sur_hubs[current_hub], def_hub=def_hubs[rand_def_hub], max_journey_size=max_journey_size)
            # Remove any resolved hubs from their associated dictionaries
            for r_hub in resolved_hubs:
                if r_hub in sur_hubs:
                    del sur_hubs[r_hub]
                else:
                    del def_hubs[r_hub]

            # Add the journey to the path
            path.append(journey)

        else:
            # Store cumulative probabilities
            cum_probs = []
            # Calculate each of the cumulative probabilities for the options
            for opt in opts:
                # Check if probability is the first
                if len(cum_probs) > 0:
                    # Add the probabilities to a cumulative probabilities list
                    cum_probs.append((opt / total_prob)+cum_probs[-1])
                else:
                    cum_probs.append(opt / total_prob)
            # Use final value in cumulative probabilities as max to allow for floating point errors
            # Select a random probability to select
            rand_choice = random.uniform(0, cum_probs[-1])
            # Loop through probabilities until find one that is higher than the random probability
            for i in range(len(cum_probs)):
                if cum_probs[i] > rand_choice:
                    # If node is selected perform journey with it
                    journey, resolved_hubs = perform_journey(
                        sur_hub=sur_hubs[current_hub], def_hub=def_hubs[hubs[i]], max_journey_size=max_journey_size)
                    # Remove the resolved hubs from their associated dictionaries
                    for r_hub in resolved_hubs:
                        if r_hub in sur_hubs:
                            del sur_hubs[r_hub]
                        else:
                            del def_hubs[r_hub]

                    # Add the journey to the path
                    path.append(journey)

                    # Break to avoid unnecessary computation
                    break

    return path
