from client import Client
from helpers.data_getter import get_data
from helpers.configuration import CAPACITIES

class Problem:
    def __init__(self, instance):
        dimension, capacity, demand, coordinates = get_data(instance)

        # point 0 of the file is the depot, the rest are clients
        self.depot = coordinates[0]
        self.clients = [Client(demand[i], coordinates[i]) for i in range(1, dimension)]

        # truck capacity
        self.capacity = capacity

    def get_total_demand(self):
        # total demand of all clients in kg (the depot has no demand)
        return sum(c.demand for c in self.clients)

    def get_clients_distances(self):
        for i, c in enumerate(self.clients):
            print(f"Client {i} has distance {c.get_distance(self.depot)} from the depot")

if __name__ == '__main__':
    p = Problem(1)
    print(p.depot, p.capacity)
    p.get_clients_distances()