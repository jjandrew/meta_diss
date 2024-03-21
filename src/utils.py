"""
General utilities for use throughout the project
"""
from typing import Dict, List
from model.depot import Depot
from math import inf
import copy


def fitness(path: List[Dict[str, int]], model: Dict[int, Depot]) -> int:
    """
    Function for calculating fitness (distance) of a solution

    params:
        path - List of {from, to, s} dictionaries
        model - The hubs in the solution

    returns
        Total distance of the solution
    """

    # Counter for total distance
    total_dist = 0

    # For each of the journeys
    for j in path:
        # Assign hub1 to the relative hubs in the model
        hub1: Depot = model[j['from']]

        # Get the distance to the 'to' hub in the journey
        dist = hub1.get_connections()[j['to']]

        # sum the distance with total distance
        total_dist += dist

    return total_dist


def is_resolved(model: Dict[int, Depot]) -> bool:
    """
    Returns whether or not a model is in equilibrium
    params:
        model - A list of hubs representing the model

    Returns
        Boolean value representing whether model is in equilibrium
    """
    # If any of the hubs are not in equilibrium, return false
    for hub in model:
        if model[hub].get_s() != 0:
            return False
    # If all hubs in equiirbium, return true
    return True


def get_closest_hub(hub: Depot, model: Dict[int, Depot]) -> Depot:
    """
    Get the closest connection to a hub

    params
        hub - Hub to find closest connection

    returns
        closest Hub
    """
    # Get the connections to a hub
    connections = hub.get_connections()

    # Check there are connections
    if not connections:
        print("No connection present")
        return None

    # Get the name of the hub with the minimum connection
    closest_hub_name = min(connections, key=connections.get)
    # Get the object for the closest hub
    closest_hub = next(
        (model[hub] for hub in model if model[hub].get_name() == closest_hub_name), None)

    return closest_hub


def reduce_model(model: Dict[int, Depot], max_journey_size: int) -> List[Dict[str, int]]:
    """
    Reduces the model by adding journeys that must be in a best solution

    params:
        model - a dictionary of hubs which have a supply value to be solved
        max_journey_size - The maximum number of goods that can be moved between hubs

    returns
        List[{from, to, s}]
    """
    journeys = []

    # For each hub in the model
    for hub_name in model:
        hub = model[hub_name]
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
                    Depot.move_s(start=hub, end=closest_hub, s=quantity)
                    # Add journey to journeys
                    journeys.append(
                        {'from': hub.get_name(), 'to': closest_hub.get_name(), 's': quantity})
                else:
                    # Quantity to move is minimum of max_journey_size and remaining deficits / surplus of two hubs
                    quantity = min(max_journey_size, abs(
                        hub.get_s()), closest_hub.get_s())
                    Depot.move_s(start=closest_hub, end=hub, s=quantity)
                    # Add journey to journeys
                    journeys.append(
                        {'from': closest_hub.get_name(), 'to': hub.get_name(), 's': quantity})

    return journeys


