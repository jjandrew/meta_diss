"""
Tests for the main ACO algorithm
"""
import unittest
from searches.aco.create_matrices import create_dist_matrix, create_pher_matrix, create_heur_matrix
from searches.aco.AS import AS
from model.hub import Hub
from model.model import create_model


class TestACOClass(unittest.TestCase):
    """
    Class for the testing of the ACO algorithm
    """
    model = {}

    @classmethod
    def setUpClass(cls):
        """Setup for the tests (to create the model)"""
        # Create 3 hubs
        hub0 = Hub(name=0, s=10, long=0, lat=0)
        hub1 = Hub(name=1, s=-4, long=1, lat=2)
        hub2 = Hub(name=2, s=-6, long=2, lat=0)

        # Place in a dictionary of name: Hub
        cls.model = {0: hub0, 1: hub1, 2: hub2}

        # Add the connections
        hub0.add_connection(hub1)
        hub0.add_connection(hub2)
        hub1.add_connection(hub2)

    def test_AS(self):
        """
        Tests the AS algorithm of ACO
        """
        model = create_model(n=100, alpha=2)

        # Generate the distance and pheromone matrices
        d = create_dist_matrix(model=model)
        p = create_pher_matrix(model=model, dist_matrix=d)
        h = create_heur_matrix(dist_matrix=d)

        max_journey_size = 5

        # Perform the AS algorithm
        path, fitness, start_fitness = AS(
            model=model, m=1, e=0.5, Q=10, d=d, p=p, h=h, n=100, max_journey_size=max_journey_size)

        self.assertLessEqual(fitness, start_fitness)
