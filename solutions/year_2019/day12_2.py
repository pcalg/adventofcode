"""
solution AdventOfCode 2019 day 12 part 2.

https://adventofcode.com/2019/day/12#part2.

author: pca

"""

from general.general import read_day
from itertools import combinations
from collections import Counter
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as p3
import matplotlib.animation as animation
from matplotlib import cm
import math


#def lcm(x, y):
def lcm(values):
    result = values[0]
    for value in values[1:]:
        result = abs(result * value) // math.gcd(result, value)
    return result


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
        self.initial_coordinates = coordinates
        self.initial_velocity = (0, 0, 0)

        self.coordinates = coordinates
        self.velocity = (0, 0, 0)

    def is_initial(self, dimension):
        return self.coordinates[dimension] == self.initial_coordinates[dimension] \
               and self.velocity[dimension] == self.initial_velocity[dimension]

    def move(self):
        x, y, z = self.coordinates
        dx, dy, dz = self.velocity

        self.coordinates = x + dx, y + dy, z + dz

    def __repr__(self):
        return f"C: {self.coordinates} V: {self.velocity}"


class Simulation:
    def __init__(self, moons: list[Moon]):
        self.moons = moons
        self.pairs = list(combinations(moons, 2))
        self.location_count = Counter()
        self.periodic = dict()
        self.steps = 0

    def get_all_coordinates(self):
        result = list()
        for moon in self.moons:
            for coord in moon.coordinates:
                result.append(coord)
        return tuple(result)

    def is_initial(self, idx):
        """
        Are all the moons on their initial state?
        """
        for moon in self.moons:
            if not moon.is_initial(idx):
                return False
        return True

    def is_all_periodic(self):
        for dimension in ['x', 'y', 'z']:
            if dimension not in self.periodic:
                return False
        return True

    def simulate(self):

        self.location_count[self.get_all_coordinates()] += 1

        # apply gravity
        for moon_pair in self.pairs:
            moon_1, moon_2 = moon_pair
            velocity_moon_1, velocity_moon_2 = new_velocity(moon_1.coordinates, moon_2.coordinates, moon_1.velocity, moon_2.velocity)
            moon_1.velocity = velocity_moon_1
            moon_2.velocity = velocity_moon_2

        # apply velocity
        for moon in self.moons:
            moon.move()

        self.steps += 1

        # Now check if for a single dimension each moon is in the initial state
        # this as the moons only affect each other in a single dimension
        # see the new_velocity function.
        for idx, dimension in enumerate(['x', 'y', 'z']):
            if self.is_initial(idx) and dimension not in self.periodic:
                self.periodic[dimension] = self.steps

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

def update(num, simulator, sc):
    simulator.simulate()

    xs = [moon.coordinates[0] for moon in simulator.moons]
    ys = [moon.coordinates[1] for moon in simulator.moons]
    zs = [moon.coordinates[2] for moon in simulator.moons]

    sc._offsets3d = (xs, ys, zs)


def make_animation(all_coords, frames):

    moons = [Moon(coords) for coords in all_coords]

    s = Simulation(moons)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    sc = ax.scatter([], [], [], alpha=0.5)

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_xlim(-300, 300)
    ax.set_ylim(-300, 300)
    ax.set_zlim(-300, 300)

    ani = animation.FuncAnimation(fig, update, frames=frames, interval=70, fargs=(s, sc))
    ani.save(r"moon_animation.mp4")


def main(args=None):

    moon_locations = read_day(2019, 12)

    all_coords = [convert_coord(location) for location in moon_locations]

    moons = [Moon(coords) for coords in all_coords]

    s = Simulation(moons)

    while not s.is_all_periodic():
        s.simulate()

    all_values = list(s.periodic.values())

    print(lcm(all_values))

    # make an animation for fun
    print("Making animation")
    make_animation(all_coords, 500)

    print("Finished")


if __name__ == "__main__":
    main()
