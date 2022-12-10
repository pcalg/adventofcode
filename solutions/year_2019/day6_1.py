"""
solution adventofcode day 6 part 1.

https://adventofcode.com/2019/day/6

author: pca
"""

from general.general import read_day
import networkx as nx


def path_total(orbit_map):
    G = nx.Graph()
    G.add_edges_from(orbit_map)
    path_lengths = nx.single_source_shortest_path_length(G, source='COM')

    return sum(path_lengths.values())


def main():
    orbit_map = [orbit.split(')') for orbit in read_day(2019, 6)]

    total = path_total(orbit_map)

    print(f"Total length is: {total}")


if __name__ == "__main__":
    main()
