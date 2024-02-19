"""
Unit tests for the crossover method of the genetic algorithm
"""
import unittest
from searches.ga.crossover import aware_crossover
from model.hub import Hub
from model.model import create_model
from searches.random import random_search
import copy
from searches.ga.population import encode_solution


class TestUniformCrossover(unittest.TestCase):
    """
    Test class for the uniform crossover function
    """

    def test_crossover_works_when_parents_identical(self):
        """
        Tests the crossover method returns two children identical to the parents
        """
        hub_0 = Hub(name=0, s=28, long=0, lat=0)
        hub_1 = Hub(name=1, s=-4, long=0, lat=0)
        hub_2 = Hub(name=2, s=-84, long=0, lat=0)
        hub_3 = Hub(name=3, s=65, long=0, lat=0)
        hub_4 = Hub(name=4, s=-16, long=0, lat=0)
        hub_5 = Hub(name=5, s=11, long=0, lat=0)

        model = {0: hub_0, 1: hub_1, 2: hub_2, 3: hub_3, 4: hub_4, 5: hub_5}

        parent1 = [{'from': 3, 'to': 4, 's': 16}, {'from': 0, 'to': 2, 's': 20}, {'from': 0, 'to': 2, 's': 8},
                   {'from': 3, 'to': 2, 's': 20}, {'from': 3, 'to': 1,
                                                   's': 4}, {'from': 3, 'to': 2, 's': 20},
                   {'from': 5, 'to': 2, 's': 11}, {'from': 3, 'to': 2, 's': 5}]

        parent2 = random_search(
            model=copy.deepcopy(model), max_journey_size=20)

        print(parent2)

        parent1 = encode_solution(path=parent1)
        parent2 = encode_solution(path=parent2)

        res_child_1, res_child_2 = aware_crossover(
            parent_1=parent1, parent_2=parent2, model=model, max_journey_size=20)

        print()
        print("Final children:")

        print(res_child_1)
        print(res_child_2)

    def test_crossover_works_when_parents_identica(self):
        """
        Tests the crossover method returns two children identical to the parents
        """

        # Create two parents
        parent1 = [(0, 1, 1), (0, 2, 2), (0, 2, 3), (0, 1, 2), (0, 3, 4)]
        parent2 = [(0, 1, 1), (0, 1, 2), (0, 2, 2), (0, 2, 3), (0, 3, 4)]

        # Generate uniorm crossover result
        # res_child_1, res_child_2 = aware_crossover(
        #     parent_1=parent1, parent_2=parent2)

        # print(res_child_1)
        # print(res_child_2)
