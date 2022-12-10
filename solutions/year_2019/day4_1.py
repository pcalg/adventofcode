"""
solution Adventofcode 2019 day 4 part 1.

https://adventofcode.com/2019/day/4

author: pca
"""

from general.general import read_day

def valid_pw(pw_str: str) -> bool:
    has_double = False

    if len(pw_str) != 6:
        return False

    max_digit = 0
    prev_digit = -1

    for ch in pw_str:
        cur_digit = int(ch)
        # decreasing
        if cur_digit < max_digit:
            return False
        else:
            max_digit = cur_digit

        if cur_digit == prev_digit:
            has_double = True

        prev_digit = cur_digit

    return has_double

def main(args=None):

    puzzle_input = [int(ch) for ch in read_day(2019, 4)[0].split('-')]

    cnt = 0
    for val in range(puzzle_input[0], puzzle_input[1]):
        if valid_pw(str(val)):
            cnt += 1
    print(cnt)

if __name__ == "__main__":
    main()
