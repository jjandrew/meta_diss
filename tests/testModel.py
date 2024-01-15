"""
Tests for model creation
"""
import unittest
from src.model.model import create_empty_matrix, create_matrix, create_model


class TestModelCreation(unittest.TestCase):
    """Tests the model creation"""

    def test_create_empty_matrix(self):
        """Tests an empty matrix of the correct length can be created"""
        # Create a 6 x 6 matrix using n=3, a=2
        n = 3
        a = 2
        empty_matrix = create_empty_matrix(alpha=a, n=n)

        # Check there are a*n rows
        self.assertEqual(n*a, len(empty_matrix))

        # For each row
        for i in range(n*a):
            # Check there are n*a elements in the row
            self.assertEqual(n*a, len(empty_matrix[i]))

            # For each element in the row
            for j in range(n*a):
                # Check element is empty (shown using -1)
                self.assertEqual(-1, empty_matrix[i][j])

    def test_matrix_population(self):
        """
        Tests the empty matrix can be populated
        """
        # Create a matrix with 10 hubs, a scaling factor of 5 and a minimum distance between hubs of 2
        alpha = 5
        n = 10
        matrix = create_matrix(n=n, a=alpha, min_dist=2)

        # Check every element is present somewhere in the matrix
        # Create a set of the n hub values
        vals = set()
        for i in range(n):
            vals.add(i)

        # Loop through each element in the array and make sure all vals are present
        for i in range(n*alpha):
            for j in range(n*alpha):
                if matrix[i][j] != -1:
                    # Remove this value from the set of possible values
                    vals.remove(matrix[i][j])

        # check all vals present
        self.assertEqual(0, len(vals))

    def test_matrix_population_can_deal_with_impossible_task(self):
        """
        Tests the matrix population function can deal if not able to fit all hubs in
        """
        # Create a matrix with 10 hubs, a scaling factor of 0 and a minimum distance between hubs of 2
        alpha = 0
        n = 10
        # Test an error is thrown
        try:
            _ = create_matrix(n=n, a=alpha, min_dist=2)
            self.fail("Expected ValueError")
        except:
            pass

        # Create a matrix with 10 hubs, a scaling factor of 1 and a minimum distance between hubs of 10
        alpha = 1
        # Test an error is thrown
        try:
            _ = create_matrix(n=n, a=alpha, min_dist=10)
            self.fail("Expected ValueError")
        except:
            pass

    def test_model_creation(self):
        """
        Tests an array of hubs, with distances to each other is returned when model is created
        """

        pass
