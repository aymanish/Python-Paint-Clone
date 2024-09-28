# utils/settings.py

import pygame

# Color constants
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE  = (0, 0, 255)
GREY  = (160, 160, 160)
DARK_GREY = (50, 50, 50)  # Dark grey for UI background
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
YELLOW = (255, 255, 0)
CYAN   = (0, 255, 255)
PINK   = (255, 192, 203)
BROWN  = (165, 42, 42)

# Brush dynamics
MIN_SPEED = 50    # Minimum speed (pixels per second) corresponding to maximum brush size
MAX_SPEED = 1000  # Maximum speed (pixels per second) corresponding to minimum brush size
MIN_BRUSH_SIZE = 1
MAX_BRUSH_SIZE = 20

# Game settings
FPS = 240
WIDTH, HEIGHT = 800, 600  # Fixed window size
TOOLBAR_HEIGHT = 100
PIXEL_SIZE = 4  # Adjusted PIXEL_SIZE based on new WIDTH and ROWS
ROWS = (HEIGHT - TOOLBAR_HEIGHT) // PIXEL_SIZE  # Adjusted to fit within canvas height
COLS = WIDTH // PIXEL_SIZE
BG_COLOR = WHITE
UI_BG_COLOR = DARK_GREY          # Changed to DARK_GREY for better contrast
CANVAS_BORDER_COLOR = BLACK
CANVAS_BORDER_WIDTH = 2
DRAW_GRID_LINES = False

def get_font(size):
    return pygame.font.SysFont("comicsans", size)
