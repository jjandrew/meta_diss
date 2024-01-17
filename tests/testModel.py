"""
Tests for model creation
"""
import unittest
from src.model.model import create_empty_matrix, create_locations, create_model, generate_s_vals
from src.classes.hub import Hub


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
        a = 5
        n = 10
        locs = create_locations(n=n, alpha=a, min_dist=2)

        # Check every element is present somewhere in the matrix
        # Create a set of the n hub values
        vals = set()
        for i in range(n):
            vals.add(i)

        # Loop through each element in the array and make sure all vals are present
        for hub in locs:
            vals.remove(hub['name'])

        # check all vals present
        self.assertEqual(0, len(vals))

        # Check all hub locations are unique
        locs_set = set()
        for hub in locs:
            if (hub['long'], hub['lat']) in locs_set:
                self.fail("Repeated location present in model")
            locs_set.add((hub['long'], hub['lat']))

    def test_matrix_population_can_deal_with_impossible_task(self):
        """
        Tests the matrix population function can deal if not able to fit all hubs in
        """
        # Create a matrix with 10 hubs, a scaling factor of 0 and a minimum distance between hubs of 2
        alpha = 0
        n = 10
        # Test an error is thrown
        try:
            _ = create_locations(n=n, a=alpha, min_dist=2)
            self.fail("Expected ValueError")
        except:
            pass

        # Create a matrix with 10 hubs, a scaling factor of 1 and a minimum distance between hubs of 10
        alpha = 1
        # Test an error is thrown
        try:
            _ = create_locations(n=n, a=alpha, min_dist=10)
            self.fail("Expected ValueError")
        except:
            pass

    def test_model_creation(self):
        """
        Tests an array of hubs, with distances to each other is returned when valid model is requested
        """
        # Create a 3 hub model
        n = 3
        alpha = 2
        model = create_model(n=n, alpha=alpha, min_dist=1,
                             max_def=-100, max_sur=100)

        # Test 3 hubs are returned
        self.assertEqual(3, len(model))

        # Test every item in the model is a hub object
        for hub in model:
            self.assertIsInstance(hub, Hub)

        # Check the sum of s of all hubs is 0
        sum_s = 0
        for hub in model:
            sum_s += hub.get_s()
        self.assertEqual(0, sum_s)

        # Check s value of hub class is 0
        self.assertEqual(0, Hub.get_total_s())

        # Check hubs aren't initialised with s=0
        for hub in model:
            self.assertNotEqual(0, hub.get_s())

        # Check the distances between hubs are correct manhattan distances and all distances are present
        # Compare all possible pairs of hubs
        for i in range(len(model)):
            for j in range(i, len(model)):
                # Get longitude and latitude for the first hub in pair
                long_1 = model[i].get_long()
                lat_1 = model[i].get_lat()

                # Get longitude and latitude for the second hub in the pair
                long_2 = model[j].get_long()
                lat_2 = model[j].get_lat()

                # Calculate manhattan distance
                dist = abs(long_1 - long_2) + abs(lat_1 - lat_2)

                # Check connection present in both
                connections_1 = model[i].get_connections()
                connections_2 = model[j].get_connections()

                # Check connection in 1st of pair
                self.assertEqual(dist, connections_1[j])

                # Check connection in 2nd of the pair
                self.assertEqual(dist, connections_2[i])

    def test_generate_s_vals(self):
        """Test that generate_s_vals method correctly assigns values to s attribute"""
        # Generate 100 values between -100 and 100
        vals = generate_s_vals(n=100, max_def=-100, max_sur=100)

        # Check 100 values
        self.assertEqual(100, len(vals))

        # Sum each of the values
        sum_vals = 0
        for v in vals:
            # check each val between -100 and 100
            self.assertTrue(-100 <= v <= 100)
            # check each val not 0
            self.assertNotEqual(v, 0)

            # Add to the sum
            sum_vals += v
        # check sums to 0
        self.assertEqual(sum_vals, 0)
