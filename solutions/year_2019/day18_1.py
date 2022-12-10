"""
solution AdventOfCode 2019 day 18 part 1.

https://adventofcode.com/2019/day/18.

author: pca

"""

from general.general import read_day, measure
import heapq


def create_grid2d(grid_txt):
    skip_ch = ['#', '.']
    grid2d = dict()
    nodes = dict()

    for y, line in enumerate(grid_txt):
        for x, ch in enumerate(line):
            grid2d[(y, x)] = ch
            if ch not in skip_ch:
                nodes[ch] = (y, x)

    return grid2d, nodes


def find_distances(grid2d, node_ch, node_pos):
    """
    Find the distances using BFS from node_ch to the next reachable node (key or door).
    """
    distances = {}
    node_neighbours = set()

    deltas = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    q = [(0, node_pos)]
    visited = set()

    while len(q) > 0:
        d, pos = q.pop(0)
        visited.add(pos)

        # find neighbours
        y, x = pos
        for dy, dx in deltas:
            neighbour_pos = y + dy, x + dx
            neighbour_ch = grid2d[neighbour_pos]

            # only move to a next nodes if it's an empty space
            if neighbour_ch == '.' and neighbour_pos not in visited:
                q.append((d + 1, neighbour_pos))

            # we don't want to store the empty cells or doors as nodes
            if neighbour_ch not in ['.', '#'] and neighbour_pos not in visited:
                distances[(node_ch, neighbour_ch)] = d + 1
                node_neighbours.add(neighbour_ch)

    return distances, node_neighbours

@measure
def solve(distances, neighbours):
    """
    Find the minimum distance needed to find all the keys.

    :param distances:  dictionary that contains the length of the edges {(from, to): distance, ...}
    :param neighbours: dictionary that contains the neighbours for each node
    :return: minimum distance
    """

    n_keys = len([k for k in neighbours.keys() if k.islower()])

    frontier = []
    visited = set()

    heapq.heappush(frontier, (0, '@', frozenset()))

    cnt = 0

    while len(frontier) > 0:
        d, node, keys = heapq.heappop(frontier)
        cnt += 1

        # Skip if already been in this state
        if (node, keys) not in visited:
            visited.add((node, keys))

            if len(keys) == n_keys:
                print(f"Distance: {d} cnt: {cnt}")
                return d

            nb_list = neighbours[node]

            for neighbour in nb_list:
                # When at a door, we need a key to go through, otherwise we can always pass.
                can_pas = (neighbour.isupper() and neighbour.lower() in keys) or (not neighbour.isupper())

                if can_pas:
                    # Found a new key, then add it to our keys
                    if neighbour.islower() and neighbour not in keys:
                        neighbour_keys = keys.union([neighbour])
                    else:
                        neighbour_keys = keys

                    heapq.heappush(frontier, (d + distances[(node, neighbour)], neighbour, neighbour_keys))

    return None

def reachable_graph(grid2d, nodes):

    distances = {}
    neighbours = {}

    # for each node use BFS to find the reachable other nodes
    for node in nodes:
        d, node_neighbours = find_distances(grid2d, node, nodes[node])
        distances.update(d)
        neighbours[node] = node_neighbours

    return distances, neighbours


def main(args=None):
    grid_txt = read_day(2019, 18)

    grid2d, nodes = create_grid2d(grid_txt)

    distances, neighbours = reachable_graph(grid2d, nodes)

    dist = solve(distances, neighbours)

    print(f"Distance: {dist}")


if __name__ == "__main__":
    main()
