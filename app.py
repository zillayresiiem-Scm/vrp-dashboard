"""
Zee AI Supply Chain Solutions — Enterprise VRP Optimizer
Built by Zillay Husnian
Run: streamlit run app.py
"""

import re
import streamlit as st
import pandas as pd

# ─── Page Config ──────────────────────────────────────────────
st.set_page_config(
    page_title="Zee AI Supply Chain Solutions · Enterprise VRP Optimizer",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── CSS (UNCHANGED) ─────────────────────────────────────────
st.markdown("""<style>
html, body { font-family: Arial; }
</style>""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# HELPER FUNCTION (FIX FOR YOUR ERROR ✅)
# ═══════════════════════════════════════════════════════════════
def sec(icon, label, step=None):
    badge = f"STEP {step} · " if step else ""
    st.markdown(f"### {badge}{icon} {label}")

# ═══════════════════════════════════════════════════════════════
# CORE FUNCTIONS (UNCHANGED)
# ═══════════════════════════════════════════════════════════════

def parse_matrix(raw):
    return [list(map(int, line.split(","))) for line in raw.strip().split("\n")]

def parse_demands(raw):
    return list(map(int, raw.split(",")))

def calculate_cost(routes, dist):
    return sum(dist[r[i]][r[i+1]] for r in routes for i in range(len(r)-1))

def compute_savings(dist):
    n = len(dist)
    savings = []
    for i in range(1, n):
        for j in range(i+1, n):
            s = dist[0][i] + dist[0][j] - dist[i][j]
            savings.append((i, j, s))
    return sorted(savings, key=lambda x: x[2], reverse=True)

def run_vrp(matrix, demands, capacity):
    routes = [[0, i, 0] for i in range(1, len(matrix))]
    savings = compute_savings(matrix)

    for i, j, s in savings:
        r_i = next((r for r in routes if i in r[1:-1]), None)
        r_j = next((r for r in routes if j in r[1:-1]), None)

        if r_i != r_j and r_i and r_j:
            load = sum(demands[n] for n in r_i+r_j)
            if load <= capacity:
                routes.remove(r_i)
                routes.remove(r_j)
                routes.append([0] + r_i[1:-1] + r_j[1:-1] + [0])

    return routes

# ═══════════════════════════════════════════════════════════════
# SIDEBAR (UPDATED BRANDING)
# ═══════════════════════════════════════════════════════════════

with st.sidebar:
    st.markdown("## 🚀 Zee AI")
    st.caption("Supply Chain Solutions")

    matrix_raw = st.text_area("Distance Matrix",
                             value="0,10,8,7,12\n10,0,5,6,11\n8,5,0,3,9\n7,6,3,0,4\n12,11,9,4,0")

    demands_raw = st.text_area("Node Demands", value="0,4,6,5,7")
    capacity = st.number_input("Vehicle Capacity", value=15)

    solve_btn = st.button("▶ Solve")

# ═══════════════════════════════════════════════════════════════
# HEADER (FIXED — NO ERROR NOW)
# ═══════════════════════════════════════════════════════════════

st.markdown("""
<div style='padding:1rem 0;'>
    <div style='color:#e76f51;font-size:0.7rem;'>Enterprise Optimization Engine</div>
    <div style='font-size:2rem;font-weight:800;'>Zee AI VRP Optimizer</div>
    <div style='color:#888;'>AI-powered Supply Chain Routing</div>
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# RUN SOLVER
# ═══════════════════════════════════════════════════════════════

if solve_btn:
    with st.spinner("Running Zee AI Optimization Engine..."):
        matrix = parse_matrix(matrix_raw)
        demands = parse_demands(demands_raw)
        routes = run_vrp(matrix, demands, capacity)
        cost = calculate_cost(routes, matrix)

        st.success("Optimization Complete 🚀")

        # STEP 1
        sec("📍", "Initial Route Allocation — Baseline Distribution", step=1)

        # RESULT
        sec("🚚", "Optimized Fleet Routing Plan", step=2)

        for i, r in enumerate(routes):
            st.write(f"Vehicle {i+1}: {' → '.join(map(str,r))}")

        st.metric("Total Cost", cost)

# ═══════════════════════════════════════════════════════════════
# FOOTER
# ═══════════════════════════════════════════════════════════════

st.markdown("---")
st.markdown(
    "Zee AI Supply Chain Solutions · Built by Zillay Husnian",
)
