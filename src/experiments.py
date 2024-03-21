from searches.aco.AS import AS
from searches.aco.create_matrices import create_dist_matrix, create_heur_matrix, create_pher_matrix
from searches.ga.ga import ga
from searches.sa.sa import sa
from searches.random import random_search
from utils import fitness
from visualise import read_model, show_best, plot_comparison
import copy
import numpy as np
import time

if __name__ == "__main__":
    for n in range(80, 81, 20):
        print(f"N={n}")
        alpha = 2
        model = read_model(filename=str(n))

        aco_vals = []
        aco_best_convergence = []
        aco_times = []

        ga_vals = []
        ga_best_convergence = []
        ga_times = []

        sa_vals = []
        sa_best_convergence = []
        sa_times = []

        rs_vals = []
        rs_best_convergence = []
        rs_times = []

        iters = 50000
        num_runs = 5

        for i in range(num_runs):
            print(f'Run Number {i+1}')

            # ACO
            print("Starting ACO")
            d = create_dist_matrix(model=model)
            p = create_pher_matrix(
                model=model, dist_matrix=d, p_min=1, p_max=1)
            h = create_heur_matrix(dist_matrix=d)

            aco_start_time = time.time()
            as_run = AS(model=model, m=1, e=0.2, Q=100, d=d, p=p, h=h,
                        n=iters, max_journey_size=20, alpha=1, beta=3)
            aco_time_dif = time.time() - aco_start_time
            aco_times.append(aco_time_dif)
            show_best(as_run)
            aco_vals.append(as_run[-1])
            aco_vals.sort()
            if aco_vals[0] == as_run[-1]:
                aco_best_convergence = as_run

            # GA
            print("Starting GA")
            ga_start_time = time.time()
            ga_run = ga(mutation_rate=0.5, pop_size=50, t_size=10, n=iters,
                        model=model, max_journey_size=20, crossover_rate=0.6)
            ga_time_dif = time.time() - ga_start_time
            ga_times.append(ga_time_dif)
            show_best(ga_run)
            ga_vals.append(ga_run[-1])
            ga_vals.sort()
            if ga_vals[0] == ga_run[-1]:
                ga_best_convergence = ga_run

            # SA
            print("Starting SA")
            initial_temp = (alpha * n) / 3
            end_temp = 0.001
            cr = (end_temp/initial_temp)**(1/(iters - 1))
            sa_start_time = time.time()
            sa_run = sa(start_temp=initial_temp, cool_r=cr,
                        max_journey_size=20, model=copy.deepcopy(model), n=iters)
            sa_time_dif = time.time() - sa_start_time
            sa_times.append(sa_time_dif)
            show_best(sa_run)
            sa_vals.append(sa_run[-1])
            sa_vals.sort()
            if sa_vals[0] == sa_run[-1]:
                sa_best_convergence = sa_run

            # Random
            print("Starting Random Search")
            rs_start_time = time.time()
            rs_run = []
            for _ in range(iters):
                solution = random_search(
                    model=copy.deepcopy(model), max_journey_size=20)
                rs_run.append(fitness(path=solution, model=model))
            rs_time_dif = time.time() - rs_start_time
            rs_times.append(rs_time_dif)
            show_best(rs_run)
            rs_vals.append(rs_run[-1])
            rs_vals.sort()
            if rs_vals[0] == rs_run[-1]:
                rs_best_convergence = rs_run

            print()

        print("#############")
        print("#############")
        # ACO STATS
        aco_av = np.mean(aco_vals)
        aco_best = min(aco_vals)
        aco_worst = max(aco_vals)

        # GA STATS
        ga_av = np.mean(ga_vals)
        ga_best = min(ga_vals)
        ga_worst = max(ga_vals)

        # SA STATS
        sa_av = np.mean(sa_vals)
        sa_best = min(sa_vals)
        sa_worst = max(sa_vals)

        # RS STATS
        rs_av = np.mean(rs_vals)
        rs_best = min(rs_vals)
        rs_worst = max(rs_vals)

        # Outpus stats
        print(
            f"Solution Quality \nACO --- Avg: {aco_av}, Best: {aco_best}, Worst: {aco_worst} \nGA --- Avg: {ga_av}, Best: {ga_best}, Worst: {ga_worst} \nSA --- Avg: {sa_av}, Best: {sa_best}, Worst: {sa_worst} \nRandom --- Avg: {rs_av}, Best: {rs_best}, Worst: {rs_worst} \n")

        print()

        # ACO STATS
        aco_av = np.mean(aco_times)
        aco_best = min(aco_times)
        aco_worst = max(aco_times)

        # GA STATS
        ga_av = np.mean(ga_times)
        ga_best = min(ga_times)
        ga_worst = max(ga_times)

        # SA STATS
        sa_av = np.mean(sa_times)
        sa_best = min(sa_times)
        sa_worst = max(sa_times)

        # Random STATS
        rs_av = np.mean(rs_times)
        rs_best = min(rs_times)
        rs_worst = max(rs_times)

        # Outpus stats
        print(
            f"Algorithm Execution Times\nACO --- Avg: {aco_av}, Best: {aco_best}, Worst: {aco_worst} \nGA --- Avg: {ga_av}, Best: {ga_best}, Worst: {ga_worst} \nSA --- Avg: {sa_av}, Best: {sa_best}, Worst: {sa_worst} \nRandom --- Avg: {rs_av}, Best: {rs_best}, Worst: {rs_worst} \n")

        # Comparison
        plot_comparison(aco=aco_best_convergence,
                        ga=ga_best_convergence, sa=sa_best_convergence, rs=rs_best_convergence, n=n)

        print()
        print("---------------------")
        print("---------------------")
        print()
