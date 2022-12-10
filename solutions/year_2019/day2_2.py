"""
solution adventofcode day 2 part 2.

https://adventofcode.com/2019/day/2#part2

author: pca
"""

from general.general import read_day
import operator


def execute_instruction(pc, state):
    funcs = {1: operator.add, 2: operator.mul}

    current_instruction = state[pc]

    # we are finished when we see instruction 99
    if current_instruction == 99:
        return True, -1, -1

    fn = funcs[current_instruction]

    # get values from memory address
    input_loc_a = state[pc + 1]
    input_loc_b = state[pc + 2]
    output_loc = state[pc + 3]

    res = fn(state[input_loc_a], state[input_loc_b])

    # not finished
    return False, output_loc, res


def run_intcode(program_state):

    pc = 0

    finished, output_loc, res = execute_instruction(pc, program_state)

    while not finished:
        program_state[output_loc] = res
        pc += 4
        finished, output_loc, res = execute_instruction(pc, program_state)

    return program_state


def create_program_state(program_str):
    return {pos: int(ch) for pos, ch in enumerate(program_str.split(','))}


def main():
    puzzle_input = read_day(2019, 2)[0]

    for noun in range(0, 100):
        for verb in range(0, 100):
            program_state = create_program_state(puzzle_input)

            # adjust to "1202 program alarm" state
            program_state[1] = noun
            program_state[2] = verb

            run_intcode(program_state)

            # found the answer?
            if program_state[0] == 19690720:
                print(f"noun: {noun}, verb: {verb}, result: {100 * noun + verb}")
                break

if __name__ == "__main__":
    main()
