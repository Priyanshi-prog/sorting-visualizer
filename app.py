import streamlit as st
import random
import time

# --- Page Configuration ---
st.set_page_config(
    page_title="Algorithm Visualizer",
    page_icon="📊",
    layout="wide"
)

# --- Sorting Algorithms (Generators for Animation) ---

def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                yield arr

def selection_sort(arr):
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
        yield arr

def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
            yield arr
        arr[j + 1] = key
        yield arr

def merge_sort(arr, start, end):
    if end <= start:
        return
    mid = start + (end - start) // 2
    yield from merge_sort(arr, start, mid)
    yield from merge_sort(arr, mid + 1, end)
    yield from merge(arr, start, mid, end)

def merge(arr, start, mid, end):
    merged = []
    leftIdx = start
    rightIdx = mid + 1
    while leftIdx <= mid and rightIdx <= end:
        if arr[leftIdx] < arr[rightIdx]:
            merged.append(arr[leftIdx])
            leftIdx += 1
        else:
            merged.append(arr[rightIdx])
            rightIdx += 1
    while leftIdx <= mid:
        merged.append(arr[leftIdx])
        leftIdx += 1
    while rightIdx <= end:
        merged.append(arr[rightIdx])
        rightIdx += 1
    for i, val in enumerate(merged):
        arr[start + i] = val
        yield arr

def quick_sort(arr, start, end):
    if start >= end:
        return
    pivot = arr[end]
    pivot_idx = start
    for i in range(start, end):
        if arr[i] < pivot:
            arr[i], arr[pivot_idx] = arr[pivot_idx], arr[i]
            pivot_idx += 1
        yield arr
    arr[end], arr[pivot_idx] = arr[pivot_idx], arr[end]
    yield arr
    yield from quick_sort(arr, start, pivot_idx - 1)
    yield from quick_sort(arr, pivot_idx + 1, end)

def heap_sort(arr):
    n = len(arr)
    def heapify(n, i):
        largest = i
        l, r = 2 * i + 1, 2 * i + 2
        if l < n and arr[i] < arr[l]: largest = l
        if r < n and arr[largest] < arr[r]: largest = r
        if largest != i:
            arr[i], arr[largest] = arr[largest], arr[i]
            yield arr
            yield from heapify(n, largest)
            
    for i in range(n // 2 - 1, -1, -1):
        yield from heapify(n, i)
    for i in range(n - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        yield arr
        yield from heapify(i, 0)

# --- Sidebar UI ---
st.sidebar.header("⚙️ Configuration")
algo_name = st.sidebar.selectbox(
    "Choose Algorithm",
    ["Bubble Sort", "Selection Sort", "Insertion Sort", "Merge Sort", "Quick Sort", "Heap Sort"]
)

size = st.sidebar.slider("Array Size", 5, 100, 50)
speed = st.sidebar.select_slider("Animation Speed", options=["Slow", "Normal", "Fast", "Instant"], value="Fast")

speed_delay = {"Slow": 0.3, "Normal": 0.1, "Fast": 0.02, "Instant": 0.001}

# --- Main Dashboard ---
st.title("Sorting Algorithm Dashboard")
st.markdown(f"Currently visualizing: **{algo_name}**")

# Info Box
algo_info = {
    "Bubble Sort": "$O(n^2)$",
    "Selection Sort": "$O(n^2)$",
    "Insertion Sort": "$O(n^2)$",
    "Merge Sort": "$O(n \log n)$",
    "Quick Sort": "$O(n \log n)$",
    "Heap Sort": "$O(n \log n)$"
}
st.info(f"Average Time Complexity: {algo_info[algo_name]}")

# Data State
if 'arr' not in st.session_state or st.sidebar.button("Generate New Array"):
    st.session_state.arr = random.sample(range(1, 101), size)

# Plotting
plot_placeholder = st.empty()
plot_placeholder.bar_chart(st.session_state.arr)

if st.button("▶️ Start Sorting"):
    arr_to_sort = st.session_state.arr.copy()
    
    # Select Generator
    if algo_name == "Bubble Sort": gen = bubble_sort(arr_to_sort)
    elif algo_name == "Selection Sort": gen = selection_sort(arr_to_sort)
    elif algo_name == "Insertion Sort": gen = insertion_sort(arr_to_sort)
    elif algo_name == "Merge Sort": gen = merge_sort(arr_to_sort, 0, len(arr_to_sort)-1)
    elif algo_name == "Quick Sort": gen = quick_sort(arr_to_sort, 0, len(arr_to_sort)-1)
    else: gen = heap_sort(arr_to_sort)

    for updated_arr in gen:
        plot_placeholder.bar_chart(updated_arr)
        time.sleep(speed_delay[speed])
    
    st.success("Sorting Complete!")
