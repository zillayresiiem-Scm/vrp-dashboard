"""
Enterprise Vehicle Routing Problem (VRP) Solver
Built with Streamlit + Google OR-Tools
Run: streamlit run app.py
"""

import streamlit as st
import re
import io
import csv
from typing import Optional

# ─── Page Config ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="VRP Solver | Enterprise Edition",
    page_icon="🚛",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=IBM+Plex+Sans:wght@300;400;500;600&display=swap');

html, body, [class*="css"] {
    font-family: 'IBM Plex Sans', sans-serif;
}

/* ── Main background ── */
.stApp {
    background: #0d0f14;
    color: #e2e8f0;
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: #111318 !important;
    border-right: 1px solid #1e2530;
}
section[data-testid="stSidebar"] * {
    color: #cbd5e1 !important;
}
section[data-testid="stSidebar"] .stTextArea textarea,
section[data-testid="stSidebar"] .stNumberInput input {
    background: #181c25 !important;
    border: 1px solid #2a3444 !important;
    color: #e2e8f0 !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.82rem !important;
    border-radius: 6px !important;
}
section[data-testid="stSidebar"] .stTextArea textarea:focus,
section[data-testid="stSidebar"] .stNumberInput input:focus {
    border-color: #3b82f6 !important;
    box-shadow: 0 0 0 2px rgba(59,130,246,0.25) !important;
}
section[data-testid="stSidebar"] label {
    font-size: 0.78rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.06em !important;
    text-transform: uppercase !important;
    color: #64748b !important;
}

