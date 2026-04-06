"""
Enterprise Supply Chain Optimization Engine — Clarke–Wright VRP Solver
Run: streamlit run app.py
"""

import re
import streamlit as st
import pandas as pd

# ─── Page Config ─────────────────────────────────────────
st.set_page_config(
    page_title="Supply Chain Optimization Engine",
    page_icon="🚚",
    layout="wide",
)

# ─── SIMPLE CLEAN CSS ─────────────────────────────────────
st.markdown("""
<style>
body {font-family: 'Inter', sans-serif;}
.metric {font-size: 28px; font-weight: bold;}
</style>
""", unsafe_allow_html=True)

# ═════════════════════════════════════════════════════════
# CORE FUNCTIONS
# ═════════════════════════════════════════════════════════

def parse_matrix(raw):
    matrix = []
    for line in raw.strip().splitlines():
        row = [int(x) for x in re.split(r"[,\s]+", line.strip()) if x]
        matrix.append(row)
    return matrix

def parse_demands(raw):
    return [int(x) for x in re.split(r"[,\s]+", raw.strip()) if x]

def calculate_cost(routes, dist):
    total = 0
    for r in routes:
        for i in range(len(r)-1):
            total += dist[r[i]][r[i+1]]
    return total

def compute_savings(dist, n):
    s = []
    for i in range(1, n):
        for j in range(i+1, n):
            saving = dist[0][i] + dist[0][j] - dist[i][j]
            s.append((i,j,saving))
    return sorted(s, key=lambda x: x[2], reverse=True)

def run_vrp(dist, demands, cap):
    n = len(dist)
    routes = [[0,i,0] for i in range(1,n)]
    savings = compute_savings(dist,n)

    for i,j,s in savings:
        ri = next((r for r in routes if i in r), None)
        rj = next((r for r in routes if j in r), None)

        if ri != rj:
            load = sum(demands[x] for x in ri[1:-1]) + sum(demands[x] for x in rj[1:-1])
            if load <= cap:
                new = ri[:-1] + rj[1:]
                routes.remove(ri)
                routes.remove(rj)
                routes.append(new)

    return routes

# ═════════════════════════════════════════════════════════
# SIDEBAR
# ═════════════════════════════════════════════════════════

with st.sidebar:
    st.title("🚚 Optimization Engine")

    matrix_raw = st.text_area("Distance Matrix",
        "0,10,8,7,12\n10,0,5,6,11\n8,5,0,3,9\n7,6,3,0,4\n12,11,9,4,0")

    demands_raw = st.text_area("Demands",
        "0,4,6,5,7")

    capacity = st.number_input("Capacity", value=15)

    solve = st.button("Solve")

# ═════════════════════════════════════════════════════════
# MAIN HEADER (ENTERPRISE)
# ═════════════════════════════════════════════════════════

st.markdown("""<div style='padding:1.6rem 0 0.6rem 0;'>
<div style='font-size:12px;font-weight:700;letter-spacing:2px;color:#e76f51;'>SUPPLY CHAIN OPTIMIZATION ENGINE</div>
<div style='font-size:34px;font-weight:800;'>Intelligent Route Optimization Platform</div>
<div style='color:#666;'>AI-driven logistics planning · cost minimization · fleet efficiency analytics</div>
</div>""", unsafe_allow_html=True)

# ═════════════════════════════════════════════════════════
# RUN
# ═════════════════════════════════════════════════════════

if solve:
    dist = parse_matrix(matrix_raw)
    demands = parse_demands(demands_raw)

    routes = run_vrp(dist, demands, capacity)
    cost = calculate_cost(routes, dist)

    st.subheader("🚚 Optimized Routes")

    for i,r in enumerate(routes):
        st.write(f"Vehicle {i+1}: {' → '.join(map(str,r))}")

    st.metric("Total Cost", cost)

# ═════════════════════════════════════════════════════════
# FOOTER
# ═════════════════════════════════════════════════════════

st.markdown("""
<hr>
<div style='text-align:center;font-size:12px;color:#999;'>
Enterprise Logistics Optimization Engine · Powered by Clarke–Wright Heuristic · Scalable VRP Framework
</div>
""", unsafe_allow_html=True)
