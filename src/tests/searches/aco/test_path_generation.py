"""
Tests a valid path can be generated in the AS algorithm using matrices
"""
import unittest
from searches.aco.path_generation import perform_journey, generate_path
from searches.aco.create_matrices import create_heur_matrix, create_dist_matrix, create_pher_matrix
from model.tnrp_model import create_model
from model.depot import Depot
from utils import is_complete


class TestASPathGenerationClass(unittest.TestCase):
    """
    Class for testing the path generation in the AS algorithm
    """

    def test_perform_journey(self):
        """
        Tests that the journey performing function works correctly
        """
        dep_0 = Depot(name=0, s=5, x=0, y=0)
        dep_1 = Depot(name=1, s=-5, x=0, y=0)
        dep_2 = Depot(name=2, s=10, x=0, y=0)
        dep_3 = Depot(name=3, s=-10, x=0, y=0)
        dep_4 = Depot(name=4, s=3, x=0, y=0)

        max_j_size = 5

        # Create a move where both depots are resolved
        journey, result = perform_journey(
            sur_dep=dep_0, def_dep=dep_1, max_journey_size=max_j_size)
        # Check the journey is of the correct format and both depot names are returned
        expected = [0, 1]
        expected_journey = {'from': 0, 'to': 1, 's': 5}
        self.assertEqual(expected_journey, journey)
        self.assertEqual(result, expected)

        # Reset depots
        dep_0 = Depot(name=0, s=5, x=0, y=0)
        dep_1 = Depot(name=1, s=-5, x=0, y=0)

        # Create a move where just the deficit depot is resolved
        journey, result = perform_journey(
            sur_dep=dep_2, def_dep=dep_1, max_journey_size=max_j_size)
        # check just the deficit depot to resolve and correct journey returned
        expected = [1]
        expected_journey = {'from': 2, 'to': 1, 's': 5}
        self.assertEqual(expected_journey, journey)
        self.assertEqual(result, expected)

        # Reset depots
        dep_1 = Depot(name=1, s=-5, x=0, y=0)
        dep_2 = Depot(name=2, s=10, x=0, y=0)

        # Create a move where just the surplus depot is resolved
        journey, result = perform_journey(
            sur_dep=dep_0, def_dep=dep_3, max_journey_size=max_j_size)
        # Check just the surplus depot to resolve and correct journey returned
        expected = [0]
        expected_journey = {'from': 0, 'to': 3, 's': 5}
        self.assertEqual(expected_journey, journey)
        self.assertEqual(result, expected)

        # Reset depots
        dep_0 = Depot(name=0, s=5, x=0, y=0)
        dep_3 = Depot(name=3, s=-10, x=0, y=0)

        # Create a move where neither depot resolved
        journey, result = perform_journey(
            sur_dep=dep_2, def_dep=dep_3, max_journey_size=max_j_size)
        # checks neither depot to return but max journey size is used for journey
        expected = []
        expected_journey = {'from': 2, 'to': 3, 's': 5}
        self.assertEqual(expected_journey, journey)
        self.assertEqual(result, expected)

        # Reset depots
        dep_2 = Depot(name=2, s=10, x=0, y=0)
        dep_3 = Depot(name=3, s=-10, x=0, y=0)

        # Create a move where j size is less than max_j_size
        journey, result = perform_journey(
            sur_dep=dep_4, def_dep=dep_1, max_journey_size=max_j_size)
        expected = [4]
        expected_journey = {'from': 4, 'to': 1, 's': 3}
        self.assertEqual(expected_journey, journey)
        self.assertEqual(result, expected)

    def test_valid_path_generation(self):
        """
        Tests a valid path is generated
        """
        # Create the model
        dep_0 = Depot(name=0, s=4, x=0, y=0)
        dep_1 = Depot(name=1, s=-3, x=3, y=2)
        dep_2 = Depot(name=2, s=-1, x=1, y=1)

        model = {0: dep_0, 1: dep_1, 2: dep_2}

        dep_0.add_connection(dep_1)
        dep_0.add_connection(dep_2)
        dep_1.add_connection(dep_2)

        max_j_size = 3

        # Create matrices
        d = create_dist_matrix(model=model)
        h = create_heur_matrix(dist_matrix=d)
        p = [
            [0, 0.5, 0.5],
            [0, 0, 0],
            [0, 0, 0]
        ]

        # Split the suplus and deficit depots
        sur_deps = {0: dep_0}
        def_deps = {1: dep_1, 2: dep_2}

        # Generate a path
        path = generate_path(sur_deps=sur_deps, def_deps=def_deps, d=d,
                             h=h, p=p, max_journey_size=max_j_size)

        expected = [{'from': 0, 'to': 2, 's': 1}, {'from': 0, 'to': 1, 's': 3}]

        self.assertCountEqual(path, expected)

    def test_solutions_created_are_valid(self):
        """
        Tests valid solutions are created for a larger model
        """
        # Create a model
        model = create_model(n=100, alpha=2, max_def=-20, max_sur=20)

        d = create_dist_matrix(model=model)
        h = create_heur_matrix(dist_matrix=d)
        p = create_pher_matrix(model=model, dist_matrix=d)

        # Split the model into surplus and deficit depots
        sur_deps = {dep: model[dep] for dep in model if model[dep].get_s() > 0}
        def_deps = {dep: model[dep] for dep in model if model[dep].get_s() < 0}

        max_j_size = 10

        path = generate_path(sur_deps=sur_deps, def_deps=def_deps,
                             d=d, h=h, p=p, max_journey_size=max_j_size)

        complete = is_complete(path=path, original_model_state=model)

        self.assertTrue(complete)

    def test_path_generation_uses_pheromone_matrix(self):
        """
        Tests that path generation is more likely to choose edges with more pheromone
        """
        # Create the model
        dep_0 = Depot(name=0, s=4, x=0, y=0)
        dep_1 = Depot(name=1, s=-3, x=3, y=2)
        dep_2 = Depot(name=2, s=-1, x=1, y=1)

        model = {0: dep_0, 1: dep_1, 2: dep_2}

        dep_0.add_connection(dep_1)
        dep_0.add_connection(dep_2)
        dep_1.add_connection(dep_2)

        # Split the model into surplus and deficit depots
        sur_deps = {dep: model[dep] for dep in model if model[dep].get_s() > 0}
        def_deps = {dep: model[dep] for dep in model if model[dep].get_s() < 0}

        max_j_size = 3

        # create the pheromone matrix
        p = [[0, 1, 0],
             [0, 0, 0],
             [0, 0, 0]]

        d = create_dist_matrix(model=model)
        h = create_heur_matrix(dist_matrix=d)

        # Generate 10 paths
        for _ in range(10):
            # Generate path with all emphasis on pheromone
            path = generate_path(sur_deps=sur_deps, def_deps=def_deps, d=d,
                                 h=h, p=p, max_journey_size=max_j_size, alpha=1000, beta=0.01)

            # Test that the path always adds 0->1 first despite longer distance
            expected = [{'from': 0, 'to': 1, 's': 3},
                        {'from': 0, 'to': 2, 's': 1}]

            self.assertEqual(path, expected)

    def test_path_generation_uses_heuristic_matrix(self):
        """
        Tests that path generation is more likely to choose edges with a greater heuristic
        """
        # Create the model
        dep_0 = Depot(name=0, s=4, x=0, y=0)
        dep_1 = Depot(name=1, s=-3, x=3, y=2)
        dep_2 = Depot(name=2, s=-1, x=1, y=1)

        model = {0: dep_0, 1: dep_1, 2: dep_2}

        dep_0.add_connection(dep_1)
        dep_0.add_connection(dep_2)
        dep_1.add_connection(dep_2)

        # Split the model into surplus and deficit depots
        sur_deps = {dep: model[dep] for dep in model if model[dep].get_s() > 0}
        def_deps = {dep: model[dep] for dep in model if model[dep].get_s() < 0}

        max_j_size = 3

        # create the pheromone matrix
        p = [[0, 1000, 0.01],
             [0, 0, 0],
             [0, 0, 0]]

        d = create_dist_matrix(model=model)
        h = create_heur_matrix(dist_matrix=d)

        # Generate 10 paths
        for _ in range(10):
            # Generate path with all emphasis on pheromone
            path = generate_path(sur_deps=sur_deps, def_deps=def_deps, d=d,
                                 h=h, p=p, max_journey_size=max_j_size, alpha=0.1, beta=1000)

            # Test that the path always adds 0->2 first despite significantly more pheromone on 0->1
            expected = [{'from': 0, 'to': 2, 's': 1},
                        {'from': 0, 'to': 1, 's': 3}]

            self.assertEqual(path, expected)
