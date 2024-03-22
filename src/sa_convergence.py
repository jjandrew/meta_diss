"""
File for testing the convergence pattern of the SA algorithm
"""
from visualise import plot_convergence, read_model, show_best
from searches.sa.sa import sa
import copy


if __name__ == "__main__":
    # Set the problem size to perform the experiment on
    n = 30
    model = read_model(filename=str(n))
    alpha = 2
    max_j_size = 20

    # Select the number of fitness evaluations
    iters = 10000

    # Set the algorithm hyperparameters
    initial_temp = (alpha * n) / 3
    end_temp = 0.001
    cr = (end_temp/initial_temp)**(1/(iters - 1))

    # Execute the SA algorithm using the hyperparameters
    vals, _ = sa(start_temp=initial_temp, cool_r=cr,
                 max_journey_size=max_j_size, model=copy.deepcopy(model), n=iters)

    # Show the best fitness at each iteration
    show_best(vals)

    # Plot the fitness of the algorithm
    plot_convergence(fitness_vals=vals, algo="SA")
