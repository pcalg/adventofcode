from general.general import read_day
from general.puzzle import PuzzleInterface

test = False

puzzle_input = read_day(2022, 2, test)


def get_values(puzzle_input):
    translation = {"A": "R", "B": "P", "C": "S", "X": "R", "Y": "P", "Z": "S"}

    result = []
    for line in puzzle_input:
        opponent = translation[line[0]]
        response = translation[line[-1]]
        result.append((opponent, response))
    return result


def calc_score(game):
    score_table = {"R": 1, "P": 2, "S": 3}

    opponent, response = game

    if opponent == response:
        score = 3
    elif (opponent, response) not in [("S", "P"), ("P", "R"), ("R", "S")]:
        score = 6
    else:
        score = 0

    return score + score_table[response]


class PuzzleDay2(PuzzleInterface):
    def solve_part_1(self):
        games = get_values(self.puzzle_contents)

        total = 0
        for game in games:
            total += calc_score(game)

        return total

    def solve_part_2(self):
        win_choice = {"P": "S", "R": "P", "S": "R"}
        loose_choice = {"S": "P", "P": "R", "R": "S"}

        games = get_values(self.puzzle_contents)

        total = 0
        for game in games:

            opponent, response = game

            if response == "R":
                response = loose_choice[opponent]
            elif response == "P":
                response = opponent
            else:
                response = win_choice[opponent]

            total += calc_score((opponent, response))

        return total


puzzle = PuzzleDay2(puzzle_input)

print(f"Solution {puzzle.solve_part_1()}")
print(f"Solution {puzzle.solve_part_2()}")
