"""
solution AdventOfCode 2019 day 17 part 2.

https://adventofcode.com/2019/day/17.

author: pca

"""

from general.general import read_day, measure
from solutions.year_2019.int_machine import IntMachine
from collections import defaultdict
from general.visualize import visualize_grid
from pathlib import Path
from itertools import combinations


def cross2d(direction_current, direction_next):
    dc_y, dc_x = direction_current
    dn_y, dn_x = direction_next
    return dc_y * dn_x - dc_x * dn_y


def find_turn(grid, pos, current_direction):
    deltas = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    turns = {-1: 'R', 1: 'L'}

    cy, cx = current_direction
    y, x = pos
    mirror_cy, mirror_cx = -cy, -cx

    for dy, dx in deltas:
        if grid[y + dy, x + dx] == '#' and (dy, dx) != (mirror_cy, mirror_cx):
            # dy, dx is the way to go and we have made sure we're not going backwards
            turn = turns[cross2d((cy, cx), (dy, dx))]
            return turn, (dy, dx)

    # nowhere to go
    return '', (0, 0)


def walk_grid(grid, start_pos):
    """
    Walk over the scaffold ("#") to find the total route.
    """

    result = []

    # robot is initially turned upwards
    current_direction = (-1, 0)

    y, x = start_pos

    distance = 1

    while True:
        turn, current_direction = find_turn(grid, (y, x), current_direction)

        # done when there is nowhere to go anymore
        if turn == '':
            break

        dy, dx = current_direction

        # possible to move, then do so
        while grid[(y + dy, x + dx)] == '#':
            y += dy
            x += dx
            distance += 1

        # not possible to move in this direction anymore
        result.append((turn, distance))
        distance = 0

    return result


def save_grid(fn: Path, ascii_output):
    with open(fn, 'w') as f:
        for ch in ascii_output:
            f.write(ch)


def to_grid(ascii_output):
    grid = defaultdict(lambda: '.')
    x = 0
    max_x = 0
    y = 0
    start_pos = (0, 0)

    for ch in ascii_output:
        if ch == '\n':
            y += 1
            x = 0
        else:
            grid[(y, x)] = ch
            x += 1
            if x > max_x:
                max_x = x
            if ch == '^':
                start_pos = (y, x)

    return grid, (y + 1, max_x + 1), start_pos


def len_route(current_route):
    """
    Calculate the length of this route as when it is translated to ascii commands.

    current_route: tuples with the current route.
    [('L', 8),('R', 10),('L', 9) -->] will be translated to L,8,R,10,L,9 (comma's also count)

    total_length = length each direction + length each number + (number of tuples * 2) - 1

    """
    n_tuples = len(current_route)

    if n_tuples == 0:
        return 0
    else:
        return sum([len(direction) + len(str(n)) for direction, n in current_route]) + n_tuples * 2 - 1


def all_sub_lists(route):
    """
    Generate all valid sub routes in the route list.
    Valid routes are routes that take up at most 20 characters.
    """
    for start_idx in range(len(route)):
        for end_idx in range(start_idx + 1, len(route) + 1):
            if len_route(route[start_idx: end_idx]) <= 20:
                yield route[start_idx: end_idx]


def possible_register_values(route):
    """
    We have 3 registers, so use the sub lists to find all the values possible for the 3 registers.
    """
    return combinations(all_sub_lists(route), 3)


def has_possible_route(total_route, sub_routes):
    """
    Check how it is possible to construct the total route from the sub_routes (part a, b and c)

    Sub_routes has 3 items (0, 1, 2)

    """

    # start at idx
    state = [(total_route, [])]

    while len(state) > 0:
        current_route, actions = state.pop()

        # Found a solution when we covered the whole route
        if len(current_route) == 0:
            # Also the main routine (the actions) also has a restriction of 20 chars
            if (len(actions) * 2 - 1) <= 20:
                return True, actions
            else:
                continue

        # check if a sub_route matches
        for idx, sub_route in enumerate(sub_routes):
            size = len(sub_route)
            if size > 0 and current_route[:size] == sub_route:
                state.append((current_route[size:], actions + [idx]))

    # no solution
    return False, None


def find_actions(route, registers_values):
    lookup = {0: 'A', 1: 'B', 2: 'C'}

    for registers_value in registers_values:
        found, actions = has_possible_route(route, registers_value)
        if found:
            return registers_value, [lookup[n] for n in actions]

    return None, None


def to_ascii(s, new_line=10):
    return [ord(ch) for ch in s] + [new_line]


@measure
def main(args=None):
    program_code = read_day(2019, 17)[0]

    m = IntMachine(program_code, [])
    m.run()

    # convert output to ascii
    ascii_output = [chr(val) for val in m.output]

    g, dimensions, start_pos = to_grid(ascii_output)

    # get an idea on how the grid looks like
    img = visualize_grid(g, dimensions, {'.': (255, 255, 255), '#': (0, 0, 0), '^': (128, 128, 0)}, box_size=10)
    img.save("grid_day17.png")
    save_grid("grid_day17.txt", ascii_output)

    # find the directions to walk the whole grid
    route = walk_grid(g, start_pos)

    # need to split the route in to parts of max 20 chars, so find all possible combinations
    all_registers_values = possible_register_values(route)

    # find the right combination for the three 3 registers
    registers, actions = find_actions(route, all_registers_values)

    # setup the program for the IntMachine
    function_main = to_ascii(",".join(actions))
    function_A = to_ascii(",".join([d + "," + str(v) for d, v in registers[0]]))
    function_B = to_ascii(",".join([d + "," + str(v) for d, v in registers[1]]))
    function_C = to_ascii(",".join([d + "," + str(v) for d, v in registers[2]]))
    video_feed = to_ascii(["n"])

    total_input = function_main + function_A + function_B + function_C + video_feed

    m_walker = IntMachine(program_code, total_input)
    m_walker.memory[0] = 2
    m_walker.max_steps = 1500000
    m_walker.run()

    print(f"Amount of dust collected: {m_walker.output[-1]}")


if __name__ == "__main__":
    main()
