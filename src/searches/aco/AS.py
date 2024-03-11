"""
Executes the main body of the AS algorithm
"""
from typing import List, Dict
from model.hub import Hub
from math import inf
from searches.aco.pathGeneration import generate_path
from searches.aco.pheromone import update_pheromone
from utils import fitness


def AS(model: Dict[int, Hub], m: int, e: float, Q: int, d: List[List[float]],
       p: List[List[float]], h: List[List[float]], n: int, max_journey_size: int,
       alpha=1, beta=2) -> int:
    """
    Performs the AS algorithm on the data

    params:
    model - The model as dictionary of hub_name: Hub object
    m - population size
    e - evaporation rate
    Q - constant for fitness normalisation
    d - distance matrix
    p - pheromone matrix
    n - Termination condition - number of fitness evals before termination
    max_journey_size - The maximum size of each journey
    alpha - The exponent used to scale the pheromone matrix
    beta - The exponent used to scale the heuristic matrix

    returns:
    min cost route
    """
    # TODO maybe add in a heuristic matrix using s / total_s
    # TODO maybe need to add a 3rd dimension into p of s to be moved

    # Split hubs into surplus and deficit hubs
    surplus_hubs = {hub: model[hub] for hub in model if model[hub].get_s() > 0}
    deficit_hubs = {hub: model[hub] for hub in model if model[hub].get_s() < 0}

    # Set min fitness to infinity and path to empty as no better solution found
    min_fitness = inf
    min_path = []

    # Store fitness as progression
    all_fitnesses = []

    # Num fitness evals for termination criterion
    fitness_evals = 0

    # Store start fitness to check for convergence
    start_fitness = -1
    start_path = []

    # print(p)
    # Repeat until termination criterion is met
    while fitness_evals < n:
        paths = []
        fitnesses = []

        # Create a population of m ants:
        for _ in range(m):

            # Check if fitness condition broken
            if fitness_evals == n:
                break

            # Generate a path
            path = generate_path(
                sur_hubs=surplus_hubs, def_hubs=deficit_hubs, d=d, h=h, p=p, max_journey_size=max_journey_size, alpha=alpha, beta=beta)

            # Calculate the fitness of the solution
            ant_fitness = fitness(path=path, model=model)

            all_fitnesses.append(ant_fitness)

            fitness_evals += 1

            if ant_fitness < min_fitness:
                min_fitness = ant_fitness
                min_path = path

            # Add paths and fitnesses to population paths and fitnesses
            paths.append(path)
            # print()
            # print(path)
            fitnesses.append(ant_fitness)

        # Update the pheromone using the population

        update_pheromone(p=p, paths=paths, fitnesses=fitnesses, e=e, Q=Q)

        # print()
        # print()
        # print(p)

    # for row in p:
    #     print(row)

    # print()
    # start_path.sort(key=lambda j: (j['from'], j['to'], -j['s']))
    # print(start_path)
    # print()
    # min_path.sort(key=lambda j: (j['from'], j['to'], -j['s']))
    # print(min_path)

    return all_fitnesses
