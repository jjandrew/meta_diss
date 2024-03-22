"""
File for testing the convergence pattern of the AS algorithm
"""
from visualise import plot_convergence, read_model, show_best
from searches.aco.AS import AS
from searches.aco.create_matrices import create_dist_matrix, create_heur_matrix, create_pher_matrix


if __name__ == "__main__":
    # Set the problem size to perform the experiment on
    n = 30
    model = read_model(filename=str(n))
    max_j_size = 20

    # Select the number of fitness evaluations
    iters = 10000

    # Create the matrices for the AS algorithm
    d = create_dist_matrix(model=model)
    p = create_pher_matrix(model=model, dist_matrix=d, p_min=1, p_max=1)
    h = create_heur_matrix(dist_matrix=d)

    # Set the algorithm hyperparameters
    m = 1
    e = 0.2
    Q = 100
    alpha = 1
    beta = 2

    # Execute the AS algorithm using the hyperparameters
    vals, _ = AS(model=model, m=m, e=e, Q=Q, d=d,
                 p=p, h=h, n=iters, max_journey_size=max_j_size, alpha=alpha, beta=beta)

    # Show the best fitness at each iteration
    show_best(vals)

    # Plot the fitness of the algorithm
    plot_convergence(fitness_vals=vals, algo="ACO")
