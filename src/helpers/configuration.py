# transport emissions in g of CO2 per tonne per km
EMISIONS = {
    "truck": 311,
    "car": 772,
    "bike": 0
}

# vehicle capacities in kg
CAPACITIES = {
    "truck": 21000,
    "car": 1500,
    "bike": 100
}

# refrigerator: g of CO2 to keep 1 t cold during one day
FRIDGE_EMISIONS = 42

# bike allowed only if demand <= 500 kg AND round trip <= 6 km
BIKE_MAX_DEMAND = 500  # kg
BIKE_MAX_ROUND_TRIP = 6  # km

# building emissions in g of CO2
BUILDING_EMISIONS = {
    "truck": 15000000,  # base case
    "car": 600000,  # optional scenarios
    "bike": 96000,
    "fridge": 257000
}

# vehicle weights in kg 
# Todo: check values!!
VEHICLE_WEIGHTS = {
    "truck": 10000,
    "car": 2000,
    "bike": 20
    }

RESULTS_FOLDERS = {"shared": "results",
                   "local": "tests"}

# map units: instance coordinates are in hectometres (1 unit = 100 m)
HM_PER_KM = 10