def improve_solution(solution: List[Dict[str, int]], model: Dict[int, Depot], max_journey_size: int) -> List[Dict[str, int]]:
    """
    Improves the final solution in the scenario that the fitness can be improved by a journey adding more s to a surplus hub

    params:
        solution - The previous best solution in form List[{'from', 'to', 's'}]
        model - A list of Hub objects representing the model

    returns
        New best solution in shortest form
    """
    # temp_storage of additional surplus to move
    additional_surplus = {}

    final_solution = []
    # Get a list of all journeys shorter than max_journey_size
    shorter_journeys = []
    for journey in solution:
        if journey['s'] < max_journey_size:
            shorter_journeys.append(journey)
        else:
            final_solution.append(journey)

    # Group them by hubs they are going to
    grouped_shorter_journeys = {}
    for journey in shorter_journeys:
        # deficit node already exists in dictionary
        if journey['to'] in grouped_shorter_journeys:
            grouped_shorter_journeys[journey['to']].append(journey)
        else:  # deficit node not in dictionary
            grouped_shorter_journeys[journey['to']] = [journey]

    # For each of the deficit nodes (Z)
    for def_node in grouped_shorter_journeys.keys():
        # Get a value for the Z_hub and its connections
        Z_hub = model[def_node]
        Z_connections = Z_hub.get_connections()
        # print()
        # print()
        # print(f'Deficit node: {def_node}')

        # For hub (A) in hubs from furthest to closest to final node (Z)

        ordered_journeys = sorted(
            grouped_shorter_journeys[def_node], key=lambda x: Z_connections[x['from']], reverse=True)

        # print(ordered_journeys)

        for journey_index in range(len(ordered_journeys)):
            journey = ordered_journeys[journey_index]
            # print()
            # print(
            #     f'Journey looking at from: {journey["from"]}, index = {journey_index}')

            # check how much needs to be moved = additional_surplus[A] + journey[s] (Q)
            to_move = -1
            # Check if A in additional surplus
            # if there has been a move to A previously
            if journey['from'] in additional_surplus:
                # Add this to the quantity to move
                to_move = additional_surplus[journey['from']] + journey['s']
            else:  # If not
                # Just need to move the quantity of the journey
                to_move = journey['s']

            # TODO haven't found test w surplus

            # print(f'Needs to move {to_move}')

            # Check to_move has been calculated correctly
            if to_move < 0:
                raise ValueError("Incorrect calculation of quantity to move")

            # while Q >= max_journey size then perform move of max journey size from A to Z
            while to_move >= max_journey_size:
                # print("To move exceeds journey size")
                final_solution.append(
                    {"from": journey["from"], "to": def_node, "s": max_journey_size})
                # Remove quantity from to move and reset surplus of node
                to_move -= max_journey_size
                additional_surplus[journey['from']] = 0
                # print(f'To move now at {to_move}')

            # If to_move is 0 then next journey
            if to_move == 0:
                continue

            # Look for the nearest hub to A that is in ordered journeys and is closer to Z (B)
            final_closest: Depot = None
            dist_from_A = inf
            # Get the hub objects for A and Z
            A_hub = model[journey['from']]
            A_connections = A_hub.get_connections()

            # TODO fairly sure working to here

            # Loop through all journeys to Z that are from a hub that is closer to Z (B)
            for j_index in range(journey_index + 1, len(ordered_journeys)):
                j = ordered_journeys[j_index]
                # Get hub object for B
                B_hub = model[j['from']]
                # print(f'B = {B_hub.get_name()}, index = {j_index}')

                # Make sure B and A hubs are not the same
                if B_hub == A_hub:
                    continue

                # Check B closer to A than Z
                is_closer_to_A = A_connections[B_hub.get_name(
                )] < A_connections[Z_hub.get_name()]

                # Check if this hub would be the new closest to B
                is_new_closest = A_connections[B_hub.get_name()] < dist_from_A

                # If it is both of these things then set the new_closest values
                if is_closer_to_A and is_new_closest:
                    final_closest = B_hub
                    dist_from_A = A_connections[B_hub.get_name()]

            # If no beneficial journey found
            if final_closest is None:
                # Keep journey in final solution and pick next journey
                # print('No beneficial journey found, keep current one')
                journey_to_add = {
                    'from': journey['from'], 'to': journey['to'], 's': to_move}
                # print(f'Added - {journey_to_add}')
                final_solution.append(journey_to_add)
                continue

            # print(f'Looking at new closest - {final_closest.get_name()}')

            # Else add journey moving all (s) from A to B
            final_solution.append(
                {'from': A_hub.get_name(), 'to': final_closest.get_name(), 's': to_move})
            # print(f'Added jouirney: {final_solution[-1]}')
            # Add additional surplus for B
            # Check if final_closest already in the additional surplus dictionary
            if final_closest.get_name() in additional_surplus:
                additional_surplus[final_closest.get_name()] += to_move
            else:
                additional_surplus[final_closest.get_name()] = to_move

            # print(
            #     f'Additional surplus of {final_closest.get_name()} is {additional_surplus[final_closest.get_name()]}')

    return final_solution


def apply_path(path: List[Dict[str, int]], model: Dict[int, Depot]):
    """
    Applies a list of journeys to a model to get a new model state

    params
        path - A list of dictionaries of {from, to, s} to apply to the model
        model - A list of hubs in original state
    """
    # For every journey
    for journey in path:
        # Get the hub objects the journey is going from and to
        from_hub = model[journey['from']]
        to_hub = model[journey['to']]

        # Move the correct quantitiy between the hubs
        Depot.move_s(start=from_hub, end=to_hub, s=journey['s'])


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
