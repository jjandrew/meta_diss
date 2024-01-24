"""
A brute force approach to solving the problem
"""
from typing import List, Dict
from src.classes.hub import Hub
from src.utils import reduce_model, calc_distance
import itertools
from math import inf


# Now for testing
from src.model.model import create_model


def brute(model: List[Hub], max_journey_size: int) -> List[Dict[str, int]]:
    """
    Performs a brute force search on the model that is passed in

    params:
        model - a list of hubs which have a supply value to be solved
        max_journey_size - The maximum number of goods that can be moved between hubs

    returns
        List[{from, to, s}]
    """
    # Reduce the model to get a list of guaranteed shortest journeys
    journeys = reduce_model(model=model, max_journey_size=max_journey_size)

    # generate all possible journeys
    all_journeys = []
    # Generate all pairs of unequal hubs
    for hub_1 in model:
        for hub_2 in model:
            if hub_1 != hub_2:
                # Generate all possible quantities up to the max journey size
                for quantity in range(1, max_journey_size + 1):
                    all_journeys.append((hub_1, hub_2, quantity))

    # For each of these journeys, keep adding journeys until all s's at 0

    print("All journeys added")

    print(len(all_journeys))

    # find all permutations of journeys
    perms = list(itertools.permutations(all_journeys))

    print("Permutations generated")

    # Initialize variables to track the best solution
    best_sequence = None
    min_distance = inf

    # Check all permutations
    for perm in perms:
        print(perm)
        fitness = calc_distance(perm)

        # Check if the current sequence is better than the current best
        if fitness < min_distance:
            min_distance = fitness
            best_sequence = perm

    return best_sequence


if __name__ == "__main__":
    model = create_model(n=4, alpha=2, max_def=-10, max_sur=10)
    print("Starting model")
    for hub in model:
        print(hub)

    print()
    print("Brute force")
    brute(model=model, max_journey_size=3)
