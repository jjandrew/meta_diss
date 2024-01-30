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
    n = 1000
    model = create_model(n=n, alpha=2)

    def test_random_search(self):
        """Checks that the function returns a valid solution"""
        # Sum the absolute s values of the models
        model_abs_s = 0
        for hub in self.model:
            model_abs_s += abs(hub.get_s())

        # Obtain a solution
        solution = random_search(model=self.model, max_journey_size=20)

        # Calculate total S and unique hubs
        solution_s = 0
        hubs = set()
        for s in solution:
            solution_s += s['s']
            hubs.add(s['to'])
            hubs.add(s['from'])

        # Assert absolute sum of solution s = 2 * sum of absolute of original s of model
        self.assertEqual(model_abs_s, solution_s * 2)

        # Check n unique hubs all used in solution
        self.assertEqual(self.n, len(hubs))
