from .client import Client
from .depot import Depot
from .vehicle import Vehicle
from .helpers.data_getter import get_data

class Problem:
    def __init__(self, instance):
        dimension, capacity, demand, coordinates = get_data(instance)

        # point 0 of the file is the depot, the rest are clients
        self.depot = Depot(coordinates[0])
        self.clients = [Client(demand[i], coordinates[i]) for i in range(1, dimension)]

        # truck capacity taken from the instance file (CAPACITY)
        self.truck = Vehicle(capacity, "truck")

    def get_total_demand(self):
        # total demand of all clients in kg (the depot has no demand)
        return sum(c.demand for c in self.clients)

if __name__ == '__main__':
    p = Problem(1)
    print(len(p.clients), p.depot.x, p.depot.y, p.truck.capacity, p.truck.emisions)