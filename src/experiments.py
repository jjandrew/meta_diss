"""
Performs the comparison of algorithms on the TNRP
"""
import copy
import numpy as np
import time
from searches.aco.AS import AS
from searches.aco.create_matrices import create_dist_matrix, create_heur_matrix, create_pher_matrix
from searches.ga.ga import ga
from searches.sa.sa import sa
from searches.random_search import random_search
from utils import fitness
from visualise import read_model, show_best, plot_convergence_comparison, plot_time_comparison, plot_fitness_comparison

if __name__ == "__main__":
    # Create an array of the problem sizes explored in the experiment
    prob_sizes = []

    # Store the computation times for the metaheuristic algorithm
    aco_comp_times = []
    ga_comp_times = []
    sa_comp_times = []

    # Store the best final fitness for each algorithm
    aco_fitnesses = []
    ga_fitnesses = []
    sa_fitnesses = []
    rs_fitnesses = []

    # Obtain the range of TNRP problem size instances to be used
    for n in range(10, 21, 10):
        # Output the model size
        print(f"N={n}")
        # Add model size to sizes explored
        prob_sizes.append(n)

        # alpha value used to scale average distance between depots in the model
        alpha = 2

        # Read the model from the text file
        model = read_model(filename=str(n))

        # Create empty lists for storing fitness values, best convergence paths and computation times
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

        # Set a value for the number of runs of each algorithm
        num_runs = 2

        # Set a value for the number of fitness evaluations for each algorithm
        iters = 5000

        for i in range(num_runs):  # Perform the number of runs
            print(f'Run Number {i+1}')

        ###############################################

            # ACO algorithm execution
            print("Starting ACO")
            # Create the distance, pheromone and heuristic matrices
            d = create_dist_matrix(model=model)
            # Pheromone matrix values initialised between 1 and 1
            p = create_pher_matrix(
                model=model, dist_matrix=d, p_min=1, p_max=1)
            h = create_heur_matrix(dist_matrix=d)

            # Store the start time of the AS algorithm
            aco_start_time = time.time()
            # Perform the AS algorithm using parameters decided in testing
            as_run, _ = AS(model=model, m=1, e=0.2, Q=100, d=d, p=p, h=h,
                           n=iters, max_journey_size=20, alpha=1, beta=3)
            # Calculate the difference in time from when the AS started to now
            aco_time_dif = time.time() - aco_start_time
            aco_times.append(aco_time_dif)

            # Only show improvements in best fitness
            show_best(as_run)

            # Add the best value from the run to the values of each algorithm run
            aco_vals.append(as_run[-1])
            # Sort the values of the previous runs
            aco_vals.sort()
            # If this run has the best fitness then store its convergence
            if aco_vals[0] == as_run[-1]:
                aco_best_convergence = as_run

        ###############################################

            # Genetic Algorithm
            print("Starting GA")
            # Store the start time of the GA algorithm
            ga_start_time = time.time()
            # Perform the GA algorithm using parameters decided in testing
            ga_run, _ = ga(mutation_rate=0.5, pop_size=50, t_size=10, n=iters,
                           model=model, max_journey_size=20, crossover_rate=0.6)
            # Calculate the difference in time from when the GA started to now
            ga_time_dif = time.time() - ga_start_time
            ga_times.append(ga_time_dif)

            # Only show improvements in best fitness
            show_best(ga_run)

            # Add the best value from the run to the values of each algorithm run
            ga_vals.append(ga_run[-1])
            # Sort the values of the previous runs
            ga_vals.sort()
            # If this run has the best fitness then store its convergence
            if ga_vals[0] == ga_run[-1]:
                ga_best_convergence = ga_run

        ###############################################

            # Simulated Annealing
            print("Starting SA")
            # Calculate the initial and end temperature using values found in testing
            initial_temp = (alpha * n) / 3
            end_temp = 0.001
            # Calcuate the cooling rate using values from testing
            cr = (end_temp/initial_temp)**(1/(iters - 1))

            # Store the start time of the SA algorithm
            sa_start_time = time.time()
            # Perform the SA algorithm using parameters decided in testing
            sa_run, _ = sa(start_temp=initial_temp, cool_r=cr,
                           max_journey_size=20, model=copy.deepcopy(model), n=iters)
            # Calculate the difference in time from when the SA started to now
            sa_time_dif = time.time() - sa_start_time
            sa_times.append(sa_time_dif)

            # Only show improvements in best fitness
            show_best(sa_run)

            # Add the best value from the run to the values of each algorithm run
            sa_vals.append(sa_run[-1])
            # Sort the values of the previous runs
            sa_vals.sort()
            # If this run has the best fitness then store its convergence
            if sa_vals[0] == sa_run[-1]:
                sa_best_convergence = sa_run

        ###############################################

            # Random Search
            print("Starting Random Search")
            # Store the start time of the random search
            rs_start_time = time.time()
            # Store the value for each of the iteration runs
            rs_run = []
            # Perform the random search up to the number of fitness evaluations
            for _ in range(iters):
                solution = random_search(
                    model=copy.deepcopy(model), max_journey_size=20)
                # Add the fitness of solution to the random search run
                rs_run.append(fitness(path=solution, model=model))
            # Calculate length of time for random search to execute
            rs_time_dif = time.time() - rs_start_time
            rs_times.append(rs_time_dif)

            # Only show improvements in best fitness
            show_best(rs_run)

            # Add the best value from the run to the values of each algorithm run
            rs_vals.append(rs_run[-1])
            # Sort the values of the previous runs
            rs_vals.sort()
            # If this run has the best fitness then store its convergence
            if rs_vals[0] == rs_run[-1]:
                rs_best_convergence = rs_run

            print()

        print("#############")
        print("#############")

        # Calculate mean, best and worst final fitness for each of the algorithms runs
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

        # Add the best fitness of each algorithm to the store of all fitnesses
        aco_fitnesses.append(aco_best)
        ga_fitnesses.append(ga_best)
        sa_fitnesses.append(sa_best)
        rs_fitnesses.append(rs_best)

        # Outpus stats
        print(
            f"Solution Quality \nACO --- Avg: {aco_av}, Best: {aco_best}, Worst: {aco_worst} \nGA --- Avg: {ga_av}, Best: {ga_best}, Worst: {ga_worst} \nSA --- Avg: {sa_av}, Best: {sa_best}, Worst: {sa_worst} \nRandom --- Avg: {rs_av}, Best: {rs_best}, Worst: {rs_worst} \n")

        print()

        # Calculate mean, best and worst compuation runs for each of the algorithms runs
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

        # Store the mean computation time for each algorithm
        aco_comp_times.append(aco_av)
        ga_comp_times.append(ga_av)
        sa_comp_times.append(sa_av)

        # Outpus computation times
        print(
            f"Algorithm Execution Times\nACO --- Avg: {aco_av}, Best: {aco_best}, Worst: {aco_worst} \nGA --- Avg: {ga_av}, Best: {ga_best}, Worst: {ga_worst} \nSA --- Avg: {sa_av}, Best: {sa_best}, Worst: {sa_worst} \nRandom --- Avg: {rs_av}, Best: {rs_best}, Worst: {rs_worst} \n")

        # Plot a comparison of convergences
        plot_convergence_comparison(aco=aco_best_convergence,
                                    ga=ga_best_convergence, sa=sa_best_convergence, rs=rs_best_convergence, n=n)

        print()
        print("---------------------")
        print("---------------------")
        print()

    # Plot the time comparison
    plot_time_comparison(aco=aco_comp_times, ga=ga_comp_times,
                         sa=sa_comp_times, sizes=prob_sizes)

    # Plot the quality comparison
    plot_fitness_comparison(aco=aco_fitnesses, ga=ga_fitnesses,
                            sa=sa_fitnesses, rs=rs_fitnesses, sizes=prob_sizes)
