import streamlit as st
import numpy as np
import plotly.graph_objects as go

# --- Page Configuration ---
st.set_page_config(page_title="Algorithm Performance Lab", layout="wide")

st.title("📈 Sorting Algorithm Complexity Dashboard")
st.markdown("""
This dashboard visualizes the **mathematical efficiency** of sorting algorithms. 
Instead of watching bars move, we are looking at how much "work" a computer does as the input size grows.
""")

# --- Sidebar ---
st.sidebar.header("Select Algorithm")
algo = st.sidebar.selectbox(
    "Choose an Algorithm",
    ["Bubble Sort", "Selection Sort", "Insertion Sort", "Merge Sort", "Quick Sort", "Heap Sort"]
)

# --- Complexity Data Generation ---
n = np.linspace(1, 100, 100)

def get_complexities(name):
    # O(n^2) = n**2, O(n log n) = n * log2(n), O(n) = n
    if name == "Bubble Sort":
        return n, n**2, n**2, "Optimized Bubble Sort can reach O(n) if data is already sorted."
    elif name == "Selection Sort":
        return n**2, n**2, n**2, "Selection sort always scans the entire remaining list, so all cases are O(n²)."
    elif name == "Insertion Sort":
        return n, n**2, n**2, "Very efficient for nearly sorted data (O(n))."
    elif name == "Merge Sort":
        val = n * np.log2(n)
        return val, val, val, "Merge Sort is extremely consistent. It always takes O(n log n)."
    elif name == "Quick Sort":
        avg_best = n * np.log2(n)
        return avg_best, avg_best, n**2, "Quick Sort is usually fast, but hits O(n²) if the pivot is poorly chosen."
    elif name == "Heap Sort":
        val = n * np.log2(n)
        return val, val, val, "Heap Sort is guaranteed O(n log n) and doesn't use extra memory."

best, avg, worst, desc = get_complexities(algo)

# --- Plotting ---
fig = go.Figure()

# Worst Case - Red
fig.add_trace(go.Scatter(x=n, y=worst, name='Worst Case',
                         line=dict(color='#dc3545', width=4)))

# Average Case - Orange
fig.add_trace(go.Scatter(x=n, y=avg, name='Average Case',
                         line=dict(color='#fd7e14', width=4, dash='dash')))

# Best Case - Green
fig.add_trace(go.Scatter(x=n, y=best, name='Best Case',
                         line=dict(color='#28a745', width=4, dash='dot')))

fig.update_layout(
    title=f"Time Complexity Growth: {algo}",
    xaxis_title="Input Size (Number of Items)",
    yaxis_title="Operations (Time Taken)",
    legend_title="Scenarios",
    hovermode="x unified",
    template="plotly_white",
    height=600
)

# --- Display Layout ---
col1, col2 = st.columns([3, 1])

with col1:
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Analysis")
    st.info(desc)
    st.write("**Color Guide:**")
    st.success("🟢 **Green (Best):** Minimum time needed.")
    st.warning("🟠 **Orange (Avg):** Usual time expected.")
    st.error("🔴 **Red (Worst):** Maximum time possible.")

st.divider()

# --- Technical Comparison Table ---
st.subheader("Quick Reference Table")
comparison_data = {
    "Algorithm": ["Bubble", "Selection", "Insertion", "Merge", "Quick", "Heap"],
    "Best": ["O(n)", "O(n²)", "O(n)", "O(n log n)", "O(n log n)", "O(n log n)"],
    "Average": ["O(n²)", "O(n²)", "O(n²)", "O(n log n)", "O(n log n)", "O(n log n)"],
    "Worst": ["O(n²)", "O(n²)", "O(n²)", "O(n log n)", "O(n²)", "O(n log n)"]
}
st.table(comparison_data)
