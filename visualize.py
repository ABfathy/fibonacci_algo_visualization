# visualize.py

import time
import math

class TreeVisualizer:
    # Increase default max_levels
    def __init__(self, canvas, max_levels=8, horiz_sp=1.5, vert_sp=1.3): # Changed default max_levels from 6 to 8
        """
        :param canvas: Tkinter Canvas to draw on
        :param max_levels: max depth before truncating / scaling
        :param horiz_sp: extra horizontal spacing multiplier
        :param vert_sp: extra vertical spacing multiplier
        """
        self.canvas      = canvas
        self.base_radius = 20
        self.base_gap    = 70
        self.max_levels  = max_levels # Now defaults to 8
        self.horiz_sp    = horiz_sp
        self.vert_sp     = vert_sp
        self.memo_color  = "lightblue"
        self.visited     = set()
        self.trunc_color = "lightgrey" # Color for truncated nodes

    def reset(self):
        """ Clear memo‐visit history """
        self.visited.clear()

    def draw_tree(self, n, memoization=False):
        """
        Kick off a new draw of Fibonacci(n).
        This ALWAYS resets visited and uses scaling + spacing.
        """
        # 1) compute zoom‐out scale (using logic from previous refinement)
        effective_depth = max(0, n) # Use n directly for depth estimation in Fib tree
        clamped_max_levels = max(1, self.max_levels)

        if effective_depth > clamped_max_levels:
             # Adjust scaling factor calculation slightly for better visual results
             scale = clamped_max_levels / float(effective_depth + 1) # Add 1 to avoid overly aggressive scaling
        else:
             scale = 1.0
        scale = min(1.0, scale)
        scale = max(0.05, scale)

        self.node_radius = self.base_radius * scale
        self.level_gap = self.base_gap * scale * self.vert_sp
        self.scale = scale
        self.visited.clear()

        # 2) start from top‐center
        try:
            width = self.canvas.winfo_width()
            if width <= 1: width = int(self.canvas.cget('width'))
        except tk.TclError:
             width = int(self.canvas.cget('width'))

        root_x = width / 2
        root_y = max(self.node_radius, 10) + 5

        # 3) draw recursively
        self._draw(n, root_x, root_y, level=0, memoization=memoization)
        self.canvas.update_idletasks()


    def _draw(self, n, x, y, level, memoization):
        """ Internal recursive drawer """
        r = self.node_radius
        draw_r = max(r, 1)
        font_size = max(7, int(10 * self.scale)) # Calculate font size once

        # --- MODIFIED TRUNCATION ---
        # Check if current level reaches the maximum allowed depth
        if level >= self.max_levels:
            # Draw the node with its number 'n' but in grey
            self.canvas.create_oval(x - draw_r, y - draw_r, x + draw_r, y + draw_r,
                                    fill=self.trunc_color, outline="grey") # Use specific truncation color
            self.canvas.create_text(x, y, text=str(n), # Show the number 'n'
                                    font=("Helvetica", font_size, "bold"), fill="black") # Black text
            return # Stop recursion here, DO NOT draw children
        # --- END MODIFIED TRUNCATION ---


        # pick color (only if not truncated)
        is_cached = memoization and n in self.visited
        if is_cached:
            color = self.memo_color
        else:
            # Base cases (n=0, n=1) can also have a distinct color if desired, e.g., lightyellow
            # Otherwise, use standard compute/recursive colors
             # if n <= 1:
             #    color = "lightyellow"
             # else:
             color = "lightgreen" if memoization else "lightcoral"

        # draw node
        self.canvas.create_oval(x - draw_r, y - draw_r, x + draw_r, y + draw_r, fill=color, outline="")
        self.canvas.create_text(x, y, text=str(n), font=("Helvetica", font_size, "bold"))

        # mark visited in DP mode *before* recursive calls for correct coloring logic
        if memoization and not is_cached:
            self.visited.add(n)

        # Base case or cached node: stop recursion down this path
        if n <= 1 or is_cached:
            return

        # --- Horizontal Offset Calculation (using logic from previous refinement) ---
        try:
            width = self.canvas.winfo_width()
            if width <= 1: width = int(self.canvas.cget('width'))
        except tk.TclError:
            width = int(self.canvas.cget('width'))

        exponent = level + 1
        # Adjusted base_offset formula slightly for potentially better spacing
        base_offset = (width / 2.0) / (1.8 ** exponent)
        scaled_offset = base_offset * self.scale
        min_r = max(draw_r, 1)
        min_off = (min_r * 2) * self.horiz_sp
        offset = max(scaled_offset, min_off)
        # --- End of Offset Calculation ---

        # Child positions
        ny = y + self.level_gap
        lx = x - offset
        rx = x + offset

        # Draw lines first
        self.canvas.create_line(x, y + draw_r, lx, ny - draw_r, fill="grey")
        self.canvas.create_line(x, y + draw_r, rx, ny - draw_r, fill="grey")

        # Recursive calls for children
        self._draw(n - 1, lx, ny, level + 1, memoization)
        self._draw(n - 2, rx, ny, level + 1, memoization)