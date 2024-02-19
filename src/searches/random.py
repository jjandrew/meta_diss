"""
Creates a random solution to the model passed in
"""
from typing import List, Dict
from model.hub import Hub
from utils import is_resolved
import random
import copy


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


def random_search(model: Dict[int, Hub], max_journey_size: int) -> List[Dict[str, int]]:
    """
    Performs a random search on the model that is passed in

    params:
        model - a dictionary of hub name: hub objectio of hubs which have a supply value to be solved
        max_journey_size - The maximum number of goods that can be moved between hubs

    returns
        List of journeys of form [{from, to, s}]
    """
    path = []

    # Split hubs into surplus and deficit hubs
    sur_hubs = {hub: model[hub] for hub in model if model[hub].get_s() > 0}
    def_hubs = {hub: model[hub] for hub in model if model[hub].get_s() < 0}

    # Repeat until no more surplus hubs left
    while len(sur_hubs) > 0:
        # Pick a random surplus hub
        sur_hub = random.choice(list(sur_hubs.keys()))
        # Pick a random deficit hub
        def_hub = random.choice(list(def_hubs.keys()))

        # Perform the journey from surplus to deficit hub
        journey, resolved_hubs = perform_journey(
            sur_hub=sur_hubs[sur_hub], def_hub=def_hubs[def_hub], max_journey_size=max_journey_size)

        # Add the journey
        path.append(journey)

        # Remove any resolved hubs
        for r_hub in resolved_hubs:
            if r_hub in sur_hubs:
                del sur_hubs[r_hub]
            else:
                del def_hubs[r_hub]

    return path
