# utils/grid.py

import pygame
from .settings import *
from collections import deque

class Grid:
    def __init__(self, rows, cols, color):
        self.rows = rows
        self.cols = cols
        self.color = color
        self.grid = self.init_grid()

    def init_grid(self):
        return [[self.color for _ in range(self.cols)] for _ in range(self.rows)]

    def clear(self):
        self.grid = self.init_grid()

    def set_cell_color(self, row, col, color):
        if 0 <= row < self.rows and 0 <= col < self.cols:
            self.grid[row][col] = color

    def set_cell_color_circle(self, center_pos, radius, color):
        center_x, center_y = center_pos
        center_row = center_y // PIXEL_SIZE
        center_col = center_x // PIXEL_SIZE
        pix_radius = int(radius // PIXEL_SIZE) + 1

        for row in range(center_row - pix_radius, center_row + pix_radius + 1):
            for col in range(center_col - pix_radius, center_col + pix_radius + 1):
                if 0 <= row < self.rows and 0 <= col < self.cols:
                    x = col * PIXEL_SIZE + PIXEL_SIZE // 2
                    y = row * PIXEL_SIZE + PIXEL_SIZE // 2
                    dx = x - center_x
                    dy = y - center_y
                    distance = (dx * dx + dy * dy) ** 0.5
                    if distance <= radius:
                        self.set_cell_color(row, col, color)

    def set_cell_color_line(self, pos1, pos2, brush_size, color):
        x1, y1 = pos1
        x2, y2 = pos2
        dx = x2 - x1
        dy = y2 - y1
        distance = max(abs(dx), abs(dy))
        steps = int(distance * 2) + 1  # Increase steps for smoother lines

        for i in range(steps):
            t = i / steps if steps != 0 else 0
            x = int(x1 + dx * t)
            y = int(y1 + dy * t)
            self.set_cell_color_circle((x, y), brush_size, color)

    def flood_fill(self, pos, new_color):
        x, y = pos
        row = y // PIXEL_SIZE
        col = x // PIXEL_SIZE

        if not (0 <= row < self.rows and 0 <= col < self.cols):
            return

        target_color = self.grid[row][col]
        if target_color == new_color:
            return

        queue = deque()
        queue.append((row, col))
        self.grid[row][col] = new_color

        while queue:
            current_row, current_col = queue.popleft()

            # Check all four directions
            neighbors = [
                (current_row - 1, current_col),  # Up
                (current_row + 1, current_col),  # Down
                (current_row, current_col - 1),  # Left
                (current_row, current_col + 1)   # Right
            ]

            for n_row, n_col in neighbors:
                if 0 <= n_row < self.rows and 0 <= n_col < self.cols:
                    if self.grid[n_row][n_col] == target_color:
                        self.grid[n_row][n_col] = new_color
                        queue.append((n_row, n_col))

    def draw(self, win):
        for i, row in enumerate(self.grid):
            for j, color in enumerate(row):
                pygame.draw.rect(
                    win,
                    color,
                    (j * PIXEL_SIZE, i * PIXEL_SIZE, PIXEL_SIZE, PIXEL_SIZE),
                )
        # Draw grid lines if enabled
        if DRAW_GRID_LINES:
            for i in range(self.rows + 1):
                pygame.draw.line(
                    win, BLACK, (0, i * PIXEL_SIZE), (WIDTH, i * PIXEL_SIZE)
                )
            for j in range(self.cols + 1):
                pygame.draw.line(
                    win,
                    BLACK,
                    (j * PIXEL_SIZE, 0),
                    (j * PIXEL_SIZE, HEIGHT - TOOLBAR_HEIGHT),
                )

    def get_cell_from_pos(self, pos):
        x, y = pos
        row = y // PIXEL_SIZE
        col = x // PIXEL_SIZE
        if 0 <= row < self.rows and 0 <= col < self.cols:
            return row, col
        return None
