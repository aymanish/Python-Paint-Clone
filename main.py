#import utils package
from utils import*
from utils.button import Button

#app window set up
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint App")

###########FUNCTIONALITY#######################

def init_grid(rows, cols, color):
    grid = []
    for i in range(rows):
        grid.append([])
        #use _ instead of j if you dont plan to use the loop variable
        for _ in range(cols):
            grid[i].append(color)
    return grid


#draw function:
def draw_grid(win, grid):

    #iterate the row was well as its index(i) -> 0:(row)
    for i, row in enumerate(grid):
        #get index and color of pixels: pixel -> color(x,x,x)
        for j, pixel in enumerate(row):
            pygame.draw.rect(win, pixel, (j*PIXEL_SIZE, i*PIXEL_SIZE, PIXEL_SIZE, PIXEL_SIZE))
    
    #enable gridlines:
    if DRAW_GRID_LINES:
        for i in range(ROWS+1):
            pygame.draw.line(win, BLACK, (0, i*PIXEL_SIZE), (WIDTH, i*PIXEL_SIZE))
        for i in range(COLS+1):
            pygame.draw.line(win, BLACK, (i*PIXEL_SIZE, 0), (i*PIXEL_SIZE, HEIGHT - TOOLBAR_HEIGHT))

def draw(win, grid, buttons):
    win.fill(BG_COLOR)
    #draw on grid
    draw_grid(win, grid)

    #draw buttons:
    for button in buttons:
        button.draw(win)

    #update display:
    pygame.display.update()

def get_xy_from_pos(pos):
    x,y = pos #tuple unpacking
    row = y // PIXEL_SIZE
    col = x // PIXEL_SIZE
    if row >= ROWS:
        raise IndexError
    return row, col





#EVENT LOOP/MAIN###############################

#event loop setup:
run = True
#clock setup:
clock = pygame.time.Clock()
grid = init_grid(ROWS, COLS, BG_COLOR)
drawing_color = BLACK

button_pos = HEIGHT - TOOLBAR_HEIGHT/2 - 25
buttons = [Button(10, button_pos, 50, 50, BLACK),
           Button(70, button_pos, 50, 50, RED),
           Button(130, button_pos, 50, 50, GREEN),
           Button(190, button_pos, 50, 50, BLUE),
           Button(250, button_pos, 50, 50, WHITE, 'ERASE'),
           Button(310, button_pos, 50, 50, WHITE, 'CLEAR')
           ]


while run:
    clock.tick(FPS)
    #check if events have occured inside forloop:
    for event in pygame.event.get():
        #check if quit app:
        if event.type == pygame.QUIT:
            run = False
        #use mouse to draw color:
        if pygame.mouse.get_pressed()[0]:
            pos = pygame.mouse.get_pos()
            try:
                row, col = get_xy_from_pos(pos)
                grid[row][col] = drawing_color
            except IndexError:
                #splice untill clear button
                for button in buttons:
                    if not button.clicked(pos):
                        continue
                    #set color
                    if (button.text == None) or (button.text == 'ERASE'): 
                        drawing_color = button.color
                    if button.text == 'CLEAR':
                        grid = init_grid(ROWS, COLS, BG_COLOR)
                        
                        

    draw(WIN, grid, buttons)
pygame.quit()