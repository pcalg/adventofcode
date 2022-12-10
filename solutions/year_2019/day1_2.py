"""

solution adventofcode day1 part 2

https://adventofcode.com/2019/day/1#part2

author: pca
"""

from general.general import read_day

def fuel_requirement(module_mass):
    """
    Fuel required to launch a given module is based on its mass. Specifically, to find the fuel required for a module,
    take its mass, divide by three, round down, and subtract 2. Repeat this for the weight of the fuel until the added
    weight is 0.

    :param module_mass:
    :return: fuel_requirement
    """
    total = 0
    current_mass = module_mass

    while (current_mass // 3 - 2) > 0:
        current_mass = current_mass // 3 - 2
        total += current_mass

    return total


def main():

    puzzle_input = [int(n) for n in read_day(2019, 1, test=False)]

    fuel_requirements = [fuel_requirement(mass) for mass in puzzle_input]

    print(f"The answer is: {sum(fuel_requirements)}")


if __name__ == "__main__":
    main()
