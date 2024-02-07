"""
Mutation functions for the genetic algorithm
"""
from typing import List
import random


def swap(parent: List[tuple], mutation_rate: float) -> List[tuple]:
    """
    Swaps two random deficit hubs with a probability of mutation_rate

    params
        parent - The chromosome
        mutation_rate - The chance of the mutation happening
    """
    # Generate a random float between 0 and 1
    rand = random.random()

    # Check if the random value > mutation rate
    if rand > mutation_rate:
        # If it is, no mutation occurs and parent is returned
        return parent

    # Create a set of deficit hubs
    def_hubs = {deficit for _, deficit, _ in parent}

    # If only one deficit hub then can't perform a swap operation
    if len(def_hubs) <= 1:
        return parent

    # Pick two random deficit hubs in the solution to swap
    while True:
        # Pick two random deficit hubs in the solution to swap
        [pos1, pos2] = random.sample(range(len(parent)), 2)

        # Check the deficit hubs at the positions are not the same
        if parent[pos1][1] == parent[pos2][1]:
            continue

        # Swap at the two positions
        first = (parent[pos2][0], parent[pos1][1], parent[pos2][2])
        second = (parent[pos1][0], parent[pos2][1], parent[pos1][2])

        parent[pos1] = first
        parent[pos2] = second
        break

    return parent
