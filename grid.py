import pygame
from config import *

def create_grid(locked_positions={}):
    grid = [[BLACK for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            if (x, y) in locked_positions:
                grid[y][x] = locked_positions[(x, y)]

    return grid

def draw_grid(grid):
    for y in range(GRID_HEIGHT):
        for x in range(GRID_WIDTH):
            pygame.draw.rect(screen, grid[y][x], (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)

    for y in range(GRID_HEIGHT):
        pygame.draw.line(screen, GRAY, (0, y * BLOCK_SIZE), (SCREEN_WIDTH, y * BLOCK_SIZE))
    for x in range(GRID_WIDTH):
        pygame.draw.line(screen, GRAY, (x * BLOCK_SIZE, 0), (x * BLOCK_SIZE, SCREEN_HEIGHT))

def draw_window(grid):
    screen.fill(BLACK)
    draw_grid(grid)
    pygame.display.update()

def clear_rows(grid, locked):
    increment = 0
    for y in range(GRID_HEIGHT - 1, -1, -1):
        row = grid[y]
        if BLACK not in row:
            increment += 1
            ind = y
            for x in range(GRID_WIDTH):
                try:
                    del locked[(x, y)]
                except:
                    continue

    if increment > 0:
        for key in sorted(list(locked), key=lambda k: k[1])[::-1]:
            x, y = key
            if y < ind:
                newKey = (x, y + increment)
                locked[newKey] = locked.pop(key)

    return increment
