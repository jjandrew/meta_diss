"""
Generates a path for an ant
"""
import random
import copy
from typing import List, Dict, Tuple
from model.depot import Depot


def perform_journey(sur_dep: Depot, def_dep: Depot, max_journey_size: int) -> Tuple[Dict[str, int], List[int]]:
    """
    Performs a jouurney of maximum quanitity from surplus depot to deficit depot

    params
        sur_dep - The surplus depot
        def_dep - The deficit depot
        max_journey_size - The maximum size of journey allowed

    returns
        Tuple of journey as {from, to, s} and List of depots that have reach equilibrium as a result
    """
    # Calculate the movement size as the minimum quantity to resolve a journey or breach maximum journey size
    move_size = min(sur_dep.get_s(), abs(def_dep.get_s()), max_journey_size)

    # Perform the movement
    Depot.move_s(start=sur_dep, end=def_dep, s=move_size)

    # Put the journey in a dictionary
    journey = {'from': sur_dep.get_name(), 'to': def_dep.get_name(),
               's': move_size}

    # Check if any of the depots have reach equilibrium
    equilibrium_deps = []
    if sur_dep.get_s() == 0:
        equilibrium_deps.append(sur_dep.get_name())

    if def_dep.get_s() == 0:
        equilibrium_deps.append(def_dep.get_name())

    return journey, equilibrium_deps


def generate_path(sur_deps: Dict[int, Depot], def_deps: Dict[int, Depot],
                  d: List[List[float]], h: List[List[float]], p: List[List[float]], max_journey_size: int,
                  alpha=1, beta=2) -> List[Dict[str, int]]:
    """
    Generates a path from surplus to deficit depots using distance and pheromone matrices

    params:
        sur_deps - The surplus depots in the model
        def_deps - The deficit depots in the model
        d - distance matrix
        h - heuristic matrix
        p - pheromone matrix
        max_journey_size - Maximum journey size
        alpha - The exponent used to scale the pheromone matrix (default=1)
        beta - The exponent used to scale the heuristic matrix (default=2)

    returns 
        Path as list of journeys as dictionaries {from, to, s}
    """
    # Make copies of the surplus and deficit depots so the rest of the algorithm isn't affected
    sur_deps = copy.deepcopy(sur_deps)
    def_deps = copy.deepcopy(def_deps)

    # Store the path
    path = []

    # Continue until all depots are in equilibrium
    while len(sur_deps) != 0:
        # Pick the current depot as a random surplus depot
        current_dep = random.choice(list(sur_deps.keys()))

        # Store the transition probabilities, and total probabilities
        probs = []
        total_prob = 0
        # Store the corresponding depot to each of the probabilities
        deps = []

        # For each of the neighbours to the surplus depot
        for i in range(len(d[current_dep])):
            # Check neighbour is a deficit depot that still to be resolved
            if i in def_deps:
                # Calculate pher^alpha * heur^beta
                pher = p[current_dep][i]
                heur = h[current_dep][i]
                n = pher**alpha * heur**beta
                # Add n to the transition probabilities
                probs.append(n)

                # Keen track of the total probabilities
                total_prob += n

                # Store the corresponding depot to the probability
                deps.append(i)

        # If there are no choices with any pheromone (due to over-evaporation) choose a random deficit depot next
        if total_prob == 0:
            # Pick a random deficit depot
            rand_def_dep = random.choice(list(def_deps.keys()))
            # Perform a journey to the random deficit depot
            journey, resolved_deps = perform_journey(
                sur_dep=sur_deps[current_dep], def_dep=def_deps[rand_def_dep], max_journey_size=max_journey_size)
            # Remove any resolved depots from their associated dictionaries
            for r_dep in resolved_deps:
                if r_dep in sur_deps:
                    del sur_deps[r_dep]
                else:
                    del def_deps[r_dep]

            # Add the journey to the path
            path.append(journey)

        else:  # If there was pheromone present
            # Calculate the cumulative probabilities
            cum_probs = []
            for prob in probs:
                # Check if probability is the first
                if len(cum_probs) > 0:  # If it is not then
                    # Add the probabilities to a cumulative probabilities list
                    cum_probs.append((prob / total_prob)+cum_probs[-1])
                else:  # If it is
                    # Add the probability / the total probability
                    cum_probs.append(prob / total_prob)

            # Use final value in cumulative probabilities as max to allow for floating point errors
            # Select a random number between 0 and 1
            rand_choice = random.uniform(0, cum_probs[-1])
            # Loop through probabilities until find one that is higher than the random probability
            for i in range(len(cum_probs)):
                if cum_probs[i] > rand_choice:
                    # If depot is selected perform journey from the surplus depot to it
                    journey, resolved_deps = perform_journey(
                        sur_dep=sur_deps[current_dep], def_dep=def_deps[deps[i]],
                        max_journey_size=max_journey_size)
                    # Remove the resolved depots from their associated dictionaries
                    for r_dep in resolved_deps:
                        if r_dep in sur_deps:
                            del sur_deps[r_dep]
                        else:
                            del def_deps[r_dep]

                    # Add the journey to the path
                    path.append(journey)

                    # Break to avoid unnecessary computation
                    break

    return path
