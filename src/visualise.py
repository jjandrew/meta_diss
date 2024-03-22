import matplotlib.pyplot as plt
from model.depot import Depot
from typing import Dict, List


def write_model(model: Dict[int, Depot], filename="values"):
    with open(f'./models/{filename}.txt', 'w') as f:
        for hub in model.values():
            f.write(str(hub) + '\n')


def read_model(filename: str) -> Dict[int, Depot]:
    model: Dict[int, Depot] = {}
    with open(f'./modelExamples/{filename}.txt', 'r') as f:
        for line in f:
            parts = line.split(' ')
            id = int(parts[1].strip(','))
            coords = parts[3]
            x, y, _ = coords.split(',')
            x = int(x.strip('('))
            y = int(y.strip(')'))
            s = int(parts[-1].strip())
            hub = Depot(name=id, s=s, long=x, lat=y)
            model[id] = hub

    # Connect all hubs
    for i in range(len(model)):
        for j in range(i, len(model)):
            model[i].add_connection(model[j])

    return model


def show_best(vals):
    for i in range(1, len(vals)):
        if vals[i] > vals[i-1]:
            vals[i] = vals[i-1]


def plot_network(model: Dict[int, Depot]):
    """
    Plots the network using matplot lib.
    Displays the supply values of each hub along with its name

    params:
        model - A list of hub objects
    """
    # Extracting data from hub objects
    names = [model[hub_name].get_name() for hub_name in model]
    x_positions = [model[hub_name].get_long() for hub_name in model]
    y_positions = [model[hub_name].get_lat() for hub_name in model]
    supply_values = [model[hub_name].get_s() for hub_name in model]

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

    # Displaying the names of each hub with higher zorder
    for name, x, y, s in zip(names, x_positions, y_positions, supply_values):
        plt.text(x, y, f'{name}\nSupply: {s}', ha='center',
                 va='center', fontsize=8, zorder=3)

    # Setting plot labels and title
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.title('Hub Network Visualization')

    # Zoom out by setting larger axis limits
    plt.xlim(min(x_positions) - 10, max(x_positions) + 10)
    plt.ylim(min(y_positions) - 10, max(y_positions) + 10)

    # Displaying the plot
    plt.show()


def plot_convergence(fitness_vals: List[int], algo: str):
    # Generate x values (position in list + 1) and y values (integer values)
    x_vals = [i for i in range(len(fitness_vals))]
    y_vals = fitness_vals

    # Plot
    plt.plot(x_vals, y_vals, marker='o', linestyle='-')
    plt.title(f'{algo} Fitness vs Number of Fitness Iterations')
    plt.xlabel('Fitness Iteration')
    plt.ylabel('Fitness')
    plt.grid(True)
    plt.show()


def plot_convergence_comparison(aco: List[int], ga: List[int], sa: List[int], rs: List[int], n: int):
    x = range(len(ga))

    # Plotting
    plt.plot(x, aco, label='ACO')
    plt.plot(x, ga, label='GA')
    plt.plot(x, sa, label='SA')
    plt.plot(x, rs, label='Random Search')

    # Adding labels and title
    plt.xlabel('Fitness Evaluations')
    plt.ylabel('Best Fitness')
    plt.title(
        f'Comparison of Algorithm Best Fitness on a {n}-depot TNRP')

    # Adding a legend
    plt.legend()

    # Displaying the plot
    plt.show()


def plot_fitness_comparison(aco: List[int], ga: List[int], sa: List[int], rs: List[int], sizes: List[int]):
    x = sizes

    # Plotting
    plt.plot(x, aco, label='ACO')
    plt.plot(x, ga, label='GA')
    plt.plot(x, sa, label='SA')
    plt.plot(x, rs, label='Random Search')

    # Adding labels and title
    plt.xlabel('No. of Depots')
    plt.ylabel('Best Fitness')
    plt.title(
        f'Comparison of Algorithm Best Fitness as TNRP size increases')

    # Adding a legend
    plt.legend()

    # Displaying the plot
    plt.show()


def plot_time_comparison(aco: List[int], ga: List[int], sa: List[int], sizes: List[int]):
    x = sizes

    # Plotting
    plt.plot(x, aco, label='ACO')
    plt.plot(x, ga, label='GA')
    plt.plot(x, sa, label='SA')

    # Adding labels and title
    plt.xlabel('No. of Depots')
    plt.ylabel('Time (s)')
    plt.title(
        f'Comparison of Algorithm Computation Times as TNRP size increases')

    # Adding a legend
    plt.legend()

    # Displaying the plot
    plt.show()
