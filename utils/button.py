from .settings import*

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

        #fill button background
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
        #outline button
        pygame.draw.rect(win, BLACK, (self.x, self.y, self.width, self.height), 2)

        #add text to middle of button by offsetting starting pos by the width of the textsurface
        if self.text:
            button_font = get_font(22)
            text_surface = button_font.render(self.text, 1, self.text_color)
            win.blit(text_surface, ((self.x + self.width/2 - text_surface.get_width()/2),(self.y + self.height/2 - text_surface.get_height()/2)))
    
    
    def clicked(self, pos):

        #tuple unpacking
        x, y = pos

        #check if x and y are within the x and y coordinates of the button:
        if not(x >= self.x and x <= self.x + self.width):
            return False
        if not(y >= self.y and y <= self.y + self.height):
            return False
        
        return True
                

