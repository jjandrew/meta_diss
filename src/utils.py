"""
General utilities for use throughout the project
"""
from typing import Dict, List
from src.classes.hub import Hub


def calc_distance(path: List[Dict[str, int]], hubs: List[Hub]) -> int:
    """
    Function for calculating fitness (distance) of a solution

    params:
        path - List of {from, to, s} dictionaries
        hubs - The hubs in the solution

    returns
        Total distance of the solution
    """
    # Convert list of hubs into a dictionary to make it easier (and faster) to search
    hub_dict = {}
    for hub in hubs:
        hub_dict[hub.get_name()] = hub

    # Counter for total distance
    total_dist = 0

    # For each of the journeys
    for j in path:
        # Assign hub1 to the relative hubs in the model
        hub1: Hub = hub_dict[j['from']]

        # Get the distance to the 'to' hub in the journey
        dist = hub1.get_connections()[j['to']]

        # sum the distance with total distance
        total_dist += dist

    return total_dist


def get_closest_hub(hub: Hub, model: List[Hub]) -> Hub:
    """
    Get the closest connection to a hub

    params
        hub - Hub to find closest connection

    returns
        closest Hub
    """
    # Get the connections to a hub
    connections = hub.get_connections()
    # Get the name of the hub with the minimum connection
    closest_hub_name = min(connections, key=connections.get)
    # Get the object for the closest hub
    closest_hub = next(
        (hub for hub in model if hub.get_name() == closest_hub_name), None)

    return closest_hub


def reduce_model(model: List[Hub], max_journey_size: int) -> List[Dict[str, int]]:
    """
    Reduces the model by adding journeys that must be in a best solution

    params:
        model - a list of hubs which have a supply value to be solved
        max_journey_size - The maximum number of goods that can be moved between hubs

    returns
        List[{from, to, s}]
    """
    journeys = []

    # For each hub in the model
    for hub in model:
        # Get the direction of the hub
        hub_surplus = True
        if hub.get_s() < 0:
            hub_surplus = False

        # Get the closest connected hub
        closest_hub = get_closest_hub(hub=hub, model=model)

        closest_hub_surplus = True
        if closest_hub.get_s() < 0:
            closest_hub_surplus = False

        # If hubs are in the opposite directions and they are both each others shortest journey
        if (hub_surplus ^ closest_hub_surplus) and (hub == get_closest_hub(hub=closest_hub, model=model)):
            # Then this is best journey
            # Perform journeys until one of the hubs is resolved
            while hub.get_s() != 0 and closest_hub.get_s() != 0:
                if hub_surplus:
                    # Quantity to move is minimum of max_journey_size and remaining deficits / surplus of two hubs
                    quantity = min(max_journey_size, hub.get_s(),
                                   abs(closest_hub.get_s()))
                    Hub.move_s(start=hub, end=closest_hub, s=quantity)
                    # Add journey to journeys
                    journeys.append(
                        {'from': hub.get_name(), 'to': closest_hub.get_name(), 's': quantity})
                else:
                    # Quantity to move is minimum of max_journey_size and remaining deficits / surplus of two hubs
                    quantity = min(max_journey_size, abs(
                        hub.get_s()), closest_hub.get_s())
                    Hub.move_s(start=closest_hub, end=hub, s=quantity)
                    # Add journey to journeys
                    journeys.append(
                        {'from': closest_hub.get_name(), 'to': hub.get_name(), 's': quantity})

    return journeys
