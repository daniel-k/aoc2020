#!/usr/bin/env python3
"""
--- Day 1: Report Repair ---

After saving Christmas five years in a row, you've decided to take a vacation at
a nice resort on a tropical island. Surely, Christmas will go on without you.

The tropical island has its own currency and is entirely cash-only. The gold
coins used there have a little picture of a starfish; the locals just call them
stars. None of the currency exchanges seem to have heard of them, but somehow,
you'll need to find fifty of these coins by the time you arrive so you can pay
the deposit on your room.

To save your vacation, you need to get all fifty stars by December 25th.

Collect stars by solving puzzles. Two puzzles will be made available on each day
in the Advent calendar; the second puzzle is unlocked when you complete the
first. Each puzzle grants one star. Good luck!

Before you leave, the Elves in accounting just need you to fix your expense
report (your puzzle input); apparently, something isn't quite adding up.

Specifically, they need you to find the two entries that sum to 2020 and then
multiply those two numbers together.

--- Part Two ---

The Elves in accounting are thankful for your help; one of them even offers you
a starfish coin they had left over from a past vacation. They offer you a second
one if you can find three numbers in your expense report that meet the same
criteria.
"""


import argparse
from functools import reduce
from itertools import permutations

parser = argparse.ArgumentParser()
parser.add_argument('--number-count', '-n', type=int, default=3)
parser.add_argument('--target-sum', '-s', type=int, default=2020)
parser.add_argument('input', type=argparse.FileType('rt'))
args = parser.parse_args()

# sorting may decrease runtime, but that is pure luck with the naive approach
input_sorted = sorted([int(line) for line in args.input.readlines()])

# build permutations and check if their sum adds up.
# note: only gets one matching pair, stops calculation afterwards
magic_entries = next(
    filter(lambda v: sum(v) == args.target_sum,
    permutations(input_sorted, args.number_count))
)

print(magic_entries)
print(reduce(lambda a, b: a*b, magic_entries, 1))
