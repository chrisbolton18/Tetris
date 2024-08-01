from config import GRID_WIDTH, GRID_HEIGHT, BLACK

def valid_space(shape, grid):
    accepted_positions = [[(x, y) for x in range(GRID_WIDTH) if grid[y][x] == BLACK] for y in range(GRID_HEIGHT)]
    accepted_positions = [x for item in accepted_positions for x in item]

    formatted_shape = convert_shape_format(shape)

    for pos in formatted_shape:
        if pos not in accepted_positions:
            if pos[1] > -1:
                return False
    return True

def convert_shape_format(shape):
    positions = []
    shape_format = shape.shape

    for y, line in enumerate(shape_format):
        row = list(line)
        for x, column in enumerate(row):
            if column == 1:
                positions.append((shape.x + x, shape.y + y))

    for i, pos in enumerate(positions):
        positions[i] = (pos[0], pos[1])

    return positions

def check_lost(positions):
    for pos in positions:
        x, y = pos
        if y < 1:
            return True
    return False
