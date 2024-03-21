"""Creates a TNRP"""
from typing import List, Dict
import random
from model.depot import Depot


def create_empty_matrix(n: int, alpha: int) -> List[List[int]]:
    """
    Creates an empty square matrix of width: (alpha * n).
    A value of -1 is used where a depot is not present

    params: 
        n - The number of depots in the matrix
        alpha - A constant to scale the matrix by

    returns:
        empty (alpha * n)^2 matrix
    """
    # Create empty matrix where an empty spot is represented by -1 value
    matrix = []
    # Add alpha * n rows of length alpha * n
    for _ in range(alpha * n):
        row = []
        for _ in range(alpha * n):
            # Add -1 as an empty location
            row.append(-1)
        matrix.append(row)
    return matrix


def create_locations(n: int, alpha: int) -> List[Dict[str, int]]:
    """
    Creates a populated ((alpha * n) * (alpha * n)) matrix containing n unique depots

    params:
        n - The number of depots in the matrix
        alpha - A constant to scale the matrix by

    returns:
        Locations and corresponding names in a list of dictionaries of form: [{"name", "long", "lat"}]
    """
    # Need to ensure alpha > 1 so all depots can be created in unique locations
    if alpha < 1:
        raise ValueError("alpha must be greater than 1")

    # Create an empty matrix
    matrix = create_empty_matrix(n=n, alpha=alpha)

    # Create an array to store the locations and names of depots
    dep_locs = []

    # Populate the matrix
    for i in range(n):  # For the n unique depot names
        # Continue until the depot is added
        added = False
        while not added:
            # Generate a random value between 0 and (alpha * n) -1 for latitude and longitude values
            long = random.randint(0, (alpha * n) - 1)
            lat = random.randint(0, (alpha * n) - 1)

            # Check whether longitude and latitude of depots is not already used
            if matrix[lat][long] == -1:  # If the location is evailable
                # Set the hub name to the position in the matrix
                matrix[lat][long] = i

                # Add the location of the depot to dep_locs list
                dep_locs.append({"name": i, "long": long, "lat": lat})
                # break from the loop
                added = True

    # Return the locations of the depots
    return dep_locs


def generate_s_vals(n: int, max_def: int, max_sur: int) -> List[int]:
    """
    Creates n depot supply values between the maximum deficit and maximum surplus 
    and ensures sum of the supply values is 0.

    params:
        n - The number of depots
        max_def - Maximum deficit value of each depot
        max_sur - Maximum surplus value of each depot

    returns:
        A list of n integer supply values, within the bounds of the TNRP
    """
    # Set initial values of total_s
    total_s = 0

    # Create an empty list for storing supply values
    s_vals = []

    # Repeat until n-1 supply values in s_vals
    while len(s_vals) < n - 1:
        # Assign 0 to the random value
        r_val = 0

        # If total supply = 0 then ramdom value is between max_def and max_sur
        if total_s == 0:
            r_val = random.randint(max_def, max_sur)

        # If the total supply < 0 then random value between (max_def - total_s) and max_sur
        # This keeps total_s between the bounds of max_def and max_sur
        elif total_s < 0:
            r_val = random.randint((max_def-total_s), max_sur)

        # If the total supply > 0 then random value between max_def and (max_sur - total_s)
        elif total_s > 0:
            r_val = random.randint(max_def, (max_sur-total_s))

        # Make sure the random value is not 0 and if so choose another number
        # No depot should be initialised with a 0 supply value
        if r_val != 0:
            # Add the supply value to total supply and the s_vals list
            total_s += r_val
            s_vals.append(r_val)

    # If total_s is 0 at this stage, will need to generate again as no difference to assign to final depot
    if total_s == 0:
        return generate_s_vals(n=n, max_def=max_def, max_sur=max_sur)

    # Assign the difference to the final depot
    s_vals.append(0-total_s)

    return s_vals


def create_model(n: int, alpha=2, max_def=-100, max_sur=100) -> Dict[int, Depot]:
    """
    Create a model with n depots at randomly generated locations.
    Each depot has a supply value (S) between max deficit and max surplus

    params:
        n - The number of depots in the matrix
        alpha - A constant to scale the matrix by (default=2)
        max_def - The maximum supply deficit value of each depot (default=-100)
        max_sur - The maximum supply surplus value of each depot (default=100)

    returns:
        A dictionary of the depot names to the depot objects: {depot_name: DepotObj}
    """
    # Need to ensure alpha > 1 so all depots can be created in unique locations
    if alpha < 1:
        raise ValueError("alpha must be greater than 1")

    # Generate the location of the depots
    dep_locs = create_locations(n=n, alpha=alpha)

    # Generate the n supply values
    s_vals = generate_s_vals(n=n, max_def=max_def, max_sur=max_sur)

    # Create the depots as Depot objects
    deps: Dict[int, Depot] = {}
    for i in range(len(dep_locs)):
        # Assign the corresponding names, locations and supply values to each hub
        new_dep = Depot(name=dep_locs[i]['name'], s=s_vals[i],
                        long=dep_locs[i]['long'], lat=dep_locs[i]['lat'])
        # Add the depot to the dictionary
        deps[new_dep.get_name()] = new_dep

    # Calculate the distances between depots
    for i in range(len(deps)):  # For each of the depots
        # Only calculate new connections as the add_connection method adds to both connections dicts
        for j in range(i, len(deps)):
            # Add the connection to both depotss
            deps[i].add_connection(deps[j])

    return deps
