"""
Performs selection for the genetic algorithm
"""
from typing import List, Dict
import random
from math import inf
from searches.ga.population import encode_solution, decode_solution
from utils import fitness
from model.hub import Hub


def tournament(pop: List[List[tuple]], t_size: int, model: Dict[int, Hub]) -> List[tuple]:
    """
    Performs tournament selection on a population

    params
        pop - The population as a list of solution chromosomes, represented as [(from, to, s)]
        t_size - The size of the tournament
        model - The model to use when evaluating solutions

    returns
        The winning solution from the tournament
    """
    # Shuffle the population
    random.shuffle(pop)

    # Create population for the tournament
    t_pop = pop[:t_size]

    # Calculate the best fitness element of the tournament
    best_path = []
    best_fitness = inf
    for i in range(t_size):
        # Calculate the fitness of the ith element
        i_fitness = fitness(path=decode_solution(path=t_pop[i]), model=model)

        # If fitness best so far, set it to the best path
        if i_fitness < best_fitness:
            # Set best fitness value to fitness of the element
            best_fitness = i_fitness
            best_path = t_pop[i]

    return best_path
