"""
solution AdventOfCode 2019 day 18 part 2.

https://adventofcode.com/2019/day/18.

author: pca

"""

from general.general import read_day, measure
import heapq


def create_grid2d(grid_txt):
    skip_ch = ['#', '.', '@']
    grid2d = dict()
    nodes = dict()

    start_pos = (0, 0)

    for y, line in enumerate(grid_txt):
        for x, ch in enumerate(line):
            if ch == "@":
                start_pos = (y, x)

            grid2d[(y, x)] = ch
            if ch not in skip_ch:
                nodes[ch] = (y, x)

    # now add the 4 start positions
    start_y, start_x = start_pos

    for idx, (dy, dx) in enumerate([(-1, -1), (1, -1), (-1, 1), (1, 1)]):
        grid2d[(start_y + dy, start_x + dx)] = '@' + str(idx)
        nodes['@' + str(idx)] = (start_y + dy, start_x + dx)

    for dy, dx in [(0, 0), (1, 0), (-1, 0), (0, 1), (0, -1)]:
        grid2d[(start_y + dy, start_x + dx)] = '#'

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

    heapq.heappush(frontier, (0, frozenset(['@0', '@1', '@2', '@3']), frozenset()))

    while len(frontier) > 0:
        d, nodes, keys = heapq.heappop(frontier)

        if (nodes, keys) not in visited:
            visited.add((nodes, keys))

            if len(keys) == n_keys:
                print(f"Distance: {d}")
                return d

            for idx, node in enumerate(nodes):
                for neighbour in neighbours[node]:
                    # When at a door, we need a key to go through, otherwise we can always pass.
                    can_pas = not (neighbour.isupper()) or (neighbour.isupper() and neighbour.lower() in keys)

                    if can_pas:
                        # Found a new key, then add it to our keys
                        if neighbour.islower() and neighbour not in keys:
                            neighbour_keys = keys.union([neighbour])
                        else:
                            neighbour_keys = keys

                        new_nodes = nodes.difference([node]).union([neighbour])

                        if not (new_nodes, neighbour) in visited:
                            heapq.heappush(frontier, (d + distances[(node, neighbour)], new_nodes, neighbour_keys))

    return None


def main(args=None):
    grid_txt = read_day(2019, 18)

    grid2d, nodes = create_grid2d(grid_txt)

    distances = dict()
    neighbours = dict()

    # for each node use BFS to find the reachable other nodes
    for node in nodes:
        d, node_neighbours = find_distances(grid2d, node, nodes[node])
        distances.update(d)
        neighbours[node] = node_neighbours

    # TODO: improve running time...
    dist = solve(distances, neighbours)

    print(f"Distance: {dist}")


if __name__ == "__main__":
    main()
