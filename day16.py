#!/usr/bin/env python3
"""
--- Day 16: Ticket Translation ---

As you're walking to yet another connecting flight, you realize that one of the
legs of your re-routed trip coming up is on a high-speed train. However, the
train ticket you were given is in a language you don't understand. You should
probably figure out what it says before you get to the train station after the
next flight.

Unfortunately, you can't actually read the words on the ticket. You can,
however, read the numbers, and so you figure out the fields these tickets must
have and the valid ranges for values in those fields.

You collect the rules for ticket fields, the numbers on your ticket, and the
numbers on other nearby tickets for the same train service (via the airport
security cameras) together into a single document you can reference (your puzzle
input).

The rules for ticket fields specify a list of fields that exist somewhere on the
ticket and the valid ranges of values for each field. For example, a rule like
class: 1-3 or 5-7 means that one of the fields in every ticket is named class
and can be any value in the ranges 1-3 or 5-7 (inclusive, such that 3 and 5 are
both valid in this field, but 4 is not).

Each ticket is represented by a single line of comma-separated values. The
values are the numbers on the ticket in the order they appear; every ticket has
the same format. For example, consider this ticket:

.--------------------------------------------------------.
| ????: 101    ?????: 102   ??????????: 103     ???: 104 |
|                                                        |
| ??: 301  ??: 302             ???????: 303      ??????? |
| ??: 401  ??: 402           ???? ????: 403    ????????? |
'--------------------------------------------------------'

Here, ? represents text in a language you don't understand. This ticket might be
represented as 101,102,103,104,301,302,303,401,402,403; of course, the actual
train tickets you're looking at are much more complicated. In any case, you've
extracted just the numbers in such a way that the first number is always the
same specific field, the second number is always a different specific field, and
so on - you just don't know what each position actually means!

Start by determining which tickets are completely invalid; these are tickets
that contain values which aren't valid for any field. Ignore your ticket for
now.

For example, suppose you have the following notes:

class: 1-3 or 5-7
row: 6-11 or 33-44
seat: 13-40 or 45-50

your ticket:
7,1,14

nearby tickets:
7,3,47
40,4,50
55,2,20
38,6,12

It doesn't matter which position corresponds to which field; you can identify
invalid nearby tickets by considering only whether tickets contain values that
are not valid for any field. In this example, the values on the first nearby
ticket are all valid for at least one field. This is not true of the other three
nearby tickets: the values 4, 55, and 12 are are not valid for any field. Adding
together all of the invalid values produces your ticket scanning error rate: 4 +
55 + 12 = 71.

Consider the validity of the nearby tickets you scanned. What is your ticket
scanning error rate?

--- Part Two ---

Now that you've identified which tickets contain invalid values, discard those
tickets entirely. Use the remaining valid tickets to determine which field is
which.

Using the valid ranges for each field, determine what order the fields appear on
the tickets. The order is consistent between all tickets: if seat is the third
field, it is the third field on every ticket, including your ticket.

For example, suppose you have the following notes:

class: 0-1 or 4-19
row: 0-5 or 8-19
seat: 0-13 or 16-19

your ticket:
11,12,13

nearby tickets:
3,9,18
15,1,5
5,14,9

Based on the nearby tickets in the above example, the first position must be
row, the second position must be class, and the third position must be seat; you
can conclude that in your ticket, class is 12, row is 11, and seat is 13.

Once you work out which field is which, look for the six fields on your ticket
that start with the word departure. What do you get if you multiply those six
values together?
"""

import argparse
from collections import defaultdict
from functools import reduce
from operator import mul
from typing import List

parser = argparse.ArgumentParser(epilog=__doc__,
                                 formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('input', type=argparse.FileType('rt'))
parser.add_argument('--part-two', action='store_true')
args = parser.parse_args()


class Range:
    left: int
    right: int

    def __init__(self, range: str):
        left, right = range.split('-')
        self.left = int(left)
        self.right = int(right)

    def __contains__(self, number: int) -> bool:
        return self.left <= number and number <= self.right


class FieldRules:
    def __init__(self, ranges: List[Range]):
        self.ranges = ranges

    def __contains__(self, number: int) -> bool:
        return any(number in r for r in self.ranges)


field_rules = {}
for line in args.input:
    line = line.strip()
    if not line:
        break

    field, ranges = line.split(': ')
    field_rules[field] = FieldRules([Range(r) for r in ranges.split(' or ')])


assert next(args.input) == 'your ticket:\n'

# parse the ticket
my_ticket = [int(n) for n in next(args.input).strip().split(',')]

assert next(args.input) == '\n'
assert next(args.input) == 'nearby tickets:\n'

nearby_tickets = [
    [int(n) for n in line.strip().split(',')]
    for line in args.input
]

invalid_numbers = []
valid_tickets = []

for ticket in nearby_tickets:
    ticket_is_valid = True
    for number in ticket:
        if not any([number in rule for rule in field_rules.values()]):
            invalid_numbers.append(number)
            ticket_is_valid = False

    if ticket_is_valid:
        valid_tickets.append(ticket)

field_positions = {}
potential_fields = defaultdict(lambda: [])

if not args.part_two:
    print(sum(invalid_numbers))
    exit()
else:
    # build a map of possible field assignments for each position
    for field, rule in field_rules.items():
        for position in range(len(field_rules)):
            if all(ticket[position] in rule for ticket in valid_tickets):
                potential_fields[position].append(field)

    # some position can only be assigned to one single field, so pick these
    # definitive assignments step by step while removing assigned fields from
    # the pool of potential assignments
    while len(field_positions) < len(field_rules):
        # if there is only one possible assignment of a position to a field
        # we can safely pick it right away
        definite_positions = [(pos, fields[0])
                              for pos, fields in potential_fields.items()
                              if len(fields) == 1]
        assert len(definite_positions) > 0

        for position, field in definite_positions:
            # add to solution and remove from pool of candidates
            field_positions[field] = position
            del potential_fields[position]

            # clean up assignments that referred to the now picked field
            for fields in potential_fields.values():
                if field in fields:
                    fields.remove(field)

    departure_positions = [field_positions[field]
                           for field in field_rules
                           if field.startswith('departure')]

    print(reduce(mul, [my_ticket[pos] for pos in departure_positions]))
