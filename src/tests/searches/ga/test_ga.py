"""
Tests the GA 
"""
import unittest
from typing import List, Dict
from model.tnrp_model import create_model
from searches.ga.ga import ga


class TestGAClass(unittest.TestCase):
    """
    Tests the GA uses the correct representation
    """

    def test_valid_solution(self):
        model = create_model(n=30, alpha=2)
        _, path = ga(mutation_rate=0.1, pop_size=40, t_size=10,
                     n=100, model=model, max_journey_size=20, crossover_rate=0.6)

        # Check that the best path is of the correct type
        self.assertIsInstance(path, List)
        for journey in path:
            self.assertIsInstance(journey, Dict)
            for key, value in journey.items():
                self.assertIsInstance(key, str)
                self.assertIsInstance(value, int)
