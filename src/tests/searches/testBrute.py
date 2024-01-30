"""Tests for the brute force algorithm"""
import unittest
from searches.brute_force.brute import brute, next_steps
from model.model import create_model
from model.hub import Hub
from searches.random.random import random_search
import copy
from utils import fitness, improve_solution


class TestBruteClass(unittest.TestCase):
    """
    Class for testing brute force algorithm
    """

    def test_brute(self):
        """
        Test for the brute force solution finder
        """
        # Create an 5 node model
        model = create_model(n=5, alpha=2, max_def=-10, max_sur=10)
        max_journey_size = 5

        # Generate a random solution
        random_solution = random_search(
            model=copy.deepcopy(model), max_journey_size=max_journey_size)

        # Get the fitness of the random solution
        random_fitness = fitness(path=random_solution, model=model)

        # Brute for the solution
        brute_solution = brute(model=model, max_journey_size=max_journey_size)
        brute_fitness = fitness(path=brute_solution, model=model)

        # Check brute force fitness is better than a random solution
        self.assertLessEqual(brute_fitness, random_fitness)

    def test_next_steps(self):
        """
        Tests that all possible next steps can be found from a starting hub
        """
        # Create a starting hub with a surplus
        starting_hub = Hub(name=0, s=2, long=0, lat=0)

        # Create three deficit hubs of different quantities of deficit
        def_hub_1 = Hub(name=1, s=-1, long=0, lat=0)
        def_hub_2 = Hub(name=2, s=-2, long=0, lat=0)
        def_hub_3 = Hub(name=3, s=-5, long=0, lat=0)

        def_hubs = {1: def_hub_1, 2: def_hub_2, 3: def_hub_3}

        # Obtain the next journeys
        next_js = next_steps(starting_hub=starting_hub,
                             deficit_hubs=def_hubs, max_journey_size=3)

        # Expected journeys, where no s is greater than absolute values of starting hub s, def_hub s or max_journey_size
        expected_journeys = [{'from': 0, 'to': 1, 's': 1}, {'from': 0, 'to': 2, 's': 1}, {
            'from': 0, 'to': 2, 's': 2}, {'from': 0, 'to': 3, 's': 1}, {'from': 0, 'to': 3, 's': 2}]

        self.assertEqual(next_js, expected_journeys)
