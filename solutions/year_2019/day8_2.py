"""
solution AdventOfCode 2019 day 8 part 2.

https://adventofcode.com/2019/day/8

author: pca
"""

from general.general import read_day
from PIL import Image


def make_layers(dimensions, image_data):
    width, height = dimensions
    layer_size = width * height

    if (len(image_data) % layer_size) != 0:
        raise ValueError("Dimensions don't correspond with the length of the image data.")

    # create the layers
    for layer_idx in range(0, len(image_data), layer_size):
        yield image_data[layer_idx:layer_idx + layer_size]


def collect_image_data(dimensions, layers):
    color_lookup = {'0': (0, 0, 0), '1': (255, 255, 255)}

    img_colors = dict()
    width, height = dimensions

    for layer in layers:
        for idx, val in enumerate(layer):
            y = idx // width
            x = idx % width

            # not transparant and not yet found in a previous layer
            if val != '2' and (x, y) not in img_colors:
                img_colors[(x, y)] = color_lookup[val]

    return img_colors


def show_image(dimensions, img_colors):
    img = Image.new('RGB', dimensions)
    for pos in img_colors:
        img.putpixel(pos, img_colors[pos])
    img.show()


def main(args=None):

    image_data = read_day(2019, 8)[0]

    dimensions = 25, 6

    layers = make_layers(dimensions, image_data)
    image_data = collect_image_data(dimensions, layers)

    # show this as a picture.
    show_image(dimensions, image_data)

    print(f"Finished")


if __name__ == "__main__":
    main()
