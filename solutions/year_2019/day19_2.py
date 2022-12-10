"""
solution AdventOfCode 2019 day 19 part 2.

https://adventofcode.com/2019/day/19.

author: pca

"""

from general.general import read_day
from general.general import measure
from solutions.year_2019.int_machine import IntMachine
from collections import defaultdict
from general.visualize import visualize_grid

def find_borders(grid, y, width):
    border_left, border_right = 0, 0

    for x in range(1, width - 1):
        if grid[(y, x - 1)] == '.' and grid[(y, x)] == '#':
            border_left = x
        if grid[(y, x + 1)] == '.' and grid[(y, x)] == '#':
            border_right = x

    return border_left, border_right

def track_borders(program_code, grid, start_y, width, max_y):
    left_x, right_x = find_borders(grid, start_y, width)

    left_borders = dict()
    right_borders = dict()

    for y in range(start_y + 1, max_y + 1):
        # beam moves only max 1 position to the right each y
        if not is_pulled(program_code, (y, left_x)):
            left_x += 1
        if is_pulled(program_code, (y, right_x + 1)):
            right_x += 1
        left_borders[y] = left_x
        right_borders[y] = right_x

    return left_borders, right_borders


def is_pulled(program_code, pos):
    y, x = pos

    m = IntMachine(program_code, [x, y])
    m.silent = True
    m.run()
    return m.output == [1]

@measure
def solve(program_code, grid):

    # get enough information on the borders to start scanning.
    left_borders, right_borders = track_borders(program_code, grid, 49, 50, 1500)

    # just run through the border locations and see if a position is valid
    for y in range(50, 1400):
        left_x = left_borders[y]
        right_x = right_borders[y]
        for x in range(left_x, right_x + 1):
            # check if adding 100 to y is within the beam
            if x >= left_borders[y + 99] and x + 99 <= right_borders[y]:
                return y, x

    return None

def main(args=None):
    program_code = read_day(2019, 19)[0]

    grid = defaultdict(str)

    cnt = 0

    for x in range(50):
        for y in range(50):
            if is_pulled(program_code, (y, x)):
                grid[(y, x)] = '#'
                cnt += 1
            else:
                grid[(y, x)] = '.'

    # add the borders to the grid (to use in the visualization)
    left_borders, right_borders = track_borders(program_code, grid, 49, 50, 1500)
    for y in left_borders:
        x = left_borders[y]
        grid[(y, x)] = '#'
    for y in right_borders:
        x = right_borders[y]
        grid[(y, x)] = '#'

    y, x = solve(program_code, grid)
    print(f"Location: y, x {(y, x)} solution: {x * 10000 + y}")

    # add the 100x100 rectangle to the grid
    for dy in range(100):
        for dx in range(100):
            grid[(y + dy, x + dx)] = 'O'

    # visualize the grid to check the solution
    img = visualize_grid(grid, (1200, 500), colors={'#': 'blue', '.': 'white', '': 'white', 'O': 'red'}, outline=None)
    img.show()


if __name__ == "__main__":
    main()
