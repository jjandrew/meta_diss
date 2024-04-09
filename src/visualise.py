"""
Allows for the visualisation of the experiments and the TNRP
"""
import matplotlib.pyplot as plt
from typing import Dict, List
from TNRP_model.depot import Depot


def write_model(model: Dict[int, Depot], filename: str):
    """
    Writes a new TNRP to a text file

    params:
        model - The TNRP model to write to the text file in the form depot name: Depot object
        filename - The name of the file located in ./modelExamples/<filename>.txt to write to
    """
    # Open the text file
    with open(f'./models/{filename}.txt', 'w') as f:
        # Overwrite each line with the to_string method to print out a TNRP
        for depot in model.values():
            f.write(str(depot) + '\n')


def read_model(filename: str) -> Dict[int, Depot]:
    """
    Reads a TNRP from a text file

    params:
        filename - The name of the file located in ./modelExamples/<filename>.txt

    returns:
        The TNRP model as a dictionary of depot_name: Depot Object
    """
    model: Dict[int, Depot] = {}
    # Open the text file
    with open(f'./modelExamples/{filename}.txt', 'r') as f:
        # For each of the lines (depots)
        for line in f:
            # Split the line by spaces
            parts = line.split(' ')
            # Obtain the name of the depot
            id = int(parts[1].strip(','))
            # Obtain the coordinates of the depot
            coords = parts[3]
            x, y, _ = coords.split(',')
            x = int(x.strip('('))
            y = int(y.strip(')'))
            # Obtain the initial supply value of the depot
            s = int(parts[-1].strip())
            # Create the initial depot object
            dep = Depot(name=id, s=s, x=x, y=y)
            # Add depot object to the TNRP model
            model[id] = dep

    # Connect all depots in the model
    for i in range(len(model)):
        for j in range(i, len(model)):
            model[i].add_connection(model[j])

    return model


def show_best(vals: List[int]):
    """
    Changes a convergence graph in place to only show improvements in best fitness

    params:
        vals - The fitness values for each iteration
    """
    # For each of the positions in the array
    for i in range(1, len(vals)):
        # If the position is a worse fitness then set its value to the best fitness so far
        if vals[i] > vals[i-1]:
            vals[i] = vals[i-1]


def plot_network(model: Dict[int, Depot]):
    """
    Plots the network using matplot lib.
    Displays the supply values of each depot along with its name

    params:
        model - A list of depot objects
    """
    # Extracting data from depot objects
    names = [model[dep_name].get_name() for dep_name in model]
    x_positions = [model[dep_name].get_long() for dep_name in model]
    y_positions = [model[dep_name].get_lat() for dep_name in model]
    supply_values = [model[dep_name].get_s() for dep_name in model]

    # Plotting the network
    plt.figure(figsize=(10, 6))

    # Draw lines connecting all points with zorder set to a lower value
    for i in range(len(model)):
        for j in range(i+1, len(model)):
            plt.plot([x_positions[i], x_positions[j]], [
                     y_positions[i], y_positions[j]], 'k--', linewidth=0.5, zorder=1)

    # Scatter plot with points and text using plot with marker
    size_of_points = 50
    plt.plot(x_positions, y_positions, 'o', markersize=size_of_points, alpha=1,
             color='darkorange', markeredgecolor='k', markeredgewidth=1, zorder=2)

    # Displaying the names of each depot with higher zorder
    for name, x, y, s in zip(names, x_positions, y_positions, supply_values):
        plt.text(x, y, f'{name}\nSupply: {s}', ha='center',
                 va='center', fontsize=8, zorder=3)

    # Setting plot labels and title
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.title('TNRP Network Visualization')

    # Zoom out by setting larger axis limits
    plt.xlim(min(x_positions) - 10, max(x_positions) + 10)
    plt.ylim(min(y_positions) - 10, max(y_positions) + 10)

    # Displaying the plot
    plt.show()


def plot_convergence(fitness_vals: List[int], algo: str):
    """
    Plots the convergence of an algorithm on the TNRP

    paramsL
        fitness_vals: The fitness values to plot in the convergence
        algo: The name of the algorithm to plot
    """

    # Generate x values (position in list + 1) and y values (fitness values)
    x_vals = [i for i in range(len(fitness_vals))]
    y_vals = fitness_vals

    # Plot the x and y values on a graph
    plt.plot(x_vals, y_vals, marker='o', linestyle='-')
    plt.title(f'{algo} Fitness vs Number of Fitness Iterations')
    plt.xlabel('Fitness Iteration')
    plt.ylabel('Fitness')
    plt.show()


def plot_convergence_comparison(aco: List[int], ga: List[int], sa: List[int], rs: List[int], n: int):
    """
    Plots a comparison of algorithm convergences on a graph

    params:
        aco - The fitness values for the ACO algorithm
        ga - The fitness values for the GA
        sa - The fitness values for the SA
        rs- the fitness values for the Random Search
        n - The number of depots in the TNRP
    """
    # Obtain the number of fitness iterations
    x = range(len(ga))

    # Plot each algorithm as its own line
    plt.plot(x, aco, label='ACO')
    plt.plot(x, ga, label='GA')
    plt.plot(x, sa, label='SA')
    plt.plot(x, rs, label='Random Search')

    plt.xlabel('Fitness Evaluations')
    plt.ylabel('Best Fitness')
    plt.title(
        f'Comparison of Algorithm Best Fitness on a {n}-depot TNRP')

    # Display a key
    plt.legend()

    plt.show()


def plot_fitness_comparison(aco: List[int], ga: List[int], sa: List[int], rs: List[int], sizes: List[int]):
    """
    Plots a comparison of algorithm best fitnesses for each problem size on a graph

    params:
        aco - The best fitness values of the ACO algorithm for each problem size
        ga - The best fitness values of the GA algorithm for each problem size
        sa - The best fitness values of the SA algorithm for each problem size
        rs- The best fitness values of the Random Search algorithm for each problem size
        sizes - List of problem sizes corresponding to positions of other lists
    """
    # Set x values to the problem sizes
    x = sizes

    # Plot each algorithm as its own line
    plt.plot(x, aco, label='ACO')
    plt.plot(x, ga, label='GA')
    plt.plot(x, sa, label='SA')
    plt.plot(x, rs, label='Random Search')

    plt.xlabel('No. of Depots')
    plt.ylabel('Best Fitness')
    plt.title(
        f'Comparison of Algorithm Best Fitness as TNRP size increases')

    # Add a key
    plt.legend()

    plt.show()


def plot_time_comparison(aco: List[int], ga: List[int], sa: List[int], sizes: List[int]):
    """
    Plots a comparison of algorithm computation time for each problem size on a graph

    params:
        aco - The mean computation times of the ACO algorithm for each problem size
        ga - The mean computation times of the GA algorithm for each problem size
        sa - The mean computation times of the SA algorithm for each problem size
        sizes - List of problem sizes corresponding to positions of other lists
    """
    # Set x values to the problem sizes
    x = sizes

    # Plot each algorithm as its own line
    plt.plot(x, aco, label='ACO')
    plt.plot(x, ga, label='GA')
    plt.plot(x, sa, label='SA')

    plt.xlabel('No. of Depots')
    plt.ylabel('Time (s)')
    plt.title(
        f'Comparison of Algorithm Computation Times as TNRP size increases')

    # Add a key
    plt.legend()

    # Displaying the plot
    plt.show()
