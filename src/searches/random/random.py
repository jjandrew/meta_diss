"""
Creates a random solution to the model passed in
"""
from typing import List, Dict
from src.classes.hub import Hub
import random


def random_search(model: List[Hub], max_journey_size: int) -> List[Dict[str, int]]:
    """
    Performs a random search on the model that is passed in

    params:
        model - a list of hubs which have a supply value to be solved
        max_journey_size - The maximum number of goods that can be moved between hubs

    returns
        List[{from, to, s}]
    """
    journeys = []

    # while there are still hubs to be resolved
    while len(model) > 1:
        # Choose a random hub to resolve
        rand_loc = random.randint(0, len(model) - 1)
        # Remove it from the model to stop unnecessary computation
        chosen_hub = model.pop(rand_loc)

        # Check if the chosen hub is in deficit or surplus
        surplus = False
        if chosen_hub.get_s() > 0:
            surplus = True

        # Continue until resolution
        while chosen_hub.get_s() != 0:
            # Choose a random hub to perform move with
            mv_loc = random.randint(0, len(model) - 1)
            movement_hub = model[mv_loc]

            # Do nothing if the chosen hub does not work towards a solution
            if surplus and movement_hub.get_s() > 0:
                continue
            elif not surplus and movement_hub.get_s() < 0:
                continue

            # Doesn't resolve chosen hub, therefore abs(chosen_hub.get(s)) > max_journey_size
            # or more to resolve in chosen_hub than movement hub
            if (abs(chosen_hub.get_s()) > max_journey_size) or abs(chosen_hub.get_s()) > abs(movement_hub.get_s()):
                # Check if journey would resolve the movement hub
                if abs(movement_hub.get_s()) > max_journey_size:  # Will not resolve
                    # Perform a journey of maximum size
                    # If chosen hub in surplus then moving from chosen hub
                    if surplus:
                        # Add journey to list
                        journeys.append({'from': chosen_hub.get_name(
                        ), 'to': movement_hub.get_name(), 's': max_journey_size})
                        # Move from chosen hub to movement hub
                        Hub.move_s(start=chosen_hub,
                                   end=movement_hub, s=max_journey_size)
                    else:  # chosen hub in deficit
                        # Add journey to list
                        journeys.append({'from': movement_hub.get_name(
                        ), 'to': chosen_hub.get_name(), 's': max_journey_size})
                        # Move from movement hub to chosen hub
                        Hub.move_s(start=movement_hub,
                                   end=chosen_hub, s=max_journey_size)
                else:  # Move will resolve movement hub
                    # Move absolute of its value
                    if surplus:  # Chosen in surplus

                        # Add journey to list
                        journeys.append({'from': chosen_hub.get_name(
                        ), 'to': movement_hub.get_name(), 's': abs(movement_hub.get_s())})
                        # Move from chosen to movement
                        Hub.move_s(start=chosen_hub, end=movement_hub,
                                   s=abs(movement_hub.get_s()))
                    else:  # Chosen in deficit
                        # Add journey to list
                        journeys.append({'from': movement_hub.get_name(
                        ), 'to': chosen_hub.get_name(), 's': abs(movement_hub.get_s())})
                        # Move from movement to chose
                        Hub.move_s(start=movement_hub, end=chosen_hub,
                                   s=abs(movement_hub.get_s()))
                    # Pop movement hub from model as it is resolved
                    model.pop(mv_loc)

            # Else difference is resolved with this journey
            else:
                # Move chosen_hub.get(s) in right direction
                if surplus:  # if chosen hub in surplus
                    # Add journey to list
                    journeys.append({'from': chosen_hub.get_name(
                    ), 'to': movement_hub.get_name(), 's': abs(chosen_hub.get_s())})
                    # Move from chosen to movement
                    Hub.move_s(start=chosen_hub, end=movement_hub,
                               s=abs(chosen_hub.get_s()))
                else:  # chosen hub in deficit
                    # Add journey to list
                    journeys.append({'from': movement_hub.get_name(
                    ), 'to': chosen_hub.get_name(), 's': abs(chosen_hub.get_s())})
                    # Move from movement to chosen
                    Hub.move_s(start=movement_hub, end=chosen_hub,
                               s=abs(chosen_hub.get_s()))

    return journeys
