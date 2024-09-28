# utils/slider.py

import pygame
from .settings import get_font, BLACK

class Slider:
    def __init__(self, x, y, width, height, min_val, max_val, start_val, color=BLACK, label=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.min_val = min_val
        self.max_val = max_val
        self.value = start_val
        self.grabbed = False
        self.knob_radius = height // 2
        self.knob_x = x + ((start_val - min_val) / (max_val - min_val)) * width
        self.color = color  # Slider line and knob color
        self.label = label  # Optional label for the slider

    def draw(self, win):
        # Draw slider line
        pygame.draw.line(
            win,
            self.color,
            (self.rect.x, self.rect.y + self.rect.height // 2),
            (self.rect.x + self.rect.width, self.rect.y + self.rect.height // 2),
            2,
        )
        # Draw knob
        pygame.draw.circle(
            win,
            self.color,
            (int(self.knob_x), self.rect.y + self.rect.height // 2),
            self.knob_radius,
        )
        # Draw min and max labels
        font = get_font(12)
        min_label = font.render(str(int(self.min_val)), True, self.color)
        max_label = font.render(str(int(self.max_val)), True, self.color)
        win.blit(
            min_label,
            (self.rect.x - min_label.get_width() // 2, self.rect.y + self.rect.height + 5),
        )
        win.blit(
            max_label,
            (
                self.rect.x + self.rect.width - max_label.get_width() // 2,
                self.rect.y + self.rect.height + 5,
            ),
        )
        # Draw label if available
        if self.label:
            label_font = get_font(14)
            label_surface = label_font.render(self.label, True, self.color)
            win.blit(
                label_surface,
                (
                    self.rect.x + self.rect.width // 2 - label_surface.get_width() // 2,
                    self.rect.y - label_surface.get_height() - 5,
                ),
            )

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.is_over_knob(event.pos):
                self.grabbed = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.grabbed = False
        elif event.type == pygame.MOUSEMOTION:
            if self.grabbed:
                self.knob_x = min(
                    max(event.pos[0], self.rect.x), self.rect.x + self.rect.width
                )
                self.update_value()

    def is_over_knob(self, pos):
        x, y = pos
        dx = x - self.knob_x
        dy = y - (self.rect.y + self.rect.height // 2)
        return dx * dx + dy * dy <= self.knob_radius * self.knob_radius

    def update_value(self):
        ratio = (self.knob_x - self.rect.x) / self.rect.width
        self.value = self.min_val + ratio * (self.max_val - self.min_val)
