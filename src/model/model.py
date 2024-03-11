"""Creates a model for the problem to be solved by the algorithms"""

from typing import List, Dict
import random
from model.hub import Hub


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


def generate_s_vals(n: int, max_def: int, max_sur: int) -> List[int]:
    """
    Creates n values of hub supply for the hubs created such that sum of the s values is 0

    params:
        n - The number of hubs
        max_def - Maximum deficit value of each hub
        max_sur - Maximum surplus value of each hub

    returns:
        A list of n s values, where no s value is 0, the sum of the values is 0 and the values stay within the range
    """
    # Set initia values of total_s and s vals for each hub
    total_s = 0
    s_vals = []

    # Repeat until n-1 s values in s_vals
    while len(s_vals) < n - 1:
        r_val = 0
        # If total_s = 0 then val between max_def and max_sur
        if total_s == 0:
            r_val = random.randint(max_def, max_sur)

        # elif total_s < 0 then val between (max_def - total_s) and max_sur
        # This keeps total_s between the bounds of max_def and max_sur
        elif total_s < 0:
            r_val = random.randint((max_def-total_s), max_sur)

        # Elif total_s > 0 then val between max_def and (max_sur - total_s)
        elif total_s > 0:
            r_val = random.randint(max_def, (max_sur-total_s))

        # Make sure r_val is not 0 and if so choose another number
        if r_val != 0:
            # Add it to total s and to s_vals
            total_s += r_val
            s_vals.append(r_val)

    # If total_s has reach 0 at this stage, will need to generate again
    if total_s == 0:
        return generate_s_vals(n=n, max_def=max_def, max_sur=max_sur)

    # Add the final s_val so that it sums to 0
    s_vals.append(0-total_s)

    return s_vals


def create_model(n: int, alpha: int, min_dist=1, max_def=-100, max_sur=100) -> Dict[int, Hub]:
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
        A dictionary of the hub names corresponding to the hub objects
    """
    # Generate the location of the hubs
    hub_locs = create_locations(n=n, alpha=alpha, min_dist=min_dist)

    # Generate the n s_vals
    s_vals = generate_s_vals(n=n, max_def=max_def, max_sur=max_sur)

    # Create the hubs as hub objects
    hubs: Dict[int, Hub] = {}
    for i in range(len(hub_locs)):
        # TODO calculate an s for the hub
        new_hub = Hub(name=hub_locs[i]['name'], s=s_vals[i],
                      long=hub_locs[i]['long'], lat=hub_locs[i]['lat'])
        hubs[new_hub.get_name()] = new_hub

    # Calculate manhattan distances between hubs
    for i in range(len(hubs)):
        # Only calculate for new hubs as the add_connection method adds to both connections dicts
        for j in range(i, len(hubs)):
            # Add the connection to both hubs
            hubs[i].add_connection(hubs[j])

    return hubs
