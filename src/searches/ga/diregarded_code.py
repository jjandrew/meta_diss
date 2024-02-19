from typing import List, Tuple, Dict
from model.hub import Hub
import random


def uniform(parent_1: List[Tuple[int, int, int]], parent_2: List[Tuple[int, int, int]]) -> Tuple[List[Tuple[int, int, int]], List[Tuple[int, int, int]]]:
    """
    Performs a uniform crossover on two parents. 
    This means that each gene in the child will be randomly taken from either parent using a coin toss.
    Genes being chosen are which parent the trips to a deficit node are used.

    params
        parent_1 - The first parent solution
        parent_2 - The second parent solution

    Returns
        Two children which have inherited alternative characteristics from each parent
    """
    # Create a dictionary of deficit nodes and corresponding journeys
    parent_1_def_nodes = {}
    # For each journey in parent 1
    for j in parent_1:
        # Deficit node is always in middle position
        def_node = j[1]

        # If def_node in parent_1_def_nodes append j to parent_1_def_nodes[def_node]
        if def_node in parent_1_def_nodes:
            parent_1_def_nodes[def_node].append(j)
        # Otherwise create new entry of parent_1_def_nodes[def_node] = j
        else:
            parent_1_def_nodes[def_node] = [j]

    # Create a dictionary of deficit nodes and corresponding journeys
    parent_2_def_nodes = {}
    # For each journey in parent 2
    for j in parent_2:
        # Deficit node is always in middle position
        def_node = j[1]

        # If def_node in parent_2_def_nodes append j to parent_2_def_nodes[def_node]
        if def_node in parent_2_def_nodes:
            parent_2_def_nodes[def_node].append(j)
        # Otherwise create new entry of parent_2_def_nodes[def_node] = j
        else:
            parent_2_def_nodes[def_node] = [j]

    # Create the two children
    child_1 = []
    child_2 = []

    # For each deficit node in the set of deficit nodes
    for def_node in set(parent_1_def_nodes):
        # Choose a random boolean value (0 or 1)
        random_bool = random.choice([0, 1])

        # Need to find all journeys to the deficit node for each parent
        parent_1_js_to_node = parent_1_def_nodes.get(def_node, [])
        parent_2_js_to_node = parent_2_def_nodes.get(def_node, [])

        # If 0 then child 1 gets the corresponding gene from parent 1 and child 2 gets gene from parent 2
        if random_bool == 0:
            child_1.extend(parent_1_js_to_node)
            child_2.extend(parent_2_js_to_node)

        # Else if 1 then child 1 gets corresponding gene from parent 2 and child 2 gets gene from parent 1
        else:
            child_1.extend(parent_2_js_to_node)
            child_2.extend(parent_1_js_to_node)

    # Return the children
    return child_1, child_2


"""
The fixing functions for swapping surplus hubs until a valid solution is found
"""


def macro_fixing(over_res_hubs: List[int], under_res_hubs: List[int], path: List[Tuple[int, int, int]],
                 sur_js: Dict[int, List[int]], model: Dict[int, Hub]):
    """
    Swaps surplus hub names in a path and may split journeys into smaller chunks if beneficial

    params
        over_res_hubs - The over resolved surplus hubs (surplus -> defict)
        under_res_hubs - The under resolved suplus hubs (surplus -> surplus)
        path - The original path of form [(from, to, s)]
        sur_js - The indexes of the paths for the surplus hubs
        model - The model as a dictionary of hub_name: Hub object
    """
    # Go through each of the journeys for the over_res_hubs
    for over_res_hub_name in over_res_hubs:
        # Shuffle the journeys to be explored
        random.shuffle(sur_js[over_res_hub_name])
        for journey_idx in sur_js[over_res_hub_name]:
            # Get the s val of the over resolved hub
            over_res_s = model[over_res_hub_name].get_s()
            # Check over resolved hub not resolved
            if over_res_s == 0:
                break
            # Get the quantity of s in the journey
            journey_s = path[journey_idx][2]
            # Shuffle the under resolved hubs
            random.shuffle(under_res_hubs)
            for under_res_hub_name in under_res_hubs:
                # If the quantity of the journey is lower than the under resolved hub surplus and the over resolved hub's deficit (switch surplus hub)
                under_res_s = model[under_res_hub_name].get_s()
                over_res_s = model[over_res_hub_name].get_s()

                if journey_s <= under_res_s and journey_s <= abs(over_res_s):
                    # Move the s quantity of journey to the under resolved hub
                    Hub.move_s(start=model[under_res_hub_name],
                               end=model[over_res_hub_name], s=journey_s)

                    # Alter the journey surplus hub name
                    path[journey_idx] = (
                        under_res_hub_name, path[journey_idx][1], path[journey_idx][2])
                    # Check if the swap was able to resolve
                    if under_res_s == journey_s:
                        # If resolved then remove the hub_name from under resolved hubs
                        under_res_hubs.remove(under_res_hub_name)
                    # Break from the loop
                    break
                # Else if the journey can be split to resolve the hub
                elif journey_s > under_res_s or journey_s > abs(over_res_s):
                    # Split journey into one of size that would resolve
                    to_move = -1
                    if under_res_s <= abs(over_res_s):  # Under resolved is fixed
                        under_res_hubs.remove(under_res_hub_name)
                        to_move = under_res_s
                    else:
                        to_move = abs(over_res_s)

                    # Move the supply
                    Hub.move_s(start=model[under_res_hub_name],
                               end=model[over_res_hub_name], s=to_move)

                    # Add journey to the path
                    path.append(
                        (under_res_hub_name, path[journey_idx][1], to_move))

                    # Alter the previous journey in the path for lower quantity moved
                    path[journey_idx] = (
                        over_res_hub_name, path[journey_idx][1], journey_s-to_move)
                    break


