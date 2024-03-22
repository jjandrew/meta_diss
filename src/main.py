from model.tnrp_model import create_model
from visualise import plot_network, plot_convergence, write_model, read_model, show_best
from model.depot import Depot
from searches.brute_force.brute import brute
from searches.ga.ga import ga
from searches.aco.AS import AS
from searches.sa.sa import sa
from searches.aco.create_matrices import create_dist_matrix, create_heur_matrix, create_pher_matrix
from utils import reduce_model
import numpy as np
import copy
from searches.random_search import random_search
from utils import fitness


if __name__ == "__main__":
    n = 30
    alpha = 2
    # model = create_model(n=n, alpha=2)
    model = read_model(filename="30")
    # write_model(model)

    iters = 10000

    # d = create_dist_matrix(model=model)
    # p = create_pher_matrix(model=model, dist_matrix=d, p_min=1, p_max=1)
    # h = create_heur_matrix(dist_matrix=d)

    initial_temp = (alpha * n) / 3
    end_temp = 0.001
    cr = (end_temp/initial_temp)**(1/(iters - 1))
    vals = sa(start_temp=initial_temp, cool_r=cr,
              max_journey_size=20, model=copy.deepcopy(model), n=iters)

    # vals = AS(model=model, m=1, e=0.2, Q=100, d=d,
    #           p=p, h=h, n=10000, max_journey_size=20, alpha=1, beta=3)

    # vals = ga(mutation_rate=0.1, pop_size=50, t_size=10, n=10000,
    #           model=model, max_journey_size=20, crossover_rate=0.6)

    # plot_network(model=model)

    # vals = []
    # for _ in range(iters):
    #     solution = random_search(
    #         model=copy.deepcopy(model), max_journey_size=20)
    #     vals.append(fitness(path=solution, model=model))

    # show_best(vals)
    plot_convergence(vals)
