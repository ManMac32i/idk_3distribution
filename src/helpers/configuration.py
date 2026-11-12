# transport emissions in g of CO2 per tonne per km
emisions = {
    "truck": 311,
    "car": 772,
    "bike": 0
}

# vehicle capacities in kg
capacities = {
    "truck": 21000,
    "car": 1500,
    "bike": 100
}

# refrigerator: g of CO2 to keep 1 t cold during one day
fridge_emisions = 42

# bike allowed only if demand <= 500 kg AND round trip <= 6 km
bike_max_demand = 500  # kg
bike_max_round_trip = 6  # km

# building emissions in g of CO2
building = {
    "truck": 15000000,  # base case
    "car": 600000,  # optional scenarios
    "bike": 96000,
    "fridge": 257000
}