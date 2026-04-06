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

# (✅ CSS SAME — NO CHANGE)

# ═══════════════════════════════════════════════════════════════
# SIDEBAR (ONLY BRANDING CHANGED)
# ═══════════════════════════════════════════════════════════════

with st.sidebar:
    st.markdown("""
    <div style='padding:1rem 0 0.5rem 0;'>
        <div style='font-family:"Syne",sans-serif;font-size:1.35rem;font-weight:800;
                    color:#f5f0e8;letter-spacing:-0.01em;'>🚀 Zee AI</div>
        <div style='font-size:0.72rem;color:#7c7c99;margin-top:0.2rem;
                    letter-spacing:0.08em;text-transform:uppercase;'>
            Supply Chain Solutions
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

# ═══════════════════════════════════════════════════════════════
# (✅ ALL CORE LOGIC SAME — NO CHANGE)
# ═══════════════════════════════════════════════════════════════

# (I AM NOT TOUCHING YOUR ALGORITHM — KEEP SAME)

# ═══════════════════════════════════════════════════════════════
# MAIN HEADER (UPDATED)
# ═══════════════════════════════════════════════════════════════

st.markdown("""
<div style='padding:1.6rem 0 0.6rem 0;'>

    <div style='font-family:"Syne",sans-serif;font-size:0.65rem;font-weight:700;
                letter-spacing:0.22em;text-transform:uppercase;color:#e76f51;
                margin-bottom:0.3rem;'>Enterprise Optimization Engine</div>

    <div style='font-family:"Syne",sans-serif;font-size:2.1rem;font-weight:800;
                color:#1a1a2e;letter-spacing:-0.02em;line-height:1.1;'>
        Zee AI VRP Optimizer
    </div>

    <div style='font-size:0.88rem;color:#888;margin-top:0.35rem;'>
        Advanced Supply Chain Routing with AI Decision Intelligence
    </div>

</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════
# SOLVE BUTTON (SPINNER UPDATED)
# ═══════════════════════════════════════════════════════════════

if solve_btn:
    st.session_state.result = None
    st.session_state.error = None
    with st.spinner("Running Zee AI Optimization Engine..."):
        try:
            matrix  = parse_matrix(matrix_raw)
            demands = parse_demands(demands_raw, len(matrix))
            st.session_state.result = run_clarke_wright(matrix, demands, capacity)
        except Exception as e:
            st.session_state.error = str(e)

# ═══════════════════════════════════════════════════════════════
# SECTION TITLES (UPDATED TO ENTERPRISE)
# ═══════════════════════════════════════════════════════════════

# STEP 1
sec("📍", "Initial Route Allocation — Baseline Distribution", step=1)

# STEP 2
sec("💰", "Optimization Gain Analysis — S(i,j)", step=2)

# STEP 4
sec("🔄", "Route Optimization Decisions Engine", step=4)

# STEP 5
sec("🚚", "Optimized Fleet Routing Plan", step=5)

# ═══════════════════════════════════════════════════════════════
# FOOTER (UPDATED)
# ═══════════════════════════════════════════════════════════════

st.markdown("<br><br>", unsafe_allow_html=True)
st.divider()
st.markdown(
    "<div style='text-align:center;font-size:0.7rem;color:#ccc;padding:0.5rem 0;'>"
    "Zee AI Supply Chain Solutions · Built by Zillay Husnian · Enterprise Optimization Engine"
    "</div>",
    unsafe_allow_html=True,
)
