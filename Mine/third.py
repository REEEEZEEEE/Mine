import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Game settings
WIDTH, HEIGHT = 800, 900  # Extra space for input box and scoreboard
ROWS, COLS = 5, 5
CELL_SIZE = WIDTH // COLS
DEFAULT_MINES = 3
REVEALED_SCORE = 10

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Stake Mines Game")

# Textbox and scoreboard setup
font = pygame.font.SysFont(None, 24)
input_box = pygame.Rect(200, 860, 140, 32)
start_button = pygame.Rect(350, 860, 100, 32)
score = 0
input_text = ''
mines = DEFAULT_MINES
game_over = False

# Cell class to manage each cell's state
class Cell:
    def __init__(self):
        self.is_mine = False
        self.is_revealed = False
        self.is_flagged = False

    def reveal(self):
        self.is_revealed = True

# Generate the grid
grid = [[Cell() for _ in range(COLS)] for _ in range(ROWS)]

# Place mines randomly
def place_mines():
    global mines
    count = 0
    while count < mines:
        row = random.randint(0, ROWS - 1)
        col = random.randint(0, COLS - 1)
        if not grid[row][col].is_mine:
            grid[row][col].is_mine = True
            count += 1

# Draw the grid, cells, scoreboard, and input instructions
def draw_grid():
    # Draw cells
    for row in range(ROWS):
        for col in range(COLS):
            x, y = col * CELL_SIZE, row * CELL_SIZE + 50  # Offset for scoreboard
            rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
            cell = grid[row][col]
            
            if cell.is_revealed:
                if cell.is_mine:
                    pygame.draw.rect(screen, RED, rect)  # Red for mines
                else:
                    pygame.draw.rect(screen, GREEN, rect)  # Green for safe cells
            else:
                pygame.draw.rect(screen, GRAY, rect)
                if cell.is_flagged:
                    pygame.draw.rect(screen, BLUE, rect)  # Blue for flagged cells

            pygame.draw.rect(screen, BLACK, rect, 1)  # Border
    
    # Draw scoreboard
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (20, 10))
    
    # Draw input instruction and input box
    instruction_text = font.render("How many mines?", True, BLACK)
    screen.blit(instruction_text, (50, 860))
    pygame.draw.rect(screen, WHITE, input_box)
    pygame.draw.rect(screen, BLACK, input_box, 2)
    input_surface = font.render(input_text, True, BLACK)
    screen.blit(input_surface, (input_box.x + 5, input_box.y + 5))

    # Draw start button
    pygame.draw.rect(screen, WHITE, start_button)
    pygame.draw.rect(screen, BLACK, start_button, 2)
    button_text = font.render("Start", True, BLACK)
    screen.blit(button_text, (start_button.x + 15, start_button.y + 5))

# Reset the game
def reset_game():
    global grid, score, game_over
    grid = [[Cell() for _ in range(COLS)] for _ in range(ROWS)]
    score = 0
    game_over = False
    place_mines()

# Game initialization
place_mines()

# Game loop
running = True
input_active = False
while running:
    screen.fill(WHITE)
    draw_grid()

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if input_box.collidepoint(event.pos):  # Click on input box
                input_active = True
            else:
                input_active = False

            if start_button.collidepoint(event.pos):  # Click on start button
                try:
                    mines = max(1, min(int(input_text), ROWS * COLS - 1))  # Cap mines between 1 and max possible cells
                    reset_game()
                except ValueError:
                    pass  # Ignore invalid input

            if not game_over:
                x, y = pygame.mouse.get_pos()
                row, col = (y - 50) // CELL_SIZE, x // CELL_SIZE
                if 0 <= row < ROWS and 0 <= col < COLS:
                    cell = grid[row][col]
                    if event.button == 1:  # Left-click to reveal cell
                        if not cell.is_flagged:
                            cell.reveal()
                            if cell.is_mine:
                                print("You hit a mine! Game over.")
                                game_over = True
                                draw_grid()  # Redraw to show the red cell
                                pygame.display.flip()  # Update display
                                pygame.time.delay(1000)  # Pause for 1 second
                                reset_game()  # Restart game
                            else:
                                score += REVEALED_SCORE
                                print(f"Score: {score}")
                    elif event.button == 3:  # Right-click to flag cell
                        if not cell.is_revealed:
                            cell.is_flagged = not cell.is_flagged

        elif event.type == pygame.KEYDOWN:
            if input_active:  # Handle typing for mine input
                if event.key == pygame.K_RETURN:
                    input_active = False
                    try:
                        mines = max(1, min(int(input_text), ROWS * COLS - 1))
                        reset_game()
                    except ValueError:
                        pass
                    input_text = ''
                elif event.key == pygame.K_BACKSPACE:
                    input_text = input_text[:-1]
                else:
                    if event.unicode.isdigit():  # Only allow digit inputs
                        input_text += event.unicode

            if event.key == pygame.K_c and not game_over:  # Cash out with "C"
                print(f"Cash out! Final score: {score}")
                reset_game()

    pygame.display.flip()

pygame.quit()
sys.exit()
