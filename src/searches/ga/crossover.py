"""
Performs the crossover method for a GA
"""
from typing import List, Tuple, Dict
from model.hub import Hub
import random
import copy
from searches.random import random_search
from searches.ga.population import encode_solution, decode_solution
from searches.sa.neighbourhood import compress_neighbour


def aware_crossover(parent_1: List[Tuple[int, int, int]], parent_2: List[Tuple[int, int, int]], model: Dict[int, Hub], max_journey_size: int) -> Tuple[List[Tuple[int, int, int]], List[Tuple[int, int, int]]]:
    """
    Performs a crossover which tries to remain aware of solution to produce two valid children
    """
    # Crate blank arrays for a child path and child models
    child_1 = []
    child_1_model = copy.deepcopy(model)
    child_2 = []
    child_2_model = copy.deepcopy(model)

    while len(parent_1) > 0 and len(parent_2) > 0:
        # Check whether to do a crossover or not
        crossover = random.choice([False, True])
        # Select a gene from parent 1 and parent 2
        parent_1_gene_idx = random.randint(0, len(parent_1) - 1)
        parent_2_gene_idx = random.randint(0, len(parent_2) - 1)
        parent_1_gene = ()
        parent_2_gene = ()
        if not crossover:
            parent_1_gene = parent_1[parent_1_gene_idx]
            parent_2_gene = parent_2[parent_2_gene_idx]
        else:
            parent_1_gene = parent_2[parent_2_gene_idx]
            parent_2_gene = parent_1[parent_1_gene_idx]
        # Delete the gene
        del parent_1[parent_1_gene_idx]
        del parent_2[parent_2_gene_idx]

        # Try and add parent 1 gene to child 1
        par_1_sur = parent_1_gene[0]
        par_1_def = parent_1_gene[1]
        par_1_s = parent_1_gene[2]
        # If the journey can be made to the model without over resolving a hub
        if child_1_model[par_1_sur].get_s() >= par_1_s and abs(child_1_model[par_1_def].get_s()) >= par_1_s:
            # Apply the journey
            child_1.append(parent_1_gene)
            # Move within the model
            Hub.move_s(start=child_1_model[par_1_sur],
                       end=child_1_model[par_1_def], s=par_1_s)

        else:  # A hub is going to be resolved
            # Add as much as possible to resolve a hub
            min_s = min(child_1_model[par_1_sur].get_s(), abs(
                child_1_model[par_1_def].get_s()))
            # check there is a journey to add
            if min_s != 0:
                # Create the journey
                journey = (par_1_sur, par_1_def, min_s)
                # Add to the child
                child_1.append(journey)
                # Move within the model
                Hub.move_s(start=child_1_model[par_1_sur],
                           end=child_1_model[par_1_def], s=min_s)

        # Try and add parent 2 gene to child 2
        par_2_sur = parent_2_gene[0]
        par_2_def = parent_2_gene[1]
        par_2_s = parent_2_gene[2]
        # If the journey can be made to the model without over resolving a hub
        if child_2_model[par_2_sur].get_s() >= par_2_s and abs(child_2_model[par_2_def].get_s()) >= par_2_s:
            # Apply the journey
            child_2.append(parent_2_gene)
            # Move within the model
            Hub.move_s(start=child_2_model[par_2_sur],
                       end=child_2_model[par_2_def], s=par_2_s)

        else:  # A hub is going to be resolved
            # Add as much as possible to resolve a hub
            min_s = min(child_2_model[par_2_sur].get_s(), abs(
                child_2_model[par_2_def].get_s()))
            # check there is a journey to add
            if min_s != 0:
                # Create the journey
                journey = (par_2_sur, par_2_def, min_s)
                # Add to the child
                child_2.append(journey)
                # Move within the model
                Hub.move_s(start=child_2_model[par_2_sur],
                           end=child_2_model[par_2_def], s=min_s)

    # Now want to add the final journeys to resolve a model using a random search
    final_child_1_paths = encode_solution(random_search(
        model=child_1_model, max_journey_size=max_journey_size))
    child_1.extend(final_child_1_paths)

    final_child_2_paths = encode_solution(random_search(
        model=child_2_model, max_journey_size=max_journey_size))
    child_2.extend(final_child_2_paths)

    # Now compress the solutions
    # Using the compression program from SA algorithm
    encoded_child_1 = decode_solution(path=child_1)
    compressed_child_1 = compress_neighbour(
        path=encoded_child_1, max_journey_size=max_journey_size)
    child_1 = encode_solution(path=compressed_child_1)

    # Using the compression program from SA algorithm
    encoded_child_2 = decode_solution(path=child_2)
    compressed_child_2 = compress_neighbour(
        path=copy.deepcopy(encoded_child_2), max_journey_size=max_journey_size)
    child_2 = encode_solution(path=compressed_child_2)

    return child_1, child_2
