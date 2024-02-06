"""
Test case for the GA population creation
"""
import unittest
from searches.ga.population import encode_solution, gen_pop
from model.model import create_model
from typing import List


class TestGAPopulationClass(unittest.TestCase):
    """
    Class for testing GA population methods
    """

    def test_solution_encoding(self):
        """
        Tests that a valid solution is encoded correctly to create a chromosome
        """
        # Create an example solution
        example_solution = [{'from': 0, 'to': 1, 's': 2}, {'from': 3, 'to': 4, 's': 5}, {
            'from': 6, 'to': 7, 's': 8}, {'from': 9, 'to': 10, 's': 11}]

        # Create this as the expected chromosome
        expected_solution = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (9, 10, 11)]

        # Obtain the actual solution
        actual_solution = encode_solution(path=example_solution)

        # Check they are the same
        self.assertEqual(expected_solution, actual_solution)

    def test_pop_creation(self):
        """
        Tests that a population for the GA is created correctly
        """
        # TODO do I want to check that elements in the initial population are unique

        # Create a 10 hub model
        n = 10
        model = create_model(n=n, alpha=2)

        # Create a population of 3 different solutions
        pop = gen_pop(pop_size=3, model=model, max_journey_size=10)

        # check a population of size three is returned
        self.assertEqual(len(pop), 3)

        # Check population is a list of individuals
        self.assertIsInstance(pop, list)

        # For each member of the population, check it is a list of tuple
        for individual in pop:
            # Assert individual is of type list
            self.assertIsInstance(individual, list)

            # Check each of the genomes are a tuple element of 3 integers
            for genome in individual:
                self.assertIsInstance(genome, tuple)
                self.assertEqual(len(genome), 3)
                for i in genome:
                    self.assertIsInstance(i, int)
