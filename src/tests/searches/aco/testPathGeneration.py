"""
Tests a valid path can be generated using matrices
"""
import unittest
from searches.aco.pathGeneration import perform_journey
from model.hub import Hub


class TestACOPathGenerationClass(unittest.TestCase):
    """
    Class for testing the path generation in the ACO algorithms
    """

    def test_perform_journey(self):
        """
        Tests that the journey performing function works correctly
        """
        hub_0 = Hub(name=0, s=5, long=0, lat=0)
        hub_1 = Hub(name=1, s=-5, long=0, lat=0)
        hub_2 = Hub(name=2, s=10, long=0, lat=0)
        hub_3 = Hub(name=3, s=-10, long=0, lat=0)
        hub_4 = Hub(name=4, s=3, long=0, lat=0)

        max_j_size = 5

        # Create a move where both hubs resolved
        result = perform_journey(
            sur_hub=hub_0, def_hub=hub_1, max_journey_size=max_j_size)
        expected = [0, 1]
        self.assertEqual(result, expected)

        # Reset hubs
        hub_0 = Hub(name=0, s=5, long=0, lat=0)
        hub_1 = Hub(name=1, s=-5, long=0, lat=0)

        # Create a move where deficit hub is resolved
        result = perform_journey(
            sur_hub=hub_2, def_hub=hub_1, max_journey_size=max_j_size)
        expected = [1]
        self.assertEqual(result, expected)

        # Reset hubs
        hub_1 = Hub(name=1, s=-5, long=0, lat=0)
        hub_2 = Hub(name=2, s=10, long=0, lat=0)

        # Create a move where surplus hub is resolved
        result = perform_journey(
            sur_hub=hub_0, def_hub=hub_3, max_journey_size=max_j_size)
        expected = [0]
        self.assertEqual(result, expected)

        # Reset hubs
        hub_0 = Hub(name=0, s=5, long=0, lat=0)
        hub_3 = Hub(name=3, s=-10, long=0, lat=0)

        # Create a move where neither hub resolved
        result = perform_journey(
            sur_hub=hub_2, def_hub=hub_3, max_journey_size=max_j_size)
        expected = []
        self.assertEqual(result, expected)

        # Reset hubs
        hub_2 = Hub(name=2, s=10, long=0, lat=0)
        hub_3 = Hub(name=3, s=-10, long=0, lat=0)

        # Create a move where j size is less than max_j_size
        result = perform_journey(
            sur_hub=hub_4, def_hub=hub_1, max_journey_size=max_j_size)
        expected = [4]
        self.assertEqual(result, expected)
