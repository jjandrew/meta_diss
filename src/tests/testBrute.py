"""Tests for the brute force algorithm"""
import unittest
from searches.brute_force.brute import brute, next_steps
from model.model import create_model
from classes.hub import Hub


class TestHubClass(unittest.TestCase):
    """
    Class for testing brute force algorithm
    """

    def test_brute(self):
        model = create_model(n=4, alpha=2, max_def=-10, max_sur=10)
        print("Starting model")
        for hub in model:
            print(hub)

        print()
        print("Brute force")
        brute(model=model, max_journey_size=3)

    def test_next_steps(self):
        starting_hub = Hub(name=0, s=2, long=0, lat=0)

        def_hub_1 = Hub(name=1, s=-1, long=0, lat=0)
        def_hub_2 = Hub(name=2, s=-2, long=0, lat=0)
        def_hub_3 = Hub(name=3, s=-5, long=0, lat=0)

        def_hubs = [def_hub_1, def_hub_2, def_hub_3]

        next_js = next_steps(starting_hub=starting_hub,
                             deficit_hubs=def_hubs, max_journey_size=3)
