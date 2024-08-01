import pygame
import sys
import random
from config import SHAPES, SHAPE_COLORS, GRID_WIDTH, GRID_HEIGHT, BLOCK_SIZE
from grid import create_grid, draw_grid, draw_window, clear_rows
from piece import Piece
from utils import valid_space, convert_shape_format, check_lost

# Initialize pygame
pygame.init()

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

# Set up the display
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tetris")

# Function to draw text on the screen
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)

def show_menu():
    screen.fill(BLACK)
    font = pygame.font.SysFont('comicsans', 60)
    small_font = pygame.font.SysFont('comicsans', 40)

    # Draw title closer to the top
    title_text = 'Tetris'
    title_obj = font.render(title_text, True, WHITE)
    title_rect = title_obj.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
    screen.blit(title_obj, title_rect)

    # Draw menu options
    start_text = 'Start Game'
    quit_text = 'Quit'
    start_obj = small_font.render(start_text, True, BLUE)
    quit_obj = small_font.render(quit_text, True, BLUE)
    start_rect = start_obj.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    quit_rect = quit_obj.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60))
    screen.blit(start_obj, start_rect)
    screen.blit(quit_obj, quit_rect)

    pygame.display.update()

    # Event handling loop for menu
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if start_rect.collidepoint(mouse_pos):
                    print("Start Game clicked")
                    return 'Start Game'  # Return to start the game
                elif quit_rect.collidepoint(mouse_pos):
                    print("Quit clicked")
                    pygame.quit()
                    sys.exit()

def start_game():
    locked_positions = {}
    grid = create_grid(locked_positions)

    def game_loop():
        change_piece = False
        run = True
        current_piece = Piece(random.choice(SHAPES))
        next_piece = Piece(random.choice(SHAPES))
        clock = pygame.time.Clock()
        fall_time = 0
        fall_speed = 0.27

        while run:
            grid = create_grid(locked_positions)
            fall_time += clock.get_rawtime()
            clock.tick()

            if fall_time / 1000 >= fall_speed:
                fall_time = 0
                current_piece.y += 1
                if not valid_space(current_piece, grid) and current_piece.y > 0:
                    current_piece.y -= 1
                    change_piece = True

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        current_piece.x -= 1
                        if not valid_space(current_piece, grid):
                            current_piece.x += 1
                    elif event.key == pygame.K_RIGHT:
                        current_piece.x += 1
                        if not valid_space(current_piece, grid):
                            current_piece.x -= 1
                    elif event.key == pygame.K_DOWN:
                        current_piece.y += 1
                        if not valid_space(current_piece, grid):
                            current_piece.y -= 1
                    elif event.key == pygame.K_UP:
                        current_piece.rotate()
                        if not valid_space(current_piece, grid):
                            current_piece.rotate()  # Rotate back if invalid

            shape_pos = convert_shape_format(current_piece)

            for pos in shape_pos:
                x, y = pos
                if y > -1:
                    grid[y][x] = current_piece.color

            if change_piece:
                for pos in shape_pos:
                    p = (pos[0], pos[1])
                    locked_positions[p] = current_piece.color
                current_piece = next_piece
                next_piece = Piece(random.choice(SHAPES))
                change_piece = False

                clear_rows(grid, locked_positions)

                if check_lost(locked_positions):
                    run = False

            draw_window(grid)

    game_loop()  # Start the game loop

def main():
    """Main function to run the game."""
    while True:
        menu_option = show_menu()
        if menu_option == 'Start Game':
            start_game()
        elif menu_option == 'Quit':
            pygame.quit()
            break

if __name__ == "__main__":
    main()
