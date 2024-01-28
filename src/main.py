from model.model import create_model
from visualise import plot_network
from model.hub import Hub
from searches.brute_force.brute import brute
from utils import reduce_model

if __name__ == "__main__":
    sur_hub_0 = Hub(name=0, s=3, long=0, lat=1)
    sur_hub_1 = Hub(name=1, s=5, long=3, lat=4)

    def_hub_2 = Hub(name=2, s=-2, long=2, lat=3)
    def_hub_3 = Hub(name=3, s=-6, long=0, lat=5)

    model = [sur_hub_0, sur_hub_1, def_hub_2, def_hub_3]

    for i in range(0, len(model)):
        for j in range(i+1, len(model)):
            model[i].add_connection(model[j])

    # reduce_model(model=model, max_journey_size=2)

    # for hub in model:
    #     print(hub)

    print(brute(model=model, max_journey_size=2))
