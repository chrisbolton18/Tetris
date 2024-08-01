import sys
import pygame
import random
from config import *
from grid import create_grid, draw_grid, draw_window, clear_rows
from piece import Piece
from utils import valid_space, convert_shape_format, check_lost
from menu import show_menu

pygame.init()  # Initialize pygame

def game_loop():
    """Main game loop where the game runs."""
    locked_positions = {}
    grid = create_grid(locked_positions)

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

def main():
    """Main function to run the game."""
    while True:
        menu_option = show_menu()
        if menu_option == 'Start Game':
            game_loop()
        elif menu_option == 'Quit':
            pygame.quit()
            break

if __name__ == "__main__":
    main()
