'''
==========================================
 Title:  Maze Generation
 Author: Burak Sekili
 Date:   6 April 2020
==========================================
'''

import pygame
import time
from random import randint

WIDTH = 600
HEIGHT = 600
BOX_WIDTH = 60
FPS = 30

# column_size is actually size of x coordinates in 2d coordinate system
column_size = int(WIDTH / BOX_WIDTH)
# row_size is actually size of y coordinates in 2d coordinate system
row_size = int(HEIGHT / BOX_WIDTH)

entry_x = 0
entry_y = 0

exit_x = column_size - 1
exit_y = row_size - 1

delay_time = 0.1

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Generator")

# visited_cells keeps visited cells as a tuple coordinates.
# etc. ((0, 0), (0,1))
visited_cells = [(entry_x, entry_y)]

# unvisited_cells is used to find solution path in maze.
# it has same properties as 'visited_cells'
unvisited_cells = []

# These are dictionaries to keep
# which wall in maze is collapsed.
# They take tuple coordinate pixel as a key, and
# boolean result as a value. If values is True,
# we do not have wall.
broken_walls_right = {}
broken_walls_left = {}
broken_walls_up = {}
broken_walls_down = {}

environment = []
RED = (240, 0, 0)
WHITE = (255, 255, 255)
CELL_COLOR = (0, 102, 102)
BLACK = (0, 0, 0)
screen.fill(BLACK)


def generate_environment():
    for x in range(0, WIDTH, BOX_WIDTH):
        for y in range(0, HEIGHT, BOX_WIDTH):
            rect = pygame.Rect(x, y, BOX_WIDTH, BOX_WIDTH)
            pygame.draw.rect(screen, WHITE, rect, 1)
            broken_walls_right[x, y] = False
            broken_walls_left[x, y] = False
            broken_walls_up[x, y] = False
            broken_walls_down[x, y] = False


def find_neighbours(x, y):
    neighbours = []
    if x - 1 >= 0 and (x - 1, y) not in visited_cells:
        neighbours.append((x - 1, y))
    if x + 1 < column_size and (x + 1, y) not in visited_cells:
        neighbours.append((x + 1, y))

    if y - 1 >= 0 and (x, y - 1) not in visited_cells:
        neighbours.append((x, y - 1))
    if y + 1 < row_size and (x, y + 1) not in visited_cells:
        neighbours.append((x, y + 1))
    return neighbours


def break_wall(cell, movement_direction):
    x = cell[0] * BOX_WIDTH  # To draw rectangles in grid system, we need to move;
    y = cell[1] * BOX_WIDTH  # BOX_WIDTH by BOX_WIDTH pixel, instead of 1px by 1px.
    w = BOX_WIDTH - 1  # alias for BOX_WIDTH - 1
    interval = 2  # interval is used to distinguish rectangles on grid easily.

    # movement_direction = 0 means go to the right
    if movement_direction == 0:
        rect = pygame.Rect(x + 1, y + 1, 2 * w - interval, w)
        pygame.draw.rect(screen, CELL_COLOR, rect, 0)

    # movement_direction = 1 means go to the left
    elif movement_direction == 1:
        rect = pygame.Rect(x - BOX_WIDTH + 1, y + 1, 2 * w - interval, w)
        pygame.draw.rect(screen, CELL_COLOR, rect, 0)

    # movement_direction = 2 means go to the down
    elif movement_direction == 2:
        rect = pygame.Rect(x + 1, y + 1, w, 2 * w - interval)
        pygame.draw.rect(screen, CELL_COLOR, rect)

    # movement_direction = 3 means go to the up
    elif movement_direction == 3:
        rect = pygame.Rect(x + 1, y - BOX_WIDTH + 1, w, 2 * w - interval)
        pygame.draw.rect(screen, CELL_COLOR, rect)

    pygame.display.update()


def knockdown_wall(curr, unvisited, is_solution=False):
    curr_x = curr[0] * BOX_WIDTH
    curr_y = curr[1] * BOX_WIDTH

    next_x = unvisited[0] * BOX_WIDTH
    next_y = unvisited[1] * BOX_WIDTH

    if curr[0] - unvisited[0] == -1:
        if not is_solution:
            break_wall(curr, 0)
        broken_walls_right[(curr_x, curr_y)] = True
        broken_walls_left[(next_x, next_y)] = True
    if curr[0] - unvisited[0] == 1:
        if not is_solution:
            break_wall(curr, 1)
        broken_walls_left[(curr_x, curr_y)] = True
        broken_walls_right[(next_x, next_y)] = True

    if curr[1] - unvisited[1] == -1:
        if not is_solution:
            break_wall(curr, 2)
        broken_walls_down[(curr_x, curr_y)] = True
        broken_walls_up[(next_x, next_y)] = True

    if curr[1] - unvisited[1] == 1:
        if not is_solution:
            break_wall(curr, 3)
        broken_walls_up[(curr_x, curr_y)] = True
        broken_walls_down[(next_x, next_y)] = True


