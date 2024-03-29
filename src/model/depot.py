"""
Contains the depot class used in the project
"""
from typing import Dict
from math import sqrt


class Depot:
    """
    The class defining the depots
    """

    def __init__(self, name: int, s: int, x: int, y: int) -> None:
        """
        Create the depot

        params
            name - number used to identify the depot
            s - the supply value that needs to be resolved
            x - the location of the depot in the x axis
            y - the location of the depot in the y axis
        """
        # Assign the parameters as object attributes
        self.name = name
        self.s = s
        self.x = x
        self.y = y

        # Create an empty dictionary of connections
        self.connections = {}

    def __str__(self) -> str:
        """Depot to string method for debugging"""
        return f'Depot: {self.name}, (x,y): ({self.x},{self.y}), S: {self.s}'

    def add_connection(self, dep: 'Depot') -> None:
        """
        Add a connection between the Depot object and another depot to both dictionaries.
        The value of this connection is the euclidean distance between the two depots

        params
            dep - the other depot object to connect with
        """
        # Calculate the euclidean distance between the two depots
        dist_between = sqrt((self.x - dep.x) **
                            2 + (self.y - dep.y)**2)

        # Add the connection to both dictionaries
        self.connections[dep.name] = dist_between
        dep.connections[self.name] = dist_between

    def get_name(self) -> int:
        """
        Getter for name attribute of a depot

        Returns
            Integer representing the depot
        """
        return self.name

    def get_s(self) -> int:
        """
        Getter for the s attribute of one depot

        Returns
            Integer representing supply needed to resolve surplus / deficit of depot
        """
        return self.s

    def add_s(self, s: int):
        """
        Adds a quantity (s) to a depot's total supply

        params
            s - quanity of supply to be added
        """
        self.s += s

    def get_long(self) -> int:
        """
        Getter for the longitude attribute of the depot

        Returns
            Integer representing the longitudinal location of the depot
        """
        return self.x

    def get_lat(self) -> int:
        """
        Getter for the latitude attribute of the depot

        Returns
            Integer representing the latitudinal location of the depot
        """
        return self.y

    def get_connections(self) -> Dict[int, int]:
        """
        Getter for the distances to connected depots

        Returns
            Dictionary of depot : distance
        """
        return self.connections

    def move_s(start: 'Depot', end: 'Depot', s: int):
        """
        Moves s quanity from 'start' depot to 'end' depot
        """
        # Remove s from start depot
        start.add_s(s=0-s)

        # Add s to end depot
        end.add_s(s=s)
