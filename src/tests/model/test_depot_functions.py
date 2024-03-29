"""Tests for the depot class"""
import unittest
from model.depot import Depot


class TestHubClass(unittest.TestCase):
    """
    Tests the Depot class
    """

    def test_depot_creation(self):
        """
        Tests a depot is created correctly
        Ensures depot is created with name, s value, longitude, latitude and no connections
        """
        depot = Depot(name=0, s=50, x=10, y=11)
        # Check depots name is 0
        self.assertEqual(0, depot.get_name())
        # Check s value of depot is 50
        self.assertEqual(50, depot.get_s())
        # Check longitude of depot is 10
        self.assertEqual(10, depot.get_long())
        # Check latitude of depot is 11
        self.assertEqual(11, depot.get_lat())
        # Check there are no connections to start with
        self.assertEqual({}, depot.get_connections())

    def test_connection_added(self):
        """Tests connections between depots can be added and distance calculated"""
        # Create two depots - the distance between depots is a 3, 4, 5 pythagorean triple
        dep0 = Depot(name=0, s=10, x=0, y=0)
        dep1 = Depot(name=1, s=-10, x=3, y=4)

        # Check distance between depots is calculated correctly and added to dictionary of both depots
        dep0.add_connection(dep=dep1)
        self.assertEqual(5, dep0.get_connections()[1])
        self.assertEqual(5, dep1.get_connections()[0])

    def test_movement_of_s(self):
        """Tests supply can be moved between depots to reach an equilibrium"""
        # Create two depots
        dep0 = Depot(name=0, s=10, x=-1, y=-1)
        dep1 = Depot(name=1, s=-10, x=3, y=5)

        # Move 10 from depot 0 to depot 1
        Depot.move_s(start=dep0, end=dep1, s=10)
        # Check that supply has been taken from depot 0 and given to depot 1
        self.assertEqual(0, dep0.get_s())
        self.assertEqual(0, dep1.get_s())
