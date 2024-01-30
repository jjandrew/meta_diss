"""
Methods for the updating of a pheromone
"""
from typing import List, Dict


def update_pheromone(p: List[List[float]], paths: List[List[Dict[str, int]]], fitnesses: List[int], e: float, Q: int):
    """
    Updates the pheromone matrix of a population of ants

    params
        p - Pheromone matrix
        paths - list of paths in the population
        fitnesses - list of the corresponding path fitnesses
        e - evaporation rate (% of pheromone removed with each population)
        Q - A scaling constant for pheromone
    """
    # Evaporate edges by e%
    for v in range(len(p)):
        for n in range(len(p[v])):
            p[v][n] *= 1-e

    # Deposit pheromone
    for i in range(len(paths)):
        # Obtain the cost and path for each passed in
        path = paths[i]
        cost = fitnesses[i]
        # Add Q / cost to each of the edges used in the path
        to_add = Q / cost

        # Add the pheromone for each journey in the
        for journey in path:
            # Add to pheromone matrix for p[from][to]
            p[journey['from']][journey['to']] += to_add
