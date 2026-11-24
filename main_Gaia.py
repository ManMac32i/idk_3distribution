import os
import time
import pandas as pd

from src import Problem1, Problem2
from src.helpers import EMISIONS, VEHICLE_WEIGHTS, RESULTS_FOLDERS

def pipeline_gurobi_scenario1_comparison(gurobi_time_limit):
    instances_solved = []
    dimensions_solved = []
    sol_times = []
    values_scenario2_gurobi = []
    optimality_gaps = []
    values_scenario1 = []

    instances_not_solved = []
    dimensions_not_solved = []
    for i in range(5, 6):
        p1 = Problem1(instance=i)
        p2 = Problem2(instance=i,
                    truck_routing_emissions=EMISIONS["truck"],
                    empty_truck_weight=VEHICLE_WEIGHTS["truck"])


        time_start = time.time()

        print(f"Solving instance {i} of dimension {len(p2.clients)}...")

        sol = p2.solve_gurobi(time_limit=gurobi_time_limit)
        time_end = time.time()
        elapsed_time = time_end - time_start

        if sol is not None:
            print(f"Instance {i} solved in {elapsed_time:.2f} seconds.")

            instances_solved.append(i)
            dimensions_solved.append(len(p2.clients))
            sol_times.append(int(elapsed_time))
            values_scenario2_gurobi.append(int(sol["objective_value"]))
            optimality_gaps.append(round(sol["optimality_gap"], 3))
            values_scenario1.append(int(p1.calculate_co2()))
        else:
            print(f"Instance {i} could not be solved.")
            instances_not_solved.append(i)
            dimensions_not_solved.append(len(p2.clients))

        print("-" * 50, "\n")

    analysis_df = pd.DataFrame({
        'Instance': instances_solved,
        'Clients': dimensions_solved,
        'Sol_time_seconds': sol_times,
        'Value_Scenario2_Gurobi': values_scenario2_gurobi,
        'Optimality_Gap': optimality_gaps,
        'Value_Scenario1': values_scenario1
    })

    errors_df = pd.DataFrame({
        'Instance': instances_not_solved,
        'Clients': dimensions_not_solved
    })

    os.makedirs('results', exist_ok=True)
    if not analysis_df.empty:
        analysis_df.to_csv(f'results/summary_scenario1_scenario2_gurobi.csv', index=False)
    if not errors_df.empty:
        errors_df.to_csv(f'results/problem2_errors_gurobi_{gurobi_time_limit}.csv', index=False)

if __name__ == '__main__':
    instances = [13]
    test_mode = True # Set to True to save results in the "tests" folder, False to save in the "results" folder
    results_dir = RESULTS_FOLDERS["local"] if test_mode else RESULTS_FOLDERS["shared"]
    for instance in instances:
        p2 = Problem2(instance=instance,
                    truck_routing_emissions=EMISIONS["truck"],
                    empty_truck_weight=VEHICLE_WEIGHTS["truck"])
        
        p2.solve_gurobi(time_limit=60, test_mode=test_mode)
        p2.plot_trips_scenario2(solution_method="Gurobi",
                                csv_path=f'{results_dir}/scenario2/gurobi_instance_{instance}.csv')