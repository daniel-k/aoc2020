#!/usr/bin/env python3
"""
--- Day 7: Handy Haversacks ---

You land at the regional airport in time for your next flight. In fact, it looks
like you'll even have time to grab some food: all flights are currently delayed
due to issues in luggage processing.

Due to recent aviation regulations, many rules (your puzzle input) are being
enforced about bags and their contents; bags must be color-coded and must
contain specific quantities of other color-coded bags. Apparently, nobody
responsible for these regulations considered how long they would take to
enforce!

For example, consider the following rules:

light red bags contain 1 bright white bag, 2 muted yellow bags.
dark orange bags contain 3 bright white bags, 4 muted yellow bags.
bright white bags contain 1 shiny gold bag.
muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
dark olive bags contain 3 faded blue bags, 4 dotted black bags.
vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
faded blue bags contain no other bags.
dotted black bags contain no other bags.

These rules specify the required contents for 9 bag types. In this example,
every faded blue bag is empty, every vibrant plum bag contains 11 bags (5 faded
blue and 6 dotted black), and so on.

You have a shiny gold bag. If you wanted to carry it in at least one other bag,
how many different bag colors would be valid for the outermost bag? (In other
words: how many colors can, eventually, contain at least one shiny gold bag?)

In the above rules, the following options would be available to you:

    A bright white bag, which can hold your shiny gold bag directly.
    A muted yellow bag, which can hold your shiny gold bag directly, plus some other bags.
    A dark orange bag, which can hold bright white and muted yellow bags, either of which could then hold your shiny gold bag.
    A light red bag, which can hold bright white and muted yellow bags, either of which could then hold your shiny gold bag.

So, in this example, the number of bag colors that can eventually contain at
least one shiny gold bag is 4.

How many bag colors can eventually contain at least one shiny gold bag? (The
list of rules is quite long; make sure you get all of it.)

Your puzzle answer was 229.

--- Part Two ---

It's getting pretty expensive to fly these days - not because of ticket prices,
but because of the ridiculous number of bags you need to buy!

Consider again your shiny gold bag and the rules from the above example:

    faded blue bags contain 0 other bags.
    dotted black bags contain 0 other bags.
    vibrant plum bags contain 11 other bags: 5 faded blue bags and 6 dotted black bags.
    dark olive bags contain 7 other bags: 3 faded blue bags and 4 dotted black bags.

So, a single shiny gold bag must contain 1 dark olive bag (and the 7 bags within
it) plus 2 vibrant plum bags (and the 11 bags within each of those): 1 + 1*7 + 2
+ 2*11 = 32 bags!

Of course, the actual rules have a small chance of going several levels deeper
than this example; be sure to count all of the bags, even if the nesting becomes
topologically impractical!

Here's another example:

shiny gold bags contain 2 dark red bags.
dark red bags contain 2 dark orange bags.
dark orange bags contain 2 dark yellow bags.
dark yellow bags contain 2 dark green bags.
dark green bags contain 2 dark blue bags.
dark blue bags contain 2 dark violet bags.
dark violet bags contain no other bags.

In this example, a single shiny gold bag must contain 126 other bags.

How many individual bags are required inside your single shiny gold bag?
"""

import argparse
import re
from collections import defaultdict
from typing import Dict, Iterable, List, Set, Callable, Optional
from functools import reduce
from itertools import product
from utils import pairwise

WeightedDAG = Dict[str, Dict[str, int]]

