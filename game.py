"""
Block Blast! is a game where you place blocks on a grid to create rows or columns of blocks to clear them.
:Autor: Tyler Orme
:Dependencies: pygame (2.6.1)
:python_version: 3.11.1
"""

from pygame import *
from random import randint
from time import sleep
# Initialize the game
init()

# if stats.bin does not exist create it
try:
    with open("stats.bin", "rb") as f:
        content = f.read()
        if(len(content) == 0):
            with open("stats.bin", "wb") as f:
                f.write((0).to_bytes(4, byteorder='big'))
except FileNotFoundError:
    with open("stats.bin", "wb") as f:
        f.write((0).to_bytes(4, byteorder='big'))


WIDTH = 850
HEIGHT = 600

# Set up the screen
screen = display.set_mode((WIDTH, HEIGHT))
display.set_caption("Block Blast!")

# Set up the colors
WHITE = (255, 255, 255)
SPACE_GRAY = (50, 50, 50)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
CYAN = (0, 255, 255)

#define block shapes
I = [[1, 1, 1, 1]]
STUB = [[1, 1, 1]]
U_STUB = [[1], [1], [1]]
LIL_GUY = [[1,1]]
U_LIL_GUY = [[1], [1]]
ELBOW = [[1, 1], [1, 0]]
U_ELBOW = [[1, 1], [0, 1]]
U_ELBOW2 = [[0, 1], [1, 1]]
U_ELBOW3 = [[1, 0], [1, 1]]
U_I = [[1], [1], [1], [1]]
LONG_I = [[1, 1, 1, 1,1]]
U_LONG_I = [[1], [1], [1], [1], [1]]
BRICK = [[1, 1], [1, 1], [1, 1]]
U_BRICK = [[1, 1, 1], [1, 1, 1]]
O = [[1, 1], [1, 1]]
T = [[1, 1, 1], [0, 1, 0]]
R_T = [[0, 1, 0], [1, 1, 1]]
U_T  = [[1,0], [1,1], [1,0]]
U_R_T = [[0,1], [1,1], [0,1]]
S = [[0, 1, 1], [1, 1, 0]]
Z = [[1, 1, 0], [0, 1, 1]]
J = [[1, 0, 0], [1, 1, 1]]
L = [[0, 0, 1], [1, 1, 1]]
R_L = [[1, 1, 1], [1, 0, 0]]
U_L = [[1, 1, 1], [0, 0, 1]]
UR_L = [[1, 0, 0], [1, 1, 1]]
BIG_O = [[1,1,1], [1,1,1], [1,1,1]]
BIG_L1 = [[1,1,1], [0,0,1], [0,0,1]]
BIG_L2 = [[1,1,1], [1,0,0], [1,0,0]]
BIG_L3 = [[1,0,0], [1,0,0], [1,1,1]]
BIG_L4 = [[0,0,1], [0,0,1], [1,1,1]]


# ---------------------------------------------------------------------------------

class Block:
    COLOR_LIST = [RED, GREEN, BLUE, ORANGE, YELLOW, PURPLE, CYAN]
    BLOCK_LIST = [I, O, T, R_T, S, Z, J, L, R_L, U_L, UR_L, BIG_O, BRICK, U_BRICK, LONG_I, U_LONG_I,STUB,U_STUB,LIL_GUY,U_LIL_GUY,ELBOW,U_ELBOW,U_ELBOW2,U_ELBOW3,U_I,BIG_L1,BIG_L2,BIG_L3,BIG_L4,U_T,U_R_T]
    SIZE = 50
    def __init__(self):
        self.shape = Block.BLOCK_LIST[randint(0, len(Block.BLOCK_LIST) - 1)]
        self.color = Block.COLOR_LIST[randint(0, len(Block.COLOR_LIST) - 1)]
        self.x = 0
        self.y = 0
        self.rectangles = []
        self.placed = 0
    def draw(self):
        self.rectangles.clear()
        for x in range(len(self.shape)):
            for y in range(len(self.shape[x])):
                if self.shape[x][y] == 1:
                    #tuple object (rectangle, outline)
                    self.rectangles.append((draw.rect(screen, self.color, (50 + (self.x + y) * 50, 50 + (self.y + x) * 50, Block.SIZE, Block.SIZE), 0),draw.rect(screen, BLACK, (50 + (self.x + y) * 50, 50 + (self.y + x) * 50, Block.SIZE, Block.SIZE), 1),self.color))
    def undraw(self):
        for rectangle,outline,c in self.rectangles:
            draw.rect(screen, SPACE_GRAY, rectangle, 0)
    
