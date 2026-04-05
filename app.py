import streamlit as st
import pandas as pd
import math
import folium
import matplotlib.pyplot as plt
from streamlit_folium import st_folium
from ortools.constraint_solver import pywrapcp, routing_enums_pb2

# -----------------------------
# CONFIG
# -----------------------------
st.set_page_config(page_title="Enterprise VRP", layout="wide")

st.markdown("## 🚚 Enterprise Logistics Optimization System")
st.caption("Route Optimization | Cost | Profit | Analytics Dashboard")
st.markdown("---")

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
    num_vehicles = st.number_input("🚚 Vehicles", min_value=1, value=2)
with col2:
    vehicle_capacity = st.number_input("📦 Capacity", min_value=1, value=40)

col3, col4, col5 = st.columns(3)
with col3:
    fuel_cost_per_km = st.number_input("⛽ Fuel Cost/KM", value=50.0)
with col4:
    revenue_per_unit = st.number_input("💰 Revenue per Unit", value=200.0)
with col5:
    penalty_per_km = st.number_input("⏱️ Penalty per Extra KM", value=5.0)

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

    locations = list(zip(df['Latitude'], df['Longitude']))
    demands = df['Demand'].tolist()
    n = len(locations)

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

    st.subheader("📊 Data")
    st.dataframe(df)

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

        # -----------------------------
        # RESULTS
        # -----------------------------
        if st.session_state.routes:

            st.success("✅ Solution Found")

            total_distance = 0
            total_penalty = 0
            report_data = []

            for i,(route,load) in enumerate(st.session_state.routes):

                dist = route_distance(route, df)
                total_distance += dist

                penalty = max(0, dist - 20) * penalty_per_km
                total_penalty += penalty

                st.write(f"### 🚚 Vehicle {i+1}")
                st.write("Route:", route)
                st.write("Load:", load)
                st.write(f"Distance: {round(dist,2)} km")
                st.write(f"Penalty: {round(penalty,2)}")

                report_data.append({
                    "Vehicle": i+1,
                    "Route": str(route),
                    "Load": load,
                    "Distance": round(dist,2),
                    "Penalty": round(penalty,2)
                })

            # -----------------------------
            # FINANCIAL SUMMARY
            # -----------------------------
            total_cost = total_distance * fuel_cost_per_km
            total_revenue = total_demand * revenue_per_unit
            profit = total_revenue - total_cost - total_penalty

            st.markdown("---")
            st.subheader("💰 Financial Summary")

            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Revenue", round(total_revenue,2))
            c2.metric("Cost", round(total_cost,2))
            c3.metric("Penalty", round(total_penalty,2))
            c4.metric("Profit", round(profit,2))

            # -----------------------------
            # CHART
            # -----------------------------
            st.subheader("📊 Distance per Vehicle")

            vehicle_ids = [f"V{i+1}" for i in range(len(report_data))]
            distances = [r["Distance"] for r in report_data]

            fig, ax = plt.subplots()
            ax.bar(vehicle_ids, distances)
            ax.set_ylabel("Distance (km)")
            ax.set_title("Vehicle Distance")

            st.pyplot(fig)

            # -----------------------------
            # MAP
            # -----------------------------
            st.subheader("🗺️ Route Map")

            center = [df['Latitude'].mean(), df['Longitude'].mean()]
            m = folium.Map(location=center, zoom_start=12)

            colors = ["red", "blue", "green", "purple", "orange"]

            for i,(route,_) in enumerate(st.session_state.routes):
                coords = []

                for node in route:
                    lat = df.iloc[node]['Latitude']
                    lon = df.iloc[node]['Longitude']
                    coords.append((lat, lon))

                    folium.Marker(
                        [lat, lon],
                        popup=f"Node {node}",
                        icon=folium.Icon(color=colors[i % len(colors)])
                    ).add_to(m)

                folium.PolyLine(coords, color=colors[i % len(colors)], weight=5).add_to(m)

            st_folium(m, width=900, height=500)

            # -----------------------------
            # DOWNLOAD REPORT
            # -----------------------------
            st.subheader("📥 Download Report")

            report_df = pd.DataFrame(report_data)

            st.download_button(
                "⬇️ Download CSV Report",
                report_df.to_csv(index=False),
                "vrp_report.csv",
                "text/csv"
            )

        else:
            st.info("Click Solve to run optimization")

else:
    st.info("Upload CSV to start")
