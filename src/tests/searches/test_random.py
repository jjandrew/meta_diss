"""
Tests for the random search method
"""
import unittest
from typing import List, Dict
from searches.random_search import random_search
from TNRP_model.tnrp_model import create_model


class TestRandomSolutionClass(unittest.TestCase):
    """
    Test class for the random search method
    """
    n = 50
    model = create_model(n=n, alpha=2)

    def test_random_search(self):
        """
        Checks that the random search returns a valid solution
        """
        # Calculte the total absolute s values of the models
        model_abs_s = 0
        for dep_name in self.model:
            dep = self.model[dep_name]
            model_abs_s += abs(dep.get_s())

        # Obtain a solution
        solution = random_search(model=self.model, max_journey_size=20)

        # Calculate total S of solution and number of unique depots
        solution_s = 0
        deps = set()
        for s in solution:
            solution_s += s['s']
            deps.add(s['to'])
            deps.add(s['from'])

        # Assert absolute sum of solution s = 2 * sum of absolute of original s of model
        self.assertEqual(model_abs_s, solution_s * 2)

        # Check n unique depots all used in solution
        self.assertEqual(self.n, len(deps))

        # Check that the solution is of the correct type
        self.assertIsInstance(solution, List)
        for journey in solution:
            self.assertIsInstance(journey, Dict)
            for key, value in journey.items():
                self.assertIsInstance(key, str)
                self.assertIsInstance(value, int)
