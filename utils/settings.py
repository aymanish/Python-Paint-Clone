import pygame

#initialize pygame and pygame font:
pygame.init
pygame.font.init()

#define colors as constants:
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
BLUE = (0, 255,0)
GREEN = (0,0,255)
GREY = (160,160,160)

#define game fps:
FPS = 240

#define app window size
WIDTH, HEIGHT = 500, 600

#50x50 pixels
ROWS = COLS = 200

TOOLBAR_HEIGHT = HEIGHT - WIDTH

PIXEL_SIZE = WIDTH // COLS

BG_COLOR = WHITE

DRAW_GRID_LINES = False

#take size and return font object of specific size
def get_font(size):
    return pygame.font.SysFont("comicsans", size)
