from src import Problem1, Problem2
from src.helpers import EMISIONS, VEHICLE_WEIGHTS, RESULTS_FOLDERS


if __name__ == '__main__':
    print(f"{'Inst':>4} {'Clients':>8} {'Demand (kg)':>12} {'Truck cap (kg)':>15}, {'CO2 case 1':>15}")
    for i in range(1, 13):
        p = Problem1(i)
        print(f"{i:>4} {len(p.clients):>8} {p.get_total_demand():>12} {p.capacity:>15}, {round(p.calculate_co2(),4):>15}")

    instances = [5]
    test_mode = False # Set to True to save results in the "tests" folder, False to save in the "results" folder
    results_dir = RESULTS_FOLDERS["local"] if test_mode else RESULTS_FOLDERS["shared"]
    for instance in instances:
        p2 = Problem2(instance=instance,
                    truck_routing_emissions=EMISIONS["truck"],
                    empty_truck_weight=VEHICLE_WEIGHTS["truck"])

        p2.solve_gurobi(time_limit=60,
                        test_mode=test_mode)
        p2.plot_trips_scenario2(solution_method="Gurobi",
                                csv_path=f'{results_dir}/scenario2/gurobi_instance_{instance}.csv')