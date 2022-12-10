"""
solution AdventOfCode 2019 day 22 part 1.

https://adventofcode.com/2019/day/22.

author: pca

"""

import copy
from collections import deque

from general.general import read_day, measure


def make_deck(size):
    deck = deque()

    deck.extend([n for n in range(size)])
    return deck


def deal(deck):
    deck = copy.copy(deck)
    deck.reverse()
    return deck


def cut(deck, n: int):
    deck = copy.copy(deck)
    deck.rotate(-n)
    return deck


def deal_increment(deck, n: int):
    old_deck = copy.copy(deck)

    cnt = 0
    size = len(deck)

    idx = 0

    table = dict()

    while cnt < size:
        val = old_deck.popleft()
        table[idx % size] = val
        idx += n
        cnt += 1

    # all indices are available
    new_deck = deque()

    for idx in range(size):
        new_deck.append(table[idx])
    return new_deck


def run(size, instructions):
    deck = make_deck(size)
    for instruction in instructions:
        deck = run_instruction(deck, instruction)

    return deck


def run_instruction(deck, instruction):
    parts = instruction.split()

    if parts[-2] == 'increment':
        return deal_increment(deck, int(parts[-1]))

    if parts[0] == 'cut':
        return cut(deck, int(parts[-1]))

    if parts[-1] == 'stack':
        return deal(deck)

    # should not happen
    assert False, "Unexpected instruction."


@measure
def main(args=None):
    instructions = read_day(2019, 22)

    deck = run(10007, instructions)

    for idx, val in enumerate(deck):
        if val == 2019:
            print(f"Solution: {idx}")


if __name__ == "__main__":
    main()
