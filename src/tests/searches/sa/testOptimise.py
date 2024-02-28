import unittest
from model.model import create_model
import numpy as np
from searches.sa.sa import sa
import copy


class TestSAClass(unittest.TestCase):
    def test_optimisation(self):

        models = []
        for _ in range(3):
            models.append(create_model(n=30, alpha=2))
        orders = []

        for start_temp in range(100, 5000, 200):
            print(start_temp)
            for cool_r in np.arange(0.7, 0.99, 0.04):
                combined_perc_dif = 0
                for model in models:
                    for _ in range(5):
                        start, end = sa(start_temp=start_temp, n=5000,
                                        cool_r=cool_r, max_journey_size=20, model=copy.deepcopy(model))
                        combined_perc_dif += (start-end) / start
                orders.append({"st": start_temp, "cr": cool_r,
                               "dif": combined_perc_dif/25})

        orders.sort(key=lambda x: x['dif'])

        print(orders)
