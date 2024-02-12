"""
The fixing functions for swapping surplus hubs until a valid solution is found
"""

import random
from model.hub import Hub
from typing import List, Tuple, Dict


def fixing(over_res_hubs: List[int], under_res_hubs: List[int], path: List[Tuple[int, int, int]],
           sur_js: Dict[int, List[int]], model: Dict[int, Hub]):
    """
    Swaps surplus hub names in a path without splitting journeys down

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
                # If the quantity of the journey is lower than an under resolved hub and the over resolved hub(switch surplus hub)
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
