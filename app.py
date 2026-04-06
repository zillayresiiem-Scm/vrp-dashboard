"""
Vehicle Routing Problem (VRP) Solver
Clarke–Wright Savings Algorithm

Developed by Zillay Husnain Jatoi
Run: streamlit run app.py
"""
 
import re
import streamlit as st
import pandas as pd

# ─── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="VRP · Clarke–Wright Solver",
    page_icon="🚚",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── CSS ──────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=JetBrains+Mono:wght@400;500&family=Inter:wght@300;400;500;600&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

.stApp { background: #f8f7f4; color: #1a1a2e; }

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: #1a1a2e !important;
    border-right: none;
    box-shadow: 4px 0 24px rgba(0,0,0,0.12);
}
section[data-testid="stSidebar"] * { color: #e2ddd5 !important; }
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 { color: #f5f0e8 !important; }
section[data-testid="stSidebar"] .stTextArea textarea,
section[data-testid="stSidebar"] .stNumberInput input {
    background: #12121f !important;
    border: 1px solid #2e2e4a !important;
    color: #e2ddd5 !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.8rem !important;
    border-radius: 8px !important;
}
section[data-testid="stSidebar"] .stTextArea textarea:focus,
section[data-testid="stSidebar"] .stNumberInput input:focus {
    border-color: #f4a261 !important;
    box-shadow: 0 0 0 2px rgba(244,162,97,0.2) !important;
}
section[data-testid="stSidebar"] label {
    font-size: 0.72rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    color: #7c7c99 !important;
}

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, #e76f51 0%, #f4a261 100%) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
    padding: 0.6rem 1.4rem !important;
    letter-spacing: 0.04em !important;
    box-shadow: 0 4px 14px rgba(231,111,81,0.35) !important;
    transition: all 0.2s !important;
    width: 100%;
}
.stButton > button:hover {
    box-shadow: 0 6px 20px rgba(231,111,81,0.5) !important;
    transform: translateY(-1px) !important;
}

/* ── Section headers ── */
.sec-header {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    background: #1a1a2e;
    color: #f5f0e8;
    border-radius: 10px;
    padding: 0.7rem 1.2rem;
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    font-size: 1rem;
    letter-spacing: 0.02em;
    margin: 1.4rem 0 0.8rem 0;
}
.sec-header .step-badge {
    background: #f4a261;
    color: #1a1a2e;
    border-radius: 5px;
    font-size: 0.7rem;
    font-weight: 800;
    padding: 0.1rem 0.45rem;
    letter-spacing: 0.06em;
}

/* ── Metric row ── */
.metric-row { display: flex; gap: 1rem; margin-bottom: 1.2rem; flex-wrap: wrap; }
.metric-box {
    flex: 1;
    min-width: 140px;
    background: #1a1a2e;
    border-radius: 12px;
    padding: 1rem 1.2rem;
    text-align: center;
}
.metric-box .val {
    font-family: 'JetBrains Mono', monospace;
    font-size: 1.9rem;
    font-weight: 500;
    color: #f4a261;
    line-height: 1;
}
.metric-box .lbl {
    font-size: 0.68rem;
    font-weight: 600;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #7c7c99;
    margin-top: 0.35rem;
}

/* ── Route cards ── */
.route-card {
    background: #fff;
    border: 1px solid #e8e4de;
    border-left: 4px solid #e76f51;
    border-radius: 10px;
    padding: 1rem 1.3rem;
    margin-bottom: 0.8rem;
}
.route-card-final {
    background: #fff;
    border: 1px solid #e8e4de;
    border-left: 4px solid #2a9d8f;
    border-radius: 10px;
    padding: 1rem 1.3rem;
    margin-bottom: 0.8rem;
}
.vehicle-tag-init { font-size: 0.68rem; font-weight: 700; letter-spacing: 0.12em;
    text-transform: uppercase; color: #e76f51; margin-bottom: 0.35rem; }
.vehicle-tag-final { font-size: 0.68rem; font-weight: 700; letter-spacing: 0.12em;
    text-transform: uppercase; color: #2a9d8f; margin-bottom: 0.35rem; }
.route-path { font-family: 'JetBrains Mono', monospace; font-size: 1.05rem; color: #1a1a2e; }
.route-meta { font-size: 0.78rem; color: #888; margin-top: 0.4rem; }
.badge { display: inline-block; border-radius: 4px; padding: 0.1rem 0.5rem;
    font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; margin-right: 0.4rem; }
.badge-orange { background: rgba(231,111,81,0.1); color: #e76f51; }
.badge-teal   { background: rgba(42,157,143,0.1); color: #2a9d8f; }
.badge-blue   { background: rgba(69,123,157,0.12); color: #457b9d; }

/* ── Merge log ── */
.merge-row {
    background: #fff;
    border: 1px solid #e8e4de;
    border-radius: 8px;
    padding: 0.75rem 1.1rem;
    margin-bottom: 0.55rem;
    font-size: 0.85rem;
}
.merge-row-icon { font-size: 1rem; }
.merge-pair-label { font-family: 'JetBrains Mono', monospace; font-weight: 500; color: #1a1a2e; }
.merge-detail { color: #555; font-size: 0.78rem; margin-top: 0.15rem; }

/* ── Info box ── */
.info-box {
    background: rgba(42,157,143,0.08);
    border: 1px solid rgba(42,157,143,0.25);
    border-radius: 8px;
    padding: 0.9rem 1.2rem;
    font-size: 0.84rem;
    color: #1d6b62;
    margin-bottom: 1rem;
}

/* ── Dataframe tweaks ── */
.stDataFrame { border-radius: 10px !important; overflow: hidden; }

/* ── Divider ── */
hr { border-color: #e8e4de !important; }
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
            row = [int(p) for p in parts]
        except ValueError:
            raise ValueError(f"Row {line_no}: non-integer value found — '{line}'")
        if any(v < 0 for v in row):
            raise ValueError(f"Row {line_no}: negative distances are not allowed.")
        matrix.append(row)
    if not matrix:
        raise ValueError("No rows parsed from distance matrix.")
    n = len(matrix)
    for i, row in enumerate(matrix, 1):
        if len(row) != n:
            raise ValueError(
                f"Matrix is not square: row {i} has {len(row)} values, expected {n}."
            )
    return matrix


def parse_demands(raw: str, expected: int):
    raw = raw.strip()
    if not raw:
        raise ValueError("Demands field is empty.")
    parts = re.split(r"[,\s]+", raw.replace(",", " "))
    parts = [p for p in parts if p]
    try:
        demands = [int(p) for p in parts]
    except ValueError:
        raise ValueError("Demands contain non-integer values.")
    if len(demands) != expected:
        raise ValueError(
            f"Demands length ({len(demands)}) does not match number of nodes ({expected})."
        )
    if demands[0] != 0:
        raise ValueError(f"Depot demand (index 0) must be 0, got {demands[0]}.")
    if any(d < 0 for d in demands[1:]):
        raise ValueError("All customer demands must be non-negative.")
    return demands


def calculate_cost(routes, dist):
    total = 0
    for route in routes:
        for k in range(len(route) - 1):
            total += dist[route[k]][route[k + 1]]
    return total


def compute_savings(dist, n):
    savings = []
    for i in range(1, n):
        for j in range(i + 1, n):
            s = dist[0][i] + dist[0][j] - dist[i][j]
            savings.append({
                "i": i, "j": j, "S(i,j)": s,
                "d(0,i)": dist[0][i], "d(0,j)": dist[0][j], "d(i,j)": dist[i][j],
            })
    savings.sort(key=lambda x: x["S(i,j)"], reverse=True)
    return savings


def apply_merges(initial_routes, savings, demands, capacity, dist):
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

    def snapshot():
        return [r[:] for r in routes]

    for s in savings:
        i, j, sval = s["i"], s["j"], s["S(i,j)"]
        pair_label = f"S({i},{j}) = {sval}"

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
                        "reason": f"Nodes {i} and {j} are already in the same route.",
                        "routes_after": snapshot()})
            continue

        i_end = is_endpoint(i, ri)
        j_end = is_endpoint(j, rj)
        if not i_end or not j_end:
            bad = []
            if not i_end:
                bad.append(f"node {i} is not an endpoint of its route")
            if not j_end:
                bad.append(f"node {j} is not an endpoint of its route")
            log.append({"pair": pair_label, "saving": sval, "allowed": False,
                        "reason": "Endpoint check failed: " + "; ".join(bad) + ".",
                        "routes_after": snapshot()})
            continue

        di = route_demand(ri)
        dj = route_demand(rj)
        combined = di + dj
        if combined > capacity:
            log.append({"pair": pair_label, "saving": sval, "allowed": False,
                        "reason": (f"Capacity exceeded: {di} + {dj} = {combined} > {capacity}."),
                        "routes_after": snapshot()})
            continue

        # Orient and merge
        ri_inner = ri[1:-1]
        if ri_inner[-1] != i:
            ri_inner = ri_inner[::-1]
        rj_inner = rj[1:-1]
        if rj_inner[0] != j:
            rj_inner = rj_inner[::-1]

        merged = [0] + ri_inner + rj_inner + [0]
        for idx in sorted([ri_idx, rj_idx], reverse=True):
            routes.pop(idx)
        routes.append(merged)

        log.append({"pair": pair_label, "saving": sval, "allowed": True,
                    "reason": f"Merged: demand {di} + {dj} = {combined} <= {capacity}.",
                    "routes_after": snapshot()})

    return routes, log


def run_clarke_wright(matrix, demands, capacity):
    n = len(matrix)
    initial_routes = [[0, c, 0] for c in range(1, n)]
    initial_cost = calculate_cost(initial_routes, matrix)
    savings = compute_savings(matrix, n)
    final_routes, merge_log = apply_merges(
        initial_routes, savings, demands, capacity, matrix
    )
    final_cost = calculate_cost(final_routes, matrix)
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
    }


# ═══════════════════════════════════════════════════════════════════════════════
#  UI HELPERS
# ═══════════════════════════════════════════════════════════════════════════════

def sec(icon, label, step=None):
    badge = f"<span class='step-badge'>STEP {step}</span> " if step else ""
    st.markdown(
        f"<div class='sec-header'>{badge}{icon} {label}</div>",
        unsafe_allow_html=True,
    )


def route_str(route):
    return " → ".join(str(x) for x in route)


def render_route_card(route, demands, dist, vehicle_num, final=False):
    card_cls = "route-card-final" if final else "route-card"
    tag_cls  = "vehicle-tag-final" if final else "vehicle-tag-init"
    cost_r   = sum(dist[route[k]][route[k+1]] for k in range(len(route)-1))
    demand_r = sum(demands[nd] for nd in route[1:-1])
    bc = "badge-teal" if final else "badge-orange"
    st.markdown(
        f"<div class='{card_cls}'>"
        f"<div class='{tag_cls}'>Vehicle {vehicle_num}</div>"
        f"<div class='route-path'>{route_str(route)}</div>"
        f"<div class='route-meta'>"
        f"<span class='badge {bc}'>Cost: {cost_r}</span>"
        f"<span class='badge badge-blue'>Load: {demand_r}</span>"
        f"</div></div>",
        unsafe_allow_html=True,
    )


def render_merge_row(entry, idx):
    icon   = "✅" if entry["allowed"] else "❌"
    label  = "MERGED" if entry["allowed"] else "SKIPPED"
    color  = "#1d6b62" if entry["allowed"] else "#b5451b"
    st.markdown(
        f"<div class='merge-row'>"
        f"<span class='merge-row-icon'>{icon}</span> &nbsp;"
        f"<span class='merge-pair-label'>#{idx} &nbsp; {entry['pair']}</span>"
        f" &nbsp; <span style='color:{color};font-size:0.8rem;font-weight:600;'>{label}</span>"
        f"<div class='merge-detail'>{entry['reason']}</div>"
        f"</div>",
        unsafe_allow_html=True,
    )


# ═══════════════════════════════════════════════════════════════════════════════
#  SIDEBAR
# ═══════════════════════════════════════════════════════════════════════════════

with st.sidebar:
    st.markdown("""
    <div style='padding:1rem 0 0.5rem 0;'>
        <div style='font-family:"Syne",sans-serif;font-size:1.35rem;font-weight:800;
                    color:#f5f0e8;letter-spacing:-0.01em;'>🚚 VRP Solver</div>
        <div style='font-size:0.72rem;color:#7c7c99;margin-top:0.2rem;
                    letter-spacing:0.08em;text-transform:uppercase;'>
            Clarke–Wright Savings Method
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.divider()

    EXAMPLE_MATRIX  = "0,10,8,7,12\n10,0,5,6,11\n8,5,0,3,9\n7,6,3,0,4\n12,11,9,4,0"
    EXAMPLE_DEMANDS = "0,4,6,5,7"

    matrix_raw  = st.text_area("Distance Matrix",  value=EXAMPLE_MATRIX,  height=160)
    demands_raw = st.text_area("Node Demands (depot = 0 first)", value=EXAMPLE_DEMANDS, height=68)
    capacity    = st.number_input("Vehicle Capacity", min_value=1, max_value=100_000, value=15, step=1)

    st.markdown("<br>", unsafe_allow_html=True)
    col_s, col_r = st.columns(2)
    solve_btn = col_s.button("▶ Solve")
    reset_btn = col_r.button("↺ Reset")

    st.markdown("""
    <div style='margin-top:1.5rem;font-size:0.7rem;color:#3a3a55;line-height:1.8;'>
    <b style='color:#5a5a75'>Algorithm</b><br>
    Clarke–Wright Savings · Parallel<br><br>
    <b style='color:#5a5a75'>Savings Formula</b><br>
    S(i,j) = d(0,i) + d(0,j) − d(i,j)<br><br>
    <b style='color:#5a5a75'>Merge Rules</b><br>
    1. Both nodes are endpoints<br>
    2. Combined demand ≤ capacity<br>
    3. Not already same route
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
    with st.spinner("Computing Clarke–Wright solution..."):
        try:
            matrix  = parse_matrix(matrix_raw)
            demands = parse_demands(demands_raw, len(matrix))
            max_cust_demand = max(demands[1:]) if len(demands) > 1 else 0
            if capacity < max_cust_demand:
                raise ValueError(
                    f"Vehicle capacity ({capacity}) is less than the largest single "
                    f"customer demand ({max_cust_demand})."
                )
            st.session_state.result = run_clarke_wright(matrix, demands, capacity)
        except Exception as e:
            st.session_state.error = str(e)


# ═══════════════════════════════════════════════════════════════════════════════
#  MAIN PANEL
# ═══════════════════════════════════════════════════════════════════════════════

st.markdown("""
<div style='padding:1.6rem 0 0.6rem 0;'>
    <div style='font-family:"Syne",sans-serif;font-size:0.65rem;font-weight:700;
                letter-spacing:0.22em;text-transform:uppercase;color:#e76f51;
                margin-bottom:0.3rem;'>Step-by-Step Academic Solution</div>
    <div style='font-family:"Syne",sans-serif;font-size:2.1rem;font-weight:800;
                color:#1a1a2e;letter-spacing:-0.02em;line-height:1.1;'>
        Clarke–Wright Savings Method
    </div>
    <div style='font-size:0.88rem;color:#888;margin-top:0.35rem;'>
        Vehicle Routing Problem solver with full decision trace
    </div>
</div>
""", unsafe_allow_html=True)

if st.session_state.error:
    st.error(f"⚠️ {st.session_state.error}")

if st.session_state.result is None and not st.session_state.error:
    st.markdown("""
    <div style='text-align:center;padding:4rem 1rem;'>
        <div style='font-size:3.5rem;margin-bottom:1rem;'>🗺️</div>
        <div style='font-size:1rem;color:#888;font-weight:500;'>
            Configure your VRP inputs in the sidebar, then click
            <b style='color:#e76f51'>▶ Solve</b>
        </div>
        <div style='font-size:0.82rem;color:#bbb;margin-top:0.5rem;'>
            A pre-loaded 5-node example is ready to go
        </div>
    </div>
    """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
#  RESULTS
# ═══════════════════════════════════════════════════════════════════════════════

if st.session_state.result:
    R        = st.session_state.result
    dist     = R["matrix"]
    demands  = R["demands"]
    capacity = R["capacity"]
    n        = R["n"]

    active_final    = [r for r in R["final_routes"] if len(r) > 2]
    merges_allowed  = sum(1 for m in R["merge_log"] if m["allowed"])
    merges_rejected = sum(1 for m in R["merge_log"] if not m["allowed"])

    # ── KPI Strip ─────────────────────────────────────────────────────────────
    st.markdown(
        f"<div class='metric-row'>"
        f"<div class='metric-box'><div class='val'>{R['initial_cost']}</div>"
        f"<div class='lbl'>Initial Cost</div></div>"
        f"<div class='metric-box'><div class='val'>{R['final_cost']}</div>"
        f"<div class='lbl'>Final Cost</div></div>"
        f"<div class='metric-box'><div class='val'>{R['total_savings']}</div>"
        f"<div class='lbl'>Total Savings</div></div>"
        f"<div class='metric-box'><div class='val'>{len(active_final)}</div>"
        f"<div class='lbl'>Vehicles Used</div></div>"
        f"<div class='metric-box'><div class='val'>{merges_allowed}</div>"
        f"<div class='lbl'>Merges Done</div></div>"
        f"<div class='metric-box'><div class='val'>{merges_rejected}</div>"
        f"<div class='lbl'>Merges Skipped</div></div>"
        f"</div>",
        unsafe_allow_html=True,
    )
    st.divider()

    # ── Input Review ──────────────────────────────────────────────────────────
    with st.expander("📐 Input: Distance Matrix & Demands", expanded=False):
        labels   = [f"{'Depot' if i==0 else f'N{i}'}" for i in range(n)]
        df_mat   = pd.DataFrame(dist, index=labels, columns=labels)
        st.dataframe(df_mat, use_container_width=True)
        dem_df = pd.DataFrame(
            [{"Node": "Depot (0)" if i == 0 else i, "Demand": demands[i]}
             for i in range(n)]
        )
        st.dataframe(dem_df, use_container_width=True, hide_index=True)

    # ── STEP 1: Initial Routes ────────────────────────────────────────────────
    sec("📍", "Initial Routes — One Vehicle Per Customer", step=1)
    st.markdown(
        "<div class='info-box'>Each customer starts on its own dedicated route: "
        "<b>0 → i → 0</b>. This is the baseline before any merges are applied.</div>",
        unsafe_allow_html=True,
    )
    col_a, col_b = st.columns(2)
    for k, route in enumerate(R["initial_routes"]):
        with (col_a if k % 2 == 0 else col_b):
            render_route_card(route, demands, dist, k + 1, final=False)

    st.markdown(
        f"<div style='font-size:0.85rem;color:#555;margin-top:0.3rem;'>"
        f"<b>Total Initial Cost:</b> "
        f"<span style='font-family:\"JetBrains Mono\",monospace;color:#e76f51;"
        f"font-size:1rem;'>{R['initial_cost']}</span></div>",
        unsafe_allow_html=True,
    )

    # ── STEP 2: Savings Table ─────────────────────────────────────────────────
    sec("💰", "Savings Calculation — S(i,j) = d(0,i) + d(0,j) − d(i,j)", step=2)
    st.markdown(
        "<div class='info-box'>For every pair of customers (i, j), compute how much "
        "distance is saved by combining them into one route.</div>",
        unsafe_allow_html=True,
    )
    sav_df = pd.DataFrame(R["savings"]).rename(columns={
        "i": "Node i", "j": "Node j",
        "d(0,i)": "d(0,i)", "d(0,j)": "d(0,j)",
        "d(i,j)": "d(i,j)", "S(i,j)": "Savings S(i,j)",
    })
    st.dataframe(sav_df, use_container_width=True, hide_index=True)

    # ── STEP 3: Sorted Savings ────────────────────────────────────────────────
    sec("📊", "Sorted Savings — Descending Priority Order", step=3)
    st.markdown(
        "<div class='info-box'>Pairs are ranked by savings — highest first. "
        "We attempt merges in this order.</div>",
        unsafe_allow_html=True,
    )
    sorted_df = sav_df[["Node i", "Node j", "Savings S(i,j)"]].reset_index(drop=True)
    sorted_df.index = sorted_df.index + 1
    sorted_df.index.name = "Rank"
    st.dataframe(sorted_df, use_container_width=True)

    # ── STEP 4: Merge Decisions ───────────────────────────────────────────────
    sec("🔄", "Merge Decisions — Step-by-Step Feasibility Check", step=4)
    st.markdown(
        "<div class='info-box'>"
        "Each candidate pair is checked against three rules:<br>"
        "① Both nodes must be route endpoints &nbsp;·&nbsp; "
        "② Not already in the same route &nbsp;·&nbsp; "
        "③ Combined demand ≤ vehicle capacity"
        "</div>",
        unsafe_allow_html=True,
    )

    for idx, entry in enumerate(R["merge_log"], 1):
        render_merge_row(entry, idx)
        if entry["allowed"]:
            with st.expander(f"   ↳ Routes after merge #{idx}", expanded=False):
                mc1, mc2 = st.columns(2)
                for ki, r in enumerate(entry["routes_after"]):
                    if len(r) > 2:
                        d_r = sum(demands[nd] for nd in r[1:-1])
                        c_r = sum(dist[r[a]][r[a+1]] for a in range(len(r)-1))
                        (mc1 if ki % 2 == 0 else mc2).markdown(
                            f"<span style='font-family:\"JetBrains Mono\",monospace;"
                            f"font-size:0.82rem;'>{route_str(r)}</span> "
                            f"<span class='badge badge-blue'>load {d_r}</span>"
                            f"<span class='badge badge-teal'>cost {c_r}</span>",
                            unsafe_allow_html=True,
                        )

    # ── STEP 5: Final Routes ──────────────────────────────────────────────────
    sec("🚚", "Final Routes — Optimised Solution", step=5)
    active = [r for r in R["final_routes"] if len(r) > 2]
    idle   = len(R["final_routes"]) - len(active)

    col_fa, col_fb = st.columns(2)
    for k, route in enumerate(active):
        with (col_fa if k % 2 == 0 else col_fb):
            render_route_card(route, demands, dist, k + 1, final=True)

    if idle:
        st.markdown(
            f"<div style='font-size:0.8rem;color:#aaa;margin-top:0.3rem;'>"
            f"ℹ️ {idle} vehicle(s) were not required.</div>",
            unsafe_allow_html=True,
        )

    summary_rows = []
    for k, route in enumerate(active):
        c_r = sum(dist[route[a]][route[a+1]] for a in range(len(route)-1))
        d_r = sum(demands[nd] for nd in route[1:-1])
        summary_rows.append({
            "Vehicle": k + 1,
            "Route": route_str(route),
            "Demand": d_r,
            f"Cap ({capacity})": capacity,
            "Utilisation": f"{d_r / capacity * 100:.1f}%",
            "Route Cost": c_r,
        })
    st.dataframe(pd.DataFrame(summary_rows), use_container_width=True, hide_index=True)

    # ── STEP 6: Final Cost & Savings ──────────────────────────────────────────
    sec("🏁", "Final Cost & Total Savings Summary", step=6)
    c1, c2, c3 = st.columns(3)
    for col, val, lbl, clr in [
        (c1, R["initial_cost"],  "Initial Distance", "#e76f51"),
        (c2, R["final_cost"],    "Final Distance",   "#2a9d8f"),
        (c3, R["total_savings"], "Total Savings",    "#457b9d"),
    ]:
        col.markdown(
            f"<div style='background:#1a1a2e;border-radius:12px;padding:1.4rem;"
            f"text-align:center;'>"
            f"<div style='font-family:\"JetBrains Mono\",monospace;font-size:2.4rem;"
            f"font-weight:500;color:{clr};'>{val}</div>"
            f"<div style='font-size:0.7rem;font-weight:700;letter-spacing:0.1em;"
            f"text-transform:uppercase;color:#7c7c99;margin-top:0.4rem;'>{lbl}</div>"
            f"</div>",
            unsafe_allow_html=True,
        )

    pct = (R["total_savings"] / R["initial_cost"] * 100) if R["initial_cost"] else 0
    st.markdown(
        f"<div style='background:rgba(42,157,143,0.08);border:1px solid rgba(42,157,143,0.25);"
        f"border-radius:10px;padding:1.1rem 1.5rem;margin-top:1rem;'>"
        f"<span style='font-family:\"JetBrains Mono\",monospace;font-size:1rem;"
        f"color:#1d6b62;font-weight:600;'>"
        f"🎯 Distance reduced by {pct:.1f}% &nbsp;·&nbsp; "
        f"{R['initial_cost']} → {R['final_cost']} &nbsp;·&nbsp; "
        f"Saved {R['total_savings']} units"
        f"</span></div>",
        unsafe_allow_html=True,
    )

    # ── Audit Trail ───────────────────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    with st.expander("📋 Full Savings Audit Trail", expanded=False):
        audit = [
            {
                "Pair": m["pair"],
                "Saving": m["saving"],
                "Decision": "✅ MERGED" if m["allowed"] else "❌ SKIPPED",
                "Reason": m["reason"],
            }
            for m in R["merge_log"]
        ]
        st.dataframe(pd.DataFrame(audit), use_container_width=True, hide_index=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("<br><br>", unsafe_allow_html=True)
st.divider()
st.markdown(
    "<div style='text-align:center;font-size:0.7rem;color:#ccc;padding:0.5rem 0;'>"
    "Clarke–Wright Savings Algorithm · Parallel Version · Enterprise VRP Solver"
    "</div>",
    unsafe_allow_html=True,
)
