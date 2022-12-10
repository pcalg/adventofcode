from string import ascii_letters

from general.general import read_day
from general.puzzle import PuzzleInterface

test = False

puzzle_input = read_day(2022, 3, test)


class PuzzleDay3(PuzzleInterface):
    def solve_part_1(self):
        def score(item):
            compartment_a = set(item[:len(item) // 2])
            compartment_b = set(item[len(item) // 2:])

            r = list(compartment_a.intersection(compartment_b))[0]

            return ascii_letters.index(r) + 1

        total = 0
        for rucksack_item in puzzle_input:
            total += score(rucksack_item)

        return total

    def solve_part_2(self):
        def score(items):
            rucksack_items_set = [set(item) for item in items]

            # get the unique item that is in all the 3 lists
            r = list(set.intersection(*rucksack_items_set))[0]

            return ascii_letters.index(r) + 1

        total = 0
        for idx in range(0, len(puzzle_input), 3):
            rucksack_items = puzzle_input[idx: idx + 3]

            total += score(rucksack_items)

        return total


puzzle = PuzzleDay3(puzzle_input)

print(f"Solution {puzzle.solve_part_1()}")
print(f"Solution {puzzle.solve_part_2()}")
