"""
Tests for the repeated functions throughout the project
"""

import unittest
from src.classes.hub import Hub
from src.utils import calc_distance, get_closest_hub, reduce_model


class TestModelCreation(unittest.TestCase):
    """
    Test class for the repeated functions
    """
    model = []

    def setUp(self):
        """Setup for the tests (to create the model)"""
        # Create 3 hubs
        hub0 = Hub(name=0, s=-5, long=0, lat=0)
        hub1 = Hub(name=1, s=0, long=1, lat=2)
        hub2 = Hub(name=2, s=10, long=2, lat=0)

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

    def test_get_closest_hub(self):
        """
        Tests it is possible to get a closest hub
        """
        # Use hub 0 from the model
        hub = self.model[0]
        # Find its closest hub
        closest_hub = get_closest_hub(hub=hub, model=self.model)

        # check this is hub 1
        self.assertEqual(closest_hub, self.model[2])

    def test_reduce_model(self):
        """
        Tests the model can be successfully reduced
        """
        model_reduction_journeys = reduce_model(
            model=self.model, max_journey_size=3)

        expected_journeys = [
            {'from': 2, 'to': 0, 's': 3},
            {'from': 2, 'to': 0, 's': 2}
        ]

        self.assertEqual(model_reduction_journeys, expected_journeys)
