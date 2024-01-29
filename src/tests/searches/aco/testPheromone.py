"""
Unit tests for the pheromone update function
"""
import unittest
from searches.aco.pheromone import update_pheromone


class TestPheromoneClass(unittest.TestCase):
    """
    Class for carrying out unit tests on pheromone function
    """
    p = []

    def setUp(self) -> None:
        """
        The setup class, creating a pheromone matrix
        """
        self.p = [
            [0, 1, 1],
            [1, 0, 1],
            [1, 1, 0]
        ]

    def test_pheromone_evaporated(self):
        """
        Tests the pheromone is evaporated
        """
        e = 0.1  # Evaporation rate of 10%

        expected = [
            [0, 0.9, 0.9],
            [0.9, 0, 0.9],
            [0.9, 0.9, 0]
        ]

        # Update the pheromone and check it is evaporated
        update_pheromone(p=self.p, paths=[], costs=[], e=e, Q=1)

        self.assertEqual(self.p, expected)

    def test_pheromone_added(self):
        """
        Tests that pheromone is added correctly
        """
        # Create two paths
        paths = [
            [{'from': 0, 'to': 1, 's': 10}],
            [{'from': 1, 'to': 2, 's': 5}, {'from': 1, 'to': 0, 's': 5}]
        ]

        # Assign costs
        costs = [5, 10]

        # Create Q to a common multiple of 5 and 10
        Q = 10

        # Update pheromone without evaporation
        update_pheromone(p=self.p, paths=paths, costs=costs, e=0, Q=Q)

        # create expected new pheromone matrix
        expected = [
            [0, 3, 1],
            [2, 0, 2],
            [1, 1, 0]
        ]

        # check pheromone matrix changed correctly
        self.assertEqual(self.p, expected)
