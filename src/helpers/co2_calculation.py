from .configuration import EMISIONS, VEHICLE_WEIGHTS

def get_co2(distance, demand, vehicle, include_tare=True):
    # Transport emissions (g of CO2) of carrying `demand` kg over `distance` km (one leg).
    # distance:     km travelled (convert from hm first: hm / HM_PER_KM)
    # demand:       load carried in kg (0 for an empty leg)
    # vehicle:      "truck", "car" or "bike"
    # include_tare: True -> the empty vehicle weight VEHICLE_WEIGHTS[vehicle] also emits
    if vehicle not in EMISIONS:
        raise ValueError(f"Unknown vehicle '{vehicle}', expected one of {list(EMISIONS)}")
    if distance < 0 or demand < 0:
        raise ValueError("distance and demand must be non-negative")

    tare = VEHICLE_WEIGHTS[vehicle] if include_tare else 0
    tonnes = (demand + tare) / 1000
    return EMISIONS[vehicle] * tonnes * distance

def get_co2_roundtrip(distance, demand, vehicle, include_tare=True):
    # g of CO2 of one round trip: outbound leg with the empty vehicle + return leg carrying `demand` kg
    # (scenario 1: client goes to the depot and back; scenario 3: client goes to its fridge and back)
    # distance: one-way distance in km
    emisions_go = get_co2(distance, 0, vehicle, include_tare)
    emisions_back = get_co2(distance, demand, vehicle, include_tare)
    return emisions_go + emisions_back
