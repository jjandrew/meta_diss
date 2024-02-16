"""
Generate a random neighbouring solution for the SA algorithm
"""
from typing import List, Dict
import random
import copy


def compress_neighbour(path: List[Dict[str, int]], max_journey_size: int) -> List[Dict[str, int]]:
    """
    Compresses a neighbour to improve solution in the case where two journeys with s less than max_journey size have the same surplus and deficit nodes

    params
        path - The path a of journeys of form [{from, to, s}]
        max_journey_size - the maximum size of the journey allowed in the model

    returns
        Compressed path
    """
    # Sort path by j['from'] and the j['to'] and then j['s']
    path.sort(key=lambda j: (j['from'], j['to'], -j['s']))

    new_path = []

    to_skip = False
    for j_idx in range(len(path)-1):
        # check if should skip the next value (it has been removed)
        if to_skip:
            to_skip = False
            continue
        # Obtain the current and next journeys
        cur_j = path[j_idx]
        next_j = path[j_idx+1]

        if cur_j['from'] == next_j['from'] and cur_j['to'] == next_j['to']:
            # Compare s values, to see if possible to compress
            if cur_j['s'] == max_journey_size:
                new_path.append(path[j_idx])
                continue
            # Increase s of current journey to equal max journey size, removing from next_j
            combined_s = cur_j['s'] + next_j['s']
            if combined_s <= max_journey_size:
                # Need to delete the item in position next
                new_path.append(
                    {'from': cur_j['from'], 'to': cur_j['to'], 's': combined_s})
                to_skip = True
            else:
                # Need to add two journeys to the new path (one of max j size)
                new_path.append(
                    {'from': cur_j['from'], 'to': cur_j['to'], 's': max_journey_size})
                combined_s -= max_journey_size
                new_path.append(
                    {'from': cur_j['from'], 'to': cur_j['to'], 's': combined_s})
        else:
            new_path.append(path[j_idx])
    # Need to add the final journey in the path
    if not to_skip:
        new_path.append(path[-1])

    return new_path


def gen_neighbour(path) -> List[Dict[str, int]]:
    """
    Generates a random neighbour to a path by swapping two cities in a journey

    params
        path - The current path from the SA algorithm in form [{from ,to, s}]

    returns
        A randomly generated neighbouring path
    """
    # Pick two different journeys in the path, making sure surplus and deficit nodes are different
    # As if either were the same change won't affect the fitness
    # Store the indexes of the two selected
    j_1_idx = 0
    j_2_idx = 0

    while (path[j_1_idx]['from'] == path[j_2_idx]['from']) or (path[j_1_idx]['to'] == path[j_2_idx]['to']):
        # Calculate two random indexes in the path
        j_1_idx, j_2_idx = random.sample(range(len(path)), k=2)

    # Generate the new path
    new_path: List[Dict[str, int]] = copy.deepcopy(path)

    # If the journeys are of the same length then a straight will occur
    if new_path[j_1_idx]['s'] == new_path[j_2_idx]['s']:
        # Swap the deficit nodes
        temp = new_path[j_1_idx]['to']
        new_path[j_1_idx]['to'] = new_path[j_2_idx]['to']
        new_path[j_2_idx]['to'] = temp
        # Return the new path
        return new_path

    # If the journeys are of different length then
    # Calculate the longer journey
    longer_j = -1
    if new_path[j_1_idx]['s'] > new_path[j_2_idx]['s']:
        longer_j = 1
    else:
        longer_j = 2
    new_journey = {}
    # Split the longer journey into two parts (one of length of the smaller journey)
    if longer_j == 1:
        # Set the surplus and deficit nodes to the same as the original journey
        new_journey['from'] = new_path[j_1_idx]['from']
        new_journey['to'] = new_path[j_1_idx]['to']
        # New journey s is the same as s of journey 1 - s of journey 2
        new_journey['s'] = new_path[j_1_idx]['s'] - new_path[j_2_idx]['s']
        # Decrease the s value of the orignal journey
        new_path[j_1_idx]['s'] = new_path[j_2_idx]['s']
    elif longer_j == 2:
        # Set the surplus and deficit nodes to the same as the original journey
        new_journey['from'] = new_path[j_2_idx]['from']
        new_journey['to'] = new_path[j_2_idx]['to']
        # New journey s is the same as s of journey 2 - s of journey 1
        new_journey['s'] = new_path[j_2_idx]['s'] - new_path[j_1_idx]['s']
        # Decrease the s value of the orignal journey
        new_path[j_2_idx]['s'] = new_path[j_1_idx]['s']
    # Swap the deficit nodes of the two journeys of the same length
    temp = new_path[j_1_idx]['to']
    new_path[j_1_idx]['to'] = new_path[j_2_idx]['to']
    new_path[j_2_idx]['to'] = temp
    # Add the non swapped journey to the path
    new_path.append(new_journey)
    # return new path
    return new_path
