# main.py

import pygame
import os
import time
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
        
        # Create sliders with dynamic layout
        self.create_sliders()
        
        self.base_brush_size = int(self.base_brush_slider.value)
        self.run_app = True
        self.prev_pos = None
        self.prev_time = None
        self.dragging = False
        
        # Track the current tool: 'draw' or 'fill'
        self.current_tool = 'draw'  # Default tool
        
        # Initialize Undo and Redo stacks
        self.undo_stack = []
        self.redo_stack = []

    def create_buttons(self):
        button_size = 30  # Adjusted button size to fit within toolbar
        padding = 10
        start_x = padding
        # Calculate y-coordinate for buttons (lower half of toolbar)
        button_y = HEIGHT - TOOLBAR_HEIGHT + (TOOLBAR_HEIGHT // 2) + (TOOLBAR_HEIGHT // 2 - button_size) // 2

        # Define a list of colors to add more color buttons
        color_options = [
            BLACK, RED, GREEN, BLUE, ORANGE, PURPLE, YELLOW, CYAN, PINK, BROWN
        ]

        buttons = []
        for idx, color in enumerate(color_options):
            x = start_x + idx * (button_size + padding)
            buttons.append(Button(x, button_y, button_size, button_size, color))

        # Add ERASE and CLEAR buttons
        erase_button = Button(
            start_x + len(color_options) * (button_size + padding),
            button_y,
            button_size,
            button_size,
            WHITE,
            'ERASE'
        )
        clear_button = Button(
            start_x + (len(color_options) + 1) * (button_size + padding),
            button_y,
            button_size,
            button_size,
            WHITE,
            'CLEAR'
        )
        buttons.extend([erase_button, clear_button])

        # Add DRAW and FILL buttons
        draw_button = Button(
            start_x + (len(color_options) + 2) * (button_size + padding),
            button_y,
            button_size,
            button_size,
            GREY,
            'DRAW'
        )
        fill_button = Button(
            start_x + (len(color_options) + 3) * (button_size + padding),
            button_y,
            button_size,
            button_size,
            GREY,
            'FILL'
        )
        buttons.extend([draw_button, fill_button])

        # Add UNDO and REDO buttons
        undo_button = Button(
            start_x + (len(color_options) + 4) * (button_size + padding),
            button_y,
            button_size,
            button_size,
            GREY,
            'UNDO'
        )
        redo_button = Button(
            start_x + (len(color_options) + 5) * (button_size + padding),
            button_y,
            button_size,
            button_size,
            GREY,
            'REDO'
        )
        buttons.extend([undo_button, redo_button])

        # Add NEW and SAVE buttons
        new_button = Button(
            start_x + (len(color_options) + 6) * (button_size + padding),
            button_y,
            button_size,
            button_size,
            GREY,
            'NEW'
        )
        save_button = Button(
            start_x + (len(color_options) + 7) * (button_size + padding),
            button_y,
            button_size,
            button_size,
            GREY,
            'SAVE'
        )
        buttons.extend([new_button, save_button])

        return buttons

    def create_sliders(self):
        # Arrange sliders above the buttons within the toolbar
        slider_width = 150
        slider_height = 20
        padding = 10

        # Position sliders in the upper half of the toolbar
        # Center them horizontally or align to one side
        # Here, we'll align them to the left with some padding

        total_slider_width = 2 * (slider_width + padding)  # Two sliders
        start_x = padding  # Starting x position for sliders

        # Calculate y-coordinate for sliders (upper half of toolbar)
        slider_y = HEIGHT - TOOLBAR_HEIGHT + (TOOLBAR_HEIGHT // 4) - (slider_height // 2)

        self.base_brush_slider = Slider(
            start_x,
            slider_y,
            slider_width,
            slider_height,
            1,
            20,
            5,
            color=WHITE,
            label='Brush Size'
        )
        self.sensitivity_slider = Slider(
            start_x + slider_width + padding,
            slider_y,
            slider_width,
            slider_height,
            1,
            20,
            10,
            color=WHITE,
            label='Sensitivity'
        )

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

            # Handle slider events
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
                            self.save_state_to_undo()  # Save state before fill
                            self.grid.flood_fill(pos, self.drawing_color)
                            self.redo_stack.clear()  # Clear redo stack after new action
                        elif self.current_tool == 'draw':
                            # Start drawing
                            self.dragging = True
                            self.prev_pos = pos
                            self.prev_time = pygame.time.get_ticks()
                            self.save_state_to_undo()  # Save state before drawing
                            self.redo_stack.clear()  # Clear redo stack after new action

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    if self.dragging and self.current_tool == 'draw':
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

            elif event.type == pygame.KEYDOWN:
                # Implement keyboard shortcuts
                if (event.key == pygame.K_z) and (pygame.key.get_mods() & pygame.KMOD_CTRL):
                    self.undo()
                elif (event.key == pygame.K_y) and (pygame.key.get_mods() & pygame.KMOD_CTRL):
                    self.redo()

    def handle_button_click(self, button):
        if button.text == 'CLEAR':
            self.grid.clear()
            # After clearing, save the state
            self.save_state_to_undo()
            self.redo_stack.clear()
        elif button.text == 'ERASE':
            self.drawing_color = BG_COLOR  # Set to background color for erasing
        elif button.text == 'FILL':
            self.current_tool = 'fill'
        elif button.text == 'DRAW':
            self.current_tool = 'draw'
        elif button.text == 'NEW':
            self.grid.clear()  # Clear the canvas for a new image
            self.current_tool = 'draw'  # Reset to draw tool
            # Save state after clearing
            self.save_state_to_undo()
            self.redo_stack.clear()
        elif button.text == 'SAVE':
            self.save_image()  # Call the save function
        elif button.text == 'UNDO':
            self.undo()  # Perform undo
        elif button.text == 'REDO':
            self.redo()  # Perform redo
        elif button.text is None:
            self.drawing_color = button.color

    def save_state_to_undo(self):
        if len(self.undo_stack) >= 10:
            self.undo_stack.pop(0)  # Remove the oldest state to maintain a maximum of 10
        # Deep copy of the grid
        grid_copy = [row.copy() for row in self.grid.grid]
        self.undo_stack.append(grid_copy)

    def undo(self):
        if not self.undo_stack:
            print("Nothing to undo.")
            return
        # Save the current state to redo stack
        if len(self.redo_stack) >= 10:
            self.redo_stack.pop(0)  # Remove the oldest state to maintain a maximum of 10
        current_state = [row.copy() for row in self.grid.grid]
        self.redo_stack.append(current_state)
        
        # Restore the last state from undo stack
        last_state = self.undo_stack.pop()
        self.grid.grid = [row.copy() for row in last_state]

    def redo(self):
        if not self.redo_stack:
            print("Nothing to redo.")
            return
        # Save the current state to undo stack
        if len(self.undo_stack) >= 10:
            self.undo_stack.pop(0)  # Remove the oldest state to maintain a maximum of 10
        current_state = [row.copy() for row in self.grid.grid]
        self.undo_stack.append(current_state)
        
        # Restore the last state from redo stack
        last_state = self.redo_stack.pop()
        self.grid.grid = [row.copy() for row in last_state]

    def save_image(self):
        # Create a directory for saved images if it doesn't exist
        if not os.path.exists('saved_images'):
            os.makedirs('saved_images')

        # Get the current time to create a unique filename
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        filename = f"saved_images/image_{timestamp}.png"

        # Create a surface to draw the grid
        save_surface = pygame.Surface((COLS * PIXEL_SIZE, ROWS * PIXEL_SIZE))
        self.grid.draw(save_surface)

        # Save the surface as an image
        try:
            pygame.image.save(save_surface, filename)
            print(f"Image saved as {filename}")
        except Exception as e:
            print(f"Error saving image: {e}")

    def draw(self):
        # Fill the entire window with UI_BG_COLOR (dark grey)
        self.win.fill(UI_BG_COLOR)

        # Draw the canvas area with BG_COLOR via grid.draw()
        self.grid.draw(self.win)

        # Draw the canvas border
        canvas_rect = pygame.Rect(0, 0, COLS * PIXEL_SIZE, ROWS * PIXEL_SIZE)
        pygame.draw.rect(self.win, CANVAS_BORDER_COLOR, canvas_rect, CANVAS_BORDER_WIDTH)

        # Draw buttons on the toolbar
        for button in self.buttons:
            # Highlight the active tool button
            if (button.text == 'DRAW' and self.current_tool == 'draw') or (button.text == 'FILL' and self.current_tool == 'fill'):
                # Draw a border or change color to indicate active tool
                pygame.draw.rect(self.win, YELLOW, (button.x-2, button.y-2, button.width+4, button.height+4), 2)
            
            # Disable UNDO button if no actions to undo
            if button.text == 'UNDO' and not self.undo_stack:
                # Draw the button as disabled (e.g., lighter color)
                disabled_color = (200, 200, 200)  # Light grey
                pygame.draw.rect(self.win, disabled_color, (button.x, button.y, button.width, button.height))
                pygame.draw.rect(self.win, BLACK, (button.x, button.y, button.width, button.height), 2)
                if button.text:
                    button_font = get_font(14)
                    text_surface = button_font.render(button.text, True, BLACK)
                    self.win.blit(
                        text_surface,
                        (
                            button.x + button.width / 2 - text_surface.get_width() / 2,
                            button.y + button.height / 2 - text_surface.get_height() / 2,
                        ),
                    )
                continue  # Skip drawing the button normally

            # Disable REDO button if no actions to redo
            if button.text == 'REDO' and not self.redo_stack:
                # Draw the button as disabled (e.g., lighter color)
                disabled_color = (200, 200, 200)  # Light grey
                pygame.draw.rect(self.win, disabled_color, (button.x, button.y, button.width, button.height))
                pygame.draw.rect(self.win, BLACK, (button.x, button.y, button.width, button.height), 2)
                if button.text:
                    button_font = get_font(14)
                    text_surface = button_font.render(button.text, True, BLACK)
                    self.win.blit(
                        text_surface,
                        (
                            button.x + button.width / 2 - text_surface.get_width() / 2,
                            button.y + button.height / 2 - text_surface.get_height() / 2,
                        ),
                    )
                continue  # Skip drawing the button normally

            button.draw(self.win)
        
        # Draw sliders above the buttons
        self.base_brush_slider.draw(self.win)
        self.sensitivity_slider.draw(self.win)

        # Draw brush size indicator
        mouse_pos = pygame.mouse.get_pos()
        if mouse_pos[1] < ROWS * PIXEL_SIZE:
            # Here, we could use the dynamic_brush_size, but for simplicity, use base_brush_size
            pygame.draw.circle(self.win, self.drawing_color, mouse_pos, int(self.base_brush_size), 1)

        pygame.display.update()

if __name__ == "__main__":
    app = PaintApp()
    app.run()
