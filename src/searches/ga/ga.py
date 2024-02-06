"""
Main body of the genetic algorithm
"""
from model.hub import Hub
from typing import Dict, List
from searches.ga.population import gen_pop
from utils import fitness


def ga(mutation_rate: float, pop_size: int, n: int, model: Dict[int, Hub], max_journey_size: int) -> List[Dict[str, int]]:
    """
    The main body of the GA algorithm

    params:
        mutation_rate - The chance of a mutation occurring
        pop_size - The size of the population
        n - The termination criterion for how many populations before completion
        model - The model the algorithm is to be performed on
        max_journey_size - The maximum journey size for the problem

    returns
        The best path as a list of Dictionaries of {from, to, s}
    """
    # Generate a population of pop_size feasible solutions
    pop = gen_pop(pop_size=pop_size,  model=model,
                  max_journey_size=max_journey_size)

    # Keep track of the number of populations
    iters = 0
    # While the number of iters is lower than terminating criterion
    while iters < n:
        #  Sort the population in order of fitness (highest first)

        # Perform selection

        # Perform crossover

        # Perform mutation

        # +1 iteration as new population generated
        iters += 1
