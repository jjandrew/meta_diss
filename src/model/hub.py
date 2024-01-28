"""
Contains the classes used in the project
"""
from typing import Dict


class Hub:
    """
    The class defining the hubs
    """
    total_s = 0

    def __init__(self, name: int, s: int, long: int, lat: int) -> None:
        """
        Create the hub

        params
            name - number used to identify the hub
            s - the supply value that needs to be resolved
            long - the longitudinal location of the hub
            lat - the lateral location of the hub
        """
        # Assign these values to the object
        self.name = name
        self.s = s
        self.long = long
        self.lat = lat

        # Create an empty dictionary of connections
        self.connections = {}

        # Recalculate the total supply
        Hub.total_s += s

    def __str__(self) -> str:
        """To string method"""
        return f'Hub: {self.name}, (x,y): ({self.long},{self.lat}), S: {self.s}'

    def add_connection(self, hub: 'Hub') -> None:
        """
        Add a connection between the Hub object and another hub to both dictionaries
        The value of this connection is the manhattan distance between the two hubs

        params
            hub2 - the other Hub object to connect with
        """
        # Calculate the manhattan distance between the two hubs
        dist_between = abs(self.long - hub.long) + abs(self.lat - hub.lat)

        # Add the connection to both dictionaries
        self.connections[hub.name] = dist_between
        hub.connections[self.name] = dist_between

    def get_name(self) -> int:
        """
        Getter for name attribute of a hub

        Returns
            Integer representing the hub
        """
        return self.name

    def get_s(self) -> int:
        """
        Getter for the s attribute of one hub

        Returns
            Integer representing supply needed to resolve surplus / deficit of hub
        """
        return self.s

    def add_s(self, s: int):
        """
        Adds s to a hubs total s

        params
            s - quanity of supply to be added
        """
        self.s += s

    def get_long(self) -> int:
        """
        Getter for the longitude attribute of the hub

        Returns
            Integer representing the longitudinal location of the hub
        """
        return self.long

    def get_lat(self) -> int:
        """
        Getter for the latitude attribute of the hub

        Returns
            Integer representing the latitudinal location of the hub
        """
        return self.lat

    def get_connections(self) -> Dict[int, int]:
        """
        Getter for the distances to connected nodes

        Returns
            Dictionary of node : distance
        """
        return self.connections

    def get_total_s() -> int:
        """
        Gets the shared s value between all hubs

        Returns
            The shares s value between all nodes
        """
        return Hub.total_s

    def move_s(start: 'Hub', end: 'Hub', s: int):
        """
        Moves s quanity from 'start' hub to 'end'
        """
        # Remove s from start
        start.add_s(s=0-s)

        # Add s to end
        end.add_s(s=s)

    def reset():
        """
        Method for resetting shared s for use in unit tests
        """
        Hub.total_s = 0
