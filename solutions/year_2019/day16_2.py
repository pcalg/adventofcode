"""
solution AdventOfCode 2019 day 16 part 2.

https://adventofcode.com/2019/day/16.

author: pca

"""

from general.general import read_day
from general.general import measure


def calc_next_output(signal):
    running_sum = 0
    result = list()

    # to improve, we could just keep the reverse signal.
    signal_rev = signal[::-1]

    for digit in signal_rev:
        running_sum += digit
        # abs not needed here, because only multiplication by 1 is needed
        result.append(running_sum % 10)

    return result[::-1]

@measure
def solve(input_signal, runs=100):
    """
    The pattern is [0, 1, 0, -1]
    So for the last few indices this will be the calculation
    0 0 0 1 1 1 1 (idx: -4)
    0 0 0 0 1 1 1 (idx: -3)
    0 0 0 0 0 1 1 (idx: -2)
    0 0 0 0 0 0 1 (idx: -1)

    The puzzle offset is near the end of the signal, so we only need to consider adding a new digit to the running
    total and use that to calculate the next value.
    """

    # message offset
    offset = int(input_signal[0:7])

    total_length = len(input_signal) * 10000

    # check if offset is in the last part of the signal, otherwise we would have to consider the rest of the pattern.
    assert(offset / total_length > 0.5)


    # Which block this offset located in.
    offset_block = offset // len(input_signal)

    # No need to calculate every block, only the last blocks are needed as those contain the message.
    signal = ([int(ch) for ch in input_signal * (10000 - offset_block)])

    for _ in range(runs):
        signal = calc_next_output(signal)

    signal_str = "".join([str(d) for d in signal])

    start_idx = total_length - offset

    # read the message from the end as we don't have the first part.
    return signal_str[-start_idx:-(start_idx - 8)]


def main(args=None):

    input_signal = read_day(2019, 16)[0]

    print(f"The solution is: {solve(input_signal)}")


if __name__ == "__main__":
    main()
