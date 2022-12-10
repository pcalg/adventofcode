from collections import defaultdict

from general.general import read_day
from general.puzzle import PuzzleInterface

test = False

puzzle_input = read_day(2022, 6, test)




class PuzzleDay6(PuzzleInterface):

    def solve_part_1(self):
        pass

    def solve_part_2(self):
        pass


#puzzle = PuzzleDay6(puzzle_input)

#print(f"Solution {puzzle.solve_part_1()}")
#print(f"Solution {puzzle.solve_part_2()}")

data = puzzle_input[0]

for idx in range(4, len(data)):
    items = set(data[idx - 4: idx])
    #if len(items) == 4:
    if len(items) == 4:
        print(idx)
        break

for idx in range(14, len(data)):
    items = set(data[idx - 14: idx])
    #if len(items) == 4:
    if len(items) == 14:
        print(idx)
        break