# ---------------------------------------------------------------------------------
def create_grid():
    """create 8x8 grid in the middle of the screen
    (100, 100) to (500, 500)
    """
    for x in range(8):
        for y in range(8):
            draw.rect(screen, BLACK, (100 + x * 50, 100 + y * 50, 50, 50), 1)      
# ---------------------------------------------------------------------------------
def draw_placed_blocks():
    #draw placed rectangles
    for row in placed_rectangles:
        for col in row:
            if col:
                rectangle,outline,c = col
                draw.rect(screen, c, rectangle, 0)
                draw.rect(screen, BLACK, outline, 1)
# ---------------------------------------------------------------------------------
def draw_unplaced_blocks():
    #draw blocks
    for block in next_blocks:
        block.draw()
# ---------------------------------------------------------------------------------
def draw_best_score():
    best_score = get_best_score()
    text = font3.render(f"Best Score: {best_score}", True, ORANGE)
    screen.blit(text, (25, 15))
# ---------------------------------------------------------------------------------
def check_row_or_column_full():
    """checks if a row or column is full and removes it"""
    global score
    global line_cleared_in_turn
    global combos
    remove_row = []
    for row in range(8):
        row_count = 0
        for col in range(8):
            if placed_rectangles[row][col] is None:
                pass
            else:
                row_count += 1
        if row_count == 8:
            remove_row.append(row)
            combos += 1
            score += (10 * combos)
            line_cleared_in_turn = True

        
    remove_col = []
    for col in range(8):
        col_count = 0
        for row in range(8):
            if placed_rectangles[row][col] is None:
                pass
            else:
                col_count += 1
        if col_count == 8:
            remove_col.append(col)
            combos += 1
            score += (10 * combos)
            line_cleared_in_turn = True

    for row in remove_row:
        for col in range(8):
            if(placed_rectangles[row][col]):
                rectangle,outline,c = placed_rectangles[row][col]
                draw.rect(screen, WHITE, rectangle, 0)
                placed_rectangles[row][col] = None
    
    for col in remove_col:
        for row in range(8):
            if(placed_rectangles[row][col]):
                rectangle,outline,c = placed_rectangles[row][col]
                draw.rect(screen, WHITE, rectangle, 0)
                placed_rectangles[row][col] = None   
    if check_all_clear():
        score += 300
# ---------------------------------------------------------------------------------
def check_all_clear():
    for row in placed_rectangles:
        for col in row:
            if col:
                return False
    return True
# ---------------------------------------------------------------------------------
def valid(block):
    """
    checks if all rectangles in block are in grid and not overlapping with placed rectangles"""
    for rectangle,outline,c in block.rectangles:
        if not (100 <= rectangle.x <= 500-50 and 100 <= rectangle.y <= 500-50):
            return False
        for row in placed_rectangles:
            for col in row:
                if col == None:
                    continue
                rectangle2,outline2,c = col 
                if rectangle2.colliderect(rectangle):
                    return False
            
    return True
# ---------------------------------------------------------------------------------
def refresh_next_blocks():
    for i in range(3):
        next_blocks.append(Block())
        next_blocks[i].x = 10
        next_blocks[i].y = i * 4
        next_blocks[i].draw()
# ---------------------------------------------------------------------------------
def is_game_over():

    # if you can place at least 1 return False
    for block in next_blocks:
        shape = block.shape
        num_rows = len(shape)
        num_cols = len(shape[0])
        for x in range(8 - num_cols + 1):
            for y in range(8 - num_rows + 1):
                for i in range(num_rows):
                    for j in range(num_cols):
                        if shape[i][j] == 1 and placed_rectangles[y + i][x + j]:
                            break
                    else:
                        continue
                    break
                else:
                    return False
    return True
                

# ---------------------------------------------------------------------------------
def update_score(value):
    global score
    score += value
# ---------------------------------------------------------------------------------
def display_score():
    global score
    score_display = font1.render(f"Score: {score}", True, WHITE)
    screen.blit(score_display, (50, 50))
# ---------------------------------------------------------------------------------
def save_score(score):
    with open("stats.bin", "wb") as f:
        #best score is always first line
        f.write(score.to_bytes(4, byteorder='big'))
# ---------------------------------------------------------------------------------
def get_best_score():
    best_score = 0 
    with open("stats.bin", "rb") as f:
        best_score = f.read()
    return int.from_bytes(best_score, byteorder='big')
# ---------------------------------------------------------------------------------


# Set up the fonts
font.init()
font1 = font.Font(None, 48)
font2 = font.Font(None, 100)
font3 = font.Font(None, 36)

# Set up the sounds
mixer.init()
# bounce = mixer.Sound("bounce.wav")

# Set up the game clock
clock = time.Clock()

