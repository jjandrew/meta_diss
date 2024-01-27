"""
A brute force approach to solving the problem
"""
from typing import List, Dict
from classes.hub import Hub
from utils import reduce_model, fitness, apply_path, is_complete, improve_solution
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
    # TODO need to add improve solution

    # Create a copy of the original model state
    original_model_state = copy.deepcopy(model)

    # Reduce the model to get a list of guaranteed shortest journeys
    best_journeys = reduce_model(
        model=model, max_journey_size=max_journey_size)

    # Split hubs into surplus and deficit hubs
    surplus_hubs = [hub for hub in model if hub.get_s() > 0]
    deficit_hubs = [hub for hub in model if hub.get_s() < 0]

    # A list of the current best solution and its fitness
    best_solution = []
    best_solution_len = inf

    # A list of all current paths that are incomplete
    paths = []
    first = True
    # Repeat until no paths left
    while first or len(paths) != 0:

        # If it is the first iteration
        if first:
            # Make sure this only happens once, so change first to false
            first = False

            # Look for the next steps from each of the surplus nodes
            for sur_hub in surplus_hubs:
                # Get the next possible journeys from a surplus hub
                journeys = next_steps(
                    starting_hub=sur_hub, deficit_hubs=deficit_hubs, max_journey_size=max_journey_size)

                # Add each journey to paths
                for journey in journeys:
                    paths.append([journey])
            continue  # Only want to repeat once

        new_paths = []
        # For each of the paths
        for path in paths:
            # Create copy of original model state, with path applied
            model_in_state = copy.deepcopy(model)
            apply_path(model=model_in_state, path=path)

            # Split hubs into surplus and deficit hubs
            surplus_hubs = [hub for hub in model_in_state if hub.get_s() > 0]
            deficit_hubs = [hub for hub in model_in_state if hub.get_s() < 0]

            # store the next possible journeys
            next_js = []
            # for each surplus hub
            for sur_hub in surplus_hubs:

                # Generate all next journeys and add to next_js
                next_js.extend(next_steps(
                    starting_hub=sur_hub, deficit_hubs=deficit_hubs, max_journey_size=max_journey_size))

            # create len(next_js) copies of path and add each of the next trips to the end
            for j in next_js:
                new_path = copy.copy(path) + [j]
                new_paths.append(new_path)

        ########################### TODO WORKING TO HERE ##########################

        paths = []

        for path in new_paths:

            # Get the total path by adding to best journeys
            total_path = copy.copy(best_journeys) + path

            # Improve the solution (in the case it is beneficial to go surplus -> surplus)
            final_path = improve_solution(
                solution=total_path, model=original_model_state, max_journey_size=max_journey_size)

            # Calculate path fitness
            path_fitness = fitness(path=final_path, model=original_model_state)

            # If the path has a fitness worse (greater) than best_solution, remove from paths
            if path_fitness > best_solution_len:
                continue

            # If they are complete and better than best_solution, replace best_solution and remove from paths
            if is_complete(path=final_path, original_model_state=original_model_state):
                if (path_fitness < best_solution_len):
                    best_solution_len = path_fitness
                    best_solution = final_path

                # Path doesn't need to be checked again as it is complete
                continue

            # If not complete and a possible best solution append to paths
            paths.append(path)

    return best_solution
