"""
solution Adventofcode 2019 day 3 part 2.

https://adventofcode.com/2019/day/3

author: pca
"""

from general.general import read_day
from collections import defaultdict


def find_crossings(grid):
    # crossing is a location having multiple wires
    result = list()

    for (y, x), wire_set in grid.items():
        if len(wire_set) > 1:
            result.append((y, x))

    return result


def find_steps(routes, crossings):
    result = list()

    for crossing in crossings:
        steps = 0
        for route in routes:
            if crossing in route:
                steps += route[crossing]
        result.append(steps)

    return result


def add_single_wire(grid, routes, wire_id, wire):
    # directions in (y, x) coords
    directions = {'R': (0, 1), 'D': (-1, 0), 'L': (0, -1), 'U': (1, 0)}

    instructions = wire.split(',')

    current_route = dict()
    routes.append(current_route)

    y, x = 0, 0

    total_steps = 0

    for instruction in instructions:
        direction = instruction[0]
        steps = int(instruction[1:])

        dy, dx = directions[direction]

        for step in range(steps):
            y, x = y + dy, x + dx
            grid[(y, x)].add(wire_id)
            if (y, x) not in current_route:
                current_route[(y, x)] = total_steps + 1

            total_steps += 1


def add_wires(grid, routes, wires):
    for idx, wire in enumerate(wires):
        add_single_wire(grid, routes, idx, wire)


def main():
    wires = read_day(2019, 3)

    grid = defaultdict(set)
    routes = list()
    add_wires(grid, routes, wires)

    # find all the crossings
    crossings = find_crossings(grid)

    # find the steps to each crossing
    all_steps = find_steps(routes, crossings)

    print(f"solution: {min(all_steps)}")

    return grid, routes


if __name__ == "__main__":
    grid, routes = main()
