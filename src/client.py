from math import sqrt
from .helpers.configuration import HM_PER_KM

class Client:
    def __init__(self, demand, location):
        self.demand = demand
        self.location = location
        self.x = location[0]
        self.y = location[1]

    def get_distance(self, point):
        # Euclidean distance in km to a point given in hectometres
        x, y = point
        return sqrt((self.x - x) ** 2 + (self.y - y) ** 2) / HM_PER_KM
