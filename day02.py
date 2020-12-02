#!/usr/bin/env python3
"""
--- Day 2: Password Philosophy ---

Your flight departs in a few days from the coastal airport; the easiest way down
to the coast from here is via toboggan.

The shopkeeper at the North Pole Toboggan Rental Shop is having a bad day.
"Something's wrong with our computers; we can't log in!" You ask if you can take
a look.

Their password database seems to be a little corrupted: some of the passwords
wouldn't have been allowed by the Official Toboggan Corporate Policy that was in
effect when they were chosen.

To try to debug the problem, they have created a list (your puzzle input) of
passwords (according to the corrupted database) and the corporate policy when
that password was set.

For example, suppose you have the following list:

1-3 a: abcde
1-3 b: cdefg
2-9 c: ccccccccc

Each line gives the password policy and then the password. The password policy
indicates the lowest and highest number of times a given letter must appear for
the password to be valid. For example, 1-3 a means that the password must
contain a at least 1 time and at most 3 times.

In the above example, 2 passwords are valid. The middle password, cdefg, is not;
it contains no instances of b, but needs at least 1. The first and third
passwords are valid: they contain one a or nine c, both within the limits of
their respective policies.

How many passwords are valid according to their policies?
"""

import argparse
import re

parser = argparse.ArgumentParser(epilog=__doc__,
                                 formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('input', type=argparse.FileType('rt'))
parser.add_argument('--part-two', action='store_true')
args = parser.parse_args()

re_parse = re.compile('([0-9]+)-([0-9]+) ([a-z]): ([a-z]+)')


valid_count = 0

for line in args.input.readlines():
    line = line.strip()

    match = re_parse.match(line)
    assert match

    if not args.part_two:
        _min, _max, char, password = match.groups()
        occurences = password.count(char)

        is_valid = occurences in range(int(_min), int(_max) + 1)
    else:
        pos1, pos2, char, password = match.groups()
        first_match = bool(password[int(pos1) - 1] == char)
        second_match = bool(password[int(pos2) - 1] == char)

        is_valid = first_match ^ second_match

    valid_count += int(is_valid)

print(valid_count)
