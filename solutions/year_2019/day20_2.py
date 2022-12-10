"""
solution AdventOfCode 2019 day 20 part 2.

https://adventofcode.com/2019/day/20.

author: pca

"""

from general.general import read_day, measure
import matplotlib.pyplot as plt
from collections import Counter
import networkx as nx
import heapq

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
            distances[(node_code, -1), (node_code, 1)] = 1
            distances[(node_code, 1), (node_code, -1)] = 1

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

                    # check if it's an outer gate
                    is_on_edge = (y == 2) or (x == 2) or (y, x + 3) not in grid or (y + 3, x) not in grid

                    if node_str in ('AA', 'ZZ'):
                        idx = 0
                    elif is_on_edge:
                        idx = 1
                    else:
                        idx = -1

                    nodes_positions[(y, x)] = (node_str, idx)

    return nodes_positions

def solve(G):

    frontier = []
    visited = set()

    heapq.heappush(frontier, (0, -1, ('AA', 0), [(('AA', 0), 0)]))

    while len(frontier) > 0:
        dimension, total_distance, node, path = heapq.heappop(frontier)

        if dimension < 0:
            continue

        if node in [('AA', 0), ('ZZ', 0)] and dimension != 0:
            continue

        if node == ('ZZ', 0) and dimension == 0:
            print(f"found: {total_distance}")
            return True, total_distance, path

        if (dimension, node)  in visited:
            continue

        visited.add((dimension, node))

        # we always go to the other side of the node
        node_code, node_delta = node
        check_node = node_code, -node_delta

        for neighbour in G.neighbors(check_node):
            neighbour_code, neighbour_delta = neighbour

            # make sure we don't go back right away on the same node.
            if node_code != neighbour_code:
                # count for movement to another dimension as well (+1).
                distance = G.edges[(check_node, neighbour)]['weight'] + 1

                delta_dimension = -node_delta

                heapq.heappush(frontier, (dimension + delta_dimension, total_distance + distance, neighbour,
                                          path + [(neighbour, dimension + delta_dimension)]))

    return False, None, None

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

    res, total_distance, path = solve(G)
    print(f"Total distance: {total_distance}")

if __name__ == "__main__":
    main()
