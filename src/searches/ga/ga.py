"""
Main body of the genetic algorithm
"""
import random
import copy
from math import inf
from typing import Dict, List, Tuple
from TNRP_model.depot import Depot
from searches.ga.population import gen_pop, decode_solution
from searches.ga.selection import tournament
from searches.ga.crossover import aware_crossover
from searches.ga.mutation import swap
from searches.utils import fitness


def ga(model: Dict[int, Depot], mutation_rate: float, crossover_rate: float,
       pop_size: int, t_size: int, n: int, max_journey_size: int) -> Tuple[List[int],
                                                                           List[Dict[str, int]]]:
    """
    The main body of the GA algorithm

    params:
        model - The model the algorithm is to be performed on
        mutation_rate - The chance of a mutation occurring
        crossover_rate - The chance that a crossover occurs
        pop_size - The size of the population
        t_size - The size of the tournament
        n - The termination criterion for how many fitness evals before completion
        max_journey_size - The maximum journey size for the problem

    returns
        A tuple of fitnesses and the best path as a list of Dictionaries of {from, to, s}
    """
    # Generate a population of pop_size feasible solutions
    pop = gen_pop(pop_size=pop_size,  model=model,
                  max_journey_size=max_journey_size)

    # Store the start best_path to check convergence
    best_path = []
    best_fitness = inf

    # Store the value of each fitness evaluation
    all_fitnesses = []

    # Keep track of the number of fitness evals
    fitness_evals = 0

    # For each of the original population
    for path in pop:
        # Calculate its fitness and increment number of fitness evaluations
        fit = fitness(path=decode_solution(path=path), model=model)
        fitness_evals += 1
        # Store the result of the fitness evaluations
        all_fitnesses.append(fit)
        # If the fitness is the best so far then store it
        if fit < best_fitness:
            best_path = decode_solution(path=path)
            best_fitness = fit

    # While the number of fitness evals is lower than terminating criterion
    while fitness_evals < n:
        # Store the new population
        new_pop = []

        # Start creating the new population until it is of the correct size
        while len(new_pop) < pop_size:
            # Select two parents
            parent_1 = tournament(pop=pop, t_size=t_size, model=model)
            parent_2 = tournament(pop=pop, t_size=t_size, model=model)

            # Perform crossover
            child_1, child_2 = aware_crossover(
                parent_1=copy.deepcopy(parent_1), parent_2=copy.deepcopy(parent_2),
                model=model, max_journey_size=max_journey_size, crossover_rate=crossover_rate)

            # Perform mutation
            child_1 = swap(parent=child_1, mutation_rate=mutation_rate,
                           max_journey_size=max_journey_size)
            child_2 = swap(parent=child_2, mutation_rate=mutation_rate,
                           max_journey_size=max_journey_size)

            # Add children to the new population
            new_pop.append(child_1)
            new_pop.append(child_2)

        # If there is an odd number in population and therefore the new population is too large
        if len(new_pop) > pop_size:
            # Remove a member from the new population at random
            i = random.randint(0, len(new_pop)-1)
            del new_pop[i]

        # Assign the new population to the old one
        pop = new_pop

        # Calculate the fitness of individuals in the population
        for path in pop:
            # Check number of fitness evals isnt broken
            if fitness_evals == n:
                break
            # Calculate the fitness and increment fitness evaluations
            fit = fitness(path=decode_solution(path=path), model=model)
            fitness_evals += 1
            # Store result of evaluation
            all_fitnesses.append(fit)

            # Check if individual is fitter
            if fit < best_fitness:
                best_fitness = fit
                best_path = decode_solution(path=path)

    return all_fitnesses, best_path
