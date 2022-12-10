"""
solution adventofcode day 5 part 2.

https://adventofcode.com/2019/day/5#part2

author: pca
"""

import operator

from general.general import read_day


def is_not_zero(value):
    return value != 0


def is_zero(value):
    return value == 0


def is_less(a, b):
    return 1 if a < b else 0


def is_equal(a, b):
    return 1 if a == b else 0


class IntMachine:
    OP_ADD = 1
    OP_MUL = 2
    OP_INPUT = 3
    OP_OUTPUT = 4
    OP_JMP_TRUE = 5
    OP_JMP_FALSE = 6
    OP_LESS = 7
    OP_EQUAL = 8
    OP_HALT = 99

    def __init__(self, program_code, input_values):
        self.pc = 0

        if len(program_code) > 0:
            self.memory = {pos: int(ch) for pos, ch in enumerate(program_code.split(','))}
        else:
            self.memory = dict()

        self.output = list()
        self.input = list(input_values)
        self.halted = False
        self.max_steps = 50000

    def read_next_input(self):
        """
        read in from the input queue.
        """
        input_value = self.input[0]
        self.input = self.input[1:]

        return input_value

    def add_output(self, value):
        self.output.append(value)

    def halt(self):
        self.halted = True

    def get_value(self, location, immediate):
        if immediate == 1:
            return self.memory[location]
        else:
            store_loc = self.memory[location]
            return self.memory[store_loc]

    def execute_instruction(self):
        funcs = {IntMachine.OP_ADD: operator.add,
                 IntMachine.OP_MUL: operator.mul,
                 IntMachine.OP_INPUT: self.read_next_input,
                 IntMachine.OP_OUTPUT: self.add_output,
                 IntMachine.OP_JMP_TRUE: is_not_zero,
                 IntMachine.OP_JMP_FALSE: is_zero,
                 IntMachine.OP_LESS: is_less,
                 IntMachine.OP_EQUAL: is_equal,
                 IntMachine.OP_HALT: self.halt}

        # lookup for how many steps to move the pc after an instruction
        pc_moves = {IntMachine.OP_ADD: 4,
                    IntMachine.OP_MUL: 4,
                    IntMachine.OP_INPUT: 2,
                    IntMachine.OP_OUTPUT: 2,
                    IntMachine.OP_JMP_TRUE: 3,
                    IntMachine.OP_JMP_FALSE: 3,
                    IntMachine.OP_LESS: 4,
                    IntMachine.OP_EQUAL: 4,
                    IntMachine.OP_HALT: 1}

        opcode, (p1, p2, p3) = IntMachine.decode_instruction(self.memory[self.pc])

        fn = funcs[opcode]
        next_pc = self.pc + pc_moves[opcode]

        if opcode in [IntMachine.OP_ADD, IntMachine.OP_MUL, IntMachine.OP_LESS, IntMachine.OP_EQUAL]:
            val1 = self.get_value(self.pc + 1, p1)
            val2 = self.get_value(self.pc + 2, p2)
            # check to be on the safe side
            if p3 == 1:
                raise ValueError(f"Error at location {self.pc} for instruction {opcode}.")

            res = fn(val1, val2)
            store_loc = self.memory[self.pc + 3]
            self.memory[store_loc] = res
        # input
        elif opcode == IntMachine.OP_INPUT:
            if p1 == 1:
                raise ValueError(f"Error at location {self.pc} for instruction {opcode}.")
            res = fn()
            store_loc = self.memory[self.pc + 1]
            self.memory[store_loc] = res
        # output
        elif opcode == IntMachine.OP_OUTPUT:
            val1 = self.get_value(self.pc + 1, p1)
            fn(val1)
        elif opcode in [IntMachine.OP_JMP_FALSE, IntMachine.OP_JMP_TRUE]:
            val1 = self.get_value(self.pc + 1, p1)

            # check to be on the safe side
            if p3 == 1:
                raise ValueError(f"Error at location {self.pc} for instruction {opcode}.")

            res = fn(val1)

            if res:
                next_pc = self.get_value(self.pc + 2, p2)

        elif opcode == IntMachine.OP_HALT:
            fn()

        self.pc = next_pc

    @staticmethod
    def decode_instruction(instruction):
        """
        ABCDE
        01002

        DE - two-digit opcode,      02 == opcode 2
        C - mode of 1st parameter,  0 == position mode
        B - mode of 2nd parameter,  1 == immediate mode
        A - mode of 3rd parameter,  0 == position mode,
                                  omitted due to being a leading zero
        """

        instruction_str = str(instruction)

        # get the instruction (last two chars)
        opcode = int(instruction_str[-2:])

        # now get the param modes
        mode_param_1 = 1 if instruction_str[-3:-2] == '1' else 0
        mode_param_2 = 1 if instruction_str[-4:-3] == '1' else 0
        mode_param_3 = 1 if instruction_str[-5:-4] == '1' else 0

        param_modes = mode_param_1, mode_param_2, mode_param_3

        return opcode, param_modes

    def run(self):
        """
        Runs the loaded program
        """
        print("Starting.")

        steps = 0

        while not self.halted or steps > self.max_steps:
            self.execute_instruction()

            steps += 1

        print(f"Ending after steps: {steps}")


def main():
    program_code = read_day(2019, 5)[0]

    int_machine = IntMachine(program_code, [5])
    int_machine.run()

    print(int_machine.output)

    return int_machine


if __name__ == "__main__":
    main()
