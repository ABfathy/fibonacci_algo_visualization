# main.py

import tkinter as tk
from algorithms import fib_recursive_count, fib_dp_count
from visualize import TreeVisualizer

def run_fib(is_dp):
    # 1) parse input
    try:
        n = int(entry.get())
    except ValueError:
        output.config(text="❌ Enter a valid integer.")
        return

    # 2) clear old drawing & reset
    canvas.delete("all")
    visualizer.reset()

    # 3) compute call-counts
    result_r, calls_r   = fib_recursive_count(n)
    result_dp, calls_dp = fib_dp_count(n)
    diff = abs(calls_r - calls_dp)

    # 4) draw selected tree
    if is_dp:
        visualizer.draw_tree(n, memoization=True)
        variant = "Dynamic Programming"
        result  = result_dp
    else:
        visualizer.draw_tree(n, memoization=False)
        variant = "Recursive"
        result  = result_r

    # 5) update stats label
    output.config(text=(
        f"▶️ {variant} Result: {result}\n"
        f"🔁 Recursive calls: {calls_r}\n"
        f"💡 Memoized calls: {calls_dp}\n"
        f"Δ Step difference: {diff}"
    ))

# --- GUI setup ---
window = tk.Tk()
window.title("Fibonacci Visualization")
window.geometry("900x700")
window.configure(bg="#f0f0f0")

# Controls
frame = tk.Frame(window, bg="#f0f0f0")
frame.pack(pady=10)

tk.Label(frame, text="Enter n:", font=("Helvetica", 14), bg="#f0f0f0").pack(side="left")
entry = tk.Entry(frame, font=("Helvetica", 14), width=5)
entry.pack(side="left", padx=5)

btn_rec = tk.Button(frame, text="Run Recursive", font=("Helvetica", 12),
                    command=lambda: run_fib(False))
btn_rec.pack(side="left", padx=5)
btn_dp = tk.Button(frame, text="Run Dynamic Programming", font=("Helvetica", 12),
                   command=lambda: run_fib(True))
btn_dp.pack(side="left", padx=5)

# Canvas & Visualizer
canvas = tk.Canvas(window, width=850, height=500, bg="white")
canvas.pack(pady=20)
visualizer = TreeVisualizer(canvas, max_levels=6)

# Output & Complexity
output = tk.Label(window, text="", font=("Helvetica", 14), bg="#f0f0f0")
output.pack(pady=5)

tk.Label(window,
         text="Time Complexity → Recursive: O(2^n)   |   DP: O(n)",
         font=("Helvetica", 14, "italic"),
         bg="#f0f0f0").pack()

window.mainloop()
