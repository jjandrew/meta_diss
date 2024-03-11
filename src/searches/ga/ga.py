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
        n - The termination criterion for how many fitness evals before completion
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

    all_fitnesses = []

    # Keep track of the number of fitness evals
    fitness_evals = 0

    for path in pop:
        fit = fitness(path=decode_solution(path=path), model=model)
        fitness_evals += 1
        if fit < start_best_fitness:
            start_best_path = path
            start_best_fitness = fit

    all_fitnesses.append(start_best_fitness)

    # While the number of fitness evals is lower than terminating criterion
    while fitness_evals < n:
        # +1 iteration as new population generated

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

        # Add the new population to the old one
        pop = new_pop

        # Calculate the fitness of individuals in the population
        for path in pop:
            # Check number of fitness evals
            if fitness_evals == n:
                break
            fit = fitness(path=decode_solution(path=path), model=model)
            all_fitnesses.append(fit)
            fitness_evals += 1

    # print(f'Start path: \n {start_best_path}')
    # print(f'End path: \n {best_path}')
    return all_fitnesses
