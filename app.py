import streamlit as st
import pandas as pd
import plotly.express as px

# --- Page Configuration ---
st.set_page_config(page_title="Algorithm Complexity Lab", layout="wide")

st.title("📊 Sorting Algorithm Complexity: Case-by-Case Analysis")
st.markdown("""
This dashboard shows the **specific Time Complexity** for each sorting algorithm across its Best, Average, and Worst scenarios.
The height of the bars represents the **Growth Rate** (how much slower it gets as data grows).
""")

# --- 1. Define Specific Complexity Data ---
# Map: Algo -> Case -> (Notation, Numerical Weight for Graph)
# Weights: O(n)=1, O(n log n)=2, O(n²)=3
data_map = {
    "Bubble Sort": {
        "Best": ("O(n)", 1), 
        "Average": ("O(n²)", 3), 
        "Worst": ("O(n²)", 3)
    },
    "Selection Sort": {
        "Best": ("O(n²)", 3), 
        "Average": ("O(n²)", 3), 
        "Worst": ("O(n²)", 3)
    },
    "Insertion Sort": {
        "Best": ("O(n)", 1), 
        "Average": ("O(n²)", 3), 
        "Worst": ("O(n²)", 3)
    },
    "Merge Sort": {
        "Best": ("O(n log n)", 2), 
        "Average": ("O(n log n)", 2), 
        "Worst": ("O(n log n)", 2)
    },
    "Quick Sort": {
        "Best": ("O(n log n)", 2), 
        "Average": ("O(n log n)", 2), 
        "Worst": ("O(n²)", 3)
    },
    "Heap Sort": {
        "Best": ("O(n log n)", 2), 
        "Average": ("O(n log n)", 2), 
        "Worst": ("O(n log n)", 2)
    }
}

# --- 2. Format Data for Plotly ---
records = []
for algo, cases in data_map.items():
    for case_type, (notation, weight) in cases.items():
        records.append({
            "Algorithm": algo,
            "Scenario": case_type,
            "Complexity": notation,
            "Growth Rate": weight
        })

df = pd.DataFrame(records)

# --- 3. Create the Visualization ---
fig = px.bar(
    df,
    x="Algorithm",
    y="Growth Rate",
    color="Scenario",
    barmode="group",
    text="Complexity",  # This puts the specific O() on the bar!
    color_discrete_map={'Best': '#28a745', 'Average': '#fd7e14', 'Worst': '#dc3545'},
    title="Comparison of Complexity Classes"
)

fig.update_layout(
    yaxis=dict(
        tickmode='array',
        tickvals=[1, 2, 3],
        ticktext=['Linear: O(n)', 'Log-Linear: O(n log n)', 'Quadratic: O(n²)'],
        title="Complexity Class (Higher is Slower)"
    ),
    height=600,
    template="plotly_white"
)
fig.update_traces(textposition='outside')

# --- 4. Display Layout ---
st.plotly_chart(fig, use_container_width=True)

st.subheader("📋 Detailed Complexity Reference Table")
# Format a clean table for the user
table_df = pd.DataFrame({
    "Algorithm": list(data_map.keys()),
    "Best Case": [data_map[a]["Best"][0] for a in data_map],
    "Average Case": [data_map[a]["Average"][0] for a in data_map],
    "Worst Case": [data_map[a]["Worst"][0] for a in data_map]
})
st.table(table_df)

st.info("""
**How to read this chart:**
* **Green Bars (O(n)):** The algorithm is 'efficient' and only looks at each item once.
* **Orange Bars (O(n log n)):** The algorithm uses 'divide and conquer' to stay fast even with large data.
* **Red Bars (O(n²)):** The algorithm is 'heavy' because it compares almost every item to every other item.
""")
