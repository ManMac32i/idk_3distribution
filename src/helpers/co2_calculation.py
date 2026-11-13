from .configuration import EMISIONS

def get_co2(distance, demand, vehicle):
    """Transport emissions (g of CO2) of carrying `demand` kg over `distance` km.
    distance: km travelled with the load (convert from hm first: hm / 10)
    demand:   load carried in kg
    vehicle:  "truck", "car" or "bike"
    """
    if vehicle not in EMISIONS:
        raise ValueError(f"Unknown vehicle '{vehicle}', expected one of {list(EMISIONS)}")
    if distance < 0 or demand < 0:
        raise ValueError("distance and demand must be non-negative")

    tonnes = demand / 1000
    return EMISIONS[vehicle] * tonnes * distance
