"""
Executes the main body of the AS algorithm
"""
from typing import List


def AS(m: int, e: float, Q: int, s_meth: str, d: List[List[float]], h: List[List[float]],
       p: List[List[float]]) -> int:
    """
    Performs the AS algorithm on the data

    params:
    m - population size
    e - evaporation rate
    Q - constant for fitness normalisation
    s_meth - The name of the local search method
    d - distance matrix
    h - heurstic matrix
    p - pheromone matrix

    returns:
    min_cost from the routes created
    """
