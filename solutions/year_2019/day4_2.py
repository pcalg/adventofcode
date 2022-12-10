"""
solution Adventofcode 2019 day 4 part 1.

https://adventofcode.com/2019/day/4

author: pca
"""

from general.general import read_day

def equal_digits_blocks(pw_str: str):
    """
    Divide pw str in to blocks of equal characters

    :param pw_str:
    :return:
    """

    result = list()

    prev_ch = pw_str[0]
    block = [prev_ch]
    for ch in pw_str[1:] + ' ':
        if ch != prev_ch:
            result.append(block)
            block = [ch]
            prev_ch = ch
        else:
            block.append(ch)

    return result


def valid_pw(pw_str: str) -> bool:
    has_double = False

    if len(pw_str) != 6:
        return False

    blocks = equal_digits_blocks(pw_str)

    max_digit = 0
    for idx, block in enumerate(blocks):
        cur_digit = int(block[0])
        if cur_digit < max_digit:
            return False
        else:
            max_digit = cur_digit

        if len(block) == 2:
            has_double = True

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