parser = argparse.ArgumentParser(epilog=__doc__,
                                 formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('input', type=argparse.FileType('rt'))
parser.add_argument('--part-two', action='store_true')
args = parser.parse_args()

rules = [line.strip() for line in args.input]


dag: WeightedDAG = defaultdict(lambda: {})


for rule in rules:
    bag, contain_rules = rule.split(' bags contain ')

    sub_bags = re.split(' bag[s]?[,. ]+', contain_rules)

    # remove last element as it should be always empty
    assert sub_bags.pop() == ''

    for sub_bag in sub_bags:
        if sub_bag == 'no other':
            continue

        _, count, color, = re.split('([0-9]+) ', sub_bag)

        dag[color][bag] = int(count)


def flatten(iterable: Iterable) -> List:
    return [e for sub_iterable in iterable for e in sub_iterable]


def traverse(dag: WeightedDAG, vertex: str):
    super_vertices = list(dag[vertex])
    return super_vertices + flatten(traverse(dag, vertex)
                                    for vertex in super_vertices)


start_bag = 'shiny gold'

super_bags = set(traverse(dag, start_bag))
sub_bags = dag.keys() - super_bags - set([start_bag])

sub_bags_dag = {k: v for k, v in dag.items() if k in sub_bags}

def invert_dag(dag: WeightedDAG):
    dag_inverted = defaultdict(lambda: {})

    for vertex, next_vertices in dag.items():
        for next_vertex, weight in next_vertices.items():
            dag_inverted[next_vertex][vertex] = weight

    return dag_inverted

if not args.part_two:
    print(len(super_bags))
else:
    # invert DAG and filter out super bags before
    dag_inverted = invert_dag(sub_bags_dag)

    leafs = [vertex for vertex in sub_bags if not dag_inverted[vertex]]
    # print(leafs)

    def go_up(dag: WeightedDAG, start: str, end: str):
        next_vertices = dag[start]
        is_end = (start == end)

        if (not next_vertices) or is_end:
            return [(is_end, [start])]

        out = []
        for next_vertex, weight in next_vertices.items():
            out.extend([(is_end or keep, [start] + l) for keep, l in list(go_up(dag, next_vertex, end))])

        return out

    intermediate_bags_already_counted = set()

    dag_contained_bags = defaultdict(lambda: {})

    total_bag_count = 0

    individual_bag_count = defaultdict(lambda: 0)

    for leaf in leafs:
        valid_paths = list(filter(lambda keep_l: keep_l[0] == True, go_up(dag, leaf, start_bag)))

        for _, path in valid_paths:
            # print(path)

            for contained, container in pairwise(path):
                dag_contained_bags[contained][container] = dag[contained][container]

            s = dag_inverted[start_bag]


            weights = [dag[a][b] for a,b in pairwise(path)]
            # print(weights)

            aggregate_count = 1
            for bag, count in reversed(list(zip(path[1:-1], weights[1:]))):
                aggregate_count *= count

                if bag not in individual_bag_count:
                    individual_bag_count[bag] += aggregate_count

            bag_count = reduce(lambda a, b: a * b, weights)
            # print(bag_count)

            weighted_pairs = list(zip(pairwise(path), weights))
            # print(weighted_pairs)


            intermediate_pairs = list(weighted_pairs)[1:]
            # print(intermediate_pairs)

            intermediate_sum = sum([weight for pair, weight in filter(lambda pair: pair[0][0] not in intermediate_bags_already_counted, intermediate_pairs)])
            # print('intermediate_sum: ', intermediate_sum)

            # bag_count += intermediate_sum

            intermediate_bags_already_counted |= set([pair[0] for pair, weight in intermediate_pairs])
            # print(intermediate_bags_already_counted)

            total_bag_count += bag_count

    # print('total_bag_count: ', total_bag_count)

    # pprint(dag_contained_bags)


    def get_individual_count(dag: WeightedDAG, start: str):
        super_vertices = dag[start]
        if not super_vertices:
            return 1

        counts = []
        for vertex, weight in super_vertices.items():
            counts.append(weight * get_individual_count(dag, vertex))
        return sum(counts)

    candidates = dag_contained_bags.keys() - set(leafs) - set([start_bag])
    individual_count = sum([get_individual_count(dag_contained_bags, bag) for bag in candidates])
    # print('individual count: ', individual_count)

    print(total_bag_count + individual_count)