#create window
screen.fill(SPACE_GRAY)

create_grid()

# create score display
score = 0
combos = 0
line_cleared_in_turn = False
display_score()
draw_best_score()

# generate 3 random blocks to right of grid
next_blocks = []
for i in range(3):
    next_blocks.append(Block())
    next_blocks[i].x = 10
    next_blocks[i].y = i * 4
    next_blocks[i].draw()

selected = None
index = None

# 8x8 grid of placed rectangles
placed_rectangles = [[None for _ in range(8)] for _ in range(8)]


# Update the display
display.flip()

# ---------------------------------------------------------------------------------
# Set up the game loop
running = True
while running:
    # Set the frame rate
    clock.tick(60)

    # Handle events
    for e in event.get():
        if e.type == QUIT:
            # save score
            exit()
        
        elif e.type == MOUSEBUTTONDOWN:
            if e.button == 1:
                mouse_x, mouse_y = e.pos
                for i, block in enumerate(next_blocks):
                    for rectangle,outline,c in block.rectangles:
                        if rectangle.collidepoint(mouse_x, mouse_y):
                            selected = block
                            index = i
                            print("clicked", block.shape)

        elif e.type == MOUSEBUTTONUP and selected:
            if e.button == 1:
                if(valid(selected)):
                    next_blocks.pop(index)
                    num_blocks = len(selected.rectangles)
                    for rectangle,outline,c in selected.rectangles:
                        # rectangle and outline should have same x and y
                        x = rectangle.x
                        y = rectangle.y
                        i = x//50 - 2
                        j = y//50 - 2
                        placed_rectangles[j][i] = (rectangle, outline,c)
                    selected = None
                    index = None
                
                    check_row_or_column_full()
                    screen.fill(SPACE_GRAY)
                    draw_placed_blocks()
                    for i in range(len(next_blocks)):
                        next_blocks[i].y = i * 4
                    draw_unplaced_blocks()
                    create_grid()
                    #add 1 score for each block
                    update_score(num_blocks)
                    display_score()
                    draw_best_score()
                    if(len(next_blocks) == 0):
                            if not line_cleared_in_turn:
                                combos = 0
                            refresh_next_blocks()
                            line_cleared_in_turn = False

                    if is_game_over():
                        print("Game Over")
                        # record score and restart game
                        best_score = get_best_score()
                        if score > best_score:
                            save_score(score)
                            best_score = score
                        
                    
                        line_cleared_in_turn = False
                        placed_rectangles = [[None for _ in range(8)] for _ in range(8)]
                        screen.fill(BLUE)
                        ON_RESTART_SCREEN = True
                        text = font2.render("Game Over", True, CYAN)
                        screen.blit(text, (275, 100))
                        text = font1.render(f"Score:", True, CYAN)
                        screen.blit(text, (300, 200))
                        text = font1.render(str(score), True, WHITE)
                        screen.blit(text, (300, 235))
                        text = font1.render(f"Best Score:", True, CYAN)
                        screen.blit(text, (300, 280))
                        text = font1.render(str(best_score), True, WHITE)
                        screen.blit(text, (300, 315))
                        draw.rect(screen, GREEN, (300,360, 200, 50), 0)
                        text = font1.render("Play Again", True, WHITE)
                        screen.blit(text, (310, 370))
                        display.flip()

                        while(ON_RESTART_SCREEN):
                            for e in event.get():
                                if e.type == QUIT:
                                    exit()
                                elif e.type == MOUSEBUTTONDOWN:
                                    if e.button == 1:
                                        mouse_x, mouse_y = e.pos
                                        if 300 <= mouse_x <= 500 and 360 <= mouse_y <= 410:
                                            ON_RESTART_SCREEN = False
                                            break
                           

                        
                        screen.fill(SPACE_GRAY)
                        score = 0
                        combos = 0
                        create_grid()
                        next_blocks.clear()
                        refresh_next_blocks()
                        display_score()
                        draw_best_score()


                        
                else:
                    selected.undraw()
                    selected.x = 10
                    selected.y = index * 4
                    selected = None
                    index = None
                    create_grid()
                    display_score()
                    draw_best_score()
                    draw_placed_blocks()
                    draw_unplaced_blocks()

        elif e.type == MOUSEMOTION and selected:
            selected.x = (e.pos[0] - 50) // 50
            selected.y = (e.pos[1] - 50) // 50
            screen.fill(SPACE_GRAY)

            draw_unplaced_blocks()
            display_score()
            draw_best_score()
            draw_placed_blocks()
            create_grid()

            selected.draw()
            display.flip()
    

    

    # Update the display
    display.flip()
# ---------------------------------------------------------------------------------

# Quit the game
quit()

