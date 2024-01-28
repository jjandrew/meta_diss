"""
Tests for the main ACO algorithm
"""
import unittest
from searches.aco.create_matrices import create_dist_matrix, create_pher_matrix
from searches.aco.AS import AS
from model.hub import Hub


class TestACOClass(unittest.TestCase):
    """
    Class for the testing of the ACO algorithm
    """
    model = []

    @classmethod
    def setUpClass(cls):
        """Setup for the tests (to create the model)"""
        # Create 3 hubs
        hub0 = Hub(name=0, s=10, long=0, lat=0)
        hub1 = Hub(name=1, s=-4, long=1, lat=2)
        hub2 = Hub(name=2, s=-6, long=2, lat=0)

        # Place in an array
        cls.model = [hub0, hub1, hub2]

        # Add the connections
        hub0.add_connection(hub1)
        hub0.add_connection(hub2)
        hub1.add_connection(hub2)

    def test_AS(self):
        """
        Tests the AS algorithm of ACO
        """
