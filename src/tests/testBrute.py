"""Tests for the brute force algorithm"""
import unittest
from searches.brute_force.brute import brute
from model.model import create_model


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
