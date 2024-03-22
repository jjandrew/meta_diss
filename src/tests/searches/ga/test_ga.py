"""
Tests the GA 
"""
import unittest
from typing import List, Dict
from model.tnrp_model import create_model
from searches.ga.ga import ga


class TestGAClass(unittest.TestCase):
    """
    Tests the GA algorithm
    """

    def test_valid_solution(self):
        """
        Tests that the GA algorithm uses the correct solution representation and number of fitness calculations
        """
        # Create a model
        model = create_model(n=30, alpha=2)

        # Perform the GA algorithm
        fitnesses, path = ga(mutation_rate=0.1, pop_size=40, t_size=10,
                             n=100, model=model, max_journey_size=20, crossover_rate=0.6)

        # Check 100 fitness evaluations
        self.assertEqual(len(fitnesses), 100)

        # Check that the best path is of the correct type
        self.assertIsInstance(path, List)
        for journey in path:
            self.assertIsInstance(journey, Dict)
            for key, value in journey.items():
                self.assertIsInstance(key, str)
                self.assertIsInstance(value, int)
