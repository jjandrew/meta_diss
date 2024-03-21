"""
Tests for TNRP model creation
"""
import unittest
from model.tnrp_model import create_empty_matrix, create_locations, create_model, generate_s_vals
from model.depot import Depot
from math import sqrt


class TestModelCreationClass(unittest.TestCase):
    """Tests the model TNRP creation"""

    def test_create_empty_matrix(self):
        """Tests an empty matrix of the correct length can be created"""
        # Create a 6 x 6 matrix using n=3, a=2
        n = 3
        a = 2
        empty_matrix = create_empty_matrix(alpha=a, n=n)

        # Check there are n*a rows
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
        Tests it is possible to obtain unique depots in the matrix
        """
        # Create a matrix with 10 depots, a scaling factor of 5 and a minimum distance between depots of 2
        a = 5
        n = 10
        locs = create_locations(n=n, alpha=a)

        # Check every element is present somewhere in the matrix
        # Create a set of the n depot values
        vals = set()
        for i in range(n):
            vals.add(i)

        # Loop through each element in the array and remove the names of depts
        for depot in locs:
            vals.remove(depot['name'])

        # check no depots
        self.assertEqual(0, len(vals))

        # Check all depot locations are unique
        locs_set = set()
        for dep in locs:
            if (dep['long'], dep['lat']) in locs_set:
                self.fail("Repeated location present in model")
            locs_set.add((dep['long'], dep['lat']))

    def test_matrix_population_can_deal_with_impossible_task(self):
        """
        Tests the matrix population function can deal if not able to fit all depots in
        """
        # Create a matrix with 10 depots, a scaling factor of 0 and a minimum distance between depots of 2
        alpha = 0
        n = 10
        # Test an error is thrown
        try:
            _ = create_locations(n=n, alpha=alpha)
            self.fail("Expected ValueError")
        except ValueError:
            pass
        except:
            self.fail("Unexpected error")

        # Create a matrix with 10 depots, a scaling factor of 0.9 and a minimum distance between depots of 10
        alpha = 0.9
        # Test an error is thrown
        try:
            _ = create_locations(n=n, alpha=alpha)
            self.fail("Expected ValueError")
        except ValueError:
            pass
        except:
            self.fail("Unexpected error")

        # Create a matrix with 10 depots, a scaling factor of 1 and a minimum distance between depots of 10
        alpha = 1
        # Test no error is thrown
        try:
            _ = create_locations(n=n, alpha=alpha)
            pass
        except ValueError:
            self.fail("Create location threw an error for alpha=1")
        except:
            self.fail("Unexpected error")

    def test_generate_s_vals(self):
        """
        Test that generate_s_vals method correctly returns valid supply values
        """
        # Generate 100 values between -100 and 100
        vals = generate_s_vals(n=100, max_def=-100, max_sur=100)

        # Check there are 100 values
        self.assertEqual(100, len(vals))

        # Sum each of the values
        sum_vals = 0
        for v in vals:
            # check each val is between -100 and 100
            self.assertTrue(-100 <= v <= 100)

            # check each val is not 0
            self.assertNotEqual(v, 0)

            # Add to the sum
            sum_vals += v

        # check sum of supply values is 0
        self.assertEqual(sum_vals, 0)

    def test_model_creation(self):
        """
        Tests an array of depots, with distances to each other is returned when valid model is requested
        """
        # Create a 3 depot model
        n = 3
        alpha = 2
        model = create_model(n=n, alpha=alpha,
                             max_def=-100, max_sur=100)

        # Test 3 depots are returned
        self.assertEqual(3, len(model))

        # Test every item in the model is a depot object
        for dep in model:
            self.assertIsInstance(model[dep], Depot)

        # Check the sum of s of all depots is 0
        sum_s = 0
        for dep in model:
            sum_s += model[dep].get_s()
        self.assertEqual(0, sum_s)

        # Check depts aren't initialised with s=0
        for dep in model:
            self.assertNotEqual(0, model[dep].get_s())

        # Check the distances between depots are correct euclidean distances and all distances are present
        # Compare all possible pairs of depots
        for i in range(len(model)):
            for j in range(i, len(model)):
                # Get longitude and latitude for the first depot in pair
                long_1 = model[i].get_long()
                lat_1 = model[i].get_lat()

                # Get longitude and latitude for the second depot in the pair
                long_2 = model[j].get_long()
                lat_2 = model[j].get_lat()

                # Calculate euclidean distance
                dist = sqrt((long_1 - long_2)**2 + (lat_1 - lat_2)**2)

                # Check connection present in both
                connections_1 = model[i].get_connections()
                connections_2 = model[j].get_connections()

                # Check connection in 1st of pair
                self.assertEqual(dist, connections_1[j])

                # Check connection in 2nd of the pair
                self.assertEqual(dist, connections_2[i])
