"""
Unit tests for the crossover method of the genetic algorithm
"""
import unittest
from searches.ga.crossover import aware_crossover
from TNRP_model.depot import Depot
from searches.ga.population import encode_solution, decode_solution
from searches.utils import is_complete


class TestCrossoverClass(unittest.TestCase):
    """
    Test class for the context-aware crossover function
    """

    def test_crossover_works_when_parents_identical(self):
        """
        Tests the crossover method returns two children identical to the parents
        """
        dep_0 = Depot(name=0, s=28, x=0, y=0)
        dep_1 = Depot(name=1, s=-4, x=0, y=0)
        dep_2 = Depot(name=2, s=-84, x=0, y=0)
        dep_3 = Depot(name=3, s=65, x=0, y=0)
        dep_4 = Depot(name=4, s=-16, x=0, y=0)
        dep_5 = Depot(name=5, s=11, x=0, y=0)

        model = {0: dep_0, 1: dep_1, 2: dep_2, 3: dep_3, 4: dep_4, 5: dep_5}

        # Generate two unique solutions to the problem
        parent1 = [{'from': 3, 'to': 4, 's': 16}, {'from': 0, 'to': 2, 's': 20}, {'from': 0, 'to': 2, 's': 8},
                   {'from': 3, 'to': 2, 's': 20}, {'from': 3, 'to': 1,
                                                   's': 4}, {'from': 3, 'to': 2, 's': 20},
                   {'from': 5, 'to': 2, 's': 11}, {'from': 3, 'to': 2, 's': 5}]

        encoded_parent_1 = encode_solution(path=parent1)

        parent2 = [{'from': 0, 'to': 2, 's': 20}, {'from': 3, 'to': 2, 's': 20}, {'from': 0, 'to': 2, 's': 8}, {'from': 5, 'to': 4, 's': 11}, {
            'from': 3, 'to': 2, 's': 20}, {'from': 3, 'to': 1, 's': 4}, {'from': 3, 'to': 4, 's': 5}, {'from': 3, 'to': 2, 's': 16}]

        encoded_parent_2 = encode_solution(path=parent2)

        parent1 = encode_solution(path=parent1)
        parent2 = encode_solution(path=parent2)

        # Perform the aware crossover
        res_child_1, res_child_2 = aware_crossover(
            parent_1=parent1, parent_2=parent2, model=model, max_journey_size=20, crossover_rate=1)

        # Check that the children are valid solutions
        res_child_1_decoded = decode_solution(path=res_child_1)
        res_child_2_decoded = decode_solution(path=res_child_2)

        self.assertTrue(is_complete(path=res_child_1_decoded,
                        original_model_state=model))
        self.assertTrue(is_complete(path=res_child_2_decoded,
                        original_model_state=model))

        # Check that they both contain elements from each parent
        count_in_1 = 0
        count_in_2 = 0

        for j in res_child_1:
            if j in encoded_parent_1:
                count_in_1 += 1
            if j in encoded_parent_2:
                count_in_2 += 1

        self.assertGreater(count_in_1, 0)
        self.assertGreater(count_in_2, 0)

        count_in_1 = 0
        count_in_2 = 0
        for j in res_child_2:
            if j in encoded_parent_1:
                count_in_1 += 1
            if j in encoded_parent_2:
                count_in_2 += 1

        self.assertGreater(count_in_1, 0)
        self.assertGreater(count_in_2, 0)

    def test_no_crossover_performed_when_rate_of_0(self):
        """
        Tests that the parents are returned as children when a crossover rate of 0 is used
        """
        dep_0 = Depot(name=0, s=28, x=0, y=0)
        dep_1 = Depot(name=1, s=-4, x=0, y=0)
        dep_2 = Depot(name=2, s=-84, x=0, y=0)
        dep_3 = Depot(name=3, s=65, x=0, y=0)
        dep_4 = Depot(name=4, s=-16, x=0, y=0)
        dep_5 = Depot(name=5, s=11, x=0, y=0)

        model = {0: dep_0, 1: dep_1, 2: dep_2, 3: dep_3, 4: dep_4, 5: dep_5}

        # Generate two unique solutions to the problem
        parent1 = [{'from': 3, 'to': 4, 's': 16}, {'from': 0, 'to': 2, 's': 20}, {'from': 0, 'to': 2, 's': 8},
                   {'from': 3, 'to': 2, 's': 20}, {'from': 3, 'to': 1,
                                                   's': 4}, {'from': 3, 'to': 2, 's': 20},
                   {'from': 5, 'to': 2, 's': 11}, {'from': 3, 'to': 2, 's': 5}]

        encoded_parent_1 = encode_solution(path=parent1)

        parent2 = [{'from': 0, 'to': 2, 's': 20}, {'from': 3, 'to': 2, 's': 20}, {'from': 0, 'to': 2, 's': 8}, {'from': 5, 'to': 4, 's': 11}, {
            'from': 3, 'to': 2, 's': 20}, {'from': 3, 'to': 1, 's': 4}, {'from': 3, 'to': 4, 's': 5}, {'from': 3, 'to': 2, 's': 16}]

        encoded_parent_2 = encode_solution(path=parent2)

        parent1 = encode_solution(path=parent1)
        parent2 = encode_solution(path=parent2)

        # Perform the aware crossover
        res_child_1, res_child_2 = aware_crossover(
            parent_1=parent1, parent_2=parent2, model=model, max_journey_size=20, crossover_rate=0)

        self.assertEqual(res_child_1, encoded_parent_1)
        self.assertEqual(res_child_2, encoded_parent_2)
