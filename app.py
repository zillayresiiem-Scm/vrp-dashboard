import streamlit as st
from ortools.constraint_solver import pywrapcp, routing_enums_pb2

st.set_page_config(page_title="🚚 VRP Enterprise Solver", layout="wide")

st.title("🚚 Enterprise VRP Solver")

# ---------------- INPUT ----------------
st.header("📥 Input Data")

col1, col2 = st.columns(2)

with col1:
    matrix_text = st.text_area(
        "Distance Matrix (rows separated by new line)",
        value="0 10 8 7 12\n10 0 5 6 9\n8 5 0 4 8\n7 6 4 0 7\n12 9 8 7 0"
    )

with col2:
    demand_text = st.text_input(
        "Demands (include depot 0 demand)",
        value="0 4 6 5 7"
    )

capacity = st.number_input("Vehicle Capacity", value=15)
num_vehicles = st.number_input("Number of Vehicles", value=2)

# ---------------- PARSER ----------------
def parse_row(row):
    row = row.replace(",", " ")
    return [int(x) for x in row.split()]

def parse_matrix(text):
    lines = text.strip().split("\n")
    return [parse_row(line) for line in lines]

def parse_demands(text):
    return [int(x) for x in text.replace(",", " ").split()]

# ---------------- SOLVER ----------------
def solve_vrp(distance_matrix, demands, vehicle_capacity, num_vehicles):
    manager = pywrapcp.RoutingIndexManager(
        len(distance_matrix),
        num_vehicles,
        0
    )

    routing = pywrapcp.RoutingModel(manager)

    def distance_callback(from_index, to_index):
        return distance_matrix[
            manager.IndexToNode(from_index)
        ][
            manager.IndexToNode(to_index)
        ]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

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

    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
    )

    solution = routing.SolveWithParameters(search_parameters)

    routes = []
    total_distance = 0

    if solution:
        for vehicle_id in range(num_vehicles):
            index = routing.Start(vehicle_id)
            route = []
            route_distance = 0

            while not routing.IsEnd(index):
                node = manager.IndexToNode(index)
                route.append(node)
                previous_index = index
                index = solution.Value(routing.NextVar(index))
                route_distance += routing.GetArcCostForVehicle(
                    previous_index, index, vehicle_id
                )

            route.append(0)
            routes.append((route, route_distance))
            total_distance += route_distance

    return routes, total_distance

# ---------------- RUN ----------------
if st.button("🚀 Solve VRP"):

    try:
        distance_matrix = parse_matrix(matrix_text)
        demands = parse_demands(demand_text)

        # Validation
        n = len(distance_matrix)

        if any(len(row) != n for row in distance_matrix):
            st.error("❌ Matrix must be square")
            st.stop()

        if len(demands) != n:
            st.error("❌ Demands must match matrix size")
            st.stop()

        routes, total = solve_vrp(distance_matrix, demands, capacity, num_vehicles)

        st.success("✅ Solution Found!")

        st.header("📊 Results")

        for i, (route, dist) in enumerate(routes):
            st.write(f"🚛 Vehicle {i+1}: {' → '.join(map(str, route))}")
            st.write(f"Distance: {dist}")
            st.divider()

        st.subheader(f"🏁 Total Distance: {total}")

    except Exception as e:
        st.error(f"❌ Error: {e}")
