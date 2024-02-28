"""
Tests GA converges on an optimum
"""
import unittest
from model.model import create_model
from searches.ga.ga import ga
import numpy as np


class TestGAClass(unittest.TestCase):
    """
    Tests the GA converges and works correctly
    """

    def test_valid_solution(self):
        model = create_model(n=30, alpha=2)

        # orders = []

        # for m_rate in np.arange(0.1, 0.3, 0.05):
        #     for pop_size in range(20, 41, 10):
        #         print(m_rate, pop_size)
        #         for t_size in range(2, 11, 2):
        #             for crossover_rate in np.arange(0, 0.2, 0.05):
        #                 combined_perc_dif = 0
        #                 for _ in range(5):
        #                     start, end = ga(mutation_rate=m_rate, pop_size=pop_size, t_size=t_size,
        #                                     n=100, model=model, max_journey_size=20, crossover_rate=crossover_rate)
        #                     combined_perc_dif += (start-end) / start
        #                 orders.append({"m": m_rate, "p": pop_size,  "t": t_size,
        #                               "cr": crossover_rate, "dif":  combined_perc_dif/5})

        # orders.sort(key=lambda x: x['dif'])

        # print("__________________")
        # print("__________________")

        # print(orders)
        for _ in range(10):
            start, end = ga(mutation_rate=0.25, pop_size=40, t_size=10,
                            n=100, model=model, max_journey_size=20, crossover_rate=0.15)

            self.assertLess(end, start)
