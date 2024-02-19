"""
Tests the generation of a neighbour
"""
from searches.sa.neighbourhood import gen_neighbour, compress_neighbour, new_compression
import unittest


class TestNeighbourhoodClass(unittest.TestCase):
    """
    Test suite for the generation of a neighbour
    """

    def test_neighbourhood_can_swap_with_two_journeys_of_same_size(self):
        """
        Tests the generation of a neighbour can deal with two journeys of equal size
        """
        path = [
            {'from': 1, 'to': 2, 's': 10},
            {'from': 3, 'to': 4, 's': 10}
        ]
        expected_result = [
            {'from': 1, 'to': 4, 's': 10},
            {'from': 3, 'to': 2, 's': 10}
        ]
        result = gen_neighbour(path=path)

        self.assertEqual(expected_result, result)

    def test_neighbourhood_can_split_journeys(self):
        """
        Tests that a neighbour can split a node into two different sizes
        """
        path = [
            {'from': 1, 'to': 2, 's': 10},
            {'from': 3, 'to': 4, 's': 9}
        ]
        expected = [
            {'from': 1, 'to': 4, 's': 9},
            {'from': 3, 'to': 2, 's': 9},
            {'from': 1, 'to': 2, 's': 1}
        ]
        result = gen_neighbour(path=path)

        self.assertEqual(result, expected)

    def test_compression(self):
        """
        Tests that a path can be compressed to ensure it is optimal
        """
        path = [
            {'from': 1, 'to': 4, 's': 9},
            {'from': 3, 'to': 2, 's': 9},
            {'from': 1, 'to': 4, 's': 1},
            {'from': 3, 'to': 2, 's': 1}
        ]

        expected = [
            {'from': 1, 'to': 4, 's': 10},
            {'from': 3, 'to': 2, 's': 10}
        ]

        result = new_compression(path=path, max_journey_size=10)

        self.assertEqual(result, expected)

    def test_compression_can_do_multiple_journeys(self):
        """
        Tests that a path can be compressed when multiple journeys are in the compression
        """
        path = [
            {'from': 1, 'to': 4, 's': 8},
            {'from': 1, 'to': 4, 's': 1},
            {'from': 1, 'to': 4, 's': 1},
            {'from': 3, 'to': 2, 's': 9}
        ]

        expected = [
            {'from': 1, 'to': 4, 's': 10},
            {'from': 3, 'to': 2, 's': 9}
        ]

        result = new_compression(path=path, max_journey_size=10)

        self.assertEqual(result, expected)

    def test_compression_can_do_multiple_consecutive_compressions(self):
        """
        Tests that a path can be compressed when multiple compressions are required
        """
        path = [
            {'from': 1, 'to': 4, 's': 8},
            {'from': 1, 'to': 4, 's': 3},
            {'from': 1, 'to': 4, 's': 1},
            {'from': 3, 'to': 2, 's': 9}
        ]

        expected = [
            {'from': 1, 'to': 4, 's': 10},
            {'from': 1, 'to': 4, 's': 2},
            {'from': 3, 'to': 2, 's': 9}
        ]

        result = new_compression(path=path, max_journey_size=10)

        self.assertEqual(result, expected)
