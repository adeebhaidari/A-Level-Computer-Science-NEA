"""Handcrafted 20x20 maze with multiple solutions.

Grid encoding:
 - 0 : open cell
 - 1 : wall

START is (1,1) and END is (19,19) (0-based indices). The file exposes:
 - generate_maze() -> (grid, start, end)
 - MAZE, START, END constants

This maze is built by creating border walls and adding a few vertical/horizontal
obstacles with deliberate openings so there are multiple paths from START to END.
"""

from copy import deepcopy
from pprint import pprint

MAZE_SIZE = 20
START = (1, 1)
END = (19, 19)


def generate_maze():
    """Return a 20x20 maze (list of lists), and (start, end) coordinates.

    The function constructs the maze programmatically so it's easy to tweak.
    """
    # start with an empty grid (all open)
    grid = [[0 for _ in range(MAZE_SIZE)] for _ in range(MAZE_SIZE)]

    # add border walls
    for c in range(MAZE_SIZE):
        grid[0][c] = 1
        grid[MAZE_SIZE - 1][c] = 1
    for r in range(MAZE_SIZE):
        grid[r][0] = 1
        grid[r][MAZE_SIZE - 1] = 1

    # keep START and END open (they might be on the border)
    sr, sc = START
    er, ec = END
    grid[sr][sc] = 0
    grid[er][ec] = 0

    # Ensure adjacent cells to END are open so the end is reachable
    if er - 1 >= 0:
        grid[er - 1][ec] = 0
    if ec - 1 >= 0:
        grid[er][ec - 1] = 0

    # Add several vertical walls with spaced openings to create multiple routes
    vertical_walls = [4, 9, 14]
    # rows where openings exist (allow passage through the wall)
    open_rows = {2, 5, 8, 11, 14, 17}
    for col in vertical_walls:
        for r in range(1, MAZE_SIZE - 1):
            if r not in open_rows:
                grid[r][col] = 1

    # Add horizontal barriers with openings
    horizontal_walls = [6, 12]
    open_cols = {1, 3, 6, 9, 12, 15, 18}
    for row in horizontal_walls:
        for c in range(1, MAZE_SIZE - 1):
            if c not in open_cols:
                grid[row][c] = 1

    # Add a few extra block cells to create small dead-ends (more branching)
    extras = [
        (3, 3), (3, 4), (4, 3),
        (10, 7), (10, 8),
        (16, 13), (15, 13),
    ]
    for r, c in extras:
        # keep START and END safe
        if (r, c) not in (START, END):
            grid[r][c] = 1

    # Make sure START is open
    grid[sr][sc] = 0

    # final safety: ensure grid is MAZE_SIZE x MAZE_SIZE
    assert len(grid) == MAZE_SIZE and all(len(row) == MAZE_SIZE for row in grid)

    return grid, START, END


# module-level constants
MAZE, START, END = generate_maze()


def print_maze(grid=None):
    """Pretty-print the maze where 1=█ and 0=' '."""
    if grid is None:
        grid = MAZE
    for r, row in enumerate(grid):
        line = ''.join('█' if cell == 1 else ' ' for cell in row)
        # mark start and end for visual clarity
        if r == START[0]:
            # replace the character at START column
            line = line[:START[1]] + 'S' + line[START[1] + 1:]
        if r == END[0]:
            line = line[:END[1]] + 'E' + line[END[1] + 1:]
        print(line)


if __name__ == '__main__':
    print(f"Maze size: {MAZE_SIZE}x{MAZE_SIZE}")
    print(f"START = {START}, END = {END}\n")
    print_maze()
