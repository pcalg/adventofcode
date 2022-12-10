"""
solution AdventOfCode 2019 day 11 part 1.

https://adventofcode.com/2019/day/11.

author: pca

"""

from general.general import read_day
from solutions.year_2019.int_machine import IntMachine
from collections import defaultdict

# directions in (y, x) coords
directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]


def turn_left(current_direction):
    return (current_direction - 1) % len(directions)


def turn_right(current_direction):
    return (current_direction + 1) % len(directions)


class Robot:

    def __init__(self, program_code, grid):
        self.brain = IntMachine(program_code, [])
        self.brain.pause_output = True
        self.grid = grid
        self.route = []
        self.painted = set()
        self.position = (0, 0)
        self.direction = 0

    def turn(self, turn_direction):
        """
            turn_direction = 0: left 90 degrees and 1: right 90 degrees
        """
        current_direction = self.direction

        if turn_direction == 0:
            self.direction = turn_left(current_direction)
        else:
            self.direction = turn_right(current_direction)

    def move(self):
        y, x = self.position
        dy, dx = directions[self.direction]
        self.position = y + dy, x + dx

    def walk(self):

        while True:
            # provide input (0 is black, 1 is white)
            color = self.grid[self.position]

            self.route.append(self.position)

            self.brain.add_input(color)

            self.brain.run()

            if self.brain.halted:
                print(f"Halted: {self.brain.output}")
                break

            if not len(self.brain.output) == 1:
                raise ValueError(f"Expected one output value: {self.brain.output}")

            color_to_paint = self.brain.read_next_output()

            # continue to get the second output
            self.brain.run()

            if not len(self.brain.output) == 1:
                raise ValueError(f"Expected one output value: {self.brain.output}")

            turn_direction = self.brain.read_next_output()

            self.grid[self.position] = color_to_paint
            self.painted.add(self.position)
            self.turn(turn_direction)
            self.move()



def main(args=None):

    program_code = read_day(2019, 11)[0]

    grid = defaultdict(int)

    robot = Robot(program_code, grid)

    robot.walk()

    print(f"Number of painted panels: {len(robot.painted)}")


if __name__ == "__main__":
    main()
