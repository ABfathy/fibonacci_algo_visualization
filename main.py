import tkinter as tk
from algorithms import fib_recursive, fib_dp
from performance import measure_time
from visualize import TreeVisualizer


def run_fibonacci(is_dp):
    try:
        n = int(entry.get())
        visualizer.reset()
        canvas.delete("all")

        # Measure both
        result_r, time_r = measure_time(fib_recursive, n)
        result_dp, time_dp = measure_time(fib_dp, n)

        # Draw selected tree
        if is_dp:
            visualizer.draw_tree(n, 450, 50, 0, memoization=True)
            variant = "Dynamic Programming"
        else:
            visualizer.draw_tree(n, 450, 50, 0, memoization=False)
            variant = "Recursive"

        # Compute time difference
        time_diff = abs(time_r - time_dp)

        output.config(text=(
            f"{variant} Variant Result: " + str(result_dp if is_dp else result_r) + "\n"
            f"Recursive Time: {time_r:.6f} sec\n"
            f"DP Time: {time_dp:.6f} sec\n"
            f"Time Difference: {time_diff:.6f} sec"
        ))
    except ValueError:
        output.config(text="Please enter a valid number.")


# GUI Setup
window = tk.Tk()
window.title("Fibonacci Visualization - Recursive vs DP")
window.geometry("900x750")
window.configure(bg="#f0f0f0")

frame_top = tk.Frame(window, bg="#f0f0f0")
frame_top.pack(pady=10)

title = tk.Label(
    frame_top, text="Fibonacci Visualization", font=("Helvetica", 20, "bold"), bg="#f0f0f0"
)
title.pack()

entry_label = tk.Label(
    frame_top, text="Enter n:", font=("Helvetica", 14), bg="#f0f0f0"
)
entry_label.pack(side="left", padx=5)

entry = tk.Entry(frame_top, font=("Helvetica", 14), width=5)
entry.pack(side="left", padx=5)

btn_recursive = tk.Button(
    frame_top, text="Run Recursive", font=("Helvetica", 12), command=lambda: run_fibonacci(False)
)
btn_recursive.pack(side="left", padx=10)

btn_dp = tk.Button(
    frame_top, text="Run Dynamic Programming", font=("Helvetica", 12), command=lambda: run_fibonacci(True)
)
btn_dp.pack(side="left", padx=10)

canvas = tk.Canvas(window, width=850, height=500, bg="white")
canvas.pack(pady=20)

output = tk.Label(window, text="", font=("Helvetica", 14), bg="#f0f0f0")
output.pack()

# Time Complexity Display
complexity = tk.Label(
    window,
    text="Time Complexity → Recursive: O(2^n)   |   DP: O(n)",
    font=("Helvetica", 14, "italic"),
    bg="#f0f0f0"
)
complexity.pack(pady=10)

visualizer = TreeVisualizer(canvas)

window.mainloop()
