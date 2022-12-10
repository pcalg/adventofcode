"""
solution AdventOfCode 2019 day 14 part 1.

https://adventofcode.com/2019/day/14.

author: pca

"""

from general.general import read_day
from collections import defaultdict
from math import ceil


def parse_quantity(quantity):
    q = quantity.strip().split(' ')
    return q[1], int(q[0])


def parse_reaction(reaction):
    r = reaction.split(' => ')

    output_quantity = parse_quantity(r[-1])

    input_rule = [parse_quantity(q) for q in r[0].split(',')]

    return output_quantity, input_rule


def calculate_reactions(reactions, set_sizes, initial_chemical, initial_amount):
    orders = list()
    orders.append((initial_chemical, initial_amount))
    store = defaultdict(int)
    bought = defaultdict(int)

    while len(orders) > 0:
        chemical, order_amount = orders.pop()

        # we want to buy x amount of each chemical in the reaction list
        for reaction_chemical, reaction_amount in reactions[chemical]:
            # we now have for example 4 * A, but also total amount we would need
            total_amount = reaction_amount * order_amount

            # what is the minimum order size?
            set_size = set_sizes[reaction_chemical]

            # now check if we have this available or do we need to buy?
            needed_amount = total_amount - store[reaction_chemical]

            if needed_amount > 0:

                order_size = ceil(needed_amount / set_size)

                print(f"bought {order_size} of {reaction_chemical}")

                bought[reaction_chemical] += order_size

                # we bought order_size items.
                orders.append((reaction_chemical, order_size))

                # we might have something left, so put it in the store
                store[reaction_chemical] += order_size * set_size - total_amount
            else:
                print(f"Store has enough {store[reaction_chemical]}, withdrew: {total_amount} ")
                store[reaction_chemical] -= total_amount

    return bought, store

def create_reaction_lookups(reaction_codes):

    reactions = {output_quantity[0]: input_rule for output_quantity, input_rule
                 in [parse_reaction(r) for r in reaction_codes]}

    reactions['ORE'] = list()

    set_sizes = {output_quantity[0]: output_quantity[1] for output_quantity, input_rule
                 in [parse_reaction(r) for r in reaction_codes]}
    set_sizes['ORE'] = 1

    return reactions, set_sizes


def main(args=None):

    reaction_codes = read_day(2019, 14)
    reactions, set_sizes = create_reaction_lookups(reaction_codes)

    bought, store = calculate_reactions(reactions, set_sizes, 'FUEL', 1)
    print(bought)
    print(store)
    print(f"ORE needed {bought['ORE']}")


if __name__ == "__main__":
    main()
