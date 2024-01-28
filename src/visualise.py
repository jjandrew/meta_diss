import matplotlib.pyplot as plt
from model.hub import Hub
from typing import List


def plot_network(model: List[Hub]):
    """
    Plots the network using matplot lib.
    Displays the supply values of each hub along with its name

    params:
        model - A list of hub objects
    """
    # Extracting data from hub objects
    names = [hub.get_name() for hub in model]
    x_positions = [hub.get_long() for hub in model]
    y_positions = [hub.get_lat() for hub in model]
    supply_values = [hub.get_s() for hub in model]

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
