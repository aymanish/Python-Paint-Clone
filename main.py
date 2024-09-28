# main.py

import pygame
from utils import *
from utils.button import Button
from utils.grid import Grid
from utils.slider import Slider

class PaintApp:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.win = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Paint App")
        self.clock = pygame.time.Clock()
        self.grid = Grid(ROWS, COLS, BG_COLOR)
        self.drawing_color = BLACK
        self.buttons = self.create_buttons()
        
        # Create sensitivity slider to the left of the base brush size slider
        self.base_brush_slider = Slider(
            WIDTH - 150, 
            HEIGHT - TOOLBAR_HEIGHT / 2 - 10, 
            120, 
            20, 
            1, 
            20, 
            5, 
            color=BLACK
        )
        self.sensitivity_slider = Slider(
            WIDTH - 150 - 150, 
            HEIGHT - TOOLBAR_HEIGHT / 2 - 10, 
            120, 
            20, 
            1, 
            20, 
            10, 
            color=BLUE
        )
        
        self.base_brush_size = int(self.base_brush_slider.value)
        self.run_app = True
        self.prev_pos = None
        self.prev_time = None
        self.dragging = False
        
        # Track the current tool: 'draw' or 'fill'
        self.current_tool = 'draw'  # Default tool

    def create_buttons(self):
        button_size = 30  # Reduced button size
        padding = 10
        start_x = padding
        start_y = HEIGHT - TOOLBAR_HEIGHT + (TOOLBAR_HEIGHT - button_size) // 2

        # Define a list of colors to add more color buttons
        color_options = [
            BLACK, RED, GREEN, BLUE, ORANGE, PURPLE, YELLOW, CYAN, PINK, BROWN
        ]

        buttons = []
        for idx, color in enumerate(color_options):
            x = start_x + idx * (button_size + padding)
            buttons.append(Button(x, start_y, button_size, button_size, color))

        # Add ERASE and CLEAR buttons
        erase_button = Button(
            start_x + len(color_options) * (button_size + padding), 
            start_y, 
            button_size, 
            button_size, 
            WHITE, 
            'ERASE'
        )
        clear_button = Button(
            start_x + (len(color_options) + 1) * (button_size + padding), 
            start_y, 
            button_size, 
            button_size, 
            WHITE, 
            'CLEAR'
        )
        buttons.extend([erase_button, clear_button])

        # Add DRAW and FILL buttons
        draw_button = Button(
            start_x + (len(color_options) + 2) * (button_size + padding), 
            start_y, 
            button_size, 
            button_size, 
            GREY, 
            'DRAW'
        )
        fill_button = Button(
            start_x + (len(color_options) + 3) * (button_size + padding), 
            start_y, 
            button_size, 
            button_size, 
            GREY, 
            'FILL'
        )
        buttons.extend([draw_button, fill_button])

        return buttons

    def run(self):
        while self.run_app:
            self.clock.tick(FPS)
            self.handle_events()
            self.draw()
        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.run_app = False

            # First, handle slider events
            self.base_brush_slider.handle_event(event)
            self.sensitivity_slider.handle_event(event)

            # Update base brush size from slider's value
            self.base_brush_size = int(self.base_brush_slider.value)

            # Update sensitivity value
            sensitivity_value = self.sensitivity_slider.value
            # Map sensitivity to a factor, e.g., 1 to 20 maps to 0.1 to 2.0
            sensitivity_factor = sensitivity_value / 10.0  # 0.1 to 2.0

            # Check if any slider is being interacted with
            if self.base_brush_slider.grabbed or self.sensitivity_slider.grabbed:
                # If any slider is being dragged, do not handle other events
                continue

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    pos = event.pos
                    if pos[1] >= HEIGHT - TOOLBAR_HEIGHT:
                        # Clicked on toolbar
                        for button in self.buttons:
                            if button.clicked(pos):
                                self.handle_button_click(button)
                                break
                        self.prev_pos = None
                        self.prev_time = None
                    else:
                        if self.current_tool == 'fill':
                            # Perform fill operation on mouse click
                            self.grid.flood_fill(pos, self.drawing_color)
                        elif self.current_tool == 'draw':
                            # Start drawing
                            self.dragging = True
                            self.prev_pos = pos
                            self.prev_time = pygame.time.get_ticks()

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.dragging = False
                    self.prev_pos = None
                    self.prev_time = None

            elif event.type == pygame.MOUSEMOTION:
                if self.dragging and self.current_tool == 'draw':
                    pos = event.pos
                    current_time = pygame.time.get_ticks()

                    if self.prev_pos is not None and self.prev_time is not None:
                        dx = pos[0] - self.prev_pos[0]
                        dy = pos[1] - self.prev_pos[1]
                        distance = (dx ** 2 + dy ** 2) ** 0.5
                        time_delta = (current_time - self.prev_time) / 1000.0  # seconds

                        if time_delta > 0:
                            speed = distance / time_delta  # pixels per second
                        else:
                            speed = MAX_SPEED

                        speed = max(MIN_SPEED, min(speed, MAX_SPEED))

                        # Compute speed ratio (0 = high speed, 1 = low speed)
                        speed_ratio = (speed - MIN_SPEED) / (MAX_SPEED - MIN_SPEED)  # 0 to 1
                        speed_ratio = min(max(speed_ratio, 0), 1)  # Clamp between 0 and 1

                        # Inverse mapping: high speed -> low brush size, low speed -> high brush size
                        dynamic_brush_size = int(
                            MAX_BRUSH_SIZE - (MAX_BRUSH_SIZE - MIN_BRUSH_SIZE) * speed_ratio * sensitivity_factor
                        )
                        dynamic_brush_size = min(dynamic_brush_size, self.base_brush_size)
                        dynamic_brush_size = max(dynamic_brush_size, MIN_BRUSH_SIZE)

                        # Draw line with dynamic brush size
                        self.grid.set_cell_color_line(self.prev_pos, pos, dynamic_brush_size, self.drawing_color)

                    self.prev_pos = pos
                    self.prev_time = current_time

    def handle_button_click(self, button):
        if button.text == 'CLEAR':
            self.grid.clear()
        elif button.text == 'ERASE':
            self.drawing_color = BG_COLOR  # Set to background color for erasing
        elif button.text == 'FILL':
            self.current_tool = 'fill'
        elif button.text == 'DRAW':
            self.current_tool = 'draw'
        elif button.text is None:
            self.drawing_color = button.color

    def draw(self):
        # Fill the entire window with UI_BG_COLOR (dark grey)
        self.win.fill(UI_BG_COLOR)

        # Draw the canvas area with BG_COLOR via grid.draw()
        self.grid.draw(self.win)

        # Draw the canvas border
        canvas_rect = pygame.Rect(0, 0, WIDTH, HEIGHT - TOOLBAR_HEIGHT)
        pygame.draw.rect(self.win, CANVAS_BORDER_COLOR, canvas_rect, CANVAS_BORDER_WIDTH)

        # Draw buttons and sliders on the toolbar
        for button in self.buttons:
            # Highlight the active tool button
            if (button.text == 'DRAW' and self.current_tool == 'draw') or (button.text == 'FILL' and self.current_tool == 'fill'):
                # Draw a border or change color to indicate active tool
                pygame.draw.rect(self.win, YELLOW, (button.x-2, button.y-2, button.width+4, button.height+4), 2)
            button.draw(self.win)
        
        self.base_brush_slider.draw(self.win)
        self.sensitivity_slider.draw(self.win)

        # Draw brush size indicator
        mouse_pos = pygame.mouse.get_pos()
        if mouse_pos[1] < HEIGHT - TOOLBAR_HEIGHT:
            # Here, we could use the dynamic_brush_size, but for simplicity, use base_brush_size
            pygame.draw.circle(self.win, self.drawing_color, mouse_pos, int(self.base_brush_size), 1)

        pygame.display.update()

if __name__ == "__main__":
    app = PaintApp()
    app.run()
