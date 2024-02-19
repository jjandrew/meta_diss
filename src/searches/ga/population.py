"""
Encodes a solution into a chromosome
"""
from typing import Dict, List, Tuple
import copy
from model.hub import Hub
from searches.random import random_search


def encode_solution(path: List[Dict[str, int]]) -> List[Tuple[int, int, int]]:
    """
    Converts a path into a chromosome of form [{from, to, s}] to [(from, to, s)]

    params
        path - Path as a dictionary of [{from, to, s}]

    Returns
        Chromosome of [(from, to, s)]
    """
    encoded = []
    # For each journey in the path
    for j in path:
        # Convert into a tuple
        encoded_j = (j['from'], j['to'], j['s'])
        encoded.append(encoded_j)
    return encoded


def decode_solution(path: List[Tuple[int, int, int]]) -> List[Dict[str, int]]:
    """
    Converts a path from a chromosome of form [(from, to, s)] to [{from, to, s}]

    params
        path -  A list of tuples representing the journey of form (from, to, s)

    returns
        A list of dictionaries of journeys of form: [{from, to s}]
    """
    decoded = []
    for j in path:
        # Convert tuple into dictionary
        decoded_j = {'from': j[0], 'to': j[1], 's': j[2]}
        decoded.append(decoded_j)
    return decoded


def gen_pop(pop_size: int, model: Dict[int, Hub], max_journey_size: int) -> List[List[Tuple[int, int, int]]]:
    """
    Generates an initial population for the genetic algorithm as a list of chromosomes

    params
        pop_size - The size of the population returned
        model - The model the algorithm is performed on of type hub_name: Hub object
        max_journey_size - The maximum size journey for the problem

    returns
        List of solutions, represented as genomes of (from_hub, to_hub, s) for each journey
    """
    pop = []
    while len(pop) < pop_size:
        # Generate a copy of the model
        model_copy = copy.deepcopy(model)
        # Generate a random solution
        path = random_search(
            model=model_copy, max_journey_size=max_journey_size)
        # Add the encoded solution to the population
        pop.append(encode_solution(path=path))
    return pop
