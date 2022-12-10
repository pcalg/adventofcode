from collections import defaultdict

from general.general import read_day
from general.puzzle import PuzzleInterface

test = False

puzzle_input = read_day(2022, 5, test)


def parse_moves(line):
    move_parts = line.split(' ')
    return int(move_parts[1]), int(move_parts[3]), int(move_parts[5])


def do_move(stacks, total, from_stack, to_stack):
    # move 1 box at a time

    for _ in range(total):
        item = stacks[from_stack].pop(0)
        stacks[to_stack] = [item] + stacks[to_stack]

    return stacks


def do_move_2(stacks, total, from_stack, to_stack):
    # move multiple boxes at a time

    items = stacks[from_stack][:total]
    stacks[from_stack] = stacks[from_stack][total:]
    stacks[to_stack] = items + stacks[to_stack]

    return stacks


def run_puzzle(lines, move_func):
    stacks = defaultdict(list)

    is_stack = True

    for line in lines:
        if line == "":
            is_stack = False
        elif is_stack:
            max_len = len(line)

            for idx in range(0, max_len, 4):
                if line[idx] == "[":
                    stacks[idx // 4 + 1].append(line[idx + 1])
        else:
            move = parse_moves(line)
            stacks = move_func(stacks, *move)

    return calc_score(stacks)


def calc_score(stacks):
    result = ""
    m = max(stacks.keys())
    for idx in range(m):
        result += stacks[idx + 1][0]
    return result


class PuzzleDay5(PuzzleInterface):

    def solve_part_1(self):
        return run_puzzle(self.puzzle_contents, move_func=do_move)

    def solve_part_2(self):
        return run_puzzle(self.puzzle_contents, move_func=do_move_2)


puzzle = PuzzleDay5(puzzle_input)

print(f"Solution {puzzle.solve_part_1()}")
print(f"Solution {puzzle.solve_part_2()}")
