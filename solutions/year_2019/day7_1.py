"""
solution adventofcode day 7 part 1.

https://adventofcode.com/2019/day/7

author: pca
"""

from general.general import read_day
from solutions.year_2019.day5_2 import IntMachine
import itertools


def all_phase_settings():
    settings = [0, 1, 2, 3, 4]
    yield from itertools.permutations(settings, len(settings))


def create_machines(phase_setting, program):
    result = list()

    for phase in phase_setting:
        result.append(IntMachine(program, [phase]))

    return result


def run_all_machines(machines):
    machine_input = 0

    for machine in machines:
        machine.input.append(machine_input)
        machine.run()
        res = machine.output
        print(res)
        # check if more than one output
        machine_input = res[0]


def main():
    program = read_day(2019, 7)[0]

    max_signal = 0

    for phase in all_phase_settings():
        m = create_machines(phase, program)
        run_all_machines(m)
        cur_signal = m[4].output[0]
        if cur_signal > max_signal:
            max_signal = cur_signal

    print(f"The highest signal is: {max_signal}")


if __name__ == "__main__":
    main()
