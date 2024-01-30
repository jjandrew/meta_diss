"""
Tests a valid path can be generated using matrices
"""
import unittest
from searches.aco.pathGeneration import perform_journey, generate_path
from searches.aco.create_matrices import create_heur_matrix, create_dist_matrix, create_pher_matrix
from model.model import create_model
from model.hub import Hub
from utils import is_complete
import copy


class TestACOPathGenerationClass(unittest.TestCase):
    """
    Class for testing the path generation in the ACO algorithms
    """

    def test_perform_journey(self):
        """
        Tests that the journey performing function works correctly
        """
        hub_0 = Hub(name=0, s=5, long=0, lat=0)
        hub_1 = Hub(name=1, s=-5, long=0, lat=0)
        hub_2 = Hub(name=2, s=10, long=0, lat=0)
        hub_3 = Hub(name=3, s=-10, long=0, lat=0)
        hub_4 = Hub(name=4, s=3, long=0, lat=0)

        max_j_size = 5

        # Create a move where both hubs resolved
        journey, result = perform_journey(
            sur_hub=hub_0, def_hub=hub_1, max_journey_size=max_j_size)
        expected = [0, 1]
        expected_journey = {'from': 0, 'to': 1, 's': 5}
        self.assertEqual(expected_journey, journey)
        self.assertEqual(result, expected)

        # Reset hubs
        hub_0 = Hub(name=0, s=5, long=0, lat=0)
        hub_1 = Hub(name=1, s=-5, long=0, lat=0)

        # Create a move where deficit hub is resolved
        journey, result = perform_journey(
            sur_hub=hub_2, def_hub=hub_1, max_journey_size=max_j_size)
        expected = [1]
        expected_journey = {'from': 2, 'to': 1, 's': 5}
        self.assertEqual(expected_journey, journey)
        self.assertEqual(result, expected)

        # Reset hubs
        hub_1 = Hub(name=1, s=-5, long=0, lat=0)
        hub_2 = Hub(name=2, s=10, long=0, lat=0)

        # Create a move where surplus hub is resolved
        journey, result = perform_journey(
            sur_hub=hub_0, def_hub=hub_3, max_journey_size=max_j_size)
        expected = [0]
        expected_journey = {'from': 0, 'to': 3, 's': 5}
        self.assertEqual(expected_journey, journey)
        self.assertEqual(result, expected)

        # Reset hubs
        hub_0 = Hub(name=0, s=5, long=0, lat=0)
        hub_3 = Hub(name=3, s=-10, long=0, lat=0)

        # Create a move where neither hub resolved
        journey, result = perform_journey(
            sur_hub=hub_2, def_hub=hub_3, max_journey_size=max_j_size)
        expected = []
        expected_journey = {'from': 2, 'to': 3, 's': 5}
        self.assertEqual(expected_journey, journey)
        self.assertEqual(result, expected)

        # Reset hubs
        hub_2 = Hub(name=2, s=10, long=0, lat=0)
        hub_3 = Hub(name=3, s=-10, long=0, lat=0)

        # Create a move where j size is less than max_j_size
        journey, result = perform_journey(
            sur_hub=hub_4, def_hub=hub_1, max_journey_size=max_j_size)
        expected = [4]
        expected_journey = {'from': 4, 'to': 1, 's': 3}
        self.assertEqual(expected_journey, journey)
        self.assertEqual(result, expected)

    def test_path_generation(self):
        """
        Tests a valid path is generated using matrices provided
        """
        hub_0 = Hub(name=0, s=4, long=0, lat=0)
        hub_1 = Hub(name=1, s=-3, long=3, lat=2)
        hub_2 = Hub(name=2, s=-1, long=1, lat=1)

        model = {0: hub_0, 1: hub_1, 2: hub_2}

        hub_0.add_connection(hub_1)
        hub_0.add_connection(hub_2)
        hub_1.add_connection(hub_2)

        max_j_size = 3

        # Create matrices
        d = create_dist_matrix(model=model)
        h = create_heur_matrix(dist_matrix=d)
        p = [
            [0, 0.5, 0.5],
            [0, 0, 0],
            [0, 0, 0]
        ]

        sur_hubs = {0: hub_0}
        def_hubs = {1: hub_1, 2: hub_2}

        path = generate_path(sur_hubs=sur_hubs, def_hubs=def_hubs, d=d,
                             h=h, p=p, max_journey_size=max_j_size)

        expected = [{'from': 0, 'to': 2, 's': 1}, {'from': 0, 'to': 1, 's': 3}]

        self.assertCountEqual(path, expected)

    def test_solutions_created_are_valid(self):
        """
        Tests valid solutions are created for a larger model
        """
        # Create a model
        model = create_model(n=1000, alpha=2, max_def=-20, max_sur=20)
        model_copy = copy.deepcopy(model)

        model_dict = {hub.get_name(): hub for hub in model}

        d = create_dist_matrix(model_dict)
        h = create_heur_matrix(d)
        p = create_pher_matrix(model_dict, d)

        sur_hubs = {hub.get_name(): hub for hub in model if hub.get_s() > 0}
        def_hubs = {hub.get_name(): hub for hub in model if hub.get_s() < 0}

        max_j_size = 10

        path = generate_path(sur_hubs=sur_hubs, def_hubs=def_hubs,
                             d=d, h=h, p=p, max_journey_size=max_j_size)

        complete = is_complete(path=path, original_model_state=model_copy)

        self.assertTrue(complete)
