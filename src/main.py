from model.model import create_model
from visualise import plot_network, plot_convergence
from model.hub import Hub
from searches.brute_force.brute import brute
from searches.ga.ga import ga
from searches.aco.AS import AS
from searches.sa.sa import sa
from searches.aco.create_matrices import create_dist_matrix, create_heur_matrix, create_pher_matrix
from utils import reduce_model


def show_best(vals):
    for i in range(1, len(vals)):
        if vals[i] > vals[i-1]:
            vals[i] = vals[i-1]


if __name__ == "__main__":
    n = 100
    model = create_model(n=n, alpha=2)

    d = create_dist_matrix(model=model)
    p = create_pher_matrix(model=model, dist_matrix=d, p_min=1, p_max=1)
    h = create_heur_matrix(dist_matrix=d)

    # vals = sa(start_temp=200, cool_r=0.95,
    #           max_journey_size=20, model=model, n=20000)

    # m = 20
    # vals = AS(model=model, m=m, e=0.02, Q=1/m*n, d=d,
    #           p=p, h=h, n=10000, max_journey_size=20, alpha=1, beta=2)

    vals = ga(mutation_rate=0.25, pop_size=40, t_size=10, n=20000,
              model=model, max_journey_size=20, crossover_rate=0.15)

    show_best(vals)
    plot_convergence(vals)

    # plot_network(model=model)
