"""
File for testing the convergence pattern of the GA algorithm
"""
from visualise import plot_convergence, read_model, show_best
from searches.ga.ga import ga


if __name__ == "__main__":
    # Set the problem size to perform the experiment on
    n = 30
    model = read_model(filename=str(n))
    max_j_size = 20

    # Select the number of fitness evaluations
    iters = 10000

    # Set the algorithm hyperparameters
    m_r = 0.5
    pop_size = 50
    t_size = 10
    c_r = 0.6

    # Execute the GA algorithm using the hyperparameters
    vals, _ = ga(mutation_rate=m_r, crossover_rate=c_r, pop_size=pop_size, t_size=t_size, n=iters,
                 model=model, max_journey_size=max_j_size)

    # Show the best fitness at each iteration
    show_best(vals)

    # Plot the fitness of the algorithm
    plot_convergence(fitness_vals=vals, algo="GA")
