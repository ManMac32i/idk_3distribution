from math import ceil

from ..problem import Problem
from ..helpers.configuration import BIKE_MAX_DEMAND, BIKE_MAX_ROUND_TRIP, CAPACITIES
from ..helpers.co2_calculation import get_co2_roundtrip

class Problem1(Problem):
    """
        Scenario 1 (Drive, all-to-1): every client goes to the depot and back by itself.
        - bike iff demand <= BIKE_MAX_DEMAND kg and round trip <= BIKE_MAX_ROUND_TRIP km, otherwise car
        - ceil(demand / CAPACITIES[vehicle]) round trips, each one carrying demand / trips
        - each round trip = outbound leg with the empty vehicle + return leg with the goods
    """

    def __init__(self,
                 instance,
                 include_tare,
                 include_build):
        super().__init__(instance, include_tare, include_build)

    def calculate_co2(self):
        co2=0
        for i,c in enumerate(self.clients):
            distance = self.depot_distances_km[i+1]
            vehicle = "bike" if 2*distance <= BIKE_MAX_ROUND_TRIP and c.demand <= BIKE_MAX_DEMAND else "car"
            trips = ceil(c.demand / CAPACITIES[vehicle])
            co2 += trips * get_co2_roundtrip(distance, c.demand / trips, vehicle, self.include_tare, self.include_build)
        return co2

if __name__ == '__main__':
    instance = input("Instance: ")
    p = Problem1(instance)
    co2_emisions = p.calculate_co2()
    print(f"The total emisions for instance {instance} on case 1 is: {co2_emisions}")
