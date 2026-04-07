"""
AI Supply Chain Solutions
Clarke–Wright Savings Algorithm + Time Windows + Priority + Multi-Depot VRP

Developed by Zillay Husnain Jatoi
Run: streamlit run app.py
"""

import re
import math
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="AI Supply Chain Solutions",
    page_icon="⬡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ═══════════════════════════════════════════════════════════════════════════════
#  DESIGN SYSTEM — Obsidian × Acid-Lime
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=DM+Mono:wght@400;500&family=Bebas+Neue&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [class*="css"] {
    font-family: 'Space Grotesk', sans-serif;
    background: #0a0a0f !important;
    color: #e8e6e0 !important;
}

.stApp {
    background: #0a0a0f !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 4px; height: 4px; }
::-webkit-scrollbar-track { background: #111118; }
::-webkit-scrollbar-thumb { background: #c8f135; border-radius: 2px; }

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: #06060a !important;
    border-right: 1px solid #1a1a28 !important;
    width: 340px !important;
}
section[data-testid="stSidebar"] > div { padding-top: 0 !important; }
section[data-testid="stSidebar"] * { color: #b8b5ae !important; }
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3,
section[data-testid="stSidebar"] h4 { color: #e8e6e0 !important; }

section[data-testid="stSidebar"] .stTextArea textarea,
section[data-testid="stSidebar"] .stNumberInput input,
section[data-testid="stSidebar"] .stTextInput input {
    background: #0e0e16 !important;
    border: 1px solid #1e1e30 !important;
    color: #c8f135 !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.78rem !important;
    border-radius: 6px !important;
    transition: border-color 0.2s !important;
}
section[data-testid="stSidebar"] .stTextArea textarea:focus,
section[data-testid="stSidebar"] .stNumberInput input:focus,
section[data-testid="stSidebar"] .stTextInput input:focus {
    border-color: #c8f135 !important;
    box-shadow: 0 0 0 2px rgba(200,241,53,0.1) !important;
}
section[data-testid="stSidebar"] label {
    font-size: 0.65rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.14em !important;
    text-transform: uppercase !important;
    color: #454550 !important;
}
section[data-testid="stSidebar"] .stSelectbox select,
section[data-testid="stSidebar"] [data-baseweb="select"] {
    background: #0e0e16 !important;
    border-color: #1e1e30 !important;
    color: #c8f135 !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.78rem !important;
}
section[data-testid="stSidebar"] [data-baseweb="select"] * {
    background: #0e0e16 !important;
    color: #c8f135 !important;
}
section[data-testid="stSidebar"] .stCheckbox label {
    font-size: 0.75rem !important;
    text-transform: none !important;
    letter-spacing: 0 !important;
    color: #888 !important;
}

/* ── Buttons ── */
.stButton > button {
    background: #c8f135 !important;
    color: #0a0a0f !important;
    border: none !important;
    border-radius: 6px !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.8rem !important;
    padding: 0.55rem 1.2rem !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    transition: all 0.15s !important;
    width: 100% !important;
}
.stButton > button:hover {
    background: #d8ff45 !important;
    transform: translateY(-1px) !important;
}
.stButton > button:active {
    transform: translateY(0) !important;
    background: #a8d120 !important;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: transparent !important;
    border-bottom: 1px solid #1a1a28 !important;
    gap: 0 !important;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: #454550 !important;
    border: none !important;
    border-bottom: 2px solid transparent !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 0.72rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    padding: 0.6rem 1.2rem !important;
    transition: all 0.2s !important;
}
.stTabs [data-baseweb="tab"]:hover { color: #888 !important; }
.stTabs [aria-selected="true"] {
    color: #c8f135 !important;
    border-bottom-color: #c8f135 !important;
}
.stTabs [data-baseweb="tab-panel"] { padding: 0 !important; }

/* ── Expander ── */
.streamlit-expanderHeader {
    background: #0e0e16 !important;
    border: 1px solid #1a1a28 !important;
    border-radius: 6px !important;
    font-size: 0.78rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.06em !important;
    color: #888 !important;
}
.streamlit-expanderContent {
    background: #0e0e16 !important;
    border: 1px solid #1a1a28 !important;
    border-top: none !important;
    border-radius: 0 0 6px 6px !important;
}

/* ── Dataframe ── */
.stDataFrame {
    border-radius: 8px !important;
    overflow: hidden !important;
    border: 1px solid #1a1a28 !important;
}
.stDataFrame thead tr th {
    background: #0e0e16 !important;
    color: #c8f135 !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.7rem !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
    border-bottom: 1px solid #1a1a28 !important;
}
.stDataFrame tbody tr td {
    background: #06060a !important;
    color: #888 !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.75rem !important;
    border-bottom: 1px solid #111118 !important;
}
.stDataFrame tbody tr:hover td {
    background: #0e0e16 !important;
    color: #e8e6e0 !important;
}

/* ── Divider ── */
hr { border-color: #1a1a28 !important; }

/* ── Spinner ── */
.stSpinner > div { border-top-color: #c8f135 !important; }

/* ── Alert / Error ── */
.stAlert { background: #1a0a0a !important; border-color: #ff4444 !important; border-radius: 6px !important; }

/* ── Radio ── */
.stRadio label { font-size: 0.78rem !important; }
</style>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
#  CORE ALGORITHM
# ═══════════════════════════════════════════════════════════════════════════════

def parse_matrix(raw: str):
    raw = raw.strip()
    if not raw:
        raise ValueError("Distance matrix is empty.")
    matrix = []
    for line_no, line in enumerate(raw.splitlines(), 1):
        line = line.strip()
        if not line:
            continue
        parts = re.split(r"[,\s]+", line.replace(",", " "))
        parts = [p for p in parts if p]
        try:
            row = [float(p) for p in parts]
        except ValueError:
            raise ValueError(f"Row {line_no}: non-numeric value — '{line}'")
        if any(v < 0 for v in row):
            raise ValueError(f"Row {line_no}: negative distances not allowed.")
        matrix.append(row)
    if not matrix:
        raise ValueError("No rows parsed.")
    n = len(matrix)
    for i, row in enumerate(matrix, 1):
        if len(row) != n:
            raise ValueError(f"Matrix not square: row {i} has {len(row)} values, expected {n}.")
    return matrix


def parse_demands(raw: str, expected: int):
    raw = raw.strip()
    if not raw:
        raise ValueError("Demands field is empty.")
    parts = re.split(r"[,\s]+", raw.replace(",", " "))
    parts = [p for p in parts if p]
    try:
        demands = [float(p) for p in parts]
    except ValueError:
        raise ValueError("Demands contain non-numeric values.")
    if len(demands) != expected:
        raise ValueError(f"Demands length ({len(demands)}) ≠ nodes ({expected}).")
    if demands[0] != 0:
        raise ValueError(f"Depot demand (index 0) must be 0, got {demands[0]}.")
    if any(d < 0 for d in demands[1:]):
        raise ValueError("All customer demands must be ≥ 0.")
    return demands


def parse_time_windows(raw: str, expected: int):
    """Parse time windows as: early,late pairs per node separated by semicolons or newlines"""
    if not raw.strip():
        return None
    lines = re.split(r"[;\n]+", raw.strip())
    windows = []
    for ln in lines:
        ln = ln.strip()
        if not ln:
            continue
        parts = re.split(r"[,\s]+", ln)
        parts = [p for p in parts if p]
        if len(parts) != 2:
            raise ValueError(f"Each time window must be 'early,late'. Got: '{ln}'")
        try:
            e, l = float(parts[0]), float(parts[1])
        except ValueError:
            raise ValueError(f"Non-numeric time window: '{ln}'")
        if e > l:
            raise ValueError(f"Early time {e} > late time {l} for window '{ln}'")
        windows.append((e, l))
    if len(windows) != expected:
        raise ValueError(f"Time windows count ({len(windows)}) ≠ nodes ({expected}). Include depot as first entry (e.g. 0,999).")
    return windows


def parse_service_times(raw: str, expected: int):
    if not raw.strip():
        return [0.0] * expected
    parts = re.split(r"[,\s]+", raw.strip().replace(",", " "))
    parts = [p for p in parts if p]
    try:
        st_list = [float(p) for p in parts]
    except ValueError:
        raise ValueError("Service times contain non-numeric values.")
    if len(st_list) != expected:
        raise ValueError(f"Service times count ({len(st_list)}) ≠ nodes ({expected}).")
    return st_list


def parse_priorities(raw: str, expected_customers: int):
    if not raw.strip():
        return [1] * expected_customers
    parts = re.split(r"[,\s]+", raw.strip().replace(",", " "))
    parts = [p for p in parts if p]
    try:
        pr = [int(p) for p in parts]
    except ValueError:
        raise ValueError("Priorities contain non-integer values.")
    if len(pr) != expected_customers:
        raise ValueError(f"Priorities count ({len(pr)}) ≠ customers ({expected_customers}).")
    if any(p not in [1, 2, 3] for p in pr):
        raise ValueError("Priorities must be 1 (low), 2 (medium), or 3 (high).")
    return pr


def calculate_cost(routes, dist):
    total = 0.0
    for route in routes:
        for k in range(len(route) - 1):
            total += dist[route[k]][route[k + 1]]
    return total


def compute_route_time(route, dist, service_times):
    """Returns list of arrival times at each node (excluding initial depot)"""
    time = 0.0
    arrivals = [0.0]
    for k in range(len(route) - 1):
        travel = dist[route[k]][route[k + 1]]
        svc = service_times[route[k]] if k > 0 else 0.0
        time += travel + svc
        arrivals.append(time)
    return arrivals


def check_time_windows(route, dist, service_times, time_windows):
    """Returns (feasible, violations_list)"""
    if time_windows is None:
        return True, []
    violations = []
    time = 0.0
    for k in range(len(route) - 1):
        if k > 0:
            time += service_times[route[k - 1]]
        time += dist[route[k]][route[k + 1]]
        node = route[k + 1]
        if node == 0:
            continue
        e, l = time_windows[node]
        if time < e:
            time = e  # wait (allowed)
        elif time > l:
            violations.append(f"Node {node}: arrive {time:.1f} > deadline {l}")
    return len(violations) == 0, violations


def compute_savings(dist, n, priorities=None, alpha=0.5):
    """Enhanced savings with optional priority weighting"""
    savings = []
    for i in range(1, n):
        for j in range(i + 1, n):
            base_s = dist[0][i] + dist[0][j] - dist[i][j]
            # Priority boost: higher priority pairs get weighted savings
            if priorities:
                pi = priorities[i - 1]
                pj = priorities[j - 1]
                priority_factor = 1.0 + alpha * (pi + pj - 2) / 4.0
            else:
                priority_factor = 1.0
            weighted_s = base_s * priority_factor
            savings.append({
                "i": i, "j": j,
                "S(i,j)_base": round(base_s, 3),
                "Priority Factor": round(priority_factor, 3),
                "S(i,j)_weighted": round(weighted_s, 3),
                "d(0,i)": dist[0][i], "d(0,j)": dist[0][j], "d(i,j)": dist[i][j],
            })
    savings.sort(key=lambda x: x["S(i,j)_weighted"], reverse=True)
    return savings


def apply_merges(initial_routes, savings, demands, capacity, dist,
                 time_windows, service_times, max_route_time, enable_tw):
    routes = [r[:] for r in initial_routes]
    log = []

    def find_route_idx(node):
        for idx, r in enumerate(routes):
            if node in r[1:-1]:
                return idx
        return None

    def is_endpoint(node, route):
        inner = route[1:-1]
        return bool(inner) and (inner[0] == node or inner[-1] == node)

    def route_demand(route):
        return sum(demands[nd] for nd in route[1:-1])

    def route_travel_time(route):
        t = 0.0
        for k in range(len(route) - 1):
            t += dist[route[k]][route[k + 1]]
            if k > 0:
                t += service_times[route[k]]
        return t

    def snapshot():
        return [r[:] for r in routes]

    for s in savings:
        i, j = s["i"], s["j"]
        sval = s["S(i,j)_weighted"]
        pair_label = f"S({i},{j}) = {sval:.2f}"

        ri_idx = find_route_idx(i)
        rj_idx = find_route_idx(j)

        if ri_idx is None or rj_idx is None:
            missing = i if ri_idx is None else j
            log.append({"pair": pair_label, "saving": sval, "allowed": False,
                        "reason": f"Node {missing} not found in any active route.",
                        "routes_after": snapshot()})
            continue

        ri = routes[ri_idx]
        rj = routes[rj_idx]

        if ri_idx == rj_idx:
            log.append({"pair": pair_label, "saving": sval, "allowed": False,
                        "reason": f"Nodes {i} and {j} already on same route.",
                        "routes_after": snapshot()})
            continue

        if not is_endpoint(i, ri) or not is_endpoint(j, rj):
            bad = []
            if not is_endpoint(i, ri): bad.append(f"node {i} not an endpoint")
            if not is_endpoint(j, rj): bad.append(f"node {j} not an endpoint")
            log.append({"pair": pair_label, "saving": sval, "allowed": False,
                        "reason": "Endpoint check failed: " + "; ".join(bad) + ".",
                        "routes_after": snapshot()})
            continue

        di = route_demand(ri)
        dj = route_demand(rj)
        combined = di + dj
        if combined > capacity:
            log.append({"pair": pair_label, "saving": sval, "allowed": False,
                        "reason": f"Capacity exceeded: {di:.1f} + {dj:.1f} = {combined:.1f} > {capacity}.",
                        "routes_after": snapshot()})
            continue

        # Orient and build candidate merge
        ri_inner = ri[1:-1]
        if ri_inner[-1] != i:
            ri_inner = ri_inner[::-1]
        rj_inner = rj[1:-1]
        if rj_inner[0] != j:
            rj_inner = rj_inner[::-1]
        merged = [0] + ri_inner + rj_inner + [0]

        # Max route duration check
        if max_route_time > 0:
            rt = route_travel_time(merged)
            if rt > max_route_time:
                log.append({"pair": pair_label, "saving": sval, "allowed": False,
                            "reason": f"Route duration exceeded: {rt:.1f} > {max_route_time}.",
                            "routes_after": snapshot()})
                continue

        # Time window feasibility check
        if enable_tw and time_windows is not None:
            feasible, violations = check_time_windows(merged, dist, service_times, time_windows)
            if not feasible:
                log.append({"pair": pair_label, "saving": sval, "allowed": False,
                            "reason": "Time window violation: " + "; ".join(violations[:2]) + ".",
                            "routes_after": snapshot()})
                continue

        for idx in sorted([ri_idx, rj_idx], reverse=True):
            routes.pop(idx)
        routes.append(merged)

        log.append({"pair": pair_label, "saving": sval, "allowed": True,
                    "reason": f"Merged: demand {di:.1f}+{dj:.1f}={combined:.1f} ≤ {capacity}.",
                    "routes_after": snapshot()})

    return routes, log


def run_solver(matrix, demands, capacity, time_windows, service_times,
               priorities, max_route_time, enable_tw, priority_alpha):
    n = len(matrix)
    initial_routes = [[0, c, 0] for c in range(1, n)]
    initial_cost = calculate_cost(initial_routes, matrix)
    savings = compute_savings(matrix, n, priorities if priorities else None, priority_alpha)
    final_routes, merge_log = apply_merges(
        initial_routes, savings, demands, capacity, matrix,
        time_windows, service_times, max_route_time, enable_tw
    )
    final_cost = calculate_cost(final_routes, matrix)

    # Compute per-route analytics
    route_analytics = []
    for route in final_routes:
        if len(route) <= 2:
            continue
        cost_r = sum(matrix[route[k]][route[k+1]] for k in range(len(route)-1))
        demand_r = sum(demands[nd] for nd in route[1:-1])
        travel_time = sum(matrix[route[k]][route[k+1]] for k in range(len(route)-1))
        service_time_total = sum(service_times[nd] for nd in route[1:-1])

        # Time window compliance
        tw_status = "N/A"
        if enable_tw and time_windows:
            feasible, viols = check_time_windows(route, matrix, service_times, time_windows)
            tw_status = "✓ OK" if feasible else f"⚠ {len(viols)} violation(s)"

        # Arrival times
        arrivals = {}
        t = 0.0
        for k in range(1, len(route) - 1):
            t += matrix[route[k-1]][route[k]]
            if k > 1:
                t += service_times[route[k-1]]
            node = route[k]
            arrivals[node] = round(t, 2)
            if time_windows:
                e, l = time_windows[node]
                if t < e:
                    t = e

        route_analytics.append({
            "route": route,
            "cost": cost_r,
            "demand": demand_r,
            "travel_time": travel_time,
            "service_time": service_time_total,
            "total_time": travel_time + service_time_total,
            "utilisation": demand_r / capacity * 100,
            "tw_status": tw_status,
            "arrivals": arrivals,
        })

    return {
        "n": n,
        "initial_routes": initial_routes,
        "initial_cost": initial_cost,
        "savings": savings,
        "merge_log": merge_log,
        "final_routes": final_routes,
        "final_cost": final_cost,
        "total_savings": initial_cost - final_cost,
        "demands": demands,
        "matrix": matrix,
        "capacity": capacity,
        "time_windows": time_windows,
        "service_times": service_times,
        "priorities": priorities,
        "route_analytics": route_analytics,
    }


# ═══════════════════════════════════════════════════════════════════════════════
#  UI COMPONENTS
# ═══════════════════════════════════════════════════════════════════════════════

def render_header():
    st.markdown("""
    <div style="border-bottom: 1px solid #1a1a28; padding: 1.8rem 0 1.4rem 0; margin-bottom: 0;">
        <div style="display:flex; align-items:flex-end; gap: 1.2rem; flex-wrap:wrap;">
            <div>
                <div style="font-family:'Bebas Neue',sans-serif; font-size:2.6rem;
                            color:#e8e6e0; letter-spacing:0.06em; line-height:1;">
                    AI SUPPLY CHAIN
                    <span style="color:#c8f135;">SOLUTIONS</span>
                </div>
                <div style="font-size:0.68rem; color:#454550; letter-spacing:0.22em;
                            text-transform:uppercase; margin-top:0.3rem;">
                    Clarke–Wright Savings · CVRPTW · Priority Routing · Advanced Analytics
                </div>
            </div>
            <div style="margin-left:auto; text-align:right; padding-bottom:0.15rem;">
                <div style="font-size:0.62rem; color:#2e2e3a; letter-spacing:0.18em; text-transform:uppercase;">Developed by</div>
                <div style="font-size:0.85rem; color:#454550; font-weight:600; letter-spacing:0.04em;">Zillay Husnain Jatoi</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def kpi_strip(R, active_final, merges_allowed, merges_rejected):
    pct = (R["total_savings"] / R["initial_cost"] * 100) if R["initial_cost"] else 0
    avg_util = sum(ra["utilisation"] for ra in R["route_analytics"]) / len(R["route_analytics"]) if R["route_analytics"] else 0
    kpis = [
        ("#c8f135", f"{R['initial_cost']:.1f}", "INITIAL DIST"),
        ("#39e5b6", f"{R['final_cost']:.1f}", "OPTIMISED DIST"),
        ("#c8f135", f"{pct:.1f}%", "SAVINGS %"),
        ("#ff6b6b", f"{len(active_final)}", "VEHICLES USED"),
        ("#a78bfa", f"{merges_allowed}", "MERGES DONE"),
        ("#888", f"{merges_rejected}", "MERGES SKIPPED"),
        ("#f59e0b", f"{avg_util:.0f}%", "AVG UTILISATION"),
    ]
    cols = st.columns(len(kpis))
    for col, (color, val, label) in zip(cols, kpis):
        col.markdown(
            f"<div style='background:#06060a;border:1px solid #1a1a28;border-top:2px solid {color};"
            f"border-radius:0 0 6px 6px;padding:1rem 0.8rem;text-align:center;'>"
            f"<div style='font-family:\"DM Mono\",monospace;font-size:1.6rem;font-weight:500;color:{color};line-height:1;'>{val}</div>"
            f"<div style='font-size:0.58rem;font-weight:600;letter-spacing:0.16em;color:#2e2e3a;"
            f"text-transform:uppercase;margin-top:0.4rem;'>{label}</div>"
            f"</div>",
            unsafe_allow_html=True,
        )


def step_header(num, icon, title):
    st.markdown(
        f"<div style='display:flex;align-items:center;gap:0.7rem;margin:2rem 0 1rem 0;"
        f"padding-bottom:0.6rem;border-bottom:1px solid #1a1a28;'>"
        f"<span style='font-family:\"DM Mono\",monospace;font-size:0.62rem;font-weight:500;"
        f"color:#c8f135;background:#0e1a00;border:1px solid #2a3a00;border-radius:4px;"
        f"padding:0.2rem 0.5rem;letter-spacing:0.1em;'>STEP {num}</span>"
        f"<span style='font-size:0.95rem;font-weight:600;color:#e8e6e0;letter-spacing:0.02em;'>{icon} {title}</span>"
        f"</div>",
        unsafe_allow_html=True,
    )


VEHICLE_COLORS = ["#c8f135", "#39e5b6", "#a78bfa", "#f59e0b", "#ff6b6b", "#60cdff", "#ff9ff3", "#ffd43b"]

def route_card(ra, vehicle_num, demands, time_windows, show_tw):
    route = ra["route"]
    color = VEHICLE_COLORS[(vehicle_num - 1) % len(VEHICLE_COLORS)]
    path = " → ".join(str(x) for x in route)
    util_bar = min(ra["utilisation"], 100)

    tw_block = ""
    if show_tw and time_windows and ra["arrivals"]:
        arr_parts = []
        for node, t in ra["arrivals"].items():
            e, l = time_windows[node]
            ok = "✓" if e <= t <= l else "⚠"
            arr_parts.append(f"N{node}:{t:.0f}[{e:.0f}-{l:.0f}]{ok}")
        tw_block = (
            f"<div style='margin-top:0.6rem;font-family:\"DM Mono\",monospace;"
            f"font-size:0.65rem;color:#454550;line-height:1.8;'>"
            + "  ".join(arr_parts[:8]) + ("…" if len(arr_parts) > 8 else "") +
            f"</div>"
        )

    st.markdown(
        f"<div style='background:#06060a;border:1px solid #1a1a28;"
        f"border-left:3px solid {color};border-radius:0 6px 6px 0;padding:1rem 1.2rem;"
        f"margin-bottom:0.7rem;'>"
        f"<div style='font-size:0.6rem;font-weight:600;letter-spacing:0.18em;"
        f"text-transform:uppercase;color:{color};margin-bottom:0.4rem;'>Vehicle {vehicle_num}</div>"
        f"<div style='font-family:\"DM Mono\",monospace;font-size:0.9rem;color:#e8e6e0;"
        f"word-break:break-all;'>{path}</div>"
        f"<div style='margin-top:0.7rem;background:#0e0e16;border-radius:2px;height:3px;overflow:hidden;'>"
        f"<div style='background:{color};width:{util_bar:.1f}%;height:100%;'></div></div>"
        f"<div style='display:flex;gap:1.2rem;margin-top:0.5rem;'>"
        f"<span style='font-size:0.68rem;color:#454550;'>Cost <span style='color:{color};font-family:\"DM Mono\",monospace;'>{ra['cost']:.1f}</span></span>"
        f"<span style='font-size:0.68rem;color:#454550;'>Load <span style='color:{color};font-family:\"DM Mono\",monospace;'>{ra['demand']:.0f}</span></span>"
        f"<span style='font-size:0.68rem;color:#454550;'>Util <span style='color:{color};font-family:\"DM Mono\",monospace;'>{ra['utilisation']:.0f}%</span></span>"
        f"<span style='font-size:0.68rem;color:#454550;'>Time <span style='color:{color};font-family:\"DM Mono\",monospace;'>{ra['total_time']:.1f}</span></span>"
        f"{'<span style=\"font-size:0.68rem;color:#454550;\">TW <span style=\"color:#39e5b6;font-family:DM Mono,monospace;\">' + ra['tw_status'] + '</span></span>' if show_tw else ''}"
        f"</div>"
        f"{tw_block}"
        f"</div>",
        unsafe_allow_html=True,
    )


def merge_row(entry, idx):
    icon = "✓" if entry["allowed"] else "✗"
    color = "#c8f135" if entry["allowed"] else "#ff4444"
    bg = "#0a1400" if entry["allowed"] else "#1a0000"
    label = "MERGED" if entry["allowed"] else "SKIPPED"
    st.markdown(
        f"<div style='background:{bg};border:1px solid {'#1a2800' if entry['allowed'] else '#2a0000'};"
        f"border-radius:6px;padding:0.65rem 1rem;margin-bottom:0.4rem;"
        f"display:flex;align-items:flex-start;gap:0.7rem;'>"
        f"<span style='font-family:\"DM Mono\",monospace;font-size:0.7rem;color:{color};"
        f"font-weight:600;min-width:14px;margin-top:1px;'>{icon}</span>"
        f"<div style='flex:1;'>"
        f"<div style='display:flex;align-items:center;gap:0.6rem;'>"
        f"<span style='font-family:\"DM Mono\",monospace;font-size:0.8rem;color:#e8e6e0;font-weight:500;'>#{idx} {entry['pair']}</span>"
        f"<span style='font-size:0.6rem;letter-spacing:0.12em;text-transform:uppercase;"
        f"color:{color};background:{'#0a1400' if entry['allowed'] else '#1a0000'};"
        f"border:1px solid {color};border-radius:3px;padding:0.1rem 0.4rem;'>{label}</span>"
        f"</div>"
        f"<div style='font-size:0.72rem;color:#454550;margin-top:0.2rem;'>{entry['reason']}</div>"
        f"</div></div>",
        unsafe_allow_html=True,
    )


# ═══════════════════════════════════════════════════════════════════════════════
#  SIDEBAR
# ═══════════════════════════════════════════════════════════════════════════════

EXAMPLE_MATRIX = (
    "0,10,8,7,12,15,9\n"
    "10,0,5,6,11,13,7\n"
    "8,5,0,3,9,10,4\n"
    "7,6,3,0,4,8,5\n"
    "12,11,9,4,0,6,10\n"
    "15,13,10,8,6,0,7\n"
    "9,7,4,5,10,7,0"
)
EXAMPLE_DEMANDS = "0,4,6,5,7,3,8"
EXAMPLE_TW = "0,999\n0,25\n5,35\n0,20\n10,40\n8,45\n0,30"
EXAMPLE_SERVICE = "0,2,3,2,4,2,3"
EXAMPLE_PRIORITY = "2,3,1,3,2,1"

with st.sidebar:
    st.markdown("""
    <div style='padding:1.5rem 0 1rem 0;border-bottom:1px solid #1a1a28;margin-bottom:1rem;'>
        <div style='font-family:"Bebas Neue",sans-serif;font-size:1.1rem;color:#e8e6e0;
                    letter-spacing:0.12em;'>⬡ SOLVER CONFIG</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div style='font-size:0.65rem;color:#2e2e3a;letter-spacing:0.16em;text-transform:uppercase;margin-bottom:0.4rem;'>Core Inputs</div>", unsafe_allow_html=True)

    matrix_raw  = st.text_area("Distance Matrix", value=EXAMPLE_MATRIX, height=140,
                                help="Square matrix. Rows separated by newlines, values by commas or spaces.")
    demands_raw = st.text_area("Node Demands (depot first = 0)", value=EXAMPLE_DEMANDS, height=55)
    capacity    = st.number_input("Vehicle Capacity", min_value=1, max_value=100_000, value=20, step=1)

    st.markdown("<div style='height:0.8rem'></div>", unsafe_allow_html=True)
    st.markdown("<div style='font-size:0.65rem;color:#2e2e3a;letter-spacing:0.16em;text-transform:uppercase;margin-bottom:0.4rem;'>Advanced Constraints</div>", unsafe_allow_html=True)

    enable_tw = st.checkbox("Enable Time Windows (VRPTW)", value=True)
    tw_raw = st.text_area("Time Windows (early,late per node)", value=EXAMPLE_TW, height=120,
                           help="One 'early,late' pair per line (or semicolon-separated). First line = depot.", disabled=not enable_tw)

    enable_service = st.checkbox("Enable Service Times", value=True)
    service_raw = st.text_area("Service Times (per node)", value=EXAMPLE_SERVICE, height=55,
                                help="Time spent servicing each node. First = depot (usually 0).", disabled=not enable_service)

    max_route_time = st.number_input("Max Route Duration (0 = unlimited)", min_value=0.0, max_value=9999.0, value=0.0, step=1.0)

    enable_priority = st.checkbox("Enable Priority Routing", value=True)
    priority_raw = st.text_area("Customer Priorities (1=low, 2=med, 3=high)", value=EXAMPLE_PRIORITY, height=55,
                                  help="One value per customer (not depot). 1=low, 2=medium, 3=high.", disabled=not enable_priority)
    priority_alpha = st.slider("Priority Weight α", min_value=0.0, max_value=2.0, value=0.5, step=0.1,
                                help="How strongly priorities bias the savings ranking.") if enable_priority else 0.5

    st.markdown("<div style='height:0.8rem'></div>", unsafe_allow_html=True)
    col_s, col_r = st.columns(2)
    solve_btn = col_s.button("▶ SOLVE")
    reset_btn = col_r.button("↺ RESET")

    st.markdown("""
    <div style='margin-top:1.5rem;padding:1rem;background:#06060a;border:1px solid #1a1a28;border-radius:6px;
                font-size:0.65rem;color:#2e2e3a;line-height:2;'>
        <div style='color:#454550;font-weight:600;margin-bottom:0.4rem;letter-spacing:0.1em;'>ALGORITHM</div>
        Clarke–Wright Parallel Savings<br>
        <span style='color:#c8f135'>S(i,j)</span> = d(0,i) + d(0,j) − d(i,j)<br><br>
        <div style='color:#454550;font-weight:600;margin-bottom:0.4rem;letter-spacing:0.1em;'>CONSTRAINTS</div>
        ① Capacity (CVRP)<br>
        ② Time Windows (VRPTW)<br>
        ③ Max Route Duration<br>
        ④ Priority Weighting<br>
        ⑤ Service Times
    </div>
    """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
#  SESSION STATE
# ═══════════════════════════════════════════════════════════════════════════════

if "result" not in st.session_state:
    st.session_state.result = None
if "error" not in st.session_state:
    st.session_state.error = None

if reset_btn:
    st.session_state.result = None
    st.session_state.error = None
    st.rerun()

if solve_btn:
    st.session_state.result = None
    st.session_state.error = None
    with st.spinner("Optimising routes..."):
        try:
            matrix  = parse_matrix(matrix_raw)
            n = len(matrix)
            demands = parse_demands(demands_raw, n)

            # Time windows
            time_windows = None
            if enable_tw:
                time_windows = parse_time_windows(tw_raw, n)

            # Service times
            service_times = [0.0] * n
            if enable_service:
                service_times = parse_service_times(service_raw, n)

            # Priorities
            priorities = None
            if enable_priority:
                priorities = parse_priorities(priority_raw, n - 1)

            max_cust_demand = max(demands[1:]) if len(demands) > 1 else 0
            if capacity < max_cust_demand:
                raise ValueError(
                    f"Vehicle capacity ({capacity}) < largest customer demand ({max_cust_demand})."
                )

            st.session_state.result = run_solver(
                matrix, demands, capacity, time_windows, service_times,
                priorities, max_route_time, enable_tw, priority_alpha
            )
        except Exception as e:
            st.session_state.error = str(e)


# ═══════════════════════════════════════════════════════════════════════════════
#  MAIN PANEL
# ═══════════════════════════════════════════════════════════════════════════════

render_header()

if st.session_state.error:
    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
    st.error(f"⚠ {st.session_state.error}")

if st.session_state.result is None and not st.session_state.error:
    st.markdown("""
    <div style='text-align:center;padding:5rem 1rem;'>
        <div style='font-family:"Bebas Neue",sans-serif;font-size:4rem;color:#1a1a28;
                    letter-spacing:0.1em;line-height:1;'>AWAITING INPUT</div>
        <div style='font-size:0.82rem;color:#2e2e3a;margin-top:1rem;max-width:400px;margin-left:auto;margin-right:auto;'>
            Configure your distance matrix, demands, and constraints in the sidebar.
            A 7-node example is pre-loaded and ready to solve.
        </div>
        <div style='margin-top:2rem;display:flex;justify-content:center;gap:2rem;flex-wrap:wrap;'>
            <div style='font-size:0.68rem;color:#2e2e3a;letter-spacing:0.12em;'>⬡ CAPACITATED VRP</div>
            <div style='font-size:0.68rem;color:#2e2e3a;letter-spacing:0.12em;'>⬡ TIME WINDOWS</div>
            <div style='font-size:0.68rem;color:#2e2e3a;letter-spacing:0.12em;'>⬡ PRIORITY ROUTING</div>
            <div style='font-size:0.68rem;color:#2e2e3a;letter-spacing:0.12em;'>⬡ SERVICE TIMES</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
#  RESULTS
# ═══════════════════════════════════════════════════════════════════════════════

if st.session_state.result:
    R = st.session_state.result
    dist      = R["matrix"]
    demands   = R["demands"]
    capacity  = R["capacity"]
    n         = R["n"]
    tw        = R["time_windows"]
    svc       = R["service_times"]
    pri       = R["priorities"]

    active_final    = [r for r in R["final_routes"] if len(r) > 2]
    merges_allowed  = sum(1 for m in R["merge_log"] if m["allowed"])
    merges_rejected = sum(1 for m in R["merge_log"] if not m["allowed"])

    st.markdown("<div style='height:1.5rem'></div>", unsafe_allow_html=True)
    kpi_strip(R, active_final, merges_allowed, merges_rejected)
    st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

    # ── TABS ──────────────────────────────────────────────────────────────────
    tabs = st.tabs([
        "STEP-BY-STEP SOLUTION",
        "FINAL ROUTES",
        "ANALYTICS",
        "MERGE LOG",
        "DATA INPUTS",
    ])

    # ── TAB 1: Step-by-Step ───────────────────────────────────────────────────
    with tabs[0]:
        st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

        # STEP 1: Initial Routes
        step_header(1, "📍", "Initial Routes — One Vehicle Per Customer")
        st.markdown(
            "<div style='font-size:0.78rem;color:#454550;margin-bottom:1rem;'>"
            "Each customer starts on its own route <span style='font-family:\"DM Mono\",monospace;"
            "color:#c8f135;'>0 → i → 0</span>. These are the baseline before any merges.</div>",
            unsafe_allow_html=True
        )
        col_a, col_b = st.columns(2)
        for k, route in enumerate(R["initial_routes"]):
            cost_r = dist[route[0]][route[1]] + dist[route[1]][route[2]]
            color = VEHICLE_COLORS[k % len(VEHICLE_COLORS)]
            with (col_a if k % 2 == 0 else col_b):
                st.markdown(
                    f"<div style='background:#06060a;border:1px solid #1a1a28;"
                    f"border-left:3px solid {color};border-radius:0 6px 6px 0;"
                    f"padding:0.7rem 1rem;margin-bottom:0.5rem;'>"
                    f"<div style='font-family:\"DM Mono\",monospace;font-size:0.82rem;"
                    f"color:#e8e6e0;'>0 → {route[1]} → 0</div>"
                    f"<div style='font-size:0.65rem;color:#2e2e3a;margin-top:0.25rem;'>"
                    f"Cost: <span style='color:{color};'>{cost_r:.1f}</span> &nbsp;·&nbsp; "
                    f"Demand: <span style='color:{color};'>{demands[route[1]]:.0f}</span>"
                    f"{'&nbsp;·&nbsp; Priority: <span style=\"color:' + color + ';\">' + str(pri[route[1]-1]) + '</span>' if pri else ''}"
                    f"</div></div>",
                    unsafe_allow_html=True
                )
        st.markdown(
            f"<div style='font-size:0.75rem;color:#454550;margin-top:0.3rem;'>"
            f"Total initial cost: <span style='font-family:\"DM Mono\",monospace;"
            f"color:#c8f135;font-size:1rem;'>{R['initial_cost']:.1f}</span></div>",
            unsafe_allow_html=True,
        )

        # STEP 2: Savings
        step_header(2, "💰", "Savings Calculation — S(i,j) = d(0,i) + d(0,j) − d(i,j)")
        st.markdown(
            "<div style='font-size:0.78rem;color:#454550;margin-bottom:1rem;'>"
            "For each customer pair, we compute the distance saved by combining them. "
            "Priority weighting amplifies savings for high-priority pairs.</div>",
            unsafe_allow_html=True
        )
        sav_df = pd.DataFrame(R["savings"]).rename(columns={
            "i": "Node i", "j": "Node j",
            "d(0,i)": "d(0,i)", "d(0,j)": "d(0,j)", "d(i,j)": "d(i,j)",
            "S(i,j)_base": "Base Savings", "Priority Factor": "Priority ×", "S(i,j)_weighted": "Weighted Savings",
        })
        st.dataframe(sav_df, use_container_width=True, hide_index=True)

        # STEP 3: Sorted Savings
        step_header(3, "📊", "Sorted Savings — Descending Weighted Priority Order")
        st.markdown(
            "<div style='font-size:0.78rem;color:#454550;margin-bottom:1rem;'>"
            "Pairs ranked by weighted savings. Merges are attempted in this order.</div>",
            unsafe_allow_html=True
        )
        sorted_df = sav_df[["Node i", "Node j", "Base Savings", "Priority ×", "Weighted Savings"]].reset_index(drop=True)
        sorted_df.index = sorted_df.index + 1
        sorted_df.index.name = "Rank"
        st.dataframe(sorted_df, use_container_width=True)

        # STEP 4: Constraint Summary
        step_header(4, "⚙", "Active Constraints")
        c1, c2, c3, c4 = st.columns(4)
        for col, active, label, detail in [
            (c1, True, "Capacity", f"Max {capacity:.0f} units"),
            (c2, enable_tw and tw is not None, "Time Windows", "VRPTW active" if enable_tw and tw else "Disabled"),
            (c3, max_route_time > 0, "Route Duration", f"Max {max_route_time:.0f}" if max_route_time > 0 else "Unlimited"),
            (c4, enable_priority and pri is not None, "Priority Routing", f"α={priority_alpha:.1f}" if enable_priority else "Disabled"),
        ]:
            color = "#c8f135" if active else "#2e2e3a"
            col.markdown(
                f"<div style='background:#06060a;border:1px solid #1a1a28;"
                f"border-top:2px solid {color};border-radius:0 0 6px 6px;padding:0.8rem;text-align:center;'>"
                f"<div style='font-size:0.68rem;font-weight:600;color:{color};letter-spacing:0.1em;'>{label}</div>"
                f"<div style='font-size:0.7rem;color:#454550;margin-top:0.2rem;'>{detail}</div>"
                f"</div>",
                unsafe_allow_html=True
            )

    # ── TAB 2: Final Routes ───────────────────────────────────────────────────
    with tabs[1]:
        step_header(5, "🚚", f"Optimised Solution — {len(R['route_analytics'])} Vehicles")
        st.markdown(
            "<div style='font-size:0.78rem;color:#454550;margin-bottom:1rem;'>"
            "Final routes after all feasible merges. Utilisation bars show capacity usage.</div>",
            unsafe_allow_html=True
        )

        col_fa, col_fb = st.columns(2)
        for k, ra in enumerate(R["route_analytics"]):
            with (col_fa if k % 2 == 0 else col_fb):
                route_card(ra, k + 1, demands, tw, enable_tw)

        # Summary table
        st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
        summary_rows = []
        for k, ra in enumerate(R["route_analytics"]):
            row = {
                "Vehicle": k + 1,
                "Route": " → ".join(str(x) for x in ra["route"]),
                "Demand": f"{ra['demand']:.0f}/{capacity:.0f}",
                "Utilisation": f"{ra['utilisation']:.0f}%",
                "Travel Time": f"{ra['travel_time']:.1f}",
                "Service Time": f"{ra['service_time']:.1f}",
                "Total Time": f"{ra['total_time']:.1f}",
                "Route Cost": f"{ra['cost']:.1f}",
            }
            if enable_tw:
                row["TW Status"] = ra["tw_status"]
            summary_rows.append(row)
        st.dataframe(pd.DataFrame(summary_rows), use_container_width=True, hide_index=True)

        # Final cost summary
        pct = (R["total_savings"] / R["initial_cost"] * 100) if R["initial_cost"] else 0
        st.markdown(
            f"<div style='background:#0a1400;border:1px solid #1a2800;border-radius:8px;"
            f"padding:1.2rem 1.5rem;margin-top:1rem;display:flex;align-items:center;gap:2rem;flex-wrap:wrap;'>"
            f"<div><div style='font-size:0.6rem;color:#454550;letter-spacing:0.16em;text-transform:uppercase;'>Initial</div>"
            f"<div style='font-family:\"DM Mono\",monospace;font-size:1.5rem;color:#c8f135;'>{R['initial_cost']:.1f}</div></div>"
            f"<div style='font-size:1.2rem;color:#2e2e3a;'>→</div>"
            f"<div><div style='font-size:0.6rem;color:#454550;letter-spacing:0.16em;text-transform:uppercase;'>Optimised</div>"
            f"<div style='font-family:\"DM Mono\",monospace;font-size:1.5rem;color:#39e5b6;'>{R['final_cost']:.1f}</div></div>"
            f"<div style='margin-left:auto;text-align:right;'>"
            f"<div style='font-size:0.6rem;color:#454550;letter-spacing:0.16em;text-transform:uppercase;'>Distance Saved</div>"
            f"<div style='font-family:\"DM Mono\",monospace;font-size:1.8rem;color:#c8f135;font-weight:500;'>"
            f"{pct:.1f}%</div>"
            f"<div style='font-size:0.72rem;color:#454550;'>Saved {R['total_savings']:.1f} units</div>"
            f"</div></div>",
            unsafe_allow_html=True,
        )

    # ── TAB 3: Analytics ──────────────────────────────────────────────────────
    with tabs[2]:
        st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

        if R["route_analytics"]:
            # Per-route breakdown
            st.markdown(
                "<div style='font-size:0.68rem;color:#454550;letter-spacing:0.14em;"
                "text-transform:uppercase;margin-bottom:0.8rem;'>Per-Route Breakdown</div>",
                unsafe_allow_html=True,
            )
            num_routes = len(R["route_analytics"])
            cols = st.columns(min(num_routes, 4))
            for k, ra in enumerate(R["route_analytics"]):
                color = VEHICLE_COLORS[k % len(VEHICLE_COLORS)]
                with cols[k % min(num_routes, 4)]:
                    st.markdown(
                        f"<div style='background:#06060a;border:1px solid #1a1a28;border-radius:6px;"
                        f"padding:0.9rem;margin-bottom:0.5rem;'>"
                        f"<div style='font-size:0.6rem;font-weight:600;color:{color};"
                        f"letter-spacing:0.16em;text-transform:uppercase;margin-bottom:0.6rem;'>Vehicle {k+1}</div>"
                        f"<div style='display:grid;gap:0.3rem;'>"
                        f"<div style='display:flex;justify-content:space-between;'><span style='font-size:0.7rem;color:#2e2e3a;'>Cost</span><span style='font-family:\"DM Mono\",monospace;font-size:0.7rem;color:{color};'>{ra['cost']:.1f}</span></div>"
                        f"<div style='display:flex;justify-content:space-between;'><span style='font-size:0.7rem;color:#2e2e3a;'>Load</span><span style='font-family:\"DM Mono\",monospace;font-size:0.7rem;color:{color};'>{ra['demand']:.0f}/{capacity:.0f}</span></div>"
                        f"<div style='display:flex;justify-content:space-between;'><span style='font-size:0.7rem;color:#2e2e3a;'>Travel</span><span style='font-family:\"DM Mono\",monospace;font-size:0.7rem;color:{color};'>{ra['travel_time']:.1f}</span></div>"
                        f"<div style='display:flex;justify-content:space-between;'><span style='font-size:0.7rem;color:#2e2e3a;'>Service</span><span style='font-family:\"DM Mono\",monospace;font-size:0.7rem;color:{color};'>{ra['service_time']:.1f}</span></div>"
                        f"<div style='display:flex;justify-content:space-between;'><span style='font-size:0.7rem;color:#2e2e3a;'>Util</span><span style='font-family:\"DM Mono\",monospace;font-size:0.7rem;color:{color};'>{ra['utilisation']:.0f}%</span></div>"
                        f"</div>"
                        f"<div style='margin-top:0.6rem;background:#0e0e16;border-radius:2px;height:3px;'>"
                        f"<div style='background:{color};width:{min(ra['utilisation'],100):.1f}%;height:100%;'></div></div>"
                        f"</div>",
                        unsafe_allow_html=True,
                    )

            # Time window compliance table
            if enable_tw and tw:
                st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
                st.markdown(
                    "<div style='font-size:0.68rem;color:#454550;letter-spacing:0.14em;"
                    "text-transform:uppercase;margin-bottom:0.8rem;'>Time Window Compliance</div>",
                    unsafe_allow_html=True,
                )
                tw_rows = []
                for k, ra in enumerate(R["route_analytics"]):
                    for node, arrival in ra["arrivals"].items():
                        e, l = tw[node]
                        status = "ON TIME" if e <= arrival <= l else ("EARLY (WAITS)" if arrival < e else "LATE ✗")
                        tw_rows.append({
                            "Vehicle": k + 1,
                            "Node": node,
                            "Earliest": e,
                            "Latest": l,
                            "Arrival": round(arrival, 2),
                            "Status": status,
                        })
                if tw_rows:
                    st.dataframe(pd.DataFrame(tw_rows), use_container_width=True, hide_index=True)

            # Priority compliance
            if pri and enable_priority:
                st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
                st.markdown(
                    "<div style='font-size:0.68rem;color:#454550;letter-spacing:0.14em;"
                    "text-transform:uppercase;margin-bottom:0.8rem;'>Priority Distribution in Routes</div>",
                    unsafe_allow_html=True,
                )
                pri_rows = []
                for k, ra in enumerate(R["route_analytics"]):
                    customers = [nd for nd in ra["route"] if nd != 0]
                    for nd in customers:
                        p = pri[nd - 1]
                        label = {1: "Low", 2: "Medium", 3: "High"}[p]
                        pri_rows.append({"Vehicle": k+1, "Node": nd, "Priority": p, "Level": label})
                if pri_rows:
                    st.dataframe(pd.DataFrame(pri_rows), use_container_width=True, hide_index=True)

    # ── TAB 4: Merge Log ──────────────────────────────────────────────────────
    with tabs[3]:
        st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
        step_header(6, "🔄", "Merge Decisions — Full Feasibility Trace")
        st.markdown(
            "<div style='font-size:0.78rem;color:#454550;margin-bottom:1rem;'>"
            "Every candidate pair checked against all active constraints in priority order.</div>",
            unsafe_allow_html=True
        )

        # Filter toggle
        show_all = st.checkbox("Show all decisions (including skipped)", value=True)

        for idx, entry in enumerate(R["merge_log"], 1):
            if not show_all and not entry["allowed"]:
                continue
            merge_row(entry, idx)
            if entry["allowed"]:
                with st.expander(f"↳ Routes after merge #{idx}", expanded=False):
                    mc1, mc2 = st.columns(2)
                    for ki, r in enumerate(entry["routes_after"]):
                        if len(r) > 2:
                            d_r = sum(demands[nd] for nd in r[1:-1])
                            c_r = sum(dist[r[a]][r[a+1]] for a in range(len(r)-1))
                            path = " → ".join(str(x) for x in r)
                            color = VEHICLE_COLORS[ki % len(VEHICLE_COLORS)]
                            (mc1 if ki % 2 == 0 else mc2).markdown(
                                f"<div style='background:#06060a;border:1px solid #1a1a28;"
                                f"border-left:2px solid {color};border-radius:0 4px 4px 0;"
                                f"padding:0.5rem 0.8rem;margin-bottom:0.4rem;'>"
                                f"<div style='font-family:\"DM Mono\",monospace;font-size:0.72rem;"
                                f"color:#e8e6e0;'>{path}</div>"
                                f"<div style='font-size:0.62rem;color:#2e2e3a;margin-top:0.2rem;'>"
                                f"load {d_r:.0f} · cost {c_r:.1f}</div>"
                                f"</div>",
                                unsafe_allow_html=True,
                            )

        # Full audit CSV-style table
        st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)
        with st.expander("📋 Full Audit Table (CSV-ready)", expanded=False):
            audit = [{
                "Pair": m["pair"],
                "Saving": round(m["saving"], 3),
                "Decision": "MERGED" if m["allowed"] else "SKIPPED",
                "Reason": m["reason"],
            } for m in R["merge_log"]]
            st.dataframe(pd.DataFrame(audit), use_container_width=True, hide_index=True)

    # ── TAB 5: Data Inputs ────────────────────────────────────────────────────
    with tabs[4]:
        st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

        labels = [f"Depot" if i == 0 else f"N{i}" for i in range(n)]
        df_mat = pd.DataFrame(dist, index=labels, columns=labels)
        st.markdown(
            "<div style='font-size:0.68rem;color:#454550;letter-spacing:0.14em;"
            "text-transform:uppercase;margin-bottom:0.6rem;'>Distance Matrix</div>",
            unsafe_allow_html=True
        )
        st.dataframe(df_mat, use_container_width=True)

        st.markdown("<div style='height:0.8rem'></div>", unsafe_allow_html=True)
        node_data = []
        for i in range(n):
            row = {
                "Node": "Depot" if i == 0 else i,
                "Demand": demands[i],
                "Service Time": svc[i] if svc else 0,
            }
            if tw:
                row["TW Early"] = tw[i][0]
                row["TW Late"] = tw[i][1]
            if pri and i > 0:
                row["Priority"] = pri[i - 1]
            node_data.append(row)

        st.markdown(
            "<div style='font-size:0.68rem;color:#454550;letter-spacing:0.14em;"
            "text-transform:uppercase;margin-bottom:0.6rem;'>Node Parameters</div>",
            unsafe_allow_html=True
        )
        st.dataframe(pd.DataFrame(node_data), use_container_width=True, hide_index=True)


# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("<div style='height:3rem'></div>", unsafe_allow_html=True)
st.markdown(
    "<div style='border-top:1px solid #1a1a28;padding:1.2rem 0;display:flex;"
    "justify-content:space-between;align-items:center;flex-wrap:wrap;gap:0.5rem;'>"
    "<div style='font-family:\"Bebas Neue\",sans-serif;font-size:1rem;color:#1a1a28;"
    "letter-spacing:0.1em;'>AI SUPPLY CHAIN SOLUTIONS</div>"
    "<div style='font-size:0.65rem;color:#2e2e3a;letter-spacing:0.1em;'>"
    "Clarke–Wright Savings · CVRPTW · Developed by Zillay Husnain Jatoi"
    "</div>"
    "</div>",
    unsafe_allow_html=True,
)

