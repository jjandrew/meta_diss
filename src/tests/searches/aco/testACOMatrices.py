"""
Tests the create matrix functions of ACO
"""
import unittest
from model.hub import Hub
from searches.aco.create_matrices import create_dist_matrix, create_pher_matrix


class TestACOMatricesClass(unittest.TestCase):
    """
    Class for testing ACO matrix creation
    """
    model = {}

    @classmethod
    def setUpClass(cls):
        """Setup for the tests (to create the model)"""
        # Create 3 hubs
        hub0 = Hub(name=0, s=-5, long=0, lat=0)
        hub1 = Hub(name=1, s=6, long=1, lat=2)
        hub2 = Hub(name=2, s=10, long=2, lat=0)

        # Place in an array
        cls.model = {0: hub0, 1: hub1, 2: hub2}

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

    def test_pheromone_matrix_creation(self):
        """
        Tests that the pheromone matrix is created correctly
        """
        # The dist matrix to be used
        dist_matrix = [
            [0, 3, 2],
            [3, 0, 3],
            [2, 3, 0]
        ]

        # Create a pheromone matrix
        pher_matrix = create_pher_matrix(
            model=self.model, dist_matrix=dist_matrix)

        # Make sure correct number of rows in pheromone matrix
        self.assertEqual(len(dist_matrix), len(pher_matrix))

        # for each row
        for i in range(0, len(dist_matrix)):
            # Corresponding pheromone matrix row is of correct size
            self.assertEqual(len(pher_matrix[i]), len(dist_matrix))

            # If the hub is a deficit hub, make sure whole row is 0
            if self.model[i].get_s() < 0:
                self.assertTrue((pher_matrix[i] == [0] * len(dist_matrix)))
                continue

            # For each element in the row
            for j in range(0, len(dist_matrix)):
                # If i and j are same (pheromone for journey from a hub to itself) pheromone is 0
                if i == j:
                    self.assertEqual(pher_matrix[i][j], 0)
                else:
                    # Make sure pheromone value is between 0 and 1
                    self.assertGreater(pher_matrix[i][j], 0)
                    self.assertLessEqual(pher_matrix[i][j], 1)
