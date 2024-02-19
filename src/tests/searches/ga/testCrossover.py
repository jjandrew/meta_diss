"""
Unit tests for the crossover method of the genetic algorithm
"""
import unittest
from searches.ga.crossover import aware_crossover
from model.hub import Hub
from searches.ga.population import encode_solution, decode_solution
from utils import is_complete


class TestUniformCrossover(unittest.TestCase):
    """
    Test class for the uniform crossover function
    """

    def test_crossover_works_when_parents_identical(self):
        """
        Tests the crossover method returns two children identical to the parents
        """
        hub_0 = Hub(name=0, s=28, long=0, lat=0)
        hub_1 = Hub(name=1, s=-4, long=0, lat=0)
        hub_2 = Hub(name=2, s=-84, long=0, lat=0)
        hub_3 = Hub(name=3, s=65, long=0, lat=0)
        hub_4 = Hub(name=4, s=-16, long=0, lat=0)
        hub_5 = Hub(name=5, s=11, long=0, lat=0)

        model = {0: hub_0, 1: hub_1, 2: hub_2, 3: hub_3, 4: hub_4, 5: hub_5}

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
            parent_1=parent1, parent_2=parent2, model=model, max_journey_size=20)

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
