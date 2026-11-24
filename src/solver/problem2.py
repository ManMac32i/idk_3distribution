import os
import gurobipy as gp
from gurobipy import GRB
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from collections import defaultdict

from ..problem import Problem
from ..helpers.configuration import EMISIONS, RESULTS_FOLDERS

class Problem2(Problem):
    def __init__(self,
                 instance,
                 truck_routing_emissions,
                 empty_truck_weight):
        super().__init__(instance)
        self.truck_routing_emissions = truck_routing_emissions # g of CO2 per tonne per km
        self.empty_truck_weight = empty_truck_weight / 1000 # convert to tonnes

    def compute_distance_matrix(self):
        # distance matrix (km) between depot (0) and clients (1..n)
        self.calculate_distance_matrix_km()
        return self.distance_matrix_km

    def solve_gurobi(self,
                     time_limit=600,
                     verbose=False,
                     test_mode=True,
                     results_fname_prefix='gurobi',
                     save_results=True):
            node_labels = list(range(len(self.clients) + 1))  # define node labels (depot is 0, clients are 1,...,n)
            client_labels = list(range(1, len(self.clients) + 1))  # define client labels (1,2,...,n)
            demands = [0] + [c.demand/1000 for c in self.clients]  # define demands in tonnes (0 for depot, positive for clients)
            distance_matrix = self.compute_distance_matrix()  # distance matrix (km)

            ######## Define model #########

            m = gp.Model(f"FCVRP_{len(node_labels)}")   # 1. create a new model

            ######## Define variables #########

            a = m.addVars(node_labels, node_labels, vtype=GRB.BINARY, name="a")  # indicator of arc being used
            q = m.addVars(node_labels, node_labels, vtype=GRB.CONTINUOUS, name="q")  # quantity of goods transported on arc

            ######## Define objective #########

            m.setObjective(self.truck_routing_emissions * gp.quicksum(distance_matrix[i, j] * q[i, j] for i in node_labels for j in node_labels if i != j) + 
                           self.truck_routing_emissions * gp.quicksum(distance_matrix[i, j] * self.empty_truck_weight * a[i, j] for i in node_labels for j in node_labels if i != j),
                           GRB.MINIMIZE) # no emission factor included here, should be added later

            ######## Define constraints #########

            m.addConstrs((q[i,i] == 0 for i in node_labels),
                         name="no_self_loops_q")
            
            m.addConstrs((a[i,i] == 0 for i in node_labels),
                         name="no_self_loops_a")
            
            m.addConstrs((q[i,j] <= self.capacity / 1000 * a[i,j] for i in node_labels for j in node_labels if i != j),
                        name="quantity_arc_relation")
            
            m.addConstrs((gp.quicksum(a[i,j] for j in node_labels) == 1 for i in client_labels),
                         name="each_client_served_once")

            m.addConstr((gp.quicksum(a[0,j] for j in node_labels) >= 1),
                         name="depot_leaves_at_least_once")

            m.addConstrs((gp.quicksum(a[i,j] for j in node_labels) == gp.quicksum(a[j,i] for j in node_labels) for i in node_labels),
                         name="flow_conservation")

            m.addConstrs((gp.quicksum(q[j,i] for j in node_labels) - gp.quicksum(q[i,j] for j in node_labels) >= demands[i] for i in client_labels),
                         name="flow_conservation")

            # Add optional constraints to speed up solving

            # m.addConstrs((a[i,j] + a[j,i] <= 1 for i in client_labels for j in client_labels if i != j),
            #              name="only_one_direction")

            ######## Specify solver parameters if needed #########

            m.Params.TimeLimit = time_limit        # secondi massimi

            if not verbose:
                m.Params.OutputFlag = 0

            ######## Solve #########

            m.optimize() 

            if m.status == GRB.OPTIMAL:
                print("Optimal solution found.")
            elif m.status == GRB.TIME_LIMIT:
                print("Time limit reached.")
            elif m.status == GRB.INFEASIBLE:
                print("Model is infeasible.")

            if m.SolCount == 0:
                print("No solution found.")
                result = None
            else: 
                a_val = m.getAttr('X', a)
                q_val = m.getAttr('X', q)

                sol = [[k[0], k[1], round(q_val[k], 2)] for k in a_val.keys() if a_val[k] > 0.5]
                sol = pd.DataFrame(sol, columns=['i', 'j', 'q'])

                result = {
                "solution": sol,
                "objective_value": m.objVal,
                "optimality_gap": m.MIPGap
                }

            if save_results:
                destination_folder = RESULTS_FOLDERS["local"] if test_mode else RESULTS_FOLDERS["shared"]
                results_dir=f"{destination_folder}/scenario2"

                if verbose:
                    print(f"Saving results to {results_dir}/{results_fname_prefix}_instance_{self.instance}.csv")
                
                os.makedirs(results_dir, exist_ok=True)
                path = f"{results_dir}/{results_fname_prefix}_instance_{self.instance}.csv"

                meta = {
                    "instance":   self.instance,
                    "status":     m.Status,                       # 2 = OPTIMAL, 9 = TIME_LIMIT, 3 = INFEASIBLE
                    "time_limit": m.Params.TimeLimit,             # parametro impostato
                    "runtime":    round(m.Runtime, 2),            # tempo effettivo
                    "obj_val":    round(m.ObjVal, 2) if result else None,
                    "obj_bound":  round(m.ObjBound, 2) if result else None,
                    "mip_gap":    round(m.MIPGap, 4) if result else None,  # gap ottenuto
                }

                with open(path, "w") as f:
                    for k, v in meta.items():
                        f.write(f"# {k}: {v}\n")
                    if m.SolCount > 0:
                        sol.to_csv(f, index=False)
            return result


    def plot_trips_scenario2(self,
                             csv_path,
                             solution_method,
                             save_fig=True,
                             show_fig=True):
        """Plot a scenario 2 solution read from a CSV file as an interactive Plotly map.

        The solution is split into trips of different colours (depot -> clients -> depot).
        Hovering over a node shows the load on the arc that leaves it.
        The title shows the instance number and the solution method, and the
        subtitle lists every metadata entry found at the top of the CSV file,
        whatever its keys are, so the function works for any solution method.

        Expected CSV format (as written by ``solve_gurobi``):

        * Optional metadata lines at the top, each of the form ``# key: value``
          (e.g. ``# runtime: 3.13``, ``# mip_gap: 0.04``).
        * Then a header row ``i,j,q`` followed by one row per arc used in the
          solution: ``i`` is the start node, ``j`` the end node (0 = depot,
          1..n = clients, in the order of ``self.clients``) and ``q`` the load
          carried on the arc in tonnes.

        Args:
            csv_path: Path to the solution CSV file.
            solution_method: Name of the method that produced the solution,
                shown in the title (e.g. "Gurobi").
            save_fig: If True, save the plot as HTML next to the CSV file
                (same name, ``.html`` extension).
            show_fig: If True, open the plot.
        """
        def split_trips(df, depot=0):
            succ = defaultdict(list)
            for i, j in zip(df["i"], df["j"]):
                succ[i].append(j)

            trips = []
            while succ[depot]:
                trip = [depot]
                node = succ[depot].pop()
                while node != depot:
                    trip.append(node)
                    node = succ[node].pop()
                trip.append(depot)
                trips.append(trip)
            return trips
        
        coords = np.asarray([self.depot] + [c.location for c in self.clients])
        df = pd.read_csv(csv_path, comment="#")

        # Read the "# key: value" metadata lines at the top of the file
        meta = {}
        with open(csv_path) as f:
            for line in f:
                if not line.startswith("#"):
                    break
                key, _, value = line[1:].partition(":")
                meta[key.strip()] = value.strip()

        def _fmt(value):
            # Round numbers for readability, leave anything else as text
            try:
                x = float(value)
            except ValueError:
                return value
            if x.is_integer():
                return f"{int(x):,}"
            return f"{x:,.4f}".rstrip("0")

        # Show all metadata in the subtitle, a few entries per line
        items = [f"{k}: {_fmt(v)}" for k, v in meta.items()]
        per_line = 4
        lines = [" | ".join(items[k:k + per_line]) for k in range(0, len(items), per_line)]
        info = "<br>".join(lines)
        load = {(i, j): q for i, j, q in zip(df["i"], df["j"], df["q"])}

        # Plotly default colours, so each trip's line and arrows share a colour
        palette = ["#636EFA", "#EF553B", "#00CC96", "#AB63FA", "#FFA15A",
                   "#19D3F3", "#FF6692", "#B6E880", "#FF97FF", "#FECB52"]

        fig = go.Figure()
        for t, trip in enumerate(split_trips(df), start=1):
            color = palette[(t - 1) % len(palette)]
            group = f"trip {t}"

            fig.add_trace(go.Scatter(
                x=coords[trip, 0], y=coords[trip, 1],
                mode="lines+markers", name=group, legendgroup=group,
                line=dict(color=color),
                marker=dict(size=11, color=color),
                text=[f"node {n}" for n in trip],
                customdata=[load.get((a, b), 0) for a, b in zip(trip, trip[1:] + [trip[-1]])],
                hovertemplate="%{text}<br>load on next arc: %{customdata}<extra></extra>",
            ))

            # Direction arrows at the midpoint of each arc of the trip
            start = coords[trip[:-1]]
            end = coords[trip[1:]]
            mid = (start + end) / 2
            delta = end - start
            # Plotly marker angle: degrees clockwise from "up"
            angles = np.degrees(np.arctan2(delta[:, 0], delta[:, 1]))

            fig.add_trace(go.Scatter(
                x=mid[:, 0], y=mid[:, 1],
                mode="markers", legendgroup=group, showlegend=False,
                marker=dict(symbol="arrow", size=12, angle=angles, color=color),
                hoverinfo="skip",
            ))

        fig.add_trace(go.Scatter(x=[coords[0, 0]], y=[coords[0, 1]], mode="markers",
                                marker=dict(size=14, symbol="square", color="black"),
                                name="depot"))
        fig.update_layout(
            title=dict(text=f"Instance {self.instance}. Solution method: {solution_method}",
                       subtitle=dict(text=info)),
            margin=dict(t=80 + 20 * len(lines)),  # room for a subtitle of any length
            yaxis_scaleanchor="x")

        if save_fig:
            fig.write_html(csv_path.replace('.csv', '.html'))
        if show_fig:
            fig.show()
        return
