if st.button("🚀 Solve VRP"):

    routes = solve_vrp(df, num_vehicles, vehicle_capacity)

    if routes is None:
        st.error("❌ No solution found!")

        # Suggestions
        total_demand = df['Demand'].sum()
        total_capacity = num_vehicles * vehicle_capacity

        st.warning("💡 Suggestions to fix:")

        if total_demand > total_capacity:
            st.write(f"👉 Increase capacity: Current = {total_capacity}, Needed ≥ {total_demand}")

            suggested_vehicles = math.ceil(total_demand / vehicle_capacity)
            st.write(f"👉 Suggested vehicles: {suggested_vehicles}")

            suggested_capacity = math.ceil(total_demand / num_vehicles)
            st.write(f"👉 Suggested capacity per vehicle: {suggested_capacity}")

        else:
            st.write("👉 Try increasing number of vehicles")
            st.write("👉 Try increasing vehicle capacity")
            st.write("👉 Check if depot demand is 0")
            st.write("👉 Ensure data is valid (no missing values)")

    else:
        st.success("✅ Solution Found!")

        for i, (route, load) in enumerate(routes):
            st.write(f"### 🚚 Vehicle {i+1}")
            st.write(f"Route: {route}")
            st.write(f"Load: {load}")
