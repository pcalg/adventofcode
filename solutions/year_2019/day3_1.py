"""
solution Adventofcode 2019 day 3 part 1.

https://adventofcode.com/2019/day/3

author: pca
"""

from general.general import read_day
from collections import defaultdict


def distances_crossings(grid):
    # crossing is a location having multiple wires
    result = list()

    for (y, x), wire_set in grid.items():
        if len(wire_set) > 1:
            result.append(abs(y) + abs(x))

    return result


def add_single_wire(grid, wire_id, wire):
    # directions in (y, x) coords
    directions = {'R': (0, 1), 'D': (-1, 0), 'L': (0, -1), 'U': (1, 0)}

    instructions = wire.split(',')

    y, x = 0, 0

    for instruction in instructions:
        direction = instruction[0]
        steps = int(instruction[1:])

        dy, dx = directions[direction]

        for _ in range(steps):
            y, x = y + dy, x + dx
            grid[(y, x)].add(wire_id)


def add_wires(grid, wires):
    for idx, wire in enumerate(wires):
        add_single_wire(grid, idx, wire)


def main():
    wires = read_day(2019, 3)

    grid = defaultdict(set)
    add_wires(grid, wires)
    print(f"solution: {min(distances_crossings(grid))}")


if __name__ == "__main__":
    main()