/* ── Buttons ── */
.stButton > button {
    width: 100%;
    background: linear-gradient(135deg, #1d4ed8 0%, #2563eb 100%) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 0.65rem 1.5rem !important;
    font-family: 'IBM Plex Sans', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    letter-spacing: 0.04em !important;
    cursor: pointer !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 4px 14px rgba(37,99,235,0.35) !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, #1e40af 0%, #1d4ed8 100%) !important;
    box-shadow: 0 6px 20px rgba(37,99,235,0.5) !important;
    transform: translateY(-1px) !important;
}

/* ── File uploader ── */
[data-testid="stFileUploader"] {
    border: 1px dashed #2a3444 !important;
    border-radius: 8px !important;
    background: #181c25 !important;
    padding: 0.5rem !important;
}

/* ── Metric cards ── */
.metric-card {
    background: #131720;
    border: 1px solid #1e2a3a;
    border-radius: 12px;
    padding: 1.2rem 1.4rem;
    text-align: center;
}
.metric-card .metric-value {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 2rem;
    font-weight: 600;
    color: #60a5fa;
    line-height: 1;
}
.metric-card .metric-label {
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #475569;
    margin-top: 0.4rem;
}

/* ── Route cards ── */
.route-card {
    background: #131720;
    border: 1px solid #1e2a3a;
    border-left: 3px solid #3b82f6;
    border-radius: 10px;
    padding: 1.1rem 1.4rem;
    margin-bottom: 0.9rem;
    transition: border-color 0.2s;
}
.route-card:hover { border-left-color: #60a5fa; }
.route-card .vehicle-header {
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #3b82f6;
    margin-bottom: 0.45rem;
}
.route-card .route-path {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 1rem;
    color: #e2e8f0;
    word-break: break-word;
}
.route-card .route-meta {
    font-size: 0.78rem;
    color: #64748b;
    margin-top: 0.5rem;
}
.route-card .badge {
    display: inline-block;
    background: rgba(59,130,246,0.12);
    color: #60a5fa;
    border-radius: 4px;
    padding: 0.1rem 0.5rem;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.78rem;
    margin-right: 0.5rem;
}

/* ── Section headings ── */
.section-title {
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: #475569;
    border-bottom: 1px solid #1e2a3a;
    padding-bottom: 0.45rem;
    margin-bottom: 1rem;
}

/* ── Matrix preview ── */
.matrix-preview {
    background: #0d1117;
    border: 1px solid #1e2a3a;
    border-radius: 8px;
    padding: 1rem;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.8rem;
    color: #94a3b8;
    overflow-x: auto;
    white-space: pre;
}

/* ── Info banner ── */
.info-banner {
    background: rgba(59,130,246,0.08);
    border: 1px solid rgba(59,130,246,0.2);
    border-radius: 8px;
    padding: 0.9rem 1.2rem;
    font-size: 0.85rem;
    color: #93c5fd;
    margin-bottom: 1.2rem;
}

/* ── Alerts ── */
.stAlert { border-radius: 8px !important; }

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: #111318;
    border-radius: 8px;
    gap: 4px;
    padding: 4px;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: #64748b !important;
    border-radius: 6px !important;
    font-size: 0.82rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.05em !important;
}
.stTabs [aria-selected="true"] {
    background: #1e2530 !important;
    color: #e2e8f0 !important;
}
</style>
""", unsafe_allow_html=True)


# ─── Helpers ──────────────────────────────────────────────────────────────────

def parse_matrix(raw: str) -> Optional[list[list[int]]]:
    """
    Parse a distance matrix from raw text.
    Supports comma-separated and space-separated values, mixed rows.
    Returns a 2-D list of ints, or raises ValueError with a clear message.
    """
    raw = raw.strip()
    if not raw:
        raise ValueError("Distance matrix input is empty.")

    matrix = []
    for line_no, line in enumerate(raw.splitlines(), start=1):
        line = line.strip()
        if not line:
            continue  # skip blank lines
        # replace commas with spaces then split
        parts = re.split(r"[,\s]+", line.replace(",", " "))
        parts = [p for p in parts if p]
        try:
            row = [int(p) for p in parts]
        except ValueError:
            raise ValueError(
                f"Row {line_no} contains non-integer value(s): '{line}'"
            )
        if any(v < 0 for v in row):
            raise ValueError(f"Row {line_no} contains negative distances.")
        matrix.append(row)

    if not matrix:
        raise ValueError("No valid rows found in distance matrix.")

    n = len(matrix)
    for i, row in enumerate(matrix, start=1):
        if len(row) != n:
            raise ValueError(
                f"Matrix is not square: row {i} has {len(row)} elements "
                f"but expected {n} (number of rows = {n})."
            )
    return matrix


def parse_demands(raw: str, expected_len: int) -> Optional[list[int]]:
    """
    Parse demand values from raw text (comma or space separated, single line or multi).
    Returns a list of ints. First element must be 0 (depot).
    """
    raw = raw.strip()
    if not raw:
        raise ValueError("Demands input is empty.")

    parts = re.split(r"[,\s]+", raw.replace(",", " "))
    parts = [p for p in parts if p]
    try:
        demands = [int(p) for p in parts]
    except ValueError:
        raise ValueError("Demands contain non-integer value(s).")

    if len(demands) != expected_len:
        raise ValueError(
            f"Demands length ({len(demands)}) does not match "
            f"number of nodes ({expected_len})."
        )
    if demands[0] != 0:
        raise ValueError(
            f"First demand (depot) must be 0, got {demands[0]}."
        )
    if any(d < 0 for d in demands):
        raise ValueError("Demands must be non-negative.")
    return demands


def solve_vrp(
    distance_matrix: list[list[int]],
    demands: list[int],
    vehicle_capacity: int,
    num_vehicles: int,
    depot: int = 0,
    time_limit_seconds: int = 10,
) -> dict:
    """
    Core VRP solver using Google OR-Tools.
    Returns a dict with routes, distances, total_distance, and status.
    """
    from ortools.constraint_solver import routing_enums_pb2
    from ortools.constraint_solver import pywrapcp

    n = len(distance_matrix)

    # ── Create routing index manager ──────────────────────────────────────────
    manager = pywrapcp.RoutingIndexManager(n, num_vehicles, depot)
    routing = pywrapcp.RoutingModel(manager)

    # ── Distance callback ─────────────────────────────────────────────────────
    def distance_callback(from_index, to_index):
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return distance_matrix[from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # ── Capacity constraint ───────────────────────────────────────────────────
    def demand_callback(from_index):
        from_node = manager.IndexToNode(from_index)
        return demands[from_node]

    demand_callback_index = routing.RegisterUnaryTransitCallback(demand_callback)
    routing.AddDimensionWithVehicleCapacity(
        demand_callback_index,
        0,                              # null capacity slack
        [vehicle_capacity] * num_vehicles,
        True,                           # start cumul to zero
        "Capacity",
    )

    # ── Search parameters ─────────────────────────────────────────────────────
    search_params = pywrapcp.DefaultRoutingSearchParameters()
    search_params.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
    )
    search_params.time_limit.seconds = time_limit_seconds

    # ── Solve ─────────────────────────────────────────────────────────────────
    solution = routing.SolveWithParameters(search_params)

    if not solution:
        return {"status": "NO_SOLUTION", "routes": [], "total_distance": 0}

    # ── Extract routes ────────────────────────────────────────────────────────
    routes = []
    total_distance = 0

    for vehicle_id in range(num_vehicles):
        index = routing.Start(vehicle_id)
        route_nodes = []
        route_load = 0
        route_distance = 0

        while not routing.IsEnd(index):
            node = manager.IndexToNode(index)
            route_nodes.append(node)
            route_load += demands[node]
            next_index = solution.Value(routing.NextVar(index))
            route_distance += routing.GetArcCostForVehicle(
                index, next_index, vehicle_id
            )
            index = next_index

        # append depot at end
        route_nodes.append(manager.IndexToNode(index))

        routes.append(
            {
                "vehicle_id": vehicle_id + 1,
                "nodes": route_nodes,
                "distance": route_distance,
                "load": route_load,
            }
        )
        total_distance += route_distance

    return {
        "status": "SOLUTION_FOUND",
        "routes": routes,
        "total_distance": total_distance,
    }


def parse_csv_upload(file) -> tuple[str, str]:
    """
    Parse a CSV file into matrix text and demand text.
    CSV format expected:
      - First row (header) is ignored.
      - Each subsequent row: node_index, demand, dist_0, dist_1, ..., dist_n
    Returns (matrix_text, demands_text).
    """
    content = file.read().decode("utf-8")
    reader = csv.reader(io.StringIO(content))
    rows = [r for r in reader if r]

    # detect if first row is header (non-numeric first cell)
    start = 0
    try:
        int(rows[0][0])
    except (ValueError, IndexError):
        start = 1

    demands_list = []
    matrix_rows = []
    for row in rows[start:]:
        row = [c.strip() for c in row if c.strip()]
        if not row:
            continue
        if len(row) < 2:
            raise ValueError("CSV rows must have at least 2 columns (index, demand).")
        demands_list.append(row[1])
        matrix_rows.append(row[2:])

    return (
        "\n".join(", ".join(r) for r in matrix_rows),
        ", ".join(demands_list),
    )


def format_route_path(nodes: list[int]) -> str:
    return " → ".join(str(n) for n in nodes)


def active_routes(routes: list[dict]) -> list[dict]:
    """Filter out vehicles that only go depot→depot."""
    return [r for r in routes if len(r["nodes"]) > 2]


# ─── UI ───────────────────────────────────────────────────────────────────────

# Header
st.markdown("""
<div style="padding:1.8rem 0 1.2rem 0;">
    <div style="font-size:0.7rem;font-weight:700;letter-spacing:0.2em;
                text-transform:uppercase;color:#3b82f6;margin-bottom:0.3rem;">
        Enterprise Edition
    </div>
    <div style="font-size:2rem;font-weight:600;color:#e2e8f0;line-height:1.1;">
        🚛 VRP Solver
    </div>
    <div style="font-size:0.88rem;color:#475569;margin-top:0.4rem;">
        Vehicle Routing Problem · Powered by Google OR-Tools
    </div>
</div>
""", unsafe_allow_html=True)

st.divider()

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙️ Configuration")
    st.markdown("<div class='section-title'>Fleet Parameters</div>", unsafe_allow_html=True)

    num_vehicles = st.number_input(
        "Number of Vehicles", min_value=1, max_value=50, value=2, step=1
    )
    vehicle_capacity = st.number_input(
        "Vehicle Capacity", min_value=1, max_value=100_000, value=15, step=1
    )

    st.markdown("<br><div class='section-title'>Input Mode</div>", unsafe_allow_html=True)
    input_mode = st.radio(
        "Choose input method", ["Manual Entry", "CSV Upload"], horizontal=True, label_visibility="collapsed"
    )

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div style='font-size:0.72rem;color:#334155;line-height:1.6;'>
    <b style='color:#475569'>Accepted formats</b><br>
    Comma-sep: <code>0, 10, 8</code><br>
    Space-sep: <code>0 10 8</code><br>
    Mixed: <code>0,10 8, 7</code>
    </div>
    """, unsafe_allow_html=True)

