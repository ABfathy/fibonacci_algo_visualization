import tkinter as tk
import math

class TreeVisualizer:
    def __init__(self, canvas, max_levels=8):
        self.canvas = canvas
        self.max_levels = max_levels
        self.base_radius = 20    # maximum radius
        self.memo_color = "lightblue"
        self.visited = set()

    def reset(self):
        self.visited.clear()

    def draw_tree(self, n, memoization=False):
        # clear and prep
        self.canvas.delete("all")
        self.reset()
        self.canvas.update_idletasks()

        # get canvas size
        width  = self.canvas.winfo_width()  or int(self.canvas.cget("width"))
        height = self.canvas.winfo_height() or int(self.canvas.cget("height"))

        # margins so nodes never touch the very edge
        margin_x = self.base_radius * 2
        margin_y = self.base_radius * 2

        # how many levels we will actually draw
        levels = min(n, self.max_levels)
        levels = max(levels, 1)  # avoid division by zero

        # vertical gap: fill top-to-bottom
        self.level_gap = (height - 2*margin_y) / levels

        # horizontal step at deepest level
        max_nodes = 2 ** levels
        h_step = (width - 2*margin_x) / (max_nodes + 1)

        # choose node radius so circles don't overlap
        self.node_radius = max(5, min(self.base_radius, h_step * 0.4))

        # store for recursive draw
        self._width     = width
        self._height    = height
        self._margin_x  = margin_x
        self._margin_y  = margin_y
        self._levels    = levels
        self._memo      = memoization

        # kick off drawing: root has index 0
        self._draw(n, level=0, index=0, parent_xy=None)
        self.canvas.update_idletasks()

    def _draw(self, n, level, index, parent_xy):
        # compute this node's x,y via even spacing:
        # denom = (2^level + 1), nodes sit at (i+1)/denom horizontally
        denom = (2 ** level) + 1
        x = self._margin_x + (index + 1) * (self._width - 2*self._margin_x) / denom
        y = self._margin_y + level * self.level_gap

        # draw connector
        if parent_xy is not None:
            px, py = parent_xy
            r = self.node_radius
            self.canvas.create_line(px, py + r, x, y - r, fill="grey")

        # color for memoization
        is_cached = self._memo and (n in self.visited)
        if is_cached:
            fill = self.memo_color
        else:
            fill = "lightgreen" if self._memo else "lightcoral"

        # draw node
        r = self.node_radius
        self.canvas.create_oval(x - r, y - r, x + r, y + r, fill=fill, outline="")
        # font size proportional to radius
        font_sz = max(6, int(r * 0.6))
        self.canvas.create_text(x, y, text=str(n), font=("Helvetica", font_sz, "bold"))

        # mark visited for memoization
        if self._memo and not is_cached:
            self.visited.add(n)

        # stop if leaf or we've reached max_levels
        if n <= 1 or level >= self.max_levels or is_cached:
            return

        # recurse left (index*2) and right (index*2+1)
        self._draw(n-1, level+1, index*2,     parent_xy=(x, y))
        self._draw(n-2, level+1, index*2 + 1, parent_xy=(x, y))
