"""Creates a model for the problem to be solved by the algorithms"""

from typing import List, Dict
import random
from src.classes.hub import Hub


def create_empty_matrix(n: int, alpha: int) -> List[List[int]]:
    """
    Creates an empty alpha x n square matrix 
    Blank values are used of -1 in each location

    params: 
        n - The number of hubs in the matrix
        alpha - A constant to scale the matrix by

    returns:
        empty (alpha * n)^2 matrix
    """
    # Create empty matrix where an empty spot is represented by -1 value
    matrix = []
    # Add alpha * n rows of length alpha * n
    for _ in range(alpha * n):
        # Add
        row = []
        for _ in range(alpha * n):
            # Add -1 as an empty location
            row.append(-1)
        matrix.append(row)

    return matrix


def create_locations(n: int, alpha: int, min_dist: int) -> List[Dict[str, int]]:
    """
    Creates a populated matrix of spread out hubs

    params:
        n - The number of hubs in the matrix
        alpha - A constant to scale the matrix by
        min_dist - The minimum distance as a manhattan distance between hubs (default = 1)

    returns:
        Populated (alpha * n)^2 matrix
    """
    # Create an empty matrix
    matrix = create_empty_matrix(n=n, alpha=alpha)
    # Faster to calculate distances between hub when locations displayed in one place
    # As only need to check n hubs, not (alpha * n)^2 comparisons
    # Create a list of discts: {name: name, long: long, lat: lat}
    # TODO maybe chance to a list of hub objects
    hub_locs = []

    # Populate the matrix
    # Create the n hubs
    for i in range(n):
        # Continue until the hub is added
        added = False
        # TODO needs a terminating condition if not possible to generate using the min_dist metric
        # TODO calculate this if it has been trying for too many attempts
        while True:
            # Generate a random value between 0 and (alpha * n) -1 for latitude and longitude values
            long = random.randint(0, (alpha * n) - 1)
            lat = random.randint(0, (alpha * n) - 1)

            # Check whether longitude and latitude of hubs is empty
            # TODO need to check it is within the minimum distance
            # TODO probably faster to check just the surrounding matrix rather than use list of node locations
            if matrix[lat][long] == -1:
                matrix[lat][long] = i
                # Add the location of the hubs to hub_locs list
                hub_locs.append({"name": i, "long": long, "lat": lat})
                # If the hub is added break from the loop
                added = True
                break

        # TODO need to add this for a later date
        if not added:
            print("Need to do something")

    # Return the locations of the hubs
    return hub_locs


def create_model(n: int, alpha: int, min_dist=1, max_def=-100, max_sur=100) -> List[Hub]:
    """
    Create a model with n hubs at randomly generated locations
    Each hub has a supply value S between max deficit and max surplus

    params:
        n - The number of hubs in the matrix
        alpha - A constant to scale the matrix by
        min_dist - The minimum distance between hubs (default = 1)
        max_def - The maximum supply deficit value
        max_sur - The maximum supply surplus value

    returns:
        A list of the hubs
    """
    # Generate the location of the hubs
    hub_locs = create_locations(n=n, alpha=alpha, min_dist=min_dist)

    # Create the hubs as hub objects
    hubs = []
    for hub in hub_locs:
        # TODO calculate an s for the hub
        new_hub = Hub(name=hub['name'], s=0, long=hub['long'], lat=hub['lat'])
        hubs.append(new_hub)

    # Calculate manhattan distances between hubs
    for i in range(len(hubs)):
        # Only calculate for new hubs as the add_connection method adds to both connections dicts
        for j in range(i, len(hubs)):
            # Add the connection to both hubs
            hubs[i].add_connection(hubs[j])

    return hubs