# ── Main Content ──────────────────────────────────────────────────────────────
col_input, col_output = st.columns([1, 1], gap="large")

with col_input:
    st.markdown("<div class='section-title'>📥 Input Data</div>", unsafe_allow_html=True)

    matrix_text = ""
    demands_text = ""
    csv_error = None

    if input_mode == "CSV Upload":
        uploaded_file = st.file_uploader(
            "Upload CSV File",
            type=["csv"],
            help="Columns: node_index, demand, dist_0, dist_1, ..., dist_n",
        )
        if uploaded_file:
            try:
                matrix_text, demands_text = parse_csv_upload(uploaded_file)
                st.success("✅ CSV parsed successfully.")
            except Exception as e:
                csv_error = str(e)
                st.error(f"CSV Parse Error: {e}")
    else:
        st.markdown("""
        <div class='info-banner'>
        Enter one row per line. Each row represents distances from that node to all others.
        Row 0 = Depot.
        </div>
        """, unsafe_allow_html=True)

        EXAMPLE_MATRIX = (
            "0, 10, 8, 7, 12\n"
            "10, 0, 5, 6, 11\n"
            "8, 5, 0, 3, 9\n"
            "7, 6, 3, 0, 4\n"
            "12, 11, 9, 4, 0"
        )
        EXAMPLE_DEMANDS = "0, 5, 4, 6, 3"

        matrix_text = st.text_area(
            "Distance Matrix",
            value=EXAMPLE_MATRIX,
            height=180,
            placeholder="0, 10, 8\n10, 0, 5\n8, 5, 0",
            help="Paste your distance matrix here. One row per line.",
        )
        demands_text = st.text_area(
            "Node Demands (depot = 0 first)",
            value=EXAMPLE_DEMANDS,
            height=80,
            placeholder="0, 5, 4, 6, 3",
            help="Demand for each node. First value must be 0 (depot).",
        )

    # ── Matrix Preview ──────────────────────────────────────────────────────
    if matrix_text:
        try:
            preview_matrix = parse_matrix(matrix_text)
            n = len(preview_matrix)
            preview_lines = []
            for i, row in enumerate(preview_matrix):
                label = "DEPOT" if i == 0 else f"  N{i:02d}"
                preview_lines.append(
                    f"{label}  " + "  ".join(f"{v:4d}" for v in row)
                )
            preview_str = f"  {''.join(f'  N{j:02d}' if j > 0 else '  DPOT' for j in range(n))}\n"
            preview_str += "\n".join(preview_lines)
            st.markdown(f"<div class='matrix-preview'>{preview_str}</div>", unsafe_allow_html=True)
            st.caption(f"Matrix: {n}×{n} · {n} nodes detected")
        except Exception:
            pass

    st.markdown("<br>", unsafe_allow_html=True)
    solve_btn = st.button("🔍 Solve VRP", type="primary")

