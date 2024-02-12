"""
Funcgtions for the fixing algorithm to make it cleaner
"""
from typing import Set, Tuple, Dict, List
from model.hub import Hub


def get_sur_and_def_hubs(model: Dict[int, Hub]) -> Tuple[Set[int], Set[int]]:
    """
    Returns the names of the surplus and deificit hubs in a model as two sets

    params
        model - A dictionary of hub name: hub object

    returns
        surplus_names, deficit_names
    """
    # Obtain a list of unbalanced surplus and deficit hubs
    surplus_hubs = set()
    deficit_hubs = set()
    # For each hub_name key
    for hub_name in model:
        # If it is in deficit (s < 0) then add to deficit hubs
        if model[hub_name].get_s() < 0:
            deficit_hubs.add(hub_name)
        # If in surplus (s > 0) then add to surplus hubs
        elif model[hub_name].get_s() > 0:
            surplus_hubs.add(hub_name)

    return surplus_hubs, deficit_hubs


def get_sur_and_def_journeys(path=List[Tuple[int, int, int]]) -> Tuple[Dict[int, List[int]], Dict[int, List[int]]]:
    """
    Returns two dictionaries showing indexes of journeys from and to certain hubs

    params
        path - The path as a list of journeys of the form (from, to, s)

    returns
        surplus, defict journeys in form {hub_name: index}
    """
    # Dictionaries for surplus and deficit journeys
    sur_js = {}
    def_js = {}

    # Loop through all the journeys in the path
    for idx in range(len(path)):
        # Surplus hub always in first position of the tuple
        sur_hub = path[idx][0]
        # Deficit hub always in position 1 of tuple
        def_hub = path[idx][1]

        # Assign indexes to the surplus and deficit dicts
        # Check if there is already an entry in dictionary
        if sur_hub in sur_js:  # if there is
            # add idx to array
            sur_js[sur_hub].append(idx)
        else:  # otherwise
            # Create a new array
            sur_js[sur_hub] = [idx]

        # if entry in deficit journeys
        if def_hub in def_js:
            # Append index onto array
            def_js[def_hub].append(idx)
        else:
            # Create a new array
            def_js[def_hub] = [idx]

    return sur_js, def_js
