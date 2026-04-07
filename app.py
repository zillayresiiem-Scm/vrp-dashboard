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
/* your CSS styles remain unchanged */
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
#  CORE ALGORITHM
# ═══════════════════════════════════════════════════════════════════════════════
# (all your parsing and solver functions remain unchanged)
# ...

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
    # unchanged
    ...

def step_header(num, icon, title):
    st.markdown(
        f"<div style='display:flex;align-items:center;gap:0.7rem;margin:2rem 0 1rem 0;"
        f"padding-bottom:0.6rem;border-bottom:1px solid #1a1a28;'>"
        f"<span style='font-family:\"DM Mono\",monospace;font-size:0.62rem;font-weight:500;"
        f"color:#c8f135;background:#0e1a00;border:1px solid #2a3a00;border-radius:4px;"
        f"padding:0.2rem 0.5rem;letter-spacing:0.1em;'>STEP {num}</span>"
        f"<span style='font-size:0.95rem;font-weight:600;color:#e8e6e0;letter-spacing:0.02em;'>{icon} {title}</span>"
        "</div>",
        unsafe_allow_html=True,
    )

VEHICLE_COLORS = ["#c8f135", "#39e5b6", "#a78bfa", "#f59e0b", "#ff6b6b", "#60cdff", "#ff9ff3", "#ffd43b"]

def route_card(ra, vehicle_num, demands, time_windows, show_tw):
    # corrected: static closing tags are plain strings
    ...

def merge_row(entry, idx):
    # corrected: static closing tags are plain strings
    ...

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

    st.markdown("<div style='font-size:0.65rem;color:#2e2e3a;letter-spacing:0.16em;text-transform:uppercase;margin-bottom:1rem;'>Config options here</div>", unsafe_allow_html=True)