# ── Output Panel ──────────────────────────────────────────────────────────────
with col_output:
    st.markdown("<div class='section-title'>📊 Solution</div>", unsafe_allow_html=True)

    if solve_btn:
        if csv_error:
            st.error(f"Cannot solve: CSV had errors — {csv_error}")
        elif not matrix_text.strip():
            st.error("Distance matrix is empty. Please enter data.")
        elif not demands_text.strip():
            st.error("Demands field is empty. Please enter demands.")
        else:
            try:
                # ── Validate & Parse ─────────────────────────────────────────
                distance_matrix = parse_matrix(matrix_text)
                n = len(distance_matrix)
                demands = parse_demands(demands_text, n)

                total_demand = sum(demands[1:])
                min_vehicles_needed = -(-total_demand // vehicle_capacity)  # ceil
                if num_vehicles < min_vehicles_needed:
                    st.warning(
                        f"⚠️ Total demand ({total_demand}) may exceed fleet capacity "
                        f"({num_vehicles} × {vehicle_capacity} = {num_vehicles * vehicle_capacity}). "
                        f"Consider ≥ {min_vehicles_needed} vehicles."
                    )

                # ── Solve ────────────────────────────────────────────────────
                with st.spinner("Solving... ⚙️"):
                    result = solve_vrp(
                        distance_matrix, demands, vehicle_capacity, num_vehicles
                    )

                if result["status"] == "NO_SOLUTION":
                    st.error(
                        "❌ No feasible solution found. Try increasing the number of "
                        "vehicles or vehicle capacity."
                    )
                else:
                    routes = result["routes"]
                    active = active_routes(routes)
                    idle_count = num_vehicles - len(active)

                    # ── KPI Strip ────────────────────────────────────────────
                    k1, k2, k3, k4 = st.columns(4)
                    for col, val, label in [
                        (k1, result["total_distance"], "Total Distance"),
                        (k2, len(active), "Active Vehicles"),
                        (k3, n - 1, "Nodes Served"),
                        (k4, idle_count, "Idle Vehicles"),
                    ]:
                        col.markdown(
                            f"<div class='metric-card'>"
                            f"<div class='metric-value'>{val}</div>"
                            f"<div class='metric-label'>{label}</div>"
                            f"</div>",
                            unsafe_allow_html=True,
                        )

                    st.markdown("<br>", unsafe_allow_html=True)

                    # ── Tabs: Routes / Raw ───────────────────────────────────
                    tab_routes, tab_raw = st.tabs(["🗺 Routes", "📋 Raw Data"])

                    with tab_routes:
                        if not active:
                            st.info("All vehicles returned without serving any node.")
                        for r in active:
                            load_pct = int(r["load"] / vehicle_capacity * 100)
                            cap_color = (
                                "#22c55e" if load_pct < 70
                                else "#f59e0b" if load_pct < 90
                                else "#ef4444"
                            )
                            path = format_route_path(r["nodes"])
                            st.markdown(
                                f"""
                                <div class='route-card'>
                                    <div class='vehicle-header'>Vehicle {r['vehicle_id']}</div>
                                    <div class='route-path'>{path}</div>
                                    <div class='route-meta'>
                                        <span class='badge'>Dist: {r['distance']}</span>
                                        <span class='badge'>Load: {r['load']}/{vehicle_capacity}</span>
                                        <span style='color:{cap_color};font-size:0.75rem;
                                                     font-family:"IBM Plex Mono",monospace;'>
                                            ▪ {load_pct}% capacity
                                        </span>
                                    </div>
                                </div>
                                """,
                                unsafe_allow_html=True,
                            )

                        if idle_count:
                            st.markdown(
                                f"<div style='font-size:0.8rem;color:#475569;margin-top:0.5rem;'>"
                                f"ℹ️ {idle_count} vehicle(s) were not needed.</div>",
                                unsafe_allow_html=True,
                            )

                    with tab_raw:
                        import json
                        raw_data = {
                            "status": result["status"],
                            "total_distance": result["total_distance"],
                            "num_vehicles": num_vehicles,
                            "vehicle_capacity": vehicle_capacity,
                            "routes": [
                                {
                                    "vehicle": r["vehicle_id"],
                                    "path": r["nodes"],
                                    "distance": r["distance"],
                                    "load": r["load"],
                                }
                                for r in active
                            ],
                        }
                        st.code(json.dumps(raw_data, indent=2), language="json")
                        st.download_button(
                            "⬇️ Download JSON",
                            data=json.dumps(raw_data, indent=2),
                            file_name="vrp_solution.json",
                            mime="application/json",
                        )

            except ValueError as e:
                st.error(f"⚠️ Validation Error: {e}")
            except ImportError:
                st.error(
                    "❌ OR-Tools not installed. Run: `pip install ortools`"
                )
            except Exception as e:
                st.error(f"❌ Unexpected error: {e}")

    else:
        st.markdown("""
        <div style='text-align:center;padding:3rem 1rem;'>
            <div style='font-size:3rem;margin-bottom:1rem;'>🗺️</div>
            <div style='font-size:0.95rem;color:#334155;font-weight:500;'>
                Configure your inputs and click <b style='color:#3b82f6'>Solve VRP</b>
            </div>
            <div style='font-size:0.8rem;color:#1e2a3a;margin-top:0.5rem;'>
                Results will appear here
            </div>
        </div>
        """, unsafe_allow_html=True)


# ─── Footer ───────────────────────────────────────────────────────────────────
st.markdown("<br><br>", unsafe_allow_html=True)
st.divider()
st.markdown("""
<div style='text-align:center;font-size:0.72rem;color:#1e2a3a;padding:0.5rem 0;'>
    VRP Solver · Google OR-Tools · PATH_CHEAPEST_ARC Strategy
</div>
""", unsafe_allow_html=True)
