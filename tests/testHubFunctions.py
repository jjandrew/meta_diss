"""Tests for the hub class"""
import unittest
from src.classes import Hub


class TestHubClass(unittest.TestCase):
    """
    Tests the Hub class
    """

    def tearDown(self) -> None:
        """code to run after each test"""
        Hub.reset()

    def test_hub_creation(self):
        """
        Tests a hub is created correctly
        Ensures hub is created with name, s value, longitude, latitude and no connections
        """
        hub = Hub(name=0, s=50, long=10, lat=11)
        # Check hubs name is 0
        self.assertEqual(0, hub.get_name())
        # Check s value of hub is 50
        self.assertEqual(50, hub.get_s())
        # Check longitude of hub is 10
        self.assertEqual(10, hub.get_long())
        # Check latitude of hub is 11
        self.assertEqual(11, hub.get_lat())
        # Check there are no connections to start with
        self.assertEqual({}, hub.get_connections())

    def test_s_increments(self):
        """Tests the s value shared between hubs is updated correctly"""
        # Checks s starts at 0
        self.assertEqual(0, Hub.get_total_s())

        # Adds to s and check updated
        _ = Hub(name=0, s=5, long=1, lat=1)
        self.assertEqual(5, Hub.get_total_s())

        # Removes from s and checks updated
        _ = Hub(name=1, s=-10, long=1, lat=1)
        self.assertEqual(-5, Hub.get_total_s())

    def test_connection_added(self):
        """Tests connections between hubs can be added"""
        # Create two hubs
        hub0 = Hub(name=0, s=10, long=-1, lat=-1)
        hub1 = Hub(name=1, s=-10, long=3, lat=5)

        # Check distance between hubs is calculated correctly and added to dictionary of both hubs
        hub0.add_connection(hub=hub1)
        self.assertEquals(10, hub0.get_connections()[1])
        self.assertEquals(10, hub1.get_connections()[0])

    def test_movement_of_s(self):
        """Tests supply can be moved between hubs to reach an equilibrium"""
        # Create two hubs
        hub0 = Hub(name=0, s=10, long=-1, lat=-1)
        hub1 = Hub(name=1, s=-10, long=3, lat=5)

        # Move 10 from hub 0 to hub 1
        Hub.move_s(start=hub0, end=hub1, s=10)
        # Check that supply has been taken from hub 0 and given to hub 1
        self.assertEqual(0, hub0.get_s())
        self.assertEqual(0, hub1.get_s())
