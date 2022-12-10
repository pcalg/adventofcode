"""
solution adventofcode day 6 part 2.

https://adventofcode.com/2019/day/6#part2

author: pca
"""

from general.general import read_day
import networkx as nx


def orbital_transfers(orbit_map, object_from, object_to):
    G = nx.Graph()
    G.add_edges_from(orbit_map)
    path = nx.shortest_path(G, source=object_from, target=object_to)

    # YOU and SAN don't count + only the transfers count (movements from a->b)
    return len(path) - 3


def main():
    orbit_map = [orbit.split(')') for orbit in read_day(2019, 6)]

    transfers = orbital_transfers(orbit_map, 'YOU', 'SAN')

    print(f"Transfers needed: {transfers}")


if __name__ == "__main__":
    main()
