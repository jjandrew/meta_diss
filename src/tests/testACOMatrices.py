"""
Tests the create matrix functions of ACO
"""
import unittest
from classes.hub import Hub
from searches.aco.create_matrices import create_dist_matrix, create_pher_matrix


class TestACOMatricesClass(unittest.TestCase):
    """
    Class for testing ACO matrix creation
    """
    model = []

    @classmethod
    def setUpClass(cls):
        """Setup for the tests (to create the model)"""
        # Create 3 hubs
        hub0 = Hub(name=0, s=-5, long=0, lat=0)
        hub1 = Hub(name=1, s=0, long=1, lat=2)
        hub2 = Hub(name=2, s=10, long=2, lat=0)

        # Place in an array
        cls.model = [hub0, hub1, hub2]

        # Add the connections
        hub0.add_connection(hub1)
        hub0.add_connection(hub2)
        hub1.add_connection(hub2)

    def test_distance_matrix_creation(self):
        """
        Tests that the distance matrix is created correctly
        """
        # Obtain the distance matrix
        dist_matrix = create_dist_matrix(self.model)

        # The expected dist matrix
        expected_matrix = [
            [0, 3, 2],
            [3, 0, 3],
            [2, 3, 0]
        ]

        # Make sure they are equal
        self.assertEqual(dist_matrix, expected_matrix)
