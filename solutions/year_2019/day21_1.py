"""
solution AdventOfCode 2019 day 21 part 1.

https://adventofcode.com/2019/day/21.

author: pca

"""

from general.general import read_day, measure, save_grid
from solutions.year_2019.int_machine import IntMachine


def to_ascii(s, new_line=10):
    return [ord(ch) for ch in s] + [new_line]


def spring_script():
    program_code = [
                # two tiles
                # -> ##..#.###
                "NOT B J",
                "NOT C T",
                "AND T J",
                "AND D J",

                "NOT C J",
                "AND D J",

                # 1 tile
                "NOT A T",
                "OR T J",

                "WALK"
              ]

    result = list()

    for program_line in program_code:
        result += to_ascii(program_line)

    return result

@measure
def main(args=None):
    program_code = read_day(2019, 21)[0]

    m = IntMachine(program_code, spring_script())
    m.run()

    print(m.output[-1])

if __name__ == "__main__":
    main()
