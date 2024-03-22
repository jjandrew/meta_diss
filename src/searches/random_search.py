"""
Creates a random solution to the model passed in
"""
import random
from typing import List, Dict, Tuple
from model.depot import Depot


def perform_journey(sur_dep: Depot, def_dep: Depot,
                    max_journey_size: int) -> Tuple[Dict[str, int], List[int]]:
    """
    Performs a journey of maximum quanitity from surplus depot to deficit depot

    params
        sur_dep - The surplus depot
        def_dep - The deficit depot
        max_journey_size - The maximum size of hourney allowed per journey

    returns
        Tuple of journey as {from, to, s} and List of any depots that have reach equilibrium as a result
    """
    # Calculate the move size as the minimum to either resolve a depot or reach the max journey size
    move_size = min(sur_dep.get_s(), abs(def_dep.get_s()), max_journey_size)

    # Update the depot objects for the movement
    Depot.move_s(start=sur_dep, end=def_dep, s=move_size)

    # Put the journey in a dictionary
    journey = {'from': sur_dep.get_name(), 'to': def_dep.get_name(),
               's': move_size}

    # Check if any of the depots have reached equilibrium
    equilibrium_deps = []
    if sur_dep.get_s() == 0:
        equilibrium_deps.append(sur_dep.get_name())

    if def_dep.get_s() == 0:
        equilibrium_deps.append(def_dep.get_name())

    return journey, equilibrium_deps


def random_search(model: Dict[int, Depot], max_journey_size: int) -> List[Dict[str, int]]:
    """
    Performs a random search on the model that is passed in

    params:
        model - the TNRP as a dictionary of depot name: Depot object
        max_journey_size - The maximum number of goods that can be moved between depots

    returns
        List of journeys of form [{from, to, s}]
    """
    path = []

    # Split depots into surplus and deficit depots
    sur_deps = {dep: model[dep] for dep in model if model[dep].get_s() > 0}
    def_deps = {dep: model[dep] for dep in model if model[dep].get_s() < 0}

    # Repeat until no more surplus depots left
    while len(sur_deps) > 0:
        # Pick a random surplus depot
        sur_dep = random.choice(list(sur_deps.keys()))
        # Pick a random deficit depot
        def_dep = random.choice(list(def_deps.keys()))

        # Perform the journey from surplus to deficit depot
        journey, resolved_deps = perform_journey(
            sur_dep=sur_deps[sur_dep], def_dep=def_deps[def_dep], max_journey_size=max_journey_size)

        # Add the journey to the solution
        path.append(journey)

        # Remove any resolved depots from the sets
        for r_dep in resolved_deps:
            if r_dep in sur_deps:
                del sur_deps[r_dep]
            else:
                del def_deps[r_dep]

    return path
