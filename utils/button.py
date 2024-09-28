import pygame
from .settings import *

class Button:
    def __init__(self, x, y, width, height, color, text=None, text_color=BLACK):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.text = text
        self.text_color = text_color

    def draw(self, win):
        # Draw button rectangle
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
        # Draw button border
        pygame.draw.rect(win, BLACK, (self.x, self.y, self.width, self.height), 2)
        # Draw text if available
        if self.text:
            button_font = get_font(14)  # Reduced font size for smaller buttons
            text_surface = button_font.render(self.text, True, self.text_color)
            win.blit(
                text_surface,
                (
                    self.x + self.width / 2 - text_surface.get_width() / 2,
                    self.y + self.height / 2 - text_surface.get_height() / 2,
                ),
            )

    def clicked(self, pos):
        x, y = pos
        return self.x <= x <= self.x + self.width and self.y <= y <= self.y + self.height
