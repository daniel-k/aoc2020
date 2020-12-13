#!/usr/bin/env python3
"""
--- Day 11: Seating System ---

Your plane lands with plenty of time to spare. The final leg of your journey is
a ferry that goes directly to the tropical island where you can finally start
your vacation. As you reach the waiting area to board the ferry, you realize
you're so early, nobody else has even arrived yet!

By modeling the process people use to choose (or abandon) their seat in the
waiting area, you're pretty sure you can predict the best place to sit. You make
a quick map of the seat layout (your puzzle input).

The seat layout fits neatly on a grid. Each position is either floor (.), an
empty seat (L), or an occupied seat (#). For example, the initial seat layout
might look like this:

L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL

Now, you just need to model the people who will be arriving shortly.
Fortunately, people are entirely predictable and always follow a simple set of
rules. All decisions are based on the number of occupied seats adjacent to a
given seat (one of the eight positions immediately up, down, left, right, or
diagonal from the seat). The following rules are applied to every seat
simultaneously:

    If a seat is empty (L) and there are no occupied seats adjacent to it, the seat becomes occupied.
    If a seat is occupied (#) and four or more seats adjacent to it are also occupied, the seat becomes empty.
    Otherwise, the seat's state does not change.

Floor (.) never changes; seats don't move, and nobody sits on the floor.

After one round of these rules, every seat in the example layout becomes
occupied:

#.##.##.##
#######.##
#.#.#..#..
####.##.##
#.##.##.##
#.#####.##
..#.#.....
##########
#.######.#
#.#####.##

After a second round, the seats with four or more occupied adjacent seats become
empty again:

#.LL.L#.##
#LLLLLL.L#
L.L.L..L..
#LLL.LL.L#
#.LL.LL.LL
#.LLLL#.##
..L.L.....
#LLLLLLLL#
#.LLLLLL.L
#.#LLLL.##

This process continues for three more rounds:

#.##.L#.##
#L###LL.L#
L.#.#..#..
#L##.##.L#
#.##.LL.LL
#.###L#.##
..#.#.....
#L######L#
#.LL###L.L
#.#L###.##

#.#L.L#.##
#LLL#LL.L#
L.L.L..#..
#LLL.##.L#
#.LL.LL.LL
#.LL#L#.##
..L.L.....
#L#LLLL#L#
#.LLLLLL.L
#.#L#L#.##

#.#L.L#.##
#LLL#LL.L#
L.#.L..#..
#L##.##.L#
#.#L.LL.LL
#.#L#L#.##
..L.L.....
#L#L##L#L#
#.LLLLLL.L
#.#L#L#.##

At this point, something interesting happens: the chaos stabilizes and further
applications of these rules cause no seats to change state! Once people stop
moving around, you count 37 occupied seats.

Simulate your seating area by applying the seating rules repeatedly until no
seats change state. How many seats end up occupied?

--- Part Two ---

As soon as people start to arrive, you realize your mistake. People don't just
care about adjacent seats - they care about the first seat they can see in each
of those eight directions!

Now, instead of considering just the eight immediately adjacent seats, consider
the first seat in each of those eight directions. For example, the empty seat
below would see eight occupied seats:

.......#.
...#.....
.#.......
.........
..#L....#
....#....
.........
#........
...#.....

The leftmost empty seat below would only see one empty seat, but cannot see any
of the occupied ones:

.............
.L.L.#.#.#.#.
.............

The empty seat below would see no occupied seats:

.##.##.
#.#.#.#
##...##
...L...
##...##
#.#.#.#
.##.##.

Also, people seem to be more tolerant than you expected: it now takes five or
more visible occupied seats for an occupied seat to become empty (rather than
four or more from the previous rules). The other rules still apply: empty seats
that see no occupied seats become occupied, seats matching no rule don't change,
and floor never changes.

Given the same starting layout as above, these new rules cause the seating area
to shift around as follows:

L.LL.LL.LL
LLLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLLL
L.LLLLLL.L
L.LLLLL.LL

#.##.##.##
#######.##
#.#.#..#..
####.##.##
#.##.##.##
#.#####.##
..#.#.....
##########
#.######.#
#.#####.##

#.LL.LL.L#
#LLLLLL.LL
L.L.L..L..
LLLL.LL.LL
L.LL.LL.LL
L.LLLLL.LL
..L.L.....
LLLLLLLLL#
#.LLLLLL.L
#.LLLLL.L#

#.L#.##.L#
#L#####.LL
L.#.#..#..
##L#.##.##
#.##.#L.##
#.#####.#L
..#.#.....
LLL####LL#
#.L#####.L
#.L####.L#

#.L#.L#.L#
#LLLLLL.LL
L.L.L..#..
##LL.LL.L#
L.LL.LL.L#
#.LLLLL.LL
..L.L.....
LLLLLLLLL#
#.LLLLL#.L
#.L#LL#.L#

#.L#.L#.L#
#LLLLLL.LL
L.L.L..#..
##L#.#L.L#
L.L#.#L.L#
#.L####.LL
..#.#.....
LLL###LLL#
#.LLLLL#.L
#.L#LL#.L#

#.L#.L#.L#
#LLLLLL.LL
L.L.L..#..
##L#.#L.L#
L.L#.LL.L#
#.LLLL#.LL
..#.L.....
LLL###LLL#
#.LLLLL#.L
#.L#LL#.L#

Again, at this point, people stop shifting around and the seating area reaches
equilibrium. Once this occurs, you count 26 occupied seats.

Given the new visibility method and the rule change for occupied seats becoming
empty, once equilibrium is reached, how many seats end up occupied?
"""

