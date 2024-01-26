from model.model import create_model
from visualise import plot_network
from classes.hub import Hub
from searches.brute_force.brute import next_steps

if __name__ == "__main__":
    starting_hub = Hub(name=0, s=2, long=0, lat=0)

    def_hub_1 = Hub(name=1, s=-1, long=0, lat=0)
    def_hub_2 = Hub(name=2, s=-2, long=0, lat=0)
    def_hub_3 = Hub(name=3, s=-5, long=0, lat=0)

    def_hubs = [def_hub_1, def_hub_2, def_hub_3]

    next_js = next_steps(starting_hub=starting_hub,
                         deficit_hubs=def_hubs, max_journey_size=3)
    print(next_js)
