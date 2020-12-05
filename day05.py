#!/usr/bin/env python3
"""
--- Day 5: Binary Boarding ---

You board your plane only to discover a new problem: you dropped your boarding
pass! You aren't sure which seat is yours, and all of the flight attendants are
busy with the flood of people that suddenly made it through passport control.

You write a quick program to use your phone's camera to scan all of the nearby
boarding passes (your puzzle input); perhaps you can find your seat through
process of elimination.

Instead of zones or groups, this airline uses binary space partitioning to seat
people. A seat might be specified like FBFBBFFRLR, where F means "front", B
means "back", L means "left", and R means "right".

The first 7 characters will either be F or B; these specify exactly one of the
128 rows on the plane (numbered 0 through 127). Each letter tells you which half
of a region the given seat is in. Start with the whole list of rows; the first
letter indicates whether the seat is in the front (0 through 63) or the back (64
through 127). The next letter indicates which half of that region the seat is
in, and so on until you're left with exactly one row.

For example, consider just the first seven characters of FBFBBFFRLR:

    Start by considering the whole range, rows 0 through 127.
    F means to take the lower half, keeping rows 0 through 63.
    B means to take the upper half, keeping rows 32 through 63.
    F means to take the lower half, keeping rows 32 through 47.
    B means to take the upper half, keeping rows 40 through 47.
    B keeps rows 44 through 47.
    F keeps rows 44 through 45.
    The final F keeps the lower of the two, row 44.

The last three characters will be either L or R; these specify exactly one of
the 8 columns of seats on the plane (numbered 0 through 7). The same process as
above proceeds again, this time with only three steps. L means to keep the lower
half, while R means to keep the upper half.

For example, consider just the last 3 characters of FBFBBFFRLR:

    Start by considering the whole range, columns 0 through 7.
    R means to take the upper half, keeping columns 4 through 7.
    L means to take the lower half, keeping columns 4 through 5.
    The final R keeps the upper of the two, column 5.

So, decoding FBFBBFFRLR reveals that it is the seat at row 44, column 5.

Every seat also has a unique seat ID: multiply the row by 8, then add the
column. In this example, the seat has ID 44 * 8 + 5 = 357.

Here are some other boarding passes:

    BFFFBBFRRR: row 70, column 7, seat ID 567.
    FFFBBBFRRR: row 14, column 7, seat ID 119.
    BBFFBBFRLL: row 102, column 4, seat ID 820.

As a sanity check, look through your list of boarding passes. What is the
highest seat ID on a boarding pass?

--- Part Two ---

Ding! The "fasten seat belt" signs have turned on. Time to find your seat.

It's a completely full flight, so your seat should be the only missing boarding
pass in your list. However, there's a catch: some of the seats at the very front
and back of the plane don't exist on this aircraft, so they'll be missing from
your list as well.

Your seat wasn't at the very front or back, though; the seats with IDs +1 and -1
from yours will be in your list.

What is the ID of your seat?
"""

import argparse
from itertools import product
from typing import Iterable

parser = argparse.ArgumentParser(epilog=__doc__,
                                 formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('input', type=argparse.FileType('rt'))
parser.add_argument('--part-two', action='store_true')
args = parser.parse_args()


def build_partitioner(lower_symbol: str, upper_symbol: str):
    assert len(lower_symbol) == 1, 'Only single character allowed'
    assert len(upper_symbol) == 1, 'Only single character allowed'

    def func(location: Iterable[str], position: int = 0) -> int:
        if not location:
            # arrived at the end of location string
            return position

        # split first character from rest of location string
        partition, *rest = location
        assert partition in (lower_symbol, upper_symbol)

        partition_size = 2**len(location)
        is_upper_partition = (partition == upper_symbol)

        position += is_upper_partition * (partition_size // 2)

        return func(rest, position)

    return func


def build_seat_validator(seats_taken):
    def validator(seat):
        # seat is valid if seats before and after it are taken
        seat_before = (seat[0] - 1, seat[1])
        seat_after = (seat[0] + 1, seat[1])

        return seat_before in seats_taken and seat_after in seats_taken

    return validator


row_partitioner = build_partitioner('F', 'B')
col_partitioner = build_partitioner('L', 'R')

seats_taken = set()

for line in args.input:
    line = line.strip()

    row = row_partitioner(line[:7])
    col = col_partitioner(line[7:])

    seats_taken.add((row, col))


if args.part_two:
    # create the set of potential seats in the plane (no first or last row)
    all_seats = set(product(range(1, 126 + 1), range(0, 7)))

    # only an empty seat could be ours
    empty_seats = all_seats - seats_taken

    # filter out the only valid seat which is ours (flight is fully booked)
    my_seat = list(filter(build_seat_validator(seats_taken), empty_seats))
    assert len(my_seat) == 1

    # overwrite so only this seat is output
    seats_taken = my_seat

print(max(row * 8 + col for row, col in seats_taken))
