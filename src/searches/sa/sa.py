"""
Performs the simulated annealing algorithm
"""
import random
import math
from typing import Dict, List, Tuple
from searches.random_search import random_search
from TNRP_model.depot import Depot
from searches.utils import fitness
from searches.sa.neighbourhood import gen_neighbour, compress_neighbour


def accept(delta_e: int, t: float):
    """
    Decides whether or not a solution should be accepted for the SA algorithm

    params
        delta_e - The change in energy (whether the solution is better or worse)
        t - The current temperature of the SA algorithn
    """
    # Check if the solution is better or worse
    if delta_e < 0:
        # If better delta_e is negative and solution is always accepted
        return True
    else:  # Otherwise
        # Generate a random float between 0 and 1
        r = random.random()
        # See if it's less than e^(-delta_e/t) and if so accept it
        if r < math.exp(-delta_e/(t)):
            return True
        else:  # Otherwise don't accept
            return False


def sa(start_temp: int, n: int, cool_r: float, max_journey_size: int,
       model: Dict[int, Depot]) -> Tuple[List[int], List[Dict[str, int]]]:
    """
    Performs the Simulated annealing algorithm on the TNRP

    params 
        start_temp - The initial temperature of the algorithm
        n - The number of fitness evals before termination
        cool_r - The value, multiplied by the temperature after each algorithm iteration
        max_journey_size - The maximum journey size
        model - The initial state of the model

    returns
        The final solution
    """
    # Check there are more than 1 unique surplus and deficit depot
    # Keep count of surplus and deficit depots
    def_deps = 0
    sur_deps = 0
    # Count number of each
    for dep_name in model:
        if model[dep_name].get_s() < 0:
            def_deps += 1
        elif model[dep_name].get_s() > 0:
            sur_deps += 1

    # if not return solution as impossible to do algorithm
    if def_deps <= 1 or sur_deps <= 1:
        print("There must be at least two different types of Depot.")
        return []

    # Set current temperature to the start temperature
    temp = start_temp

    # Generate a current solution using random search
    cur_solution = random_search(
        model=model, max_journey_size=max_journey_size)

    # Calculate the fitness (energy) of the current solution
    cur_e = fitness(path=cur_solution, model=model)

    # Store the energies from all fitness calculations and add the first energy value
    energies = []
    energies.append(cur_e)

    # Store the best solution so far
    best_solution = cur_solution
    best_e = cur_e

    # For n-1 fitness calculations (one calculation to generate initial solution)
    for _ in range(n-1):
        # Generate a random neighbour to the current solution
        neighbour = gen_neighbour(path=cur_solution)

        # Compress the neighbour to ensure best fitness
        neighbour = compress_neighbour(
            path=neighbour, max_journey_size=max_journey_size)

        # Calculate the energy of the new solution
        new_e = fitness(path=neighbour, model=model)

        # Calculate if new solution is better
        delta_e = new_e - cur_e

        # See whether to accept the new solution
        if accept(delta_e=delta_e, t=temp):  # If it is accepted
            # update the current solution and its energy
            cur_solution = neighbour
            cur_e = new_e

            # Check if new best solution
            if new_e < best_e:
                best_solution = cur_solution
                best_e = cur_e

        # Add the energy of the current solution to all energies
        energies.append(cur_e)

        # Decrease the temperature of the algorithm by multiplying by cooling rate
        temp *= cool_r

    return energies, best_solution
