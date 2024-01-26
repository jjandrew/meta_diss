"""
A brute force approach to solving the problem
"""
from typing import List, Dict
from classes.hub import Hub
from utils import reduce_model, calc_distance, improve_solution, is_resolved
from math import inf
import copy


def next_steps(starting_hub: Hub, deficit_hubs: List[Hub], max_journey_size: int) -> List[Dict[str, int]]:
    """
    Find all possible routes from a surplus hub to deficit hubs

    params:
        starting_hub - The surplus hub to look at next journeys from
        deficit_hubs - A list of all of the deficit hubs
        max_journey_size - The maximum quanitity that can be moved per journey

    Returns
        List of dictionaries of {from, to, s} of each journey
    """
    # A list of the journeys
    journeys = []

    # Go through each of the deficit hubs
    for def_hub in deficit_hubs:
        # Check deficit hub isn't resolved
        if def_hub.get_s() == 0:  # If it is
            continue  # Ignore it

        # Pick a quantity to move between 1 and minimum of max_journey_size, surplus_hub s and deficit hub s
        for s in range(1, min(max_journey_size, starting_hub.get_s(), abs(def_hub.get_s())) + 1):
            # Add the journey to next possible journeys
            journeys.append({
                'from': starting_hub.get_name(),
                'to': def_hub.get_name(),
                's': s
            })

    return journeys


def brute(model: List[Hub], max_journey_size: int) -> List[Dict[str, int]]:
    """
    Performs a brute force search on the model that is passed in

    params:
        model - a list of hubs which have a supply value to be solved
        max_journey_size - The maximum number of goods that can be moved between hubs

    returns
        List[{from, to, s}]
    """
    # Reduce the model to get a list of guaranteed shortest journeys
    journeys = reduce_model(model=model, max_journey_size=max_journey_size)

    # Now perform brute force on the rest of the model

    # Split hubs into surplus and deficit hubs
    surplus_hubs = [hub for hub in model if hub.get_s() > 0]
    deficit_hubs = [hub for hub in model if hub.get_s() < 0]

    paths = []
    # For each surplus hub
    for starting_hub in surplus_hubs:
        # Get all possible jouneys from the starting hub
        # To do this look at all of the deficit hubs
        print()

    hubs_to_resolve: List[Hub] = copy.copy(model)

    #########################################################################################################

    # Initialize variables to track the best solution
    best_sequence = None
    min_distance = inf

    # Check all permutations
    for path in paths:
        improved_path = improve_solution(solution=path, model=model,
                                         max_journey_size=max_journey_size)
        print(improved_path)
        fitness = calc_distance(path=improved_path, model=model)

        # Check if the current sequence is better than the current best
        if fitness < min_distance:
            min_distance = fitness
            best_sequence = improved_path

    return best_sequence
