import numpy as np
from scipy.spatial.distance import cdist

from .client import Client
from .helpers.data_getter import get_data
from .helpers.configuration import HM_PER_KM


class Problem:
    """Common data of an instance, shared by all scenarios.

    Node convention: 0 = depot, 1..n = clients (client label k <-> self.clients[k-1]).
    Coordinates in the instance files are in hectometres; every distance returned
    by this class is in kilometres.
    """

    def __init__(self,
                 instance,
                 include_tare,
                 include_build):
        self.instance = instance
        dimension, capacity, demand, coordinates = get_data(instance)

        self.include_tare = include_tare
        self.include_build = include_build

        # point 0 of the file is the depot, the rest are clients
        self.depot = coordinates[0]
        self.clients = [Client(demand[i], coordinates[i]) for i in range(1, dimension)]

        # numpy views of the same data, indexed by node label (0 = depot)
        self.coords_hm = np.asarray(coordinates, dtype=float)  # shape (n+1, 2), hectometres
        self.demands_kg = np.asarray(demand, dtype=float)      # shape (n+1,), depot demand = 0

        # truck capacity (kg) as given in the instance file
        self.capacity = capacity

        # distances from the depot are cheap (n+1 values): compute them always
        self.depot_distances_km = self.distances_from_km(self.coords_hm[0])
        # the full matrix is O(n^2) (~130 MB for instance 12): call calculate_distance_matrix_km() when needed
        self.distance_matrix_km = None

    def n_clients(self):
        return len(self.clients)

    def calculate_distance_matrix_km(self):
        # full (n+1) x (n+1) Euclidean distance matrix in km, computed once.
        self.distance_matrix_km = cdist(self.coords_hm, self.coords_hm) / HM_PER_KM

    def distances_from_km(self, point_hm):
        # distance (km) from any point (x, y) in hectometres to every node, shape (n+1,)
        return np.linalg.norm(self.coords_hm - np.asarray(point_hm, dtype=float), axis=1) / HM_PER_KM

    def get_total_demand(self):
        # total demand of all clients in kg (the depot has no demand)
        return sum(c.demand for c in self.clients)


if __name__ == '__main__':
    p = Problem(1)
    print(p.depot, p.capacity)
    for k in range(1, p.n_clients() + 1):
        print(f"Client {k} is {p.depot_distances_km[k]:.3f} km from the depot")
