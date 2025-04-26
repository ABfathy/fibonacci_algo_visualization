import tkinter as tk
from algorithms import fib_recursive_count, fib_dp_count
from visualize import TreeVisualizer

def zoom_factory(canvas):
    canvas.scale_factor = 1.0
    
    def zoom(event):
        cf = canvas.scale_factor
        if hasattr(event, "delta"):
            delta = event.delta
        elif hasattr(event, "num") and event.num == 4:
            delta = 120
        elif hasattr(event, "num") and event.num == 5:
            delta = -120
        else:
            delta = 0
            
        factor = 1.1 if delta > 0 else 0.9
        new = cf * factor
        
        if new < 1.0:
            factor = 1.0 / cf
            new = 1.0
            
        canvas.scale("all", event.x, event.y, factor, factor)
        canvas.scale_factor = new
        canvas.configure(scrollregion=canvas.bbox("all"))
        
    return zoom

def add_pan_support(canvas):
    canvas.last_x = 0
    canvas.last_y = 0
    
    def start_pan(event):
        canvas.scan_mark(event.x, event.y)
        canvas.last_x = event.x
        canvas.last_y = event.y
        canvas.config(cursor="fleur")
    
    def do_pan(event):
        canvas.scan_dragto(event.x, event.y, gain=1)
        canvas.last_x = event.x
        canvas.last_y = event.y
    
    def end_pan(event):
        canvas.config(cursor="")
    
    canvas.bind("<ButtonPress-1>", start_pan)
    canvas.bind("<B1-Motion>", do_pan)
    canvas.bind("<ButtonRelease-1>", end_pan)

def make_zoom_buttons(frame, canvas):
    def on_zoom_in():
        cf = canvas.scale_factor
        f = 1.1
        new = cf * f
        canvas.scale("all", canvas.winfo_width()/2, canvas.winfo_height()/2, f, f)
        canvas.scale_factor = new
        canvas.configure(scrollregion=canvas.bbox("all"))
        
    def on_zoom_out():
        cf = canvas.scale_factor
        f = 0.9
        new = cf * f
        if new < 1.0:
            f = 1.0 / cf
            new = 1.0
        canvas.scale("all", canvas.winfo_width()/2, canvas.winfo_height()/2, f, f)
        canvas.scale_factor = new
        canvas.configure(scrollregion=canvas.bbox("all"))
        
    def on_reset_view():
        # Reset to original view
        canvas.scale("all", 0, 0, 1.0/canvas.scale_factor, 1.0/canvas.scale_factor)
        canvas.scale_factor = 1.0
        canvas.xview_moveto(0)
        canvas.yview_moveto(0)
        canvas.configure(scrollregion=canvas.bbox("all"))
        
    tk.Button(frame, text="+", width=3, command=on_zoom_in).pack(side="left", padx=2)
    tk.Button(frame, text="–", width=3, command=on_zoom_out).pack(side="left", padx=2)
    tk.Button(frame, text="Reset View", command=on_reset_view).pack(side="left", padx=10)

def run_fib(is_dp):
    try:
        n = int(entry.get())
        if n < 0:
            output.config(text="Please enter a non-negative integer.")
            return
    except ValueError:
        output.config(text="Enter a valid integer.")
        return
        
    canvas.delete("all")
    visualizer.reset()
    window.update_idletasks()
    
    result_r, calls_r = fib_recursive_count(n)
    result_dp, calls_dp = fib_dp_count(n)
    diff = calls_r - calls_dp
    
    if is_dp:
        visualizer.draw_tree(n, memoization=True)
        variant, result, displayed_calls = "Dynamic Programming", result_dp, calls_dp
    else:
        visualizer.draw_tree(n, memoization=False)
        variant, result, displayed_calls = "Recursive", result_r, calls_r
        
    output.config(text=(
        f"{variant} Result: {result}\n"
        f"Recursive calls total: {calls_r}\n"
        f"Memoized calls total: {calls_dp}\n"
        f"Step difference: {diff}"
    ))
    
    # Make sure scrollregion is updated after drawing
    canvas.configure(scrollregion=canvas.bbox("all"))

window = tk.Tk()
window.title("Fibonacci Visualization")
window.geometry("900x700")
window.configure(bg="#f0f0f0")

frame = tk.Frame(window, bg="#f0f0f0")
frame.pack(pady=10)

tk.Label(frame, text="Enter n:", font=("Helvetica", 14), bg="#f0f0f0").pack(side="left")
entry = tk.Entry(frame, font=("Helvetica", 14), width=5)
entry.pack(side="left", padx=5)
entry.insert(0, "10")

tk.Button(frame, text="Run Recursive", font=("Helvetica", 12), command=lambda: run_fib(False)).pack(side="left", padx=5)
tk.Button(frame, text="Run Dynamic Programming", font=("Helvetica", 12), command=lambda: run_fib(True)).pack(side="left", padx=5)

# Create a frame for the canvas with scrollbars
canvas_frame = tk.Frame(window)
canvas_frame.pack(fill=tk.BOTH, expand=True, pady=10)

# Create horizontal and vertical scrollbars
h_scrollbar = tk.Scrollbar(canvas_frame, orient=tk.HORIZONTAL)
h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)

v_scrollbar = tk.Scrollbar(canvas_frame)
v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Create canvas with scrollbar support
canvas = tk.Canvas(canvas_frame, width=850, height=500, bg="white",
                  xscrollcommand=h_scrollbar.set, yscrollcommand=v_scrollbar.set)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Configure scrollbars to work with canvas
h_scrollbar.config(command=canvas.xview)
v_scrollbar.config(command=canvas.yview)

visualizer = TreeVisualizer(canvas, max_levels=8)

# Add zoom functionality
zoom = zoom_factory(canvas)
canvas.bind("<MouseWheel>", zoom)  # Windows and MacOS
canvas.bind("<Button-4>", zoom)     # Linux - scroll up
canvas.bind("<Button-5>", zoom)     # Linux - scroll down

# Add panning support
add_pan_support(canvas)

# Configure canvas scrolling region
canvas.configure(scrollregion=canvas.bbox("all"))

zoom_frame = tk.Frame(window, bg="#f0f0f0")
zoom_frame.pack()
make_zoom_buttons(zoom_frame, canvas)

output = tk.Label(window, text="", justify=tk.LEFT, font=("Helvetica", 14), bg="#f0f0f0")
output.pack(pady=5)

tk.Label(window, text="Time Complexity -> Recursive: O(2^n) | DP: O(n)", font=("Helvetica", 14, "italic"), bg="#f0f0f0").pack()

# Status bar with instructions
status_bar = tk.Label(window, text="Navigation: Click and drag to pan | Mouse wheel to zoom | Reset button to restore view", 
                      font=("Helvetica", 10), bd=1, relief=tk.SUNKEN, anchor=tk.W)
status_bar.pack(side=tk.BOTTOM, fill=tk.X)

window.mainloop()