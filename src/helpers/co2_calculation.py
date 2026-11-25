from .configuration import ROUTING_EMISSIONS, VEHICLE_WEIGHTS, BUILDING_EMISIONS, VEHICLE_LIFESPAN

def get_co2(distance,
            demand,
            vehicle,
            include_tare: bool,
            include_build: bool):
    # Transport emissions (g of CO2) of carrying `demand` kg over `distance` km (one leg).
    # distance:     km travelled (convert from hm first: hm / HM_PER_KM)
    # demand:       load carried in kg (0 for an empty leg)
    # vehicle:      "truck", "car" or "bike"
    # include_tare: True -> the empty vehicle weight VEHICLE_WEIGHTS[vehicle] also emits
    # include_build: True -> add the building emissions BUILDING_EMISIONS[vehicle] spread over the vehicle
    #                lifespan, i.e. BUILDING_EMISIONS[vehicle] / VEHICLE_LIFESPAN[vehicle] g per km travelled
    if vehicle not in ROUTING_EMISSIONS:
        raise ValueError(f"Unknown vehicle '{vehicle}', expected one of {list(ROUTING_EMISSIONS)}")
    if distance < 0 or demand < 0:
        raise ValueError("distance and demand must be non-negative")

    tare = VEHICLE_WEIGHTS[vehicle] if include_tare else 0
    tonnes = (demand + tare) / 1000

    if include_build and (vehicle not in VEHICLE_LIFESPAN or vehicle not in BUILDING_EMISIONS):
        raise ValueError(f"include_build=True needs VEHICLE_LIFESPAN['{vehicle}'] and BUILDING_EMISIONS['{vehicle}'] "
                         f"in configuration.py (lifespan defined for: {list(VEHICLE_LIFESPAN)})")
    build_emissions_per_km = BUILDING_EMISIONS[vehicle] / VEHICLE_LIFESPAN[vehicle] if include_build else 0
    return ROUTING_EMISSIONS[vehicle] * tonnes * distance + build_emissions_per_km * distance

def get_co2_roundtrip(distance, demand, vehicle, include_tare, include_build):
    # g of CO2 of one round trip: outbound leg with the empty vehicle + return leg carrying `demand` kg
    # (scenario 1: client goes to the depot and back; scenario 3: client goes to its fridge and back)
    # distance: one-way distance in km
    emisions_go = get_co2(distance, 0, vehicle, include_tare, include_build)
    emisions_back = get_co2(distance, demand, vehicle, include_tare, include_build)
    return emisions_go + emisions_back
