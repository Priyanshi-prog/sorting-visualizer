import streamlit as st
import random
import time
import plotly.graph_objects as go

# --- Page Config ---
st.set_page_config(page_title="Algorithm Lab 2.0", layout="wide")

# --- Sorting Logic with Color Tracking ---
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            # Highlight bars being compared (Red)
            colors = ['#636EFA'] * len(arr)
            colors[j] = colors[j+1] = '#EF553B' 
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
            yield arr, colors
        # Mark the end as sorted (Green)
        # (Simplified coloring for animation)

def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and key < arr[j]:
            colors = ['#636EFA'] * len(arr)
            colors[j+1] = '#EF553B' # Active
            arr[j + 1] = arr[j]
            j -= 1
            yield arr, colors
        arr[j + 1] = key
        yield arr, ['#00CC96'] * len(arr)

def quick_sort(arr, start, end):
    if start >= end: return
    pivot = arr[end]
    p_idx = start
    for i in range(start, end):
        colors = ['#636EFA'] * len(arr)
        colors[end] = '#AB63FA' # Pivot (Purple)
        colors[i] = '#EF553B' # Comparing
        if arr[i] < pivot:
            arr[i], arr[p_idx] = arr[p_idx], arr[i]
            p_idx += 1
        yield arr, colors
    arr[end], arr[p_idx] = arr[p_idx], arr[end]
    yield arr, colors
    yield from quick_sort(arr, start, p_idx - 1)
    yield from quick_sort(arr, p_idx + 1, end)

# (Other algorithms follow similar yield patterns...)

# --- Dashboard Layout ---
st.title("🧪 Visual Algorithm Laboratory")

col1, col2 = st.columns([1, 3])

with col1:
    algo = st.selectbox("Select Algorithm", ["Bubble Sort", "Insertion Sort", "Quick Sort"])
    size = st.slider("Data Size", 10, 50, 20)
    speed = st.select_slider("Speed", options=[0.5, 0.1, 0.01], value=0.1)
    
    st.info("""
    **Color Key:**
    - 🔵 **Blue**: Unsorted
    - 🔴 **Red**: Currently comparing/moving
    - 🟣 **Purple**: Pivot point (Quick Sort)
    - 🟢 **Green**: Completed
    """)

if 'data' not in st.session_state or st.button("New Data"):
    st.session_state.data = random.sample(range(1, 100), size)

plot_spot = st.empty()

def update_plot(arr, colors):
    fig = go.Figure(go.Bar(
        x=list(range(len(arr))), 
        y=arr, 
        marker_color=colors
    ))
    fig.update_layout(
        margin=dict(l=20, r=20, t=20, b=20),
        height=400,
        xaxis=dict(visible=False),
        yaxis=dict(visible=False)
    )
    plot_spot.plotly_chart(fig, use_container_width=True)

# Initial Plot
update_plot(st.session_state.data, ['#636EFA'] * size)

if st.button("Start Animation"):
    data = st.session_state.data.copy()
    if algo == "Bubble Sort": gen = bubble_sort(data)
    elif algo == "Insertion Sort": gen = insertion_sort(data)
    else: gen = quick_sort(data, 0, len(data)-1)

    for updated_arr, current_colors in gen:
        update_plot(updated_arr, current_colors)
        time.sleep(speed)
    
    # Final Green state
    update_plot(data, ['#00CC96'] * len(data))
