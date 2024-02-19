"""
Unit tests for the GA path fixing algorithm
"""
import unittest
from model.hub import Hub
from searches.ga.fixing.fixing import fix
from searches.ga.fixing.fixing_utils import get_sur_and_def_hubs, get_sur_and_def_journeys
from searches.ga.crossover import uniform
from searches.ga.population import encode_solution, decode_solution
from searches.random import random_search
from model.model import create_model
import copy
from utils import apply_path


class TestGAPathFixingClass(unittest.TestCase):
    """
    Test suite for GA path fixing
    """
    model = {}

    def setUp(self):
        # Create 3 hubs
        hub0 = Hub(name=0, s=-5, long=0, lat=0)
        hub1 = Hub(name=1, s=-5, long=0, lat=0)
        hub2 = Hub(name=2, s=10, long=0, lat=0)

        # Place in an array
        self.model = {0: hub0, 1: hub1, 2: hub2}

        # Add the connections
        hub0.add_connection(hub1)
        hub0.add_connection(hub2)
        hub1.add_connection(hub2)

    def test_get_surplus_and_deficit_hubs_normally(self):
        """
        Tests that the function to split hubs into surplus and deficit hubs works for two deficit and one surplus hub
        """
        # Create a dictionary of surplus and deficit hubs
        surplus, deficit = get_sur_and_def_hubs(model=self.model)

        # Using the model create sets for surplus and deficit hubs
        expected_surplus = set({2})
        expected_deficit = set({0, 1})

        # Check the expected is the same as the result
        self.assertEqual(surplus, expected_surplus)
        self.assertEqual(deficit, expected_deficit)

    def test_get_surplus_and_defict_hubs_deals_with_resolved_hubs(self):
        """
        Tests that the function to split surplus and deficit hubs works for hubs in equilibrium
        """
        # Move 5 s from a surplus to a deficit hub to resolve hub 0
        Hub.move_s(start=self.model[2], end=self.model[0], s=5)

        # Create a dictionary of surplus and deficit hubs
        surplus, deficit = get_sur_and_def_hubs(model=self.model)

        # Using the model create sets for surplus and deficit hubs
        expected_surplus = set({2})
        expected_deficit = set({1})

        # Check the expected is the same as the result
        self.assertEqual(surplus, expected_surplus)
        self.assertEqual(deficit, expected_deficit)

    def test_get_sur_and_def_js(self):
        """
        Tests it is possible to get the indexes of the journeys using surplus and deficit hubs
        """
        # Create a path
        path = [(0, 3, 1), (0, 3, 2), (1, 3, 0), (2, 4, 1)]

        # Expected surplus and deficit journeys
        expected_sur_js = {0: [0, 1], 1: [2], 2: [3]}
        expected_def_js = {3: [0, 1, 2], 4: [3]}

        # Calculate result from function
        res_sur_js, res_def_js = get_sur_and_def_journeys(path=path)

        # Check result is as expected
        self.assertEqual(res_sur_js, expected_sur_js)
        self.assertEqual(res_def_js, expected_def_js)

    def test_fixing_returns_original_path_if_model_resolved(self):
        """
        Tests nothing is fixed if original path is valid
        """
        # Create journeys to resolve the model
        path = [(2, 0, 5), (2, 1, 5)]

        # resultant path
        fix(path=path, model=self.model)

        # Expected path as fix done in place
        expected_path = [(2, 0, 5), (2, 1, 5)]

        # check res_path == expected path
        self.assertEqual(path, expected_path)

    def test_my_test(self):
        for _ in range(10000):
            hubs = [
                Hub(name=i, s=s, long=long, lat=lat)
                for i, (long, lat, s) in enumerate([
                    (13, 0, 25),
                    (5, 8, -98),
                    (13, 7, 9),
                    (1, 13, 2),
                    (1, 2, 25),
                    (9, 1, -51),
                    (11, 7, 88)
                ])
            ]

            model = {}
            for hub in hubs:
                model[hub.get_name()] = hub

            child_1 = [(6, 1, 20), (4, 1, 20), (0, 1, 20), (6, 1, 20), (0, 1, 5),
                       (6, 1, 13), (3, 5, 2), (0, 5, 20), (6, 5, 20), (6, 5, 9)]

            print()
            print()
            print()
            print()
            print("=================")
            print("=================")
            print()

            fix(path=child_1, model=copy.deepcopy(model))

            apply_path(model=model, path=decode_solution(child_1))

            for hub_name in model:
                if model[hub_name].get_s() != 0:
                    # Print out the state
                    # Print the model
                    for hub in model:
                        print(model[hub])
                    print()
                    print(child_1)
                    print()
                    for hub in model:
                        print(model[hub])
                    self.fail("Exiting")

    def test_fixing(self):
        """
        Test for fixing
        """
        for i in range(1000):
            model = create_model(n=7, alpha=2)

            path_1 = encode_solution(path=random_search(
                model=copy.deepcopy(model), max_journey_size=20))
            path_2 = encode_solution(path=random_search(
                model=copy.deepcopy(model), max_journey_size=20))

            child_1, child_2 = uniform(parent_1=path_1, parent_2=path_2)

            child_1_copy = copy.deepcopy(child_1)

            fix(path=child_1, model=copy.deepcopy(model))
            fix(path=child_2, model=copy.deepcopy(model))

            model_copy_1 = copy.deepcopy(model)
            model_copy_2 = copy.deepcopy(model)

            apply_path(model=model_copy_1, path=decode_solution(child_1))
            apply_path(model=model_copy_2, path=decode_solution(child_2))

            # for hub_name in model_copy_1:
            #     if model_copy_1[hub_name].get_s() != 0:
            #         # Print out the state
            #         # Print the model
            #         for hub in model:
            #             print(model[hub])
            #         print()
            #         print(child_1_copy)
            #         print()
            #         print(child_1)
            #         print()
            #         print(i)
            #         print()
            #         for hub in model_copy_1:
            #             print(model_copy_1[hub])
            #         self.fail("Exiting")
