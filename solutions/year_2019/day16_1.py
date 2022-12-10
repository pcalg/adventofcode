"""
solution AdventOfCode 2019 day 16 part 1.

https://adventofcode.com/2019/day/16.

author: pca

"""

from general.general import read_day
from general.general import measure
from itertools import cycle


def make_pattern(base_pattern, repeats):
    first = True

    for element in cycle(base_pattern):
        for _ in range(repeats + 1):
            if first:
                first = False
            else:
                yield element


def next_signal(base_pattern, signal):

    signal_next = []

    for idx, element in enumerate(signal):
        total = 0

        for s, p in zip(signal, make_pattern(base_pattern, idx)):
            total += s * p

        signal_next.append(abs(total) % 10)
    return signal_next


@measure
def run_all(signal):
    pattern = [0, 1, 0, -1]

    for _ in range(100):
        signal = next_signal(pattern, signal)

    return signal


def main(args=None):

    input_signal = read_day(2019, 16)[0]

    signal = [int(ch) for ch in input_signal]

    signal_result = run_all(signal)

    print("".join([str(d) for d in signal_result[0:8]]))


if __name__ == "__main__":
    main()
