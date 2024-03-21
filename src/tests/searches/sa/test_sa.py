"""
Tests the SA algorithm
"""
import unittest
from searches.sa.sa import sa, accept
from model.tnrp_model import create_model


class TestSAClass(unittest.TestCase):
    """
    Test suite for the simulated annealing algorithm
    """

    def test_acceptance_for_better_solution(self):
        """
        Tests that the acceptance algorithm performs as expected
        """
        # Negative delta means new solution is better
        delta = -100
        t = 100

        self.assertTrue(accept(delta_e=delta, t=t))

    def test_acceptance_for_equal_solution(self):
        """
        Tests an equally good solution is accepted
        """
        # Set delta to 0
        self.assertTrue(accept(delta_e=0, t=100))

    def test_acceptance_uses_temperature(self):
        """
        Tests that the acceptance function uses the exp(-delta/kt) parameter
        """
        # Positive delta means new solution is 10 worse
        delta = 10
        t = 100

        sum_trues = 0
        n = 10000
        for _ in range(n):
            if accept(delta_e=delta, t=t, k=1):
                sum_trues += 1

        self.assertAlmostEqual((sum_trues / n), 0.9, places=1)

    def test_sa(self):
        """
        Tests the SA algorithm converges on an optimum
        """
        for _ in range(10):
            model = create_model(n=20, alpha=2)
            original, final = sa(start_temp=100, n=1000, cool_r=0.90,
                                 max_journey_size=20, model=model)
            self.assertLess(final, original)