def micro_fixing(over_res_hubs: List[int], under_res_hubs: List[int], path: List[Tuple[int, int, int]],
                 sur_js: Dict[int, List[int]], def_js: Dict[int, List[int]], model: Dict[int, Hub], max_journey_size: int):
    """
    Swaps surplus hub names in a path and may split journeys into smaller chunks if beneficial

    params
        over_res_hubs - The over resolved surplus hubs (surplus -> defict)
        under_res_hubs - The under resolved suplus hubs (surplus -> surplus)
        path - The original path of form [(from, to, s)]
        sur_js - The indexes of the paths for the surplus hubs
        sur_js - The indexes of the paths for the deficit hubs
        model - The model as a dictionary of hub_name: Hub object
        max_journey_size - The largest allowed size for a journey
    """
    print()
    print("Starting")
    print()
    to_remove = []
    # Loop through each of the over resolved hubs
    for over_res_hub in over_res_hubs:
        print(f'Over resolved hub: {model[over_res_hub]}')
        # Get all of the positions of the surplus hub's journey
        over_res_hub_js = sur_js[over_res_hub]
        # Loop through each of these journeys
        for over_res_hub_j_idx in over_res_hub_js:
            over_res_journey = path[over_res_hub_j_idx]
            print(f'Looking at over journey {over_res_journey}')
            # Check if the deficit hub is visited by and under-resolved hub
            deficit_journeys = def_js[over_res_journey[1]]
            for def_res_hub_j in deficit_journeys:
                # Get the actual journey
                def_journey = path[def_res_hub_j]
                print(f'Under journey {def_journey}')
                if def_journey[0] in under_res_hubs:
                    print(
                        f'Surplus hub in oppositie direction {model[def_journey[0]]}')
                    # Increase the size of the under resolved journey up to max_journey_size
                    while model[def_journey[0]].get_s() != 0 and model[over_res_hub].get_s() != 0:
                        # Get all of the s values
                        under_res_j_size = def_journey[2]
                        print(
                            f'Under resolved journey size: {under_res_j_size}')
                        over_res_j_size = over_res_journey[2]
                        print(f'Over resolved journey size: {over_res_j_size}')

                        under_res_s = model[def_journey[0]].get_s()
                        print(f'Under resolved hub s: {under_res_s}')
                        over_res_s = model[over_res_hub].get_s()
                        print(f'Over resolved hub s: {over_res_s}')

                        # If the over resolved journey can be increased in size then do so
                        if over_res_j_size < max_journey_size:
                            # Amount to move is the minimum to resolve one of the hubs, or to hit the max journey size, or to hit minimum journey size (0)
                            to_move = min(under_res_s, abs(over_res_s),
                                          max_journey_size - under_res_j_size, over_res_j_size)
                            # Move it in the model
                            Hub.move_s(
                                start=model[def_journey[0]], end=model[over_res_hub], s=to_move)
                            # Update the journeys in the path of the under resolved hub
                            path[def_res_hub_j] = (
                                path[def_res_hub_j][0], path[def_res_hub_j][1], path[def_res_hub_j][2] + to_move)
                            # Update the journey for the over resolved hub
                            # Check that it doesn't need to be removed
                            if over_res_j_size == to_move:
                                # Remove
                                to_remove.append(over_res_hub_j_idx)
                            else:
                                # Make it smaller in quantity
                                path[over_res_hub_j_idx] = (
                                    path[over_res_hub_j_idx][0], path[over_res_hub_j_idx][1], path[over_res_hub_j_idx][2] - to_move)

                        else:
                            # Add a new journey and keep reducing
                            to_move = min(max_journey_size, abs(over_res_s),
                                          max_journey_size - under_res_j_size, over_res_j_size)
                            # Remove quantity from journey / journey all together
                        break
                break
            break

    # Remove any deleted journeys in the path
    for idx in to_remove.sort(reverse=True):
        del path[idx]
