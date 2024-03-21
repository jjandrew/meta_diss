import unittest
from searches.aco.AS import AS
from searches.aco.create_matrices import create_heur_matrix, create_dist_matrix, create_pher_matrix
from model.tnrp_model import create_model
import numpy as np


class TestACOClass(unittest.TestCase):
    def test_optimisation(self):

        n = 20
        models = []
        for _ in range(3):
            models.append(create_model(n=n, alpha=2))
        orders = []

        for Q in np.arange(5, 60, 5):
            print(Q)
            combined_perc_dif = 0
            for model in models:
                for _ in range(5):
                    d = create_dist_matrix(model=model)
                    h = create_heur_matrix(dist_matrix=d)
                    p = create_pher_matrix(
                        model=model, dist_matrix=d, p_min=1, p_max=1)
                    vals = AS(model=model, m=1, e=0.4, Q=Q*n,
                              max_journey_size=20, n=10, d=d, p=p, h=h, alpha=1, beta=6)
                    start = vals[0]
                    end = vals[-1]

                combined_perc_dif += (start-end) / start
            orders.append(
                {"Q": Q*n, "dif": combined_perc_dif/15})

        orders.sort(key=lambda x: x['dif'])

        print(orders)

        # for _ in range(10):
        #     d = create_dist_matrix(model=model)
        #     h = create_heur_matrix(dist_matrix=d)
        #     p = create_pher_matrix(model=model, dist_matrix=d)
        #     start, end = AS(model=model, m=1, e=0.7, Q=700, d=d,
        #                     p=p, h=h, n=1000, max_journey_size=20)

        #     print(start, end)
