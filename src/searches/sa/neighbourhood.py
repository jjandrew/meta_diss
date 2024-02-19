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

    # check that the legth of the path is not 1 (to stop index out of bounds errors)
    if len(path) == 1:
        return path

    new_path = []

    j_idx = 0
    # While the index is still in  bounds
    while j_idx < len(path):
        # check if j_idx at end of path
        if j_idx == len(path) - 1:
            # Add the final element
            new_path.append(path[j_idx])
            break

        # Set the comparison index to 1 more than j_idx
        cmpr_idx = j_idx+1
        # Get the current and next journeys
        cur_j = path[j_idx]
        cmpr_j = path[cmpr_idx]

        # Keep decreasing while they are the same route for the jurney
        if cur_j['from'] == cmpr_j['from'] and cur_j['to'] == cmpr_j['to']:
            # If the current journey is the of max_joruney size then increase pointers and add journey
            if cur_j['s'] == max_journey_size:
                new_path.append(path[j_idx])
                j_idx += 1
                continue

            # Otherwise increase s of the current journey to get as large as possible (up to max_journey_size)
            combined_s = cur_j['s'] + cmpr_j['s']
            if combined_s <= max_journey_size:
                # Delete the comparison journey
                del path[cmpr_idx]
                # Keep checking the journeys after until it reaches max_journey size
                while cmpr_idx < len(path) and path[cmpr_idx]['from'] == cur_j['from'] and path[cmpr_idx]['to'] == cur_j['to']:
                    # Add the s value of the comparison index to combined_s
                    combined_s += path[cmpr_idx]['s']
                    # Check if combined_s is over max_journey_size
                    if combined_s <= max_journey_size:  # If it is
                        # Delete the comparison journey
                        del path[cmpr_idx]
                    else:
                        # Set the s value of the next journey to the remaining s
                        path[cmpr_idx]['s'] = combined_s - max_journey_size

                        # Set the combined s to max_journey_size
                        combined_s = max_journey_size
                        break
                # Add the journey to new path
                new_path.append(
                    {'from': cur_j['from'], 'to': cur_j['to'], 's': combined_s})
            else:
                # Calculate the s left on the new journey
                combined_s -= max_journey_size
                # Need to add a journey of max_journey_size to the new path (one of max j size)
                new_path.append(
                    {'from': cur_j['from'], 'to': cur_j['to'], 's': max_journey_size})
                # Edit the leftover s of the comparison journey
                path[cmpr_idx]['s'] = combined_s

        else:  # Journey can't be decreased
            new_path.append(cur_j)

        j_idx += 1

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
