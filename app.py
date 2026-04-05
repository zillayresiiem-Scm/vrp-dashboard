import streamlit as st
import pandas as pd
import math
from ortools.constraint_solver import pywrapcp, routing_enums_pb2

st.set_page_config(page_title="CVRP Solver", layout="wide")

st.title("🚚 Vehicle Routing Problem (CVRP) Solver")

# -----------------------------
# FILE UPLOAD
# -----------------------------
uploaded_file = st.file_uploader("Upload CSV (ID, Latitude, Longitude, Demand)", type=["csv"])

# -----------------------------
# USER INPUTS
# -----------------------------
col1, col2 = st.columns(2)
with col1:
    num_vehicles = st.number_input("Number of Vehicles", min_value=1, value=2)
with col2:
    vehicle_capacity = st.number_input("Vehicle Capacity", min_value=1, value=50)

# -----------------------------
# HAVERSINE FUNCTION
# -----------------------------
def haversine(coord1, coord2):
    R = 6371
    lat1, lon1 = coord1
    lat2, lon2 = coord2

    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)

    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    return R * (2 * math.atan2(math.sqrt(a), math.sqrt(1 - a)))

# -----------------------------
# SOLVE FUNCTION
# -----------------------------
def solve_vrp(df, num_vehicles, vehicle_capacity):

    locations = list(zip(df['Latitude'], df['Longitude']))
    demands = df['Demand'].tolist()
    depot = 0

    # Distance matrix
    distance_matrix = [
        [int(haversine(locations[i], locations[j]) * 1000)
         for j in range(len(locations))]
        for i in range(len(locations))
    ]

    manager = pywrapcp.RoutingIndexManager(len(distance_matrix), num_vehicles, depot)
    routing = pywrapcp.RoutingModel(manager)

    # Distance callback
    def distance_callback(from_index, to_index):
        return distance_matrix[manager.IndexToNode(from_index)][manager.IndexToNode(to_index)]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Demand callback
    def demand_callback(from_index):
        return demands[manager.IndexToNode(from_index)]

    demand_callback_index = routing.RegisterUnaryTransitCallback(demand_callback)

    routing.AddDimensionWithVehicleCapacity(
        demand_callback_index,
        0,
        [vehicle_capacity] * num_vehicles,
        True,
        "Capacity"
    )

    # Solver settings
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
    )

    solution = routing.SolveWithParameters(search_parameters)

    if not solution:
        return None

    routes = []
    for vehicle_id in range(num_vehicles):
        index = routing.Start(vehicle_id)
        route = []
        load = 0

        while not routing.IsEnd(index):
            node = manager.IndexToNode(index)
            load += demands[node]
            route.append(node)
            index = solution.Value(routing.NextVar(index))

        route.append(depot)
        routes.append((route, load))

    return routes

# -----------------------------
# RUN SOLVER
# -----------------------------
if uploaded_file:

    df = pd.read_csv(uploaded_file)

    st.subheader("📊 Uploaded Data")
    st.dataframe(df)

    # Validate columns
    required_cols = ['Latitude', 'Longitude', 'Demand']
    if not all(col in df.columns for col in required_cols):
        st.error("CSV must contain: Latitude, Longitude, Demand")
    else:

        if st.button("🚀 Solve VRP"):
            routes = solve_vrp(df, num_vehicles, vehicle_capacity)

            if routes is None:
                st.error("❌ No solution found. Try increasing vehicles or capacity.")
            else:
                st.success("✅ Solution Found!")

                for i, (route, load) in enumerate(routes):
                    st.write(f"### 🚚 Vehicle {i+1}")
                    st.write(f"Route: {route}")
                    st.write(f"Load: {load}")

else:
    st.info("👆 Upload your CSV file to begin")