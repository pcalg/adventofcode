"""
solution AdventOfCode 2019 day 10 part 1.

https://adventofcode.com/2019/day/10.

author: pca

"""

from general.general import read_day
from fractions import Fraction
import math
from collections import defaultdict


def determine_quadrant(asteroid_from, asteroid_to):
    x_from, y_from = asteroid_from
    x_to, y_to = asteroid_to

    # translate to origin
    x = x_to - x_from
    y = y_to - y_from

    quadrant = None

    if x >= 0 and y >= 0:
        quadrant = 1
    elif x <= 0 <= y:
        quadrant = 2
    elif x < 0 and y <= 0:
        quadrant = 3
    elif x >= 0 >= y:
        quadrant = 4

    return quadrant


def get_positions(asteroids_input):
    positions = set()

    for y, line in enumerate(asteroids_input):
        for x, ch in enumerate(line):
            if ch == '#':
                positions.add((x, y))
    return positions


def calc_slope(asteroid_from, asteroid_to):
    x1, y1 = asteroid_from
    x2, y2 = asteroid_to

    if x1 - x2 == 0:
        return None

    return Fraction(y2-y1, x2-x1)


def asteroids_visible(current_asteroid, asteroids):
    lines = defaultdict(set)

    x1, y1 = current_asteroid

    for other_asteroid in asteroids:
        x2, y2 = other_asteroid

        if x1 == x2 and y1 == y2:
            continue

        # find relative location
        quadrant = determine_quadrant(current_asteroid, other_asteroid)

        # vertical line
        if x2 == x1:
            lines[(math.inf, quadrant)].add((x2, y2))
        else:
            slope = calc_slope(current_asteroid, other_asteroid)
            lines[(slope, quadrant)].add((x2, y2))

    return lines


def find_max_visible(asteroids):
    max_visible = 0

    for current_asteroid in asteroids:
        # not very efficient but gets the job done
        lines = asteroids_visible(current_asteroid, asteroids)
        if len(lines) > max_visible:
            max_visible = len(lines)

    return max_visible



def main(args=None):

    asteroids_input = read_day(2019, 10)

    # convert to a set.
    asteroids = get_positions(asteroids_input)

    max_visible = find_max_visible(asteroids)
    print(f"Finished, output is {max_visible}")


if __name__ == "__main__":
    main()
