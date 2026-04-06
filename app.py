import streamlit as st
import pandas as pd
import math
from ortools.constraint_solver import pywrapcp, routing_enums_pb2

st.set_page_config(page_title="VRP Dual Mode", layout="wide")

st.title("🚚 VRP Solver (Matrix + Coordinates)")

# -----------------------------
# MODE SELECT
# -----------------------------
mode = st.radio("Select Mode", ["Distance Matrix", "Coordinates"])

# -----------------------------
# COMMON INPUTS
# -----------------------------
col1, col2 = st.columns(2)
with col1:
    num_vehicles = st.number_input("Vehicles", 1, 10, 2)
with col2:
    vehicle_capacity = st.number_input("Capacity", 1, 100, 15)

# -----------------------------
# MATRIX MODE
# -----------------------------
if mode == "Distance Matrix":

    st.subheader("📊 Matrix Input")

    matrix_text = st.text_area("Distance Matrix (comma separated rows)",
    "0,10,8,7,12\n10,0,5,6,9\n8,5,0,4,8\n7,6,4,0,7\n12,9,8,7,0")

    demand_text = st.text_input("Demands", "0,4,6,5,7")

    if st.button("🚀 Solve Matrix VRP"):

        distance_matrix = [list(map(int, row.split(","))) for row in matrix_text.split("\n")]
        demands = list(map(int, demand_text.split(",")))

        n = len(distance_matrix)

        manager = pywrapcp.RoutingIndexManager(n, num_vehicles, 0)
        routing = pywrapcp.RoutingModel(manager)

        def dist_cb(i, j):
            return distance_matrix[manager.IndexToNode(i)][manager.IndexToNode(j)]

        transit = routing.RegisterTransitCallback(dist_cb)
        routing.SetArcCostEvaluatorOfAllVehicles(transit)

        def demand_cb(i):
            return demands[manager.IndexToNode(i)]

        demand_cb_i = routing.RegisterUnaryTransitCallback(demand_cb)

        routing.AddDimensionWithVehicleCapacity(
            demand_cb_i, 0,
            [vehicle_capacity]*num_vehicles,
            True, "Capacity"
        )

        search = pywrapcp.DefaultRoutingSearchParameters()
        search.first_solution_strategy = routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC

        solution = routing.SolveWithParameters(search)

        if solution:
            total_dist = 0

            for v in range(num_vehicles):
                idx = routing.Start(v)
                route = []
                dist = 0

                while not routing.IsEnd(idx):
                    node = manager.IndexToNode(idx)
                    route.append(node)
                    prev = idx
                    idx = solution.Value(routing.NextVar(idx))
                    dist += routing.GetArcCostForVehicle(prev, idx, v)

                route.append(0)
                total_dist += dist

                st.write(f"🚚 Vehicle {v+1}: {route} | Distance = {dist}")

            st.success(f"✅ Total Distance = {total_dist}")

        else:
            st.error("❌ No solution found")

# -----------------------------
# COORDINATE MODE
# -----------------------------
else:

    st.subheader("📍 Upload Coordinates CSV")

    uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

    def haversine(c1, c2):
        R = 6371
        lat1, lon1 = c1
        lat2, lon2 = c2

        phi1, phi2 = math.radians(lat1), math.radians(lat2)
        dphi = math.radians(lat2 - lat1)
        dlambda = math.radians(lon2 - lon1)

        a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
        return R * (2 * math.atan2(math.sqrt(a), math.sqrt(1 - a)))

    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.dataframe(df)

        if st.button("🚀 Solve Coordinates VRP"):

            locations = list(zip(df['Latitude'], df['Longitude']))
            demands = df['Demand'].tolist()
            n = len(locations)

            dist = [[0]*n for _ in range(n)]
            for i in range(n):
                for j in range(n):
                    dist[i][j] = int(haversine(locations[i], locations[j]) * 1000)

            manager = pywrapcp.RoutingIndexManager(n, num_vehicles, 0)
            routing = pywrapcp.RoutingModel(manager)

            def dist_cb(i, j):
                return dist[manager.IndexToNode(i)][manager.IndexToNode(j)]

            transit = routing.RegisterTransitCallback(dist_cb)
            routing.SetArcCostEvaluatorOfAllVehicles(transit)

            def demand_cb(i):
                return demands[manager.IndexToNode(i)]

            demand_cb_i = routing.RegisterUnaryTransitCallback(demand_cb)

            routing.AddDimensionWithVehicleCapacity(
                demand_cb_i, 0,
                [vehicle_capacity]*num_vehicles,
                True, "Capacity"
            )

            search = pywrapcp.DefaultRoutingSearchParameters()
            search.first_solution_strategy = routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC

            solution = routing.SolveWithParameters(search)

            if solution:
                for v in range(num_vehicles):
                    idx = routing.Start(v)
                    route = []

                    while not routing.IsEnd(idx):
                        route.append(manager.IndexToNode(idx))
                        idx = solution.Value(routing.NextVar(idx))

                    route.append(0)
                    st.write(f"🚚 Vehicle {v+1}: {route}")

            else:
                st.error("❌ No solution found")
