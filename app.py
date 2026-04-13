import streamlit as st
import random
import time

# --- Page Config ---
st.set_page_config(page_title="Algorithm Lab", layout="wide", page_icon="🧪")

# --- CSS for Custom Coloring ---
st.markdown("""
    <style>
    .metric-best { color: #28a745; font-weight: bold; }
    .metric-avg { color: #fd7e14; font-weight: bold; }
    .metric-worst { color: #dc3545; font-weight: bold; }
    .logic-box { padding: 20px; border-radius: 10px; background-color: #f0f2f6; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- Sorting Logic (Generators) ---
def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                yield arr, j+1

def selection_sort(arr):
    for i in range(len(arr)):
        min_idx = i
        for j in range(i + 1, len(arr)):
            if arr[j] < arr[min_idx]:
                min_idx = j
            yield arr, j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]

def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
            yield arr, j
        arr[j + 1] = key
        yield arr, i

def merge_sort(arr, start, end):
    if end <= start: return
    mid = (start + end) // 2
    yield from merge_sort(arr, start, mid)
    yield from merge_sort(arr, mid + 1, end)
    yield from merge(arr, start, mid, end)

def merge(arr, start, mid, end):
    L = arr[start:mid+1]
    R = arr[mid+1:end+1]
    i = j = 0
    for k in range(start, end + 1):
        if i < len(L) and (j >= len(R) or L[i] <= R[j]):
            arr[k] = L[i]
            i += 1
        else:
            arr[k] = R[j]
            j += 1
        yield arr, k

def quick_sort(arr, start, end):
    if start >= end: return
    pivot = arr[end]
    p_idx = start
    for i in range(start, end):
        if arr[i] < pivot:
            arr[i], arr[p_idx] = arr[p_idx], arr[i]
            p_idx += 1
        yield arr, i
    arr[end], arr[p_idx] = arr[p_idx], arr[end]
    yield arr, p_idx
    yield from quick_sort(arr, start, p_idx - 1)
    yield from quick_sort(arr, p_idx + 1, end)

def heap_sort(arr):
    n = len(arr)
    def heapify(n, i):
        largest = i
        l, r = 2*i + 1, 2*i + 2
        if l < n and arr[i] < arr[l]: largest = l
        if r < n and arr[largest] < arr[r]: largest = r
        if largest != i:
            arr[i], arr[largest] = arr[largest], arr[i]
            yield arr, largest
            yield from heapify(n, largest)
    for i in range(n // 2 - 1, -1, -1): yield from heapify(n, i)
    for i in range(n-1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        yield arr, i
        yield from heapify(i, 0)

# --- Sidebar ---
st.sidebar.title("🛠️ Settings")
algo = st.sidebar.selectbox("Select Algorithm", ["Quick Sort", "Merge Sort", "Heap Sort", "Insertion Sort", "Bubble Sort", "Selection Sort"])
array_size = st.sidebar.slider("Data Points", 10, 100, 50)
speed = st.sidebar.select_slider("Animation Speed", options=["Slow", "Normal", "Fast"], value="Fast")
speed_map = {"Slow": 0.2, "Normal": 0.05, "Fast": 0.01}

# --- Algorithm Metadata ---
meta = {
    "Bubble Sort": {"best": "O(n)", "avg": "O(n^2)", "worst": "O(n^2)", "desc": "Swaps adjacent items. Simple but inefficient for large data."},
    "Selection Sort": {"best": "O(n^2)", "avg": "O(n^2)", "worst": "O(n^2)", "desc": "Finds the minimum and moves it to the front. Always O(n²) because it scans everything."},
    "Insertion Sort": {"best": "O(n)", "avg": "O(n^2)", "worst": "O(n^2)", "desc": "Builds a sorted list one item at a time. Very fast for nearly sorted data."},
    "Merge Sort": {"best": "O(n log n)", "avg": "O(n log n)", "worst": "O(n log n)", "desc": "Stable, divide-and-conquer. Splitting and merging gives consistent performance."},
    "Quick Sort": {"best": "O(n log n)", "avg": "O(n log n)", "worst": "O(n^2)", "desc": "Uses a pivot. Usually the fastest in practice, but worst-case is O(n²) with bad pivots."},
    "Heap Sort": {"best": "O(n log n)", "avg": "O(n log n)", "worst": "O(n log n)", "desc": "Uses a binary heap structure. Guaranteed O(n log n) with no extra memory needed."}
}

# --- Dashboard Layout ---
st.title(f"Visualizing {algo}")

# 1. Complexity Cards
c1, c2, c3 = st.columns(3)
with c1: st.markdown(f"**Best Case** <br> <span class='metric-best'>{meta[algo]['best']}</span>", unsafe_allow_html=True)
with c2: st.markdown(f"**Average Case** <br> <span class='metric-avg'>{meta[algo]['avg']}</span>", unsafe_allow_html=True)
with c3: st.markdown(f"**Worst Case** <br> <span class='metric-worst'>{meta[algo]['worst']}</span>", unsafe_allow_html=True)

st.write(f"**Description:** {meta[algo]['desc']}")

# 2. Graph Explanation
with st.expander("📖 What does this graph represent?"):
    st.write("""
    - **Y-Axis (Height):** Represents the value of the number. Taller bars = Higher values.
    - **X-Axis (Position):** Represents the index in the array.
    - **The Animation:** Shows the physical swapping of indices as the algorithm makes decisions.
    """)

# 3. Main Logic Execution
if 'array' not in st.session_state or st.sidebar.button("Reset Data"):
    st.session_state.array = random.sample(range(1, 150), array_size)

chart = st.empty()
chart.bar_chart(st.session_state.array)

if st.button("▶️ Run Algorithm"):
    data = st.session_state.array.copy()
    
    if algo == "Bubble Sort": gen = bubble_sort(data)
    elif algo == "Selection Sort": gen = selection_sort(data)
    elif algo == "Insertion Sort": gen = insertion_sort(data)
    elif algo == "Merge Sort": gen = merge_sort(data, 0, len(data)-1)
    elif algo == "Quick Sort": gen = quick_sort(data, 0, len(data)-1)
    else: gen = heap_sort(data)

    for updated_data, current_index in gen:
        chart.bar_chart(updated_data)
        time.sleep(speed_map[speed])
    
    st.success(f"{algo} Complete!")
