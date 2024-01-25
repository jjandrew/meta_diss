from model.model import create_model
from visualise import plot_network

if __name__ == "__main__":
    model = create_model(n=10, alpha=10)
    plot_network(model=model)
