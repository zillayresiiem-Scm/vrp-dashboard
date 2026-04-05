import streamlit as st
import pandas as pd
import math
from ortools.constraint_solver import pywrapcp, routing_enums_pb2

st.set_page_config(page_title="VRP Stable App", layout="wide")

st.title("🚚 VRP Solver (Stable Version)")

# -----------------------------
# SESSION STATE
# -----------------------------
if "routes" not in st.session_state:
    st.session_state.routes = None

# -----------------------------
# INPUTS
# -----------------------------
uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

col1, col2 = st.columns(2)
with col1:
    num_vehicles = st.number_input("Vehicles", min_value=1, value=2)
with col2:
    vehicle_capacity = st.number_input("Capacity", min_value=1, value=40)

# -----------------------------
# DISTANCE
# -----------------------------
def haversine(c1, c2):
    R = 6371
    lat1, lon1 = c1
    lat2, lon2 = c2

    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lon2 - lon1)

    a = math.sin(dphi/2)**2 + math.cos(phi1)*math.cos(phi2)*math.sin(dlambda/2)**2
    return R * (2 * math.atan2(math.sqrt(a), math.sqrt(1 - a)))

# -----------------------------
# SOLVER
# -----------------------------
def solve_vrp(df):

    locations = list(zip(df['Latitude'], df['Longitude']))
    demands = df['Demand'].tolist()

    n = len(locations)

    # distance matrix
    dist = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            dist[i][j] = int(haversine(locations[i], locations[j]) * 1000)

    manager = pywrapcp.RoutingIndexManager(n, num_vehicles, 0)
    routing = pywrapcp.RoutingModel(manager)

    def distance_callback(i, j):
        return dist[manager.IndexToNode(i)][manager.IndexToNode(j)]

    transit = routing.RegisterTransitCallback(distance_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit)

    def demand_callback(i):
        return demands[manager.IndexToNode(i)]

    demand_cb = routing.RegisterUnaryTransitCallback(demand_callback)

    routing.AddDimensionWithVehicleCapacity(
        demand_cb,
        0,
        [vehicle_capacity]*num_vehicles,
        True,
        "Capacity"
    )

    search = pywrapcp.DefaultRoutingSearchParameters()
    search.first_solution_strategy = routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC

    solution = routing.SolveWithParameters(search)

    if solution is None:
        return None

    routes = []
    for v in range(num_vehicles):
        idx = routing.Start(v)
        route = []
        load = 0

        while not routing.IsEnd(idx):
            node = manager.IndexToNode(idx)
            route.append(node)
            load += demands[node]
            idx = solution.Value(routing.NextVar(idx))

        route.append(0)
        routes.append((route, load))

    return routes

# -----------------------------
# MAIN
# -----------------------------
if uploaded_file:

    df = pd.read_csv(uploaded_file)

    st.subheader("Data")
    st.dataframe(df)

    # safety check
    if not all(col in df.columns for col in ["Latitude","Longitude","Demand"]):
        st.error("CSV must contain Latitude, Longitude, Demand")
    else:

        total_demand = df["Demand"].sum()
        total_capacity = num_vehicles * vehicle_capacity

        st.write("Total Demand:", total_demand)
        st.write("Total Capacity:", total_capacity)

        if st.button("🚀 Solve"):

            if total_demand > total_capacity:
                st.error("❌ Not feasible: demand > capacity")
                st.session_state.routes = None
            else:
                st.session_state.routes = solve_vrp(df)

        if st.button("🔄 Reset"):
            st.session_state.routes = None

        # display results
        if st.session_state.routes:

            st.success("✅ Solution Found")

            for i,(route,load) in enumerate(st.session_state.routes):
                st.write(f"Vehicle {i+1}")
                st.write("Route:", route)
                st.write("Load:", load)

        elif st.session_state.routes is None:
            st.info("Click Solve to run optimization")

else:
    st.info("Upload CSV to start")

