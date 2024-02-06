"""
Performs the simulated annealing algorithm
"""
from searches.random import random
from typing import Dict, List
from model.hub import Hub


def sa(n: int, cool_r: float, max_journey_size: int, model: Dict[int, Hub]) -> List[Dict[str, int]]:
    """
    Performs the Simulated annealing algorithm

    params 
        n - The number of iterations of the algorithm before termination
        cool_r - The probability that a worse solution is accepted as the algorithm progresses
        max_journey_size - The maximum journey size
        model - The initial state of the model

    returns
        The final solution
    """
