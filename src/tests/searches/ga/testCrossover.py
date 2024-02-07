"""
Unit tests for the crossover method of the genetic algorithm
"""
import unittest
from searches.ga.crossover import uniform
import random


class TestUniformCrossover(unittest.TestCase):
    """
    Test class for the uniform crossover function
    """

    def test_crossover_works_when_parents_identical(self):
        """
        Tests the crossover method returns two children identical to the parents
        """
        # Create two parents
        parent1 = [(0, 1, 1), (0, 2, 2), (0, 2, 3), (0, 1, 2), (0, 3, 4)]
        parent2 = [(0, 1, 1), (0, 1, 2), (0, 2, 2), (0, 2, 3), (0, 3, 4)]

        # Generate uniorm crossover result
        res_child_1, res_child_2 = uniform(parent_1=parent1, parent_2=parent2)

        # Check they are equal
        self.assertEqual(res_child_1, parent2)
        self.assertEqual(res_child_2, parent2)

    def test_crossover_is_random(self):
        """
        Tests the crossover chooses parents randomly
        """
        # Create two parents
        parent1 = [(0, 2, 1), (0, 2, 2), (1, 2, 3), (1, 3, 2), (1, 3, 4)]
        parent2 = [(0, 3, 1), (0, 3, 2), (0, 2, 2), (1, 2, 3), (1, 3, 4)]

        # Generate a number of iterations to perform crossover
        num_iters = 1000

        # Generate the 3 possible crossovers
        opt_1_c_1, opt_1_c_2 = [(0, 2, 1), (0, 2, 2), (1, 2, 3), (0, 3, 1), (0, 3, 2), (1, 3, 4)], [
            (0, 2, 2), (1, 2, 3), (1, 3, 2), (1, 3, 4)]

        opt_2_c_1, opt_2_c_2 = [(0, 2, 2), (1, 2, 3), (0, 3, 1), (0, 3, 2), (1, 3, 4)], [
            (0, 2, 1), (0, 2, 2), (1, 2, 3), (1, 3, 2), (1, 3, 4)]

        opt_3_c_1, opt_3_c_2 = [(0, 2, 2), (1, 2, 3), (1, 3, 2), (1, 3, 4)], [
            (0, 2, 1), (0, 2, 2), (1, 2, 3), (0, 3, 1), (0, 3, 2), (1, 3, 4)]

        opt_4_c_1, opt_4_c_2 = [(0, 2, 1), (0, 2, 2), (1, 2, 3), (1, 3, 2), (1, 3, 4)], [
            (0, 2, 2), (1, 2, 3), (0, 3, 1), (0, 3, 2), (1, 3, 4)]

        # Create counts for the three options
        opt_1_count = 0
        opt_2_count = 0
        opt_3_count = 0
        opt_4_count = 0

        for _ in range(num_iters):
            # Generate uniorm crossover result
            res_child_1, res_child_2 = uniform(
                parent_1=parent1, parent_2=parent2)

            if res_child_1 == opt_1_c_1 and res_child_2 == opt_1_c_2:
                opt_1_count += 1

            elif res_child_1 == opt_2_c_1 and res_child_2 == opt_2_c_2:
                opt_2_count += 1

            elif res_child_1 == opt_3_c_1 and res_child_2 == opt_3_c_2:
                opt_3_count += 1

            elif res_child_1 == opt_4_c_1 and res_child_2 == opt_4_c_2:
                opt_4_count += 1

        # Check that only those possibilities were generates
        self.assertEqual(opt_1_count+opt_2_count +
                         opt_3_count+opt_4_count, num_iters)

        # Check that each option was generated approximately a third of the time
        self.assertAlmostEqual(opt_1_count/num_iters, 0.25, places=1)
        self.assertAlmostEqual(opt_2_count/num_iters, 0.25, places=1)
        self.assertAlmostEqual(opt_3_count/num_iters, 0.25, places=1)
        self.assertAlmostEqual(opt_4_count/num_iters, 0.25, places=1)
