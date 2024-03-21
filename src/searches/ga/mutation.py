"""
Mutation functions for the genetic algorithm
"""
from typing import List, Tuple
import random
from searches.ga.population import encode_solution, decode_solution
from searches.sa.neighbourhood import compress_neighbour
import copy


def swap(parent: List[Tuple[int, int, int]], mutation_rate: float, max_journey_size: int) -> List[Tuple[int, int, int]]:
    """
    Swaps two random deficit depots with a probability of mutation_rate

    params
        parent - The chromosome
        mutation_rate - The chance of the mutation happening
        max_journey_size - The maximum size of a journey
    """
    # Generate a random float between 0 and 1
    rand = random.random()

    # Check if the random value > mutation rate
    if rand > mutation_rate:
        # If it is, no mutation occurs and parent is returned
        return parent

    # Check there is more than 1 unique deficit and surplus nodes
    sur_nodes = set()
    def_nodes = set()

    # Add each f the surplus and deficit nodes to the parent
    for j in parent:
        sur_nodes.add(j[0])
        def_nodes.add(j[1])

    # If only one of either then return the parent as no swap can ba made
    if len(sur_nodes) <= 1 or len(def_nodes) <= 1:
        return parent

    # If here then mutate

    # Pick two different journeys in the parent, making sure surplus and deficit nodes are different
    # As if either were the same change won't affect the fitness
    # Store the indexes of the two selected
    j_1_idx = 0
    j_2_idx = 0

    # While the surplus nodes or the deficit nodes are the same
    while (parent[j_1_idx][0] == parent[j_2_idx][0]) or (parent[j_1_idx][1] == parent[j_2_idx][1]):
        # Calculate two random indexes in the parent
        j_1_idx, j_2_idx = random.sample(range(len(parent)), k=2)

    # Generate the new parent
    new_parent: List[Tuple[int, int, int]] = copy.deepcopy(parent)

    # If the journeys are of the same length then a straight swap of deficit nodes will occur
    if new_parent[j_1_idx][2] == new_parent[j_2_idx][2]:
        # Swap the deficit nodes
        temp = new_parent[j_1_idx][1]
        new_parent[j_1_idx] = (
            new_parent[j_1_idx][0], new_parent[j_2_idx][1], new_parent[j_1_idx][2])
        new_parent[j_2_idx] = (
            new_parent[j_2_idx][0], temp, new_parent[j_2_idx][2])
        # Return the new parent
        return new_parent

    # If the journeys are of different length then
    # Calculate the longer journey
    longer_j = -1
    if new_parent[j_1_idx][2] > new_parent[j_2_idx][2]:
        longer_j = 1
    else:
        longer_j = 2
    new_journey = ()
    # Split the longer journey into two parts (one of length of the smaller journey)
    if longer_j == 1:
        # Set the surplus and deficit nodes to the same as the original journey
        sur = new_parent[j_1_idx][0]
        deficit = new_parent[j_1_idx][1]
        # New journey s is the same as s of journey 1 - s of journey 2
        s = new_parent[j_1_idx][2] - new_parent[j_2_idx][2]
        new_journey = (sur, deficit, s)
        # Decrease the s value of the orignal journey
        new_parent[j_1_idx] = (new_parent[j_1_idx][0],
                               new_parent[j_1_idx][1], new_parent[j_2_idx][2])
    elif longer_j == 2:
        # Set the surplus and deficit nodes to the same as the original journey
        sur = new_parent[j_2_idx][0]
        deficit = new_parent[j_2_idx][1]
        # New journey s is the same as s of journey 2 - s of journey 1
        s = new_parent[j_2_idx][2] - new_parent[j_1_idx][2]
        new_journey = (sur, deficit, s)

        # Decrease the s value of the orignal journey
        new_parent[j_2_idx] = (new_parent[j_2_idx][0],
                               new_parent[j_2_idx][1], new_parent[j_1_idx][2])
    # Swap the deficit nodes of the two journeys of the same length
    temp = new_parent[j_1_idx][1]
    new_parent[j_1_idx] = (new_parent[j_1_idx][0],
                           new_parent[j_2_idx][1], new_parent[j_1_idx][2])
    new_parent[j_2_idx] = (new_parent[j_2_idx][0],
                           temp, new_parent[j_2_idx][2])
    # Add the non swapped journey to the parent
    new_parent.append(new_journey)

    # Compress the path
    decoded_path = decode_solution(path=new_parent)
    compressed_path = compress_neighbour(
        path=decoded_path, max_journey_size=max_journey_size)
    # return new parent
    return encode_solution(path=compressed_path)
