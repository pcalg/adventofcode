"""
solution adventofcode day1

https://adventofcode.com/2019/day/1

author: pca
"""

from general.general import read_day


def fuel_requirement(module_mass):
    """
    Fuel required to launch a given module is based on its mass. Specifically, to find the fuel required for a module,
    take its mass, divide by three, round down, and subtract 2.

    :param module_mass:
    :return: fuel_requirement
    """
    return module_mass // 3 - 2


def main():
    puzzle_input = [int(n) for n in read_day(2019, 1, test=False)]

    fuel_requirements = [fuel_requirement(mass) for mass in puzzle_input]

    print(sum(fuel_requirements))


if __name__ == "__main__":
    main()
