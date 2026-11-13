from math import sqrt

class Client:
    def __init__(self, demand, location):
        self.demand = demand
        self.x = location[0]
        self.y = location[1]

    def get_distance(self, depot):
        x,y = depot
        return sqrt((self.x-x)**2+(self.y-y)**2)
