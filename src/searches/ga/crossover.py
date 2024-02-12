"""
Performs the crossover method for a GA
"""
from typing import List, Tuple
import random


def uniform(parent_1: List[Tuple[int, int, int]], parent_2: List[Tuple[int, int, int]]) -> Tuple[List[Tuple[int, int, int]], List[Tuple[int, int, int]]]:
    """
    Performs a uniform crossover on two parents. 
    This means that each gene in the child will be randomly taken from either parent using a coin toss.
    Genes being chosen are which parent the trips to a deficit node are used.

    params
        parent_1 - The first parent solution
        parent_2 - The second parent solution

    Returns
        Two children which have inherited alternative characteristics from each parent
    """
    # Create a dictionary of deficit nodes and corresponding journeys
    parent_1_def_nodes = {}
    # For each journey in parent 1
    for j in parent_1:
        # Deficit node is always in middle position
        def_node = j[1]

        # If def_node in parent_1_def_nodes append j to parent_1_def_nodes[def_node]
        if def_node in parent_1_def_nodes:
            parent_1_def_nodes[def_node].append(j)
        # Otherwise create new entry of parent_1_def_nodes[def_node] = j
        else:
            parent_1_def_nodes[def_node] = [j]

    # Create a dictionary of deficit nodes and corresponding journeys
    parent_2_def_nodes = {}
    # For each journey in parent 2
    for j in parent_2:
        # Deficit node is always in middle position
        def_node = j[1]

        # If def_node in parent_2_def_nodes append j to parent_2_def_nodes[def_node]
        if def_node in parent_2_def_nodes:
            parent_2_def_nodes[def_node].append(j)
        # Otherwise create new entry of parent_2_def_nodes[def_node] = j
        else:
            parent_2_def_nodes[def_node] = [j]

    # Create the two children
    child_1 = []
    child_2 = []

    # For each deficit node in the set of deficit nodes
    for def_node in set(parent_1_def_nodes):
        # Choose a random boolean value (0 or 1)
        random_bool = random.choice([0, 1])

        # Need to find all journeys to the deficit node for each parent
        parent_1_js_to_node = parent_1_def_nodes.get(def_node, [])
        parent_2_js_to_node = parent_2_def_nodes.get(def_node, [])

        # If 0 then child 1 gets the corresponding gene from parent 1 and child 2 gets gene from parent 2
        if random_bool == 0:
            child_1.extend(parent_1_js_to_node)
            child_2.extend(parent_2_js_to_node)

        # Else if 1 then child 1 gets corresponding gene from parent 2 and child 2 gets gene from parent 1
        else:
            child_1.extend(parent_2_js_to_node)
            child_2.extend(parent_1_js_to_node)

    # Return the children
    return child_1, child_2
