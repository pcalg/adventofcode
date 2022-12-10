"""
solution AdventOfCode 2019 day 8 part 1.

https://adventofcode.com/2019/day/8

author: pca
"""

from general.general import read_day
from collections import Counter


def make_layers(dimensions, image_data):
    width, height = dimensions
    layer_size = width * height

    if (len(image_data) % layer_size) != 0:
        raise ValueError("Dimensions don't correspond with the length of the image data.")

    # create the layers
    for layer_idx in range(0, len(image_data), layer_size):
        yield image_data[layer_idx:layer_idx + layer_size]


def main(args=None):

    image_data = read_day(2019, 8)[0]

    dimensions = 25, 6

    # get a baseline for the zero count
    # there always will be a layer having less zeros than this number.
    min_zeros = Counter(image_data)['0'] + 1

    layers = make_layers(dimensions, image_data)
    total = 0

    for layer in layers:
        c = Counter(layer)
        if c['0'] < min_zeros:
            min_zeros = c['0']
            total = c['1'] * c['2']

    print(f"Result is {total}")


if __name__ == "__main__":
    main()
