"""
Tests the matrix creation functions of AS
"""
import unittest
from TNRP_model.depot import Depot
from searches.aco.create_matrices import create_dist_matrix, create_pher_matrix, create_heur_matrix


class TestASMatricesClass(unittest.TestCase):
    """
    Class for testing AS matrix creation
    """
    model = {}

    @classmethod
    def setUpClass(self):
        """Setup for the tests (to create the model)"""
        # Create 3 depots
        dep0 = Depot(name=0, s=-5, x=0, y=0)
        dep1 = Depot(name=1, s=6, x=3, y=4)
        dep2 = Depot(name=2, s=10, x=5, y=12)

        # Place in an array
        self.model = {0: dep0, 1: dep1, 2: dep2}

        # Add the connections
        dep0.add_connection(dep1)
        dep0.add_connection(dep2)
        dep1.add_connection(dep2)

    def test_distance_matrix_creation(self):
        """
        Tests that the distance matrix is created correctly
        """
        # Obtain the distance matrix
        dist_matrix = create_dist_matrix(self.model)

        # The expected dist matrix
        expected_matrix = [
            [0, 5, 13],
            [5, 0, 8.246],
            [13, 8.246, 0]
        ]

        # Make sure each value in the distance matrix is within 3 decimal places of expected matrix
        for row in range(len(dist_matrix)):
            for col in range(len(dist_matrix[row])):
                self.assertAlmostEqual(
                    dist_matrix[row][col], expected_matrix[row][col], 3)

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

            # If the depot is a deficit depot, make sure whole row is 0
            if self.model[i].get_s() < 0:
                self.assertTrue((pher_matrix[i] == [0] * len(dist_matrix)))
                continue

            # For each element in the row of a surplus depot
            for j in range(0, len(dist_matrix)):
                # If i and j are same (pheromone for journey from a depot to itself) pheromone is 0
                if i == j:
                    self.assertEqual(pher_matrix[i][j], 0)
                else:
                    # Make sure pheromone value is between 0 and 1
                    self.assertGreater(pher_matrix[i][j], 0)
                    self.assertLessEqual(pher_matrix[i][j], 1)

    def test_heuristic_matrix_creation(self):
        """
        Tests that the heuristic matrix is created correctly
        """
        # Create a distance matrix
        dist_matrix = [
            [0, 4, 2],
            [4, 0, 4],
            [2, 4, 0]
        ]

        # Calculate heuristic matrix
        h_matrix = create_heur_matrix(dist_matrix=dist_matrix)

        # Make sure 1/each val is returned
        expected = [
            [0, 0.25, 0.5],
            [0.25, 0, 0.25],
            [0.5, 0.25, 0]
        ]

        # Assert equal
        self.assertEqual(h_matrix, expected)
