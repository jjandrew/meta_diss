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
from math import inf
from utils import fitness
from searches.ga.population import decode_solution


def ga(mutation_rate: float, pop_size: int, t_size: int, n: int, model: Dict[int, Hub], max_journey_size: int, crossover_rate: float) -> List[Dict[str, int]]:
    """
    The main body of the GA algorithm

    params:
        mutation_rate - The chance of a mutation occurring
        pop_size - The size of the population
        t_size - The size of the tournament
        n - The termination criterion for how many populations before completion
        model - The model the algorithm is to be performed on
        max_journey_size - The maximum journey size for the problem
        crossover_rate - The chance that a crossover occurs

    returns
        The best path as a list of Dictionaries of {from, to, s}
    """
    # Generate a population of pop_size feasible solutions
    pop = gen_pop(pop_size=pop_size,  model=model,
                  max_journey_size=max_journey_size)

    # Store the start best_path to check convergence
    start_best_path = []
    start_best_fitness = inf

    pop_fitnesses = []

    for path in pop:
        fit = fitness(path=decode_solution(path=path), model=model)
        if fit < start_best_fitness:
            start_best_path = path
            start_best_fitness = fit

    pop_fitnesses.append(start_best_fitness)

    # Keep track of the best path and best_fitness of each population
    best_path = []
    best_fitness = inf

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
                parent_1=copy.deepcopy(parent_1), parent_2=copy.deepcopy(parent_2), model=model, max_journey_size=max_journey_size, crossover_rate=crossover_rate)

            # Perform mutation
            child_1 = swap(parent=child_1, mutation_rate=mutation_rate,
                           max_journey_size=max_journey_size)
            child_2 = swap(parent=child_2, mutation_rate=mutation_rate,
                           max_journey_size=max_journey_size)

            new_pop.append(child_1)
            new_pop.append(child_2)

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

        # Calculate the fittest individual in the pop
        for path in pop:
            fit = fitness(path=decode_solution(path=path), model=model)
            if fit < best_fitness:
                best_path = path
                best_fitness = fit
        pop_fitnesses.append(best_fitness)

    # print(f'Start path: \n {start_best_path}')
    # print(f'End path: \n {best_path}')
    return pop_fitnesses
