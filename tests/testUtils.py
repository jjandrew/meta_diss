"""
Tests for the repeated functions throughout the project
"""

import unittest
from src.classes.hub import Hub
from src.utils import calc_distance


class TestModelCreation(unittest.TestCase):
    """
    Test class for the repeated functions
    """
    model = []

    def setUp(self):
        """Setup for the tests (to create the model)"""
        # Create 3 hubs
        hub0 = Hub(name=0, s=0, long=0, lat=0)
        hub1 = Hub(name=1, s=0, long=1, lat=2)
        hub2 = Hub(name=2, s=0, long=2, lat=0)

        # Place in an array
        self.model = [hub0, hub1, hub2]

        # Add the connections
        hub0.add_connection(hub1)
        hub0.add_connection(hub2)
        hub1.add_connection(hub2)

    def test_fitness_function(self):
        """
        Unit test for the fitness function calculating the distance of a solution
        """
        # Create an example solution
        solution = [
            {'from': 0, 'to': 1, 's': 10},  # dist 3
            {'from': 0, 'to': 2, 's': 10},  # dist 2
            {'from': 0, 'to': 1, 's': 10},  # dist 3
            {'from': 2, 'to': 1, 's': 10}  # dist 3
        ]  # total dist of 11
        dist = calc_distance(path=solution, hubs=self.model)

        self.assertEqual(11, dist)
