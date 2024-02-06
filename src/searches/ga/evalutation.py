"""
Performs thee evaluation section of the genetic algorithm
"""
from searches.ga.population import encode_solution, decode_solution
from utils import fitness
from typing import List, Dict
from model.hub import Hub


def rank_pop(pop: List[List[tuple]], model: Dict[int, Hub]):
    """
    Ranks a population of solutions by their fitness from highest to lowest.
    Returns the population list in place with best quality solutions first.

    params
        pop - The population as a list of solutions in the form [(start hub, end hub, s)]
        model - The model the algorithm is performed on as a dictionary of hub name: hub object
    """
    # Replace each member ofthe population with its solution as a dictionary of [{from, to, s}]
    for i in range(len(pop)):
        pop[i] = decode_solution(path=pop[i])

    # Sort the list in descending order for fitness
    pop.sort(key=lambda x: fitness(path=x, model=model), reverse=True)

    # Convert each member of the population back into a list of tuples of form [(from, to, s)]
    for i in range(len(pop)):
        pop[i] = encode_solution(path=pop[i])
