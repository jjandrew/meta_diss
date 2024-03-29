"""
Tests for the repeated functions throughout the project
"""

import unittest
from model.depot import Depot
from utils import fitness, is_resolved, apply_path, is_complete
from model.tnrp_model import create_model
from searches.random_search import random_search
import copy


class TestUtilsClass(unittest.TestCase):
    """
    Test class for the repeated functions
    """
    model = {}

    def setUp(self):
        """Setup for the tests (to create the model)"""
        # Create 3 depots
        dep0 = Depot(name=0, s=-5, x=0, y=0)
        dep1 = Depot(name=1, s=0, x=3, y=4)
        dep2 = Depot(name=2, s=10, x=5, y=12)

        # Place in a dictionary
        self.model = {0: dep0, 1: dep1, 2: dep2}

        # Add the connections
        dep0.add_connection(dep1)
        dep0.add_connection(dep2)
        dep1.add_connection(dep2)

    def test_fitness_function(self):
        """
        Unit test for the fitness function calculating the distance of a solution
        """
        # Create an example solution
        solution = [
            {'from': 0, 'to': 1, 's': 10},  # dist 5
            {'from': 0, 'to': 2, 's': 10},  # dist 13
            {'from': 0, 'to': 1, 's': 10}  # dist 5
        ]  # total dist of 23
        dist = fitness(path=solution, model=self.model)

        self.assertEqual(23, dist)

    def test_model_resolved(self):
        """
        Test the function that checks if a model has been resolved
        """
        # Test unresolved model (shown in test suite) is not complete
        self.assertFalse(is_resolved(model=self.model))

        # Now test a correct one is complete
        # Create 3 depots that are resolved
        dep0 = Depot(name=0, s=0, x=0, y=0)
        dep1 = Depot(name=1, s=0, x=1, y=2)
        dep2 = Depot(name=2, s=0, x=2, y=0)
        # Place in an array
        model = {0: dep0, 1: dep1, 2: dep2}
        # check it is resolved
        self.assertTrue(is_resolved(model=model))

    def test_apply_path(self):
        """
        Tests the application of a path to the model
        """
        # Create an example path
        path = [
            {'from': 0, 'to': 1, 's': 10},
            {'from': 0, 'to': 2, 's': 10},
            {'from': 0, 'to': 1, 's': 11}
        ]
        20, -35, 20
        # Apply the path to the model
        apply_path(path=path, model=self.model)

        # Check that supply values are valid for each depot
        self.assertEqual(self.model[0].get_s(), -36)
        self.assertEqual(self.model[1].get_s(), 21)
        self.assertEqual(self.model[2].get_s(), 20)

    def test_is_complete(self):
        """
        Tests the is complete function which checks if a path resolves a model
        """
        # Create the model
        dep0 = Depot(name=0, s=-6, x=0, y=0)
        dep1 = Depot(name=1, s=-4, x=3, y=4)
        dep2 = Depot(name=2, s=10, x=5, y=12)

        model = {0: dep0, 1: dep1, 2: dep2}

        # Create a path that resolves the model
        path = [
            {'from': 2, 'to': 1, 's': 4},
            {'from': 2, 'to': 0, 's': 2},
            {'from': 2, 'to': 0, 's': 4}
        ]

        self.assertTrue(is_complete(path=path, original_model_state=model))

    def test_is_complete_false_if_path_doesnt_resolve(self):
        """
        Tests the is complete function returns false is a path doesn't resolve a model
        """
        # Create the model
        dep0 = Depot(name=0, s=-6, x=0, y=0)
        dep1 = Depot(name=1, s=-4, x=3, y=4)
        dep2 = Depot(name=2, s=10, x=5, y=12)

        model = {0: dep0, 1: dep1, 2: dep2}

        # Create a path that doesnt resolve the model
        path = [
            {'from': 2, 'to': 1, 's': 3},
            {'from': 2, 'to': 0, 's': 2},
            {'from': 2, 'to': 0, 's': 2}
        ]

        self.assertFalse(is_complete(path=path, original_model_state=model))
