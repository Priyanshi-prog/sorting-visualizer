import streamlit as st
import numpy as np
import plotly.express as px
import pandas as pd

# --- Page Configuration ---
st.set_page_config(page_title="Algorithm Comparison Lab", layout="wide")

st.title("📊 Comparing Sorting Algorithm 'Costs' (N=100)")
st.markdown("""
This dashboard compares the **work required** by different algorithms to sort a fixed-size list of **100 items**.
Instead of watching growth curves, we are mapping the theoretical Big O complexity to a single numerical "operation cost"
to create a direct comparison.

To make the vast difference between $O(n)$ and $O(n^2)$ viewable, this graph uses a **Logarithmic Scale** for the Y-axis.
""")

# --- 1. Define Representative Costs for a Fixed N=100 ---
# This turns the mathematical abstraction into a number for comparison.
N = 100
# O(n) is approximately N operations
COST_N = N
# O(n log2 n) is approximately N * log2(N)
COST_N_LOGN = round(N * np.log2(N))  # ~664 for N=100
# O(n^2) is approximately N^2 operations
COST_N_SQUARED = N**2 # 10,000 for N=100

# --- 2. Map Algorithms to Specific Cases and Costs ---
# Define a dictionary for each algo: mapping case -> complexity class -> cost
algorithm_data = {
    "Bubble Sort":     {"Best": COST_N,         "Average": COST_N_SQUARED,  "Worst": COST_N_SQUARED},
    "Selection Sort":  {"Best": COST_N_SQUARED, "Average": COST_N_SQUARED,  "Worst": COST_N_SQUARED},
    "Insertion Sort":  {"Best": COST_N,         "Average": COST_N_SQUARED,  "Worst": COST_N_SQUARED},
    "Merge Sort":      {"Best": COST_N_LOGN,    "Average": COST_N_LOGN,     "Worst": COST_N_LOGN},
    "Quick Sort":      {"Best": COST_N_LOGN,    "Average": COST_N_LOGN,     "Worst": COST_N_SQUARED},
    "Heap Sort":       {"Best": COST_N_LOGN,    "Average": COST_N_LOGN,     "Worst": COST_N_LOGN}
}

# --- 3. Create a DataFrame for Plotly Express ---
plot_data = []
for algo_name, cases in algorithm_data.items():
    for case_type, cost_value in cases.items():
        plot_data.append({
            "Algorithm": algo_name,
            "Scenario": case_type,
            "Operations (Cost)": cost_value
        })

df = pd.DataFrame(plot_data)

# --- 4. Plot the Clustered Bar Chart ---
color_map = {
    'Best':    '#28a745',  # Green
    'Average': '#fd7e14',  # Orange
    'Worst':   '#dc3545'   # Red
}

fig = px.bar(
    df, 
    x="Algorithm", 
    y="Operations (Cost)", 
    color="Scenario",
    barmode="group",
    color_discrete_map=color_map,
    title=f"Theoretical Operation Cost for Sorting 100 Random Items",
    log_y=True,  # IMPORTANT: Uses logarithmic scale
    text_auto='.2s', # Show values above bars
    template="plotly_white"
)

fig.update_layout(
    xaxis_title="Sorting Algorithm",
    yaxis_title="Operations (Logarithmic Scale)",
    yaxis_tickformat="s",
    legend_title="Complexity Case",
    font=dict(size=14),
    height=600
)

# --- Display Layout ---
col1, col2 = st.columns([3, 1])

with col1:
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Analysis & Interpretation")
    st.info("""
    **Understanding the Log Scale (Y-Axis):**
    On a linear scale, a cost of 100 ($O(n)$) is a tiny speck next to 10,000 ($O(n^2)$). We use a logarithmic scale to make all the bars viewable. Equal steps on the Y-axis represent a factor of 10x growth.
    """)
    st.write("**Key Observations:**")
    st.success("🟢 **Green (Best):** Shows the lowest bar (cheapest). Note how Selection sort has no low bar.")
    st.warning("🟠 **Orange (Avg):** Notice how some algorithms (Merge, Heap) are identical to their worst case.")
    st.error("🔴 **Red (Worst):** Shows the theoretical maximum cost. This is why O(n log n) is preferred for large data.")

st.markdown("---")
st.subheader("Technical Reference: Complexity to Cost Mapping (for N=100)")
col3, col4, col5 = st.columns(3)
with col3: st.metric("$O(n)$ Cost (Best Case)", COST_N)
with col4: st.metric("$O(n \log n)$ Cost (Average Case)", COST_N_LOGN)
with col5: st.metric("$O(n^2)$ Cost (Worst Case)", COST_N_SQUARED)
