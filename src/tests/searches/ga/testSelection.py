"""
Tests the evaluation method for the genetic algorithm
"""
import unittest
from model.hub import Hub
from searches.ga.selection import tournament


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
            [(0, 1, 1), (0, 1, 1), (0, 1, 1)],  # Cost - 3
            [(0, 2, 1), (0, 2, 1), (0, 2, 1)],  # Cost - 6
            [(0, 3, 1), (0, 3, 1), (0, 3, 1)]  # Cost - 9
        ]

        # Check that the best is returned in a tournament of size of population
        selected = tournament(pop=pop, t_size=3, model=model)

        # Obtain the expected journey
        expected_j = [(0, 1, 1), (0, 1, 1), (0, 1, 1)]

        self.assertEqual(selected, expected_j)

        # Check that one of the best two are returned when t_size = 2

        # Create the second expected
        expected_j_2 = [(0, 2, 1), (0, 2, 1), (0, 2, 1)]

        for _ in range(10):
            selected = tournament(pop=pop, t_size=2, model=model)
            self.assertTrue(selected == expected_j or selected == expected_j_2)
