"""
solution AdventOfCode 2019 day 21 part 1.

https://adventofcode.com/2019/day/21.

author: pca

"""

from general.general import read_day, measure
from solutions.year_2019.int_machine import IntMachine
from random import randint


def to_ascii(s, new_line=10):
    return [ord(ch) for ch in s] + [new_line]


def rand_instruction():
    instructions = ['NOT', 'OR', 'AND']
    registers = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'T', 'J']
    output_registers = ['T', 'J']

    return instructions[randint(0, len(instructions) - 1)] + " " + \
            registers[randint(0, len(registers) - 1)] + " " + \
            output_registers[randint(0, len(output_registers) - 1)]


def random_script(n):
    program_code = list()
    for _ in range(n):
        program_code.append(rand_instruction())
    program_code.append("RUN")

    result = list()

    for program_line in program_code:
        result += to_ascii(program_line)

    return result



def spring_script():
    """
    jumps on situations shown in the patterns. Here are some examples

    ^ is the driod and d is where the droid lands:

    #####.###########
        ^ABCdEFGHI
    #####..#.########
       ^ABCdEFGHI
    #####.#..########
      ^ABCdEFGHI
    #####.#.##...####
        ^ABCdEFGHI
    #####.##...#.####
      ^ABCdEFGHI
    #####.#.##...####
        ^ABCdEFGHI
    """

    program_code = [
                # jump cases for third tile to gap
                "NOT C J",
                "NOT F T",
                "AND D T",
                "AND T J",

                "NOT C T",
                "AND D T",
                "AND F T",
                "AND H T",
                "OR T J",

                # jump two tiles from gap
                "NOT B T",
                "AND D T",
                "OR T J",

                # jump on last tile before gap
                "NOT A T",
                "OR T J",
                "RUN"
    ]

    result = list()

    for program_line in program_code:
        result += to_ascii(program_line)

    return result

@measure
def main(args=None):
    program_code = read_day(2019, 21)[0]

    m = IntMachine(program_code, spring_script())
    m.max_steps = 1850000
    m.run()

    print(m.output[-1])

if __name__ == "__main__":
    main()
