"""
solution AdventOfCode 2019 day 12 part 1.

https://adventofcode.com/2019/day/12.

author: pca

"""

from general.general import read_day
from itertools import combinations


def calc_delta(a, b):
    if a == b:
        return 0

    return 1 if a < b else -1


def new_velocity(pos_1, pos_2, velocity_1, velocity_2):
    x1, y1, z1 = pos_1
    x2, y2, z2 = pos_2

    vx1, vy1, vz1 = velocity_1
    vx2, vy2, vz2 = velocity_2

    dx, dy, dz = calc_delta(x1, x2), calc_delta(y1, y2), calc_delta(z1, z2)

    return (vx1 + dx, vy1 + dy, vz1 + dz), (vx2 - dx, vy2 - dy, vz2 - dz)


def calc_energy(pos):
    return sum([abs(n) for n in pos])


class Moon:
    def __init__(self, coordinates):
        self.coordinates = coordinates
        self.velocity = (0, 0, 0)

    def move(self):
        x, y, z = self.coordinates
        dx, dy, dz = self.velocity

        self.coordinates = x + dx, y + dy, z + dz

    def __repr__(self):
        return f"coordinates: {self.coordinates} velocity: {self.velocity}"


class Simulation:
    def __init__(self, moons: Moon):
        self.moons = moons
        self.pairs = list(combinations(moons, 2))

    def simulate(self):

        # apply gravity
        for moon_pair in self.pairs:
            moon_1, moon_2 = moon_pair
            velocity_moon_1, velocity_moon_2 = new_velocity(moon_1.coordinates, moon_2.coordinates, moon_1.velocity, moon_2.velocity)
            moon_1.velocity = velocity_moon_1
            moon_2.velocity = velocity_moon_2

        # apply velocity
        for moon in self.moons:
            moon.move()

    def energy(self):
        total = 0
        for moon in self.moons:
            total += calc_energy(moon.velocity) * calc_energy(moon.coordinates)

        return total


def convert_coord(coord_line):
    """
    coord_line is in this format: <x=5, y=-1, z=5>
    """
    coord_list = coord_line.replace('<', '').replace('>', '').split(',')

    return tuple([int(coord.split('=')[1]) for coord in coord_list])



def main(args=None):

    moon_locations = read_day(2019, 12)

    all_coords = [convert_coord(location) for location in moon_locations]

    moons = [Moon(coords) for coords in all_coords]

    s = Simulation(moons)

    for _ in range(1000):
        s.simulate()

    print(f"Resulting energy is: {s.energy()}")


if __name__ == "__main__":
    main()
