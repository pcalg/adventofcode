"""
solution AdventOfCode 2019 day 13 part 2.

https://adventofcode.com/2019/day/13.

author: pca

"""

from general.general import read_day
from solutions.year_2019.int_machine import IntMachine
from enum import Enum


class Tiles(Enum):
    EMPTY = 0
    WALL = 1
    BLOCK = 2
    PADDLE = 3
    BALL = 4


def input_generator(m: IntMachine) -> int:
    """
    Provides the next input. This is based on the position of the ball.

    neutral = 0
    to the left = -1
    to the right = 1

    """
    tiles = decode_instructions(m.output)
    visualize(tiles)

    x_ball, y_ball = get_location(tiles, Tiles.BALL)
    x_paddle, y_paddle = get_location(tiles, Tiles.PADDLE)

    instruction = 0

    if x_ball > x_paddle:
        instruction = 1
    elif x_ball < x_paddle:
        instruction = -1

    return instruction


def decode_instructions(instructions):

    if len(instructions) % 3 != 0:
        raise ValueError("Expected all instructions to be in pairs of 3 (x, y, tile")

    tiles = dict()

    for idx in range(0, len(instructions), 3):
        x, y, tile = instructions[idx:idx+3]
        tiles[(x, y)] = tile

    return tiles


def visualize(tiles):
    """
    Visualize the grid.

    0 is an empty tile. No game object appears in this tile.
    1 is a wall tile. Walls are indestructible barriers.
    2 is a block tile. Blocks can be broken by the ball.
    3 is a horizontal paddle tile. The paddle is indestructible.
    4 is a ball tile. The ball moves diagonally and bounces off objects.

    """

    lookup = {0: '.', 1: '#', 2: '*', 3: 'P', 4: 'O'}

    if (-1, 0) in tiles:
        score = tiles[(-1, 0)]
    else:
        score = 0

    max_x = max(pos[0] for pos in tiles.keys())
    max_y = max(pos[1] for pos in tiles.keys())

    for y in range(0, max_y + 1):
        print("")
        for x in range(0, max_x + 1):
            val = tiles[(x, y)]
            print(lookup[val], end="")
    print("")
    print(f"Score: {score} Number of blocks left: {cnt_tiles(tiles, Tiles.BLOCK)}")


def cnt_tiles(tiles, tile_type):
    cnt = 0
    for tile in tiles.values():
        if tile == tile_type.value:
            cnt += 1
    return cnt


def get_location(tiles, tile_type):
    for pos, tile in tiles.items():
        if tile == tile_type.value:
            return pos
    return 0, 0


def main(args=None):

    program_code = read_day(2019, 13)[0]

    m = IntMachine(program_code, [])
    m.memory[0] = 2
    m.input_retriever = input_generator
    m.max_steps = 5500000
    m.run()

    output_instructions = m.output
    tiles = decode_instructions(output_instructions)
    visualize(tiles)


if __name__ == "__main__":
    main()
