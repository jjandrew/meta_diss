"""
General utilities for use throughout the project
"""
from typing import Dict, List
import copy
from model.depot import Depot


def fitness(path: List[Dict[str, int]], model: Dict[int, Depot]) -> int:
    """
    Function for calculating fitness (distance) of a solution

    params:
        path - List of {from, to, s} dictionaries
        model - The depots in the solution

    returns
        Total distance of the solution
    """
    # Counter for total distance
    total_dist = 0

    # For each of the journeys
    for j in path:
        # Calculate the surplus depot in the journey
        surplus_dep: Depot = model[j['from']]

        # Get the distance to the deficit depot in the journey
        dist = surplus_dep.get_connections()[j['to']]

        # sum the distance with total distance
        total_dist += dist

    return total_dist


def is_resolved(model: Dict[int, Depot]) -> bool:
    """
    Returns whether or not a model is in equilibrium

    params:
        model - A list of depots representing the model

    Returns
        Boolean value representing whether model is in equilibrium
    """
    # If any of the depots are not in equilibrium, return false
    for dep in model:
        if model[dep].get_s() != 0:
            return False
    # If all depots in equiirbium, return true
    return True


def apply_path(path: List[Dict[str, int]], model: Dict[int, Depot]):
    """
    Applies a list of journeys to a model to get a new model state
    params
        path - A list of dictionaries of {from, to, s} to apply to the model
        model - A list of depots in original state
    """
    # For every journey
    for journey in path:
        # Get the depot objects the journey is going from and to
        deficit_dep = model[journey['from']]
        surplus_dep = model[journey['to']]
        # Move the correct quantitiy between the hubs
        Depot.move_s(start=deficit_dep, end=surplus_dep, s=journey['s'])


def is_complete(path: List[Dict[str, int]], original_model_state: Dict[int, Depot]) -> bool:
    """
    Checks whether a path leads to a model being in equilibrium

    params
        path - The path applied to the model
        original_model_state - The original state of the model the journeys are applied to

    returns
        Boolean of whether the model is in equilibrium after the journeys are applied
    """
    # Apply the journey to the model
    model_copy = copy.deepcopy(original_model_state)
    apply_path(path=path, model=model_copy)

    # Check whether model is in equilibrium
    return is_resolved(model=model_copy)
