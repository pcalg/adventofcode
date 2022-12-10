"""
solution AdventOfCode 2019 day 15 part 2.

https://adventofcode.com/2019/day/15.

author: pca

"""

from general.general import read_day
from collections import defaultdict
from solutions.year_2019.int_machine import IntMachine
from enum import Enum
from copy import deepcopy


class Directions(Enum):
    NORTH = 1
    SOUTH = 2
    WEST = 3
    EAST = 4


class StatusCodes(Enum):
    EMPTY = -1
    WALL = 0
    OPEN = 1
    OXYGEN = 2


deltas = {Directions.NORTH: (-1, 0),  Directions.EAST: (0, 1), Directions.SOUTH: (1, 0), Directions.WEST: (0, -1)}


turns = {Directions.NORTH: Directions.EAST, Directions.EAST: Directions.SOUTH, Directions.SOUTH: Directions.WEST,
         Directions.WEST: Directions.NORTH}


grid_codes = {StatusCodes.EMPTY: ' ', StatusCodes.WALL: '#', StatusCodes.OPEN: '.', StatusCodes.OXYGEN: 'O'}


def draw_grid(grid):

    if len(grid) == 0:
        return

    ys = [y for y, _ in grid.keys()]
    xs = [x for _, x in grid.keys()]

    min_y = min(ys)
    max_y = max(ys)

    min_x = min(xs)
    max_x = max(xs)

    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            if (y, x) == (0, 0):
                print("X", end="")
            else:
                ch = grid_codes[grid[(y, x)]]
                print(ch, end="")
        print("")
    print("")


def find_oxygen(m_initial):
    """
    Use BFS to find the location of the Oxygen. This by cloning the IntMachine for each direction.
    """

    queue = list()
    grid = defaultdict(lambda: StatusCodes.EMPTY)

    queue.append((0, (0, 0), m_initial))
    visited = {(0, 0)}

    distances = {(0, 0): 0}

    oxygen_location = (0, 0)

    # Use BFS to find the route
    while len(queue) > 0:
        d, pos, m = queue.pop(0)

        y, x = pos

        # try out each direction and run the machine there
        for direction in Directions:
            dy, dx = deltas[direction]
            new_pos = y + dy, x + dx

            # no use to try if we already have been here
            if new_pos not in visited:
                visited.add(new_pos)
                distances[new_pos] = d + 1
            else:
                continue

            tmp_m = deepcopy(m)
            tmp_m.add_input(direction.value)
            tmp_m.run()

            status = tmp_m.read_next_output()

            grid[new_pos] = StatusCodes(status)

            if status in [StatusCodes.OXYGEN.value, StatusCodes.OPEN.value]:
                queue.append((d + 1, new_pos, tmp_m))
                distances[new_pos] = d + 1

            if status == StatusCodes.OXYGEN.value:
                oxygen_location = new_pos

    return oxygen_location, grid


def oxygen_fill(grid, oxygen_location):
    """
    Use BFS to find the location of the Oxygen. This by cloning the IntMachine for each direction.
    """

    queue = [(0, oxygen_location)]
    visited = {oxygen_location}

    # Use BFS to find the route
    while len(queue) > 0:
        d, pos = queue.pop(0)

        y, x = pos

        # try out each direction and run the machine there
        for direction in Directions:
            dy, dx = deltas[direction]
            new_pos = y + dy, x + dx

            # no use to try if we already have been here
            if new_pos not in visited:
                visited.add(new_pos)
            else:
                continue

            status = grid[new_pos]

            if status in [StatusCodes.OXYGEN, StatusCodes.OPEN]:
                queue.append((d + 1, new_pos))

    return d


def main(args=None):

    program_code = read_day(2019, 15)[0]
    m = IntMachine(program_code, [])
    m.max_steps = 1550000
    m.pause_output = True
    m.silent = True

    oxygen_location, grid = find_oxygen(m)

    draw_grid(grid)

    oxygen_time = oxygen_fill(grid, oxygen_location)

    print(f"Time it takes to fill: {oxygen_time}")


if __name__ == "__main__":
    main()
