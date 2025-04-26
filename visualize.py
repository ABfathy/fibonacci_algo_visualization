# visualize.py

import tkinter as tk
import time

class TreeVisualizer:
    def __init__(self, canvas):
        self.canvas = canvas
        self.node_radius = 20
        self.level_gap = 70
        self.memo_color = "lightblue"
        self.visited = {}

    def draw_tree(self, n, x, y, level=0, memoization=False):
        # Determine node color
        if memoization and n in self.visited:
            color = self.memo_color
        else:
            color = "lightgreen" if memoization else "lightcoral"

        # Draw node circle and label
        self.canvas.create_oval(
            x - self.node_radius, y - self.node_radius,
            x + self.node_radius, y + self.node_radius,
            fill=color, outline=""
        )
        self.canvas.create_text(x, y, text=str(n), font=("Helvetica", 10, "bold"))
        self.canvas.update()
        time.sleep(0.3)

        # Mark visited for memo
        if memoization:
            self.visited[n] = True

        # Stop at leaf
        if n <= 1:
            return

        # Compute dynamic horizontal offset based on level
        width = self.canvas.winfo_width()
        offset = width / (2 ** (level + 2))

        # Left child
        left_x = x - offset
        left_y = y + self.level_gap
        self.canvas.create_line(
            x, y + self.node_radius,
            left_x, left_y - self.node_radius,
            smooth=True
        )
        self.draw_tree(n - 1, left_x, left_y, level + 1, memoization)

        # Right child
        right_x = x + offset
        right_y = y + self.level_gap
        self.canvas.create_line(
            x, y + self.node_radius,
            right_x, right_y - self.node_radius,
            smooth=True
        )
        self.draw_tree(n - 2, right_x, right_y, level + 1, memoization)

    def reset(self):
        self.canvas.delete("all")
        self.visited = {}
