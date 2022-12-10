from general.general import read_day
from general.puzzle import PuzzleInterface

test = False

puzzle_input = read_day(2022, 1, test)


def get_values(puzzle_input):
    group = 0
    total = 0

    results = {}

    for line in puzzle_input:
        if line == '':
            results[group] = total
            group += 1
            total = 0
        else:
            calories = int(line)
            total += calories

    # last one
    results[group] = total

    return list(results.values())


class PuzzleDay1(PuzzleInterface):
    def solve_part_1(self):
        values = get_values(self.puzzle_contents)

        return max(values)

    def solve_part_2(self):
        values = get_values(self.puzzle_contents)

        return sum(sorted(values)[-3:])


puzzle = PuzzleDay1(puzzle_input)

print(f"Solution {puzzle.solve_part_1()}")
print(f"Solution {puzzle.solve_part_2()}")
