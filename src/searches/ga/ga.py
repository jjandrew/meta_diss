"""
Main body of the genetic algorithm
"""
from model.hub import Hub
from typing import Dict, List
from searches.ga.population import gen_pop
from searches.ga.selection import tournament
from searches.ga.crossover import aware_crossover
from searches.ga.mutation import swap
from searches.ga.fixing.fixing import fix
import random
import copy


def ga(mutation_rate: float, pop_size: int, t_size: int, n: int, model: Dict[int, Hub], max_journey_size: int) -> List[Dict[str, int]]:
    """
    The main body of the GA algorithm

    params:
        mutation_rate - The chance of a mutation occurring
        pop_size - The size of the population
        t_size - The size of the tournament
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
        # +1 iteration as new population generated
        iters += 1

        # Store the new population
        new_pop = []

        # Start creating the new population until it is of the correct size
        while len(new_pop) < pop_size:
            # Select two parents
            parent_1 = tournament(pop=pop, t_size=t_size, model=model)
            parent_2 = tournament(pop=pop, t_size=t_size, model=model)

            # Perform crossover
            child_1, child_2 = aware_crossover(
                parent_1=parent_1, parent_2=parent_2)

            # Perform mutation
            child_1 = swap(parent=child_1, mutation_rate=mutation_rate,
                           max_journey_size=max_journey_size)
            child_2 = swap(parent=child_2, mutation_rate=mutation_rate,
                           max_journey_size=max_journey_size)

        # If there is an odd number in population and new population is too large
        if len(new_pop) > pop_size:
            # Remove a member from the new population at random
            i = random.randint(0, len(new_pop)-1)
            del new_pop[i]

        # Perform a fixing algorithm on every member of the new population
        for path in new_pop:
            fix(path=path, model=copy.deepcopy(model))

        # Add the new population to the old one
        pop = new_pop
