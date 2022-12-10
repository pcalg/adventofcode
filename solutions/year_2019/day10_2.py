"""
solution AdventOfCode 2019 day 10 part 2.

https://adventofcode.com/2019/day/10#part2.

author: pca

"""

from general.general import read_day
import math
from collections import defaultdict


def get_positions(asteroids_input):
    positions = set()

    for y, line in enumerate(asteroids_input):
        for x, ch in enumerate(line):
            if ch == '#':
                positions.add((x, y))
    return positions


def calc_angle(asteroid_from, asteroid_to):
    x1, y1 = asteroid_from
    x2, y2 = asteroid_to

    if x1 == x2 and y1 == y2:
        return None

    # go to base
    x = x2 - x1
    y = y2 - y1

    # The order is clockwise and starts pointing to the North
    # -y because the y-axis is reversed.
    return (2 * math.pi + math.atan2(x, -y)) % (2 * math.pi)


def manhattan(asteroid_from, asteroid_to):
    x1, y1 = asteroid_from
    x2, y2 = asteroid_to

    return abs(x1-x2) + abs(y1-y2)


def asteroids_visible(current_asteroid, asteroids):
    lines = defaultdict(list)

    x1, y1 = current_asteroid

    for other_asteroid in asteroids:
        x2, y2 = other_asteroid

        if x1 == x2 and y1 == y2:
            continue

        # find relative location
        d = manhattan(current_asteroid, other_asteroid)

        angle = calc_angle(current_asteroid, other_asteroid)
        lines[angle].append((d, x2, y2))

    return lines


def find_max_visible(asteroids):
    max_visible = 0
    max_lines = None
    max_asteroid = None

    for current_asteroid in asteroids:
        lines = asteroids_visible(current_asteroid, asteroids)
        if len(lines) > max_visible:
            max_visible = len(lines)
            max_lines = lines
            max_asteroid = current_asteroid

    return max_visible, max_lines, max_asteroid


def order_vaporize(lines):
    vaporize_list = list()

    for angle in lines:
        asteroid_list = lines[angle]
        # make sure it's sorted
        sorted_asteroids = sorted(asteroid_list)

        for idx, asteroid in enumerate(sorted_asteroids):
            d, x, y = asteroid
            vaporize_list.append((2*math.pi * idx + angle, x, y))

    return sorted(vaporize_list)


def main(args=None):

    asteroids_input = read_day(2019, 10)

    asteroids = get_positions(asteroids_input)

    max_visible, max_lines, max_asteroid = find_max_visible(asteroids)

    vaporize = order_vaporize(max_lines)

    print(f"Finished, output is {vaporize[199]}")
    print(f"Result: {vaporize[199][1] * 100 + vaporize[199][2]}")


if __name__ == "__main__":
    main()
