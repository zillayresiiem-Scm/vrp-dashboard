import streamlit as st
import pandas as pd
import math
import numpy as np
import folium
from streamlit_folium import st_folium
from ortools.constraint_solver import pywrapcp, routing_enums_pb2

# -----------------------------
# CONFIG
# -----------------------------
st.set_page_config(page_title="Enterprise VRP", layout="wide")

st.title("🚚 Enterprise Logistics Optimization Dashboard")
st.caption("Routing | Cost | Profit | Time Penalty | Map Visualization")

# -----------------------------
# SESSION STATE
# -----------------------------
if "routes" not in st.session_state:
    st.session_state.routes = None

# -----------------------------
# INPUTS
# -----------------------------
uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

col1, col2, col3 = st.columns(3)
with col1:
    num_vehicles = st.number_input("🚚 Vehicles", 1, 20, 3)
with col2:
    vehicle_capacity = st.number_input("📦 Capacity", 1, 500, 100)
with col3:
    fuel_cost_per_km = st.number_input("⛽ Fuel Cost/KM", value=50.0)

col4, col5 = st.columns(2)
with col4:
    revenue_per_unit = st.number_input("💰 Revenue per Unit", value=200.0)
with col5:
    penalty_per_min = st.number_input("⏱️ Late Delivery Penalty", value=5.0)

# -----------------------------
# HAVERSINE
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
# DISTANCE CALC
# -----------------------------
def route_distance(route, df):
    total = 0
    for i in range(len(route)-1):
        lat1, lon1 = df.iloc[route[i]][['Latitude','Longitude']]
        lat2, lon2 = df.iloc[route[i+1]][['Latitude','Longitude']]
        total += haversine((lat1, lon1), (lat2, lon2))
    return total

# -----------------------------
# SOLVER
# -----------------------------
def solve_vrp(df):

    if 'Demand' not in df.columns:
        df['Demand'] = np.random.randint(5, 30, size=len(df))
        st.info("🤖 AI generated demand")

    locations = list(zip(df['Latitude'], df['Longitude']))
    demands = df['Demand'].tolist()

    distance_matrix = [
        [int(haversine(locations[i], locations[j])*1000)
         for j in range(len(locations))]
        for i in range(len(locations))
    ]

    manager = pywrapcp.RoutingIndexManager(len(distance_matrix), num_vehicles, 0)
    routing = pywrapcp.RoutingModel(manager)

    def dist_cb(f, t):
        return distance_matrix[manager.IndexToNode(f)][manager.IndexToNode(t)]

    transit = routing.RegisterTransitCallback(dist_cb)
    routing.SetArcCostEvaluatorOfAllVehicles(transit)

    def demand_cb(f):
        return demands[manager.IndexToNode(f)]

    demand_cb_i = routing.RegisterUnaryTransitCallback(demand_cb)

    routing.AddDimensionWithVehicleCapacity(
        demand_cb_i, 0,
        [vehicle_capacity]*num_vehicles,
        True, "Capacity"
    )

    # Time windows (optional)
    if 'ReadyTime' in df.columns and 'DueTime' in df.columns:

        time_cb = routing.RegisterTransitCallback(dist_cb)
        routing.AddDimension(time_cb, 30, 10000, False, "Time")
        time_dim = routing.GetDimensionOrDie("Time")

        for i in range(len(df)):
            idx = manager.NodeToIndex(i)
            time_dim.CumulVar(idx).SetRange(
                int(df['ReadyTime'][i]),
                int(df['DueTime'][i])
            )

    params = pywrapcp.DefaultRoutingSearchParameters()
    params.first_solution_strategy = routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC

    sol = routing.SolveWithParameters(params)

    if not sol:
        return None

    routes = []
    for v in range(num_vehicles):
        idx = routing.Start(v)
        route = []
        load = 0

        while not routing.IsEnd(idx):
            node = manager.IndexToNode(idx)
            load += demands[node]
            route.append(node)
            idx = sol.Value(routing.NextVar(idx))

        route.append(0)
        routes.append((route, load))

    return routes

# -----------------------------
# MAIN
# -----------------------------
if uploaded_file:

    df = pd.read_csv(uploaded_file)
    st.dataframe(df)

    total_demand = df['Demand'].sum() if 'Demand' in df.columns else 0
    total_capacity = num_vehicles * vehicle_capacity

    st.markdown("### 📊 KPIs")
    c1,c2,c3 = st.columns(3)
    c1.metric("Demand", total_demand)
    c2.metric("Capacity", total_capacity)
    c3.metric("Vehicles", num_vehicles)

    if st.button("🚀 Optimize"):
        st.session_state.routes = solve_vrp(df)

    if st.button("🔄 Reset"):
        st.session_state.routes = None

    # -----------------------------
    # RESULTS
    # -----------------------------
    if st.session_state.routes:

        total_distance = 0
        total_penalty = 0

        st.markdown("## 🚚 Routes")

        for i,(route, load) in enumerate(st.session_state.routes):
            dist = route_distance(route, df)
            total_distance += dist

            # penalty simulation
            late_minutes = max(0, dist - 50)
            penalty = late_minutes * penalty_per_min
            total_penalty += penalty

            st.write(f"🚚 Vehicle {i+1} | Load: {load} | Distance: {round(dist,2)} km | Penalty: {round(penalty,2)}")

        total_cost = total_distance * fuel_cost_per_km
        revenue = total_demand * revenue_per_unit
        profit = revenue - total_cost - total_penalty

        st.markdown("## 💰 Financial Summary")
        c1,c2,c3,c4 = st.columns(4)
        c1.metric("Revenue", round(revenue,2))
        c2.metric("Cost", round(total_cost,2))
        c3.metric("Penalty", round(total_penalty,2))
        c4.metric("Profit", round(profit,2))

        # -----------------------------
        # MAP
        # -----------------------------
        st.markdown("## 🗺️ Live Map")

        center = [df['Latitude'].mean(), df['Longitude'].mean()]
        m = folium.Map(location=center, zoom_start=12)

        colors = ["red","blue","green","purple","orange"]

        for i,(route,_) in enumerate(st.session_state.routes):
            coords = []

            for node in route:
                lat = df.iloc[node]['Latitude']
                lon = df.iloc[node]['Longitude']
                coords.append((lat,lon))

                folium.Marker(
                    [lat,lon],
                    icon=folium.Icon(color=colors[i%len(colors)])
                ).add_to(m)

            folium.PolyLine(coords, color=colors[i%len(colors)]).add_to(m)

        st_folium(m, width=900, height=500)

else:
    st.info("Upload CSV to start")