def find_neighbours_solution(xc, yc):
    current_neighbours = []
    coord_val_tuple = (xc * BOX_WIDTH, yc * BOX_WIDTH)

    # if there is no wall on the right, right cell can be  next cell to reach end point.
    if xc + 1 < column_size and (xc + 1, yc) not in unvisited_cells and broken_walls_right[coord_val_tuple]:
        current_neighbours.append((xc + 1, yc))

    # if there is no wall on the left, left cell can be next cell to reach end point.
    if xc - 1 >= 0 and (xc - 1, yc) not in unvisited_cells and broken_walls_left[coord_val_tuple]:
        current_neighbours.append((xc - 1, yc))

    # if there is no wall on the up, upper cell can be next cell to reach end point.
    if yc - 1 >= 0 and (xc, yc - 1) not in unvisited_cells and broken_walls_up[coord_val_tuple]:
        current_neighbours.append((xc, yc - 1))

    # if there is no wall on the up, the cell below can be next cell to reach end point.
    if yc + 1 < row_size and (xc, yc + 1) not in unvisited_cells and broken_walls_down[coord_val_tuple]:
        current_neighbours.append((xc, yc + 1))
    return current_neighbours


def generate_maze():
    path_stack = []
    initial_coord = visited_cells[0]
    path_stack.append(initial_coord)

    while len(path_stack) != 0:
        current_coord = path_stack.pop()
        curr_neighbours = find_neighbours(current_coord[0], current_coord[1])
        if len(curr_neighbours) > 0:
            path_stack.append(current_coord)

            rand_idx = randint(0, len(curr_neighbours)) % len(curr_neighbours)
            unvisited_coord = curr_neighbours[rand_idx]

            knockdown_wall(current_coord, unvisited_coord)
            visited_cells.append(unvisited_coord)
            path_stack.append(unvisited_coord)
        time.sleep(delay_time)


def knockdown_wall_sol(curr, unvisited):
    curr_x = curr[0]
    curr_y = curr[1]

    next_x = unvisited[0]
    next_y = unvisited[1]

    if curr[0] - unvisited[0] == -BOX_WIDTH:
        broken_walls_right[(curr_x, curr_y)] = True
        broken_walls_left[(next_x, next_y)] = True
    if curr[0] - unvisited[0] == BOX_WIDTH:
        broken_walls_left[(curr_x, curr_y)] = True
        broken_walls_right[(next_x, next_y)] = True

    if curr[1] - unvisited[1] == -BOX_WIDTH:
        broken_walls_down[(curr_x, curr_y)] = True
        broken_walls_up[(next_x, next_y)] = True

    if curr[1] - unvisited[1] == BOX_WIDTH:
        broken_walls_up[(curr_x, curr_y)] = True
        broken_walls_down[(next_x, next_y)] = True


def display_solution(solution_list):
    dot_size = BOX_WIDTH / 5
    mid_coord = BOX_WIDTH / 2
    (x_coord, y_coord) = solution_list[0]
    for idx in range(1, len(solution_list)):
        rect = pygame.Rect((x_coord * BOX_WIDTH) + mid_coord, (y_coord * BOX_WIDTH) + mid_coord, dot_size, dot_size)
        pygame.draw.rect(screen, RED, rect)
        pygame.display.update()

        (x_coord, y_coord) = solution_list[idx]
        time.sleep(delay_time)
    rect = pygame.Rect((exit_x * BOX_WIDTH) + mid_coord, (exit_y * BOX_WIDTH) + mid_coord, dot_size, dot_size)
    pygame.draw.rect(screen, RED, rect)
    pygame.display.update()


def solve_maze():
    solution = [(entry_x, entry_y)]
    path_stack = [(entry_x, entry_y)]
    unvisited_cells.append((entry_x, entry_y))
    while len(path_stack) > 0:
        current = path_stack.pop()
        current_cell = solution.pop()

        if current_cell[0] == exit_x and current_cell[1] == exit_y:
            solution.append(current_cell)
            break
        neighbours = find_neighbours_solution(current_cell[0], current_cell[1])
        if len(neighbours) > 0:
            path_stack.append(current)
            solution.append(current_cell)

            rand_idx = randint(0, len(neighbours)) % len(neighbours)
            unvisited = neighbours[rand_idx]

            unvisited_cells.append((unvisited[0], unvisited[1]))

            path_stack.append(unvisited)
            solution.append(unvisited)
    display_solution(solution)


if __name__ == '__main__':
    generate_environment()
    pygame.display.update()

    generate_maze()
    pygame.display.update()
    solve_maze()
    pygame.display.update()

running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


def solve_maze():
    solution = [(entry_x, entry_y)]
    path_stack = [(entry_x, entry_y)]
    unvisited_cells.append((entry_x, entry_y))
    while len(path_stack) > 0:
        current = path_stack.pop()
        current_cell = solution.pop()

        if current_cell[0] == exit_x and current_cell[1] == exit_y:
            solution.append(current_cell)
            break
        neighbours = find_neighbours_solution(current_cell[0], current_cell[1])
        if len(neighbours) > 0:
            path_stack.append(current)
            solution.append(current_cell)

            rand_idx = randint(0, len(neighbours)) % len(neighbours)
            unvisited = neighbours[rand_idx]

            unvisited_cells.append((unvisited[0], unvisited[1]))

            path_stack.append(unvisited)
            solution.append(unvisited)
    display_solution(solution)


if __name__ == '__main__':
    generate_environment()
    pygame.display.update()

    generate_maze()
    pygame.display.update()
    solve_maze()
    pygame.display.update()

running = True
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
