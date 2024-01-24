"""
A brute force approach to solving the problem
"""
from typing import List, Dict
from src.classes.hub import Hub


def brute(model: List[Hub], max_journey_size: int) -> List[Dict[str, int]]:
    """
    Performs a brute force search on the model that is passed in

    params:
        model - a list of hubs which have a supply value to be solved
        max_journey_size - The maximum number of goods that can be moved between hubs

    returns
        List[{from, to, s}]
    """
