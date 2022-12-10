"""
solution AdventOfCode 2019 day 19 part 1.

https://adventofcode.com/2019/day/19.

author: pca

"""

from collections import defaultdict

from general.general import read_day
from general.visualize import visualize_grid
from solutions.year_2019.int_machine import IntMachine


def main(args=None):
    program_code = read_day(2019, 19)[0]

    grid = defaultdict(str)

    cnt = 0

    for x in range(50):
        for y in range(50):
            m = IntMachine(program_code, [x, y])
            m.silent = True
            m.run()
            if m.output == [1]:
                grid[(y, x)] = '#'
                cnt += 1
            else:
                grid[(y, x)] = '.'

    img = visualize_grid(grid, (50, 50), colors={'#': 'blue', '.': 'white'})
    img.show()

    print(m.output)
    print(f"result: {cnt}")


if __name__ == "__main__":
    main()
