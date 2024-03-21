"""
Executes the main body of the AS algorithm
"""
from math import inf
from typing import List, Dict
from model.depot import Depot
from searches.aco.pathGeneration import generate_path
from searches.aco.pheromone import update_pheromone
from utils import fitness


def AS(model: Dict[int, Depot], m: int, e: float, Q: int, d: List[List[float]],
       p: List[List[float]], h: List[List[float]], n: int, max_journey_size: int,
       alpha=1, beta=2) -> int:
    """
    Performs the AS algorithm on the TNRP

    params:
    model - The model as dictionary of depot_name: Depot object
    m - population size
    e - evaporation rate
    Q - constant for fitness normalisation
    d - distance matrix
    p - pheromone matrix
    n - Termination condition - number of fitness evals before termination
    max_journey_size - The maximum size of each journey
    alpha - The exponent used to scale the pheromone matrix in transition probabilities (default=1)
    beta - The exponent used to scale the heuristic matrix in transition probabilities (default=2)

    returns:
        List of fitnesses at each evaluation
    """
    # Split depots into surplus and deficit depots
    surplus_deps = {dep: model[dep] for dep in model if model[dep].get_s() > 0}
    deficit_deps = {dep: model[dep] for dep in model if model[dep].get_s() < 0}

    # Empty array to store results of all fitness evals
    all_fitnesses = []

    # Store the best path so far
    best_path = []
    best_fitness = inf

    # Variable for number of fitness evaluations so far
    fitness_evals = 0

    # Repeat until termination criterion is met
    while fitness_evals < n:
        # Store the paths and fitnesses of the population
        paths = []
        fitnesses = []

        # Create a population of m ants:
        for _ in range(m):

            # Check if the termination condition is broken part-way through creation of population
            if fitness_evals == n:
                # If so end creation of population
                break

            # Generate a path using heuristic and pheromone information
            path = generate_path(
                sur_deps=surplus_deps, def_deps=deficit_deps, d=d, h=h, p=p,
                max_journey_size=max_journey_size, alpha=alpha, beta=beta)

            # Calculate the fitness of the solution
            ant_fitness = fitness(path=path, model=model)
            # Increment the number of fitness evaluations
            fitness_evals += 1
            # Add the fitness evaluation to the fitnesses list
            all_fitnesses.append(ant_fitness)

            # If the ant has the best so far fitness then store its path
            if ant_fitness < best_fitness:
                best_path = path
                best_fitness = ant_fitness

            # Add paths and fitnesses to population paths and fitnesses
            paths.append(path)
            fitnesses.append(ant_fitness)

        # Update the pheromone using the population
        update_pheromone(p=p, paths=paths, fitnesses=fitnesses, e=e, Q=Q)

    return all_fitnesses, best_path
