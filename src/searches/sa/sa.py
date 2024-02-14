"""
Performs the simulated annealing algorithm
"""
from searches.random.random import random_search
from typing import Dict, List
from model.hub import Hub
from utils import fitness
from searches.sa.neighbourhood import neighbour_gen
import random
import math


def accept(delta_e: int, t: float, k=1):
    """
    Decides whether or not a solution should be accepted for the SA algorithm

    params
        delta_e - The change in energy (whether the solution is better or worse)
        t - The current temperature of the SA algorithn
        k - Botsmann constant - default of 1
    """
    # Check if the solution is better or worse
    if delta_e < 0:
        return True
    else:
        # Generate a random float between 0 and 1
        r = random.random()
        # See if it's less than e^(-delta_e/kt) and if so accept it
        if r < math.exp(-delta_e/(k*t)):
            return True
        else:
            return False


def sa(start_temp: int, n: int, cool_r: float, max_journey_size: int, model: Dict[int, Hub]) -> List[Dict[str, int]]:
    """
    Performs the Simulated annealing algorithm

    params 
        start_temp - The initial temperature of the algorithm
        n - The number of iterations of the algorithm before termination
        cool_r - The probability that a worse solution is accepted as the algorithm progresses
        max_journey_size - The maximum journey size
        model - The initial state of the model

    returns
        The final solution
    """
    # Set initial temperature to the start temperature
    temp = start_temp

    # Generate a current solution
    cur_solution = random_search(
        model=model, max_journey_size=max_journey_size)
    # Calculate the fitness (energy) of the solution
    cur_e = fitness(path=cur_solution, model=model)

    # TODO Store the best so far ?? Maybe do not use as not really in algorithm but do anyway
    best_solution = cur_solution
    best_e = cur_e

    # For n iterations
    for _ in range(n):
        # Generate a random neighbour
        neighbour = neighbour_gen(solution=cur_solution)

        # Calculate the new energy
        new_e = fitness(path=neighbour)

        # Calculate if new solution is better
        delta_e = new_e - cur_e

        # See whether to accept the new solution
        if accept(delta_e=delta_e, t=temp):
            # If yes, update the current solution and its energy
            cur_solution = neighbour
            cur_e = new_e

            # Check if new best solution
            if new_e < best_e:
                best_solution = cur_solution
                best_e = cur_e

        temp *= cool_r

    return best_solution