import argparse
from enum import Enum
from itertools import product
from typing import Dict, Optional, Tuple

parser = argparse.ArgumentParser(epilog=__doc__,
                                 formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('input', type=argparse.FileType('rt'))
parser.add_argument('--part-two', action='store_true')
args = parser.parse_args()


class Occupation(Enum):
    FLOOR = '.'
    EMPTY = 'L'
    TAKEN = '#'


Position = Tuple[int, int]

occupations: Dict[Position, Occupation] = {
    (x, y): Occupation(char)
    for y, line in enumerate(args.input)
    for x, char in enumerate(line.strip())
}

# build directions, exclude (0, 0)
r = [-1, 0, 1]
directions = [position
              for position in product(r, r)
              if position != (0, 0)]


def pos_add(p1, p2):
    return (p1[0] + p2[0], p1[1] + p2[1])


def immediate(occupations, position, direction) -> Optional[Position]:
    neighbor_position = pos_add(position, direction)

    # default to floor, this happens at the edges
    neighbor_occupation = occupations.get(neighbor_position, Occupation.FLOOR)

    if neighbor_occupation != Occupation.FLOOR:
        return neighbor_position


def line_of_sight(occupations, position, direction) -> Optional[Position]:
    neighbor_position = pos_add(position, direction)

    # keep going in direction until we reach the end of the grid
    while neighbor_position in occupations:
        if occupations[neighbor_position] != Occupation.FLOOR:
            # found a seat in LOS
            return neighbor_position
        else:
            neighbor_position = pos_add(neighbor_position, direction)


if not args.part_two:
    neighbor_finder = immediate
    neighbor_threshold = 4
else:
    neighbor_finder = line_of_sight
    neighbor_threshold = 5

# build (and cache) the set of neighbor seats for each seat
neighbor_seats = {
    position: list(filter(lambda x: x is not None, [
                          neighbor_finder(occupations, position, direction)
                          for direction in directions]))
    for position, seat in occupations.items()
    if seat != Occupation.FLOOR
}

# no do-while in Python, so start with something obviously True
changes = True

while changes:
    changes = {}

    for position, neighbors in neighbor_seats.items():
        neighbor_count = sum(occupations[neighbor_position] == Occupation.TAKEN
                             for neighbor_position in neighbors)

        occupation = occupations[position]
        if occupation == Occupation.EMPTY and neighbor_count == 0:
            changes[position] = Occupation.TAKEN
        elif occupation == Occupation.TAKEN and neighbor_count >= neighbor_threshold:
            changes[position] = Occupation.EMPTY

    # apply changes to current occupation state
    occupations.update(changes)

print(sum([o == Occupation.TAKEN for o in occupations.values()]))
