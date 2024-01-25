"""
A brute force approach to solving the problem
"""
from typing import List, Dict
from classes.hub import Hub
from utils import reduce_model, calc_distance, improve_solution
from math import inf


# Now for testing
from model.model import create_model


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

    # Initialize variables to track the best solution
    best_sequence = None
    min_distance = inf

    # Check all permutations
    for path in paths:
        improved_path = improve_solution(solution=path, model=model,
                                         max_journey_size=max_journey_size)
        print(improved_path)
        fitness = calc_distance(path=improved_path, model=model)

        # Check if the current sequence is better than the current best
        if fitness < min_distance:
            min_distance = fitness
            best_sequence = improved_path

    return best_sequence


if __name__ == "__main__":
    model = create_model(n=4, alpha=2, max_def=-10, max_sur=10)
    print("Starting model")
    for hub in model:
        print(hub)

    print()
    print("Brute force")
    brute(model=model, max_journey_size=3)
