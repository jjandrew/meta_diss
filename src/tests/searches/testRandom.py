"""
Tests for the random search method
"""

import unittest
from searches.random.random import random_search
from model.hub import Hub
from model.model import create_model


class TestRandomSolutionClass(unittest.TestCase):
    """
    Test clas for the random search method
    """
    model = create_model(n=10000, alpha=2)

    def test_random_search(self):
        """Checks that the function returns a valid solution"""
        # Sum the absolute s values of the models
        model_abs_s = 0
        for hub in self.model:
            model_abs_s += abs(hub.get_s())

        solution = random_search(model=self.model, max_journey_size=20)

        solution_s = 0
        for s in solution:
            solution_s += s['s']

        # Assert absolute sum of solution s = 2 * sum of absolute of original s of model
        self.assertEqual(model_abs_s, solution_s * 2)
