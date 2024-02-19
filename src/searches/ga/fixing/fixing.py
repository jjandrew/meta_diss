"""
Performs a fixing algorithm on a solution to make sure it is valid
"""
from typing import List, Dict, Set, Tuple
from model.hub import Hub
from utils import apply_path, is_resolved
from searches.ga.population import decode_solution
from searches.ga.fixing.fixing_utils import get_sur_and_def_hubs, get_sur_and_def_journeys
from searches.ga.fixing.fix import macro_fixing, micro_fixing


def fix(path: List[Tuple[int, int, int]], model: Dict[int, Hub], max_journey_size=20):
    """
    Fixes the given path by making any necessary adjustments in order to 
    ensure that all deficits are resolved.

    params
        path - A list of tuples representing connections between hubs (from, to, s)
        model - The model in its original state, showing hub surplus and deficits
        max_journey_size - The maximum allowed size of a journey

    returns
        The valid path
    """
    # Decode the genome into {from, to, s} dictionary
    decoded_path = decode_solution(path=path)

    # Calculate the hubs originally in surplus or deficit
    original_sur_hubs, original_def_hubs = get_sur_and_def_hubs(
        model=model)

    # Apply the path to get the new model state
    apply_path(path=decoded_path, model=model)

    # Calculate the hubs now in surplus or deificit
    new_sur_hubs, new_def_hubs = get_sur_and_def_hubs(model=model)

    # In the case that all hubs are resolved, return the original path
    if len(new_sur_hubs) + len(new_def_hubs) == 0:
        return

    # Calculate the position of the journeys of all hubs
    sur_j_positions, def_j_positions = get_sur_and_def_journeys(path=path)

    # Calculate the surplus hubs that have been overesolved surplus -> deficit
    over_res_sur = original_sur_hubs.intersection(new_def_hubs)

    # Calculate the hubs that have been underesolved surplus -> surplus
    under_res_sur = original_sur_hubs.intersection(new_sur_hubs)

    # Fix model
    macro_fixing(over_res_hubs=list(over_res_sur), under_res_hubs=list(
        under_res_sur), path=path, sur_js=sur_j_positions, model=model)

    # Calculate the hubs now in surplus or deificit
    new_sur_hubs, new_def_hubs = get_sur_and_def_hubs(model=model)

    # In the case that all hubs are resolved, return the original path
    if len(new_sur_hubs) + len(new_def_hubs) == 0:
        return

    # Calculate the position of the journeys of all hubs
    sur_j_positions, def_j_positions = get_sur_and_def_journeys(path=path)

    # Calculate the surplus hubs that have been overesolved surplus -> deficit
    over_res_sur = original_sur_hubs.intersection(new_def_hubs)

    # Calculate the hubs that have been underesolved surplus -> surplus
    under_res_sur = original_sur_hubs.intersection(new_sur_hubs)

    # Fix model
    micro_fixing(over_res_hubs=list(over_res_sur), under_res_hubs=list(
        under_res_sur), path=path, sur_js=sur_j_positions, def_js=def_j_positions, model=model, max_journey_size=max_journey_size)

    return path
