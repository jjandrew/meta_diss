"""
Unit tests for the mutation methods in the GA algorithm
"""
import unittest
import copy
from searches.ga.mutation import swap


class TestGAMuationClass(unittest.TestCase):
    """
    Test suite for the mutation methods
    """
    parent = [(0, 2, 1), (0, 2, 2), (1, 3, 2), (1, 3, 2)]

    def test_swap_deals_with_one_unique_deficit_node(self):
        """
        Tests swap returns the parent when there is only one deficit node
        """
        # Create a parent with only 1 deficit node
        parent = [(1, 0, 1), (2, 0, 1), (1, 0, 2), (3, 0, 4)]

        # Perform the comparison 100 times
        iters = 100
        for _ in range(iters):
            # Perform the swap with a guaranteed mutation rate
            res = swap(parent=copy.copy(parent),
                       mutation_rate=1, max_journey_size=2)

            # Check no swap was perfromed
            self.assertEqual(res, parent)

    def test_swap_deals_with_one_unique_surplus_node(self):
        """
        Tests swap returns the parent when there is only one surplus node
        """
        # Create a parent with only 1 surplus node
        parent = [(0, 1, 1), (0, 2, 1), (0, 1, 2), (0, 3, 4)]

        # Perform the comparison 100 times
        iters = 100
        for _ in range(iters):
            # Perform the swap with a guaranteed mutation rate
            res = swap(parent=copy.copy(parent),
                       mutation_rate=1, max_journey_size=2)

            # Check no swap was perfromed
            self.assertEqual(res, parent)

    def test_swap_doesnt_mutate_when_mutation_rate_0(self):
        """
        Tests no mutations when mutation rate 0
        """
        # Perform 100 iterations
        iters = 100
        for _ in range(iters):
            # Try perform a swap with zero mutation rate
            res = swap(parent=copy.copy(self.parent),
                       mutation_rate=0, max_journey_size=2)
            # check no swap is performed
            self.assertEqual(self.parent, res)

    def test_swap_always_when_mutation_rate_1(self):
        """
        Tests always a mutation when mutation rate 1
        """
        # Perform 100 iterations
        iters = 100
        for _ in range(iters):
            # Try perform a swap with one mutation rate
            res = swap(parent=copy.copy(self.parent),
                       mutation_rate=1, max_journey_size=2)
            # Ensure that the result is different to the parent
            self.assertNotEqual(self.parent, res)
            # Check that at least two pairs of two deficit nodes are present
            two_count = 0
            three_count = 0
            # Count each journey in the result
            for j in res:
                # If a 2 if the deficit node then add to two count
                if j[1] == 2:
                    two_count += 1
                # If a three is the deficit node then add to 3 count
                elif j[1] == 3:
                    three_count += 1
            # Make sure 2 pairs of deficit nodes
            self.assertGreaterEqual(two_count, 2)
            self.assertGreaterEqual(three_count, 2)

    def test_swaps_half_the_time_when_mutation_rate_half(self):
        """
        Tests mutations occurr half the time when mutation rate 0.5
        """
        # Perform 1000 iterations
        iters = 1000
        # Store number of mutated results
        number_mutated = 0
        for _ in range(iters):
            # Try perform a swap with a mutation rate of 0.5
            res = swap(parent=copy.copy(self.parent),
                       mutation_rate=0.5, max_journey_size=2)
            # Increment if the result was mutated
            if res != self.parent:
                number_mutated += 1

        # Check around half were
        self.assertAlmostEqual(number_mutated/iters, 0.5, 1)
