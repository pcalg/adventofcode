from general.general import read_day
from general.puzzle import PuzzleInterface

test = False

puzzle_input = read_day(2022, 4, test)


def parse_line(line):
    return [int(item) for part in line.split(',') for item in part.split('-')]


def is_overlap(start_1, end_1, start_2, end_2):
    return (start_1 >= start_2 and end_1 <= end_2) or (start_2 >= start_1 and end_2 <= end_1)


def is_overlap_2(start_1, end_1, start_2, end_2):
    return not ((end_2 < start_1) or (end_1 < start_2) or (start_2 > end_1) or (start_1 > end_2))


class PuzzleDay4(PuzzleInterface):
    def solve_part_1(self):
        overlap = 0

        for line in puzzle_input:
            parsed_line = parse_line(line)
            if is_overlap(*parsed_line):
                overlap += 1

        return overlap

    def solve_part_2(self):
        overlap = 0

        for line in puzzle_input:
            parsed_line = parse_line(line)
            if is_overlap_2(*parsed_line):
                overlap += 1

        return overlap


puzzle = PuzzleDay4(puzzle_input)

print(f"Solution {puzzle.solve_part_1()}")
print(f"Solution {puzzle.solve_part_2()}")
