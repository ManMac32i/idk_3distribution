from src import Problem1, Problem2
from src.helpers import RESULTS_FOLDERS


if __name__ == '__main__':
    print(f"{'Inst':>4} {'Clients':>8} {'Demand (kg)':>12} {'Truck cap (kg)':>15}, {'CO2 case 1':>15}")
    for i in range(1, 13):
        p = Problem1(i, include_tare=True, include_build=False)
        print(f"{i:>4} {len(p.clients):>8} {p.get_total_demand():>12} {p.capacity:>15}, {round(p.calculate_co2(),4):>15}")

    instances = [5]
    test_mode = True # Set to True to save results in the "local_results" folder, False to save in the "results" folder
    results_dir = RESULTS_FOLDERS["local"] if test_mode else RESULTS_FOLDERS["shared"]
    for instance in instances:
        p2 = Problem2(instance=instance, include_tare=True, include_build=True)

        p2.solve_gurobi(time_limit=60,
                        test_mode=test_mode)
        p2.plot_trips_scenario2(solution_method="Gurobi",
                                csv_path=f'{results_dir}/scenario2/gurobi_instance_{instance}.csv')