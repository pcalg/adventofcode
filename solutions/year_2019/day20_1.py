"""
solution AdventOfCode 2019 day 20 part 1.

https://adventofcode.com/2019/day/20.

author: pca

"""

from general.general import read_day, measure
import matplotlib.pyplot as plt
from collections import Counter
import networkx as nx

def to_grid(grid_txt):
    grid = dict()

    for y, line in enumerate(grid_txt):
        for x, ch in enumerate(line):
            grid[(y, x)] = ch

    return grid

def node_distances(grid, node_positions, start_node):
    deltas = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    visited = set()

    q = list()
    q.append((0, start_node))

    while len(q) > 0:
        d, (y, x) = q.pop(0)

        if (y, x) in visited:
            continue

        visited.add((y, x))

        # at a node with a code?
        if (y, x) in node_positions:
            yield d, (y, x)

        # neighbours
        for dy, dx in deltas:
            if grid[(y + dy, x + dx)] == '.':
                q.append((d + 1, (y + dy, x + dx)))



def all_distances(nodes, grid):

    distances = dict()
    node_codes = set()

    for node_from in nodes.keys():
        for (d, node_to) in node_distances(grid, nodes.keys(), node_from):
            node_code_from = nodes[node_from]
            node_code_to = nodes[node_to]

            if node_code_to != node_code_from:
                distances[(node_code_from, node_code_to)] = d
                node_codes.add(node_code_from)

    # setup the portals
    for node_code, idx in node_codes:
        if idx == 1:
            distances[(node_code, 0), (node_code, 1)] = 1
            distances[(node_code, 1), (node_code, 0)] = 1

    return distances, node_codes

def read_nodes(grid):
    deltas = [((-2, 0), (-1, 0)), ((1, 0), (2, 0)), ((0, -2), (0, -1)), ((0, 1), (0, 2))]

    node_counter = Counter()
    nodes_positions = dict()

    # check for each grid location if it's a node.
    # nodes neighbour a capital letter.
    for y, x in grid:
        if grid[(y, x)] == '.':
            for ((dy1, dx1), (dy2, dx2)) in deltas:
                ch1 = grid[(y + dy1, x + dx1)]
                ch2 = grid[(y + dy2, x + dx2)]

                if ch1.isupper() and ch2.isupper():
                    node_str = ch1 + ch2
                    idx = node_counter[node_str]
                    node_counter[node_str] += 1
                    nodes_positions[(y, x)] = (node_str, idx)

    return nodes_positions

@measure
def main(args=None):
    grid_txt = read_day(2019, 20)

    grid = to_grid(grid_txt)

    nodes = read_nodes(grid)

    distances, node_codes = all_distances(nodes, grid)

    G = nx.Graph()
    G.add_weighted_edges_from([(k[0], k[1], v) for k,v in distances.items()])

    # draw graph
    positions = {v: k for k, v in nodes.items()}
    plt.figure(1, figsize=(12, 12))
    nx.draw_networkx(G, node_size=50, pos=positions, with_labels=True, font_size=8, alpha=0.5)
    plt.show()

    # shortest path
    length = nx.shortest_path_length(G, ('AA', 0), ('ZZ', 0), 'weight')
    print(f"length: {length}")


if __name__ == "__main__":
    main()
