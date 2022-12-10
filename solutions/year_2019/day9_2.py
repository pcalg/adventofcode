"""
solution AdventOfCode 2019 day 9 part 2.

https://adventofcode.com/2019/day/9#part2

author: pca

"""

from general.general import read_day
from solutions.year_2019.int_machine import IntMachine


def main(args=None):

    program_code = read_day(2019, 9)[0]

    m = IntMachine(program_code, [2])
    m.max_steps = 5000000
    m.run()

    print(f"Finished, output is {m.output}")


if __name__ == "__main__":
    main()
