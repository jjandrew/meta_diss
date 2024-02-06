"""
Tests the evaluation method for the genetic algorithm
"""
import unittest
from model.hub import Hub
from searches.ga.evalutation import rank_pop


class TestGAEvaluationClass(unittest.TestCase):
    """
    Class to test the evaluation function to rank population of a GA
    """

    def test_GA_Evaluation(self):
        """
        Tests a GA population can be ranked from highest to lowest fitness
        """
        # Create a model of 4 hubs
        hub_0 = Hub(name=0, s=-9, long=0, lat=0)
        hub_1 = Hub(name=1, s=3, long=0, lat=1)  # 1 away from 1
        hub_2 = Hub(name=2, s=3, long=0, lat=2)  # 2 away from 1
        hub_3 = Hub(name=3, s=3, long=0, lat=3)  # 3 away from 1

        # Connect the hubs
        hub_0.add_connection(hub_1)
        hub_0.add_connection(hub_2)
        hub_0.add_connection(hub_3)

        model = {0: hub_0, 1: hub_1, 2: hub_2, 3: hub_3}

        # Create a population of 3 solutions, out of order
        pop = [
            [(0, 2, 1), (0, 2, 1), (0, 1, 1)],  # Fitness - 6
            [(0, 1, 1), (0, 1, 1), (0, 1, 1)],  # Fitness - 3
            [(0, 3, 1), (0, 3, 1), (0, 3, 1)]  # Fitness - 9
        ]

        # Expected to be ordered from highest to lowest
        expected = [
            [(0, 3, 1), (0, 3, 1), (0, 3, 1)],  # Fitness - 9
            [(0, 2, 1), (0, 2, 1), (0, 1, 1)],  # Fitness - 6
            [(0, 1, 1), (0, 1, 1), (0, 1, 1)]  # Fitness - 3
        ]

        rank_pop(pop=pop, model=model)

        self.assertEqual(pop, expected)
