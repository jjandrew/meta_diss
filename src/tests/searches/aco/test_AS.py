"""
Tests for the main ACO algorithm
"""
import unittest
from typing import List, Dict
from searches.aco.create_matrices import create_dist_matrix, create_pher_matrix, create_heur_matrix
from searches.aco.AS import AS
from model.depot import Depot
from model.tnrp_model import create_model


class TestASClass(unittest.TestCase):
    """
    Class for the testing of the AS algorithm
    """
    model = {}

    def test_AS(self):
        """
        Tests the AS algorithm uses the correct representation method for paths
        And tests AS uses the correct number of fitness calculations.
        """
        model = create_model(n=50, alpha=2)

        # Generate the distance and pheromone matrices
        d = create_dist_matrix(model=model)
        p = create_pher_matrix(model=model, dist_matrix=d)
        h = create_heur_matrix(dist_matrix=d)

        max_journey_size = 5

        # Perform the AS algorithm
        fitnesses, path = AS(
            model=model, m=1, e=0.5, Q=10, d=d, p=p, h=h, n=100, max_journey_size=max_journey_size)

        # Check 100 fitness calculations
        self.assertEqual(100, len(fitnesses))

        # Check that the best path is of the correct type
        self.assertIsInstance(path, List)
        for journey in path:
            self.assertIsInstance(journey, Dict)
            for key, value in journey.items():
                self.assertIsInstance(key, str)
                self.assertIsInstance(value, int)
