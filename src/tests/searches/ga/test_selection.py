"""
Tests the evaluation method for the genetic algorithm
"""
import unittest
from TNRP_model.depot import Depot
from searches.ga.selection import tournament


class TestGAEvaluationClass(unittest.TestCase):
    """
    Class to test the evaluation function to rank population of a GA
    """

    def test_GA_Evaluation(self):
        """
        Tests a GA population can be ranked from highest to lowest fitness
        """
        # Create a model of 4 depots
        dep_0 = Depot(name=0, s=-9, x=0, y=0)
        dep_1 = Depot(name=1, s=3, x=0, y=1)  # 1 away from 1
        dep_2 = Depot(name=2, s=3, x=0, y=2)  # 2 away from 1
        dep_3 = Depot(name=3, s=3, x=0, y=3)  # 3 away from 1

        # Connect the depots
        dep_0.add_connection(dep_1)
        dep_0.add_connection(dep_2)
        dep_0.add_connection(dep_3)

        model = {0: dep_0, 1: dep_1, 2: dep_2, 3: dep_3}

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
