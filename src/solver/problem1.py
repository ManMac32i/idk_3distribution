from ..problem import Problem
from ..helpers.configuration import BIKE_MAX_DEMAND, BIKE_MAX_ROUND_TRIP
from ..helpers.co2_calculation import *

class Problem1(Problem):
    def __init__(self, instance):
        super().__init__(instance)
    
    def calculate_co2(self):
        co2 = 0
        for c in self.clients:
            distance = c.get_distance(self.depot)
            vehicle = "bike" if distance <= BIKE_MAX_ROUND_TRIP and c.demand <= BIKE_MAX_DEMAND else "car"
            co2 += round(get_co2(distance, c.demand, vehicle), 4)
        return co2

if __name__ == '__main__':
    instance = input("Instance: ")
    p = Problem1(instance)
    co2_emisions = p.calculate_co2()
    print(f"The total emisions for instance {instance} on case 1 is: {co2_emisions}")
    