#!/usr/bin/env python3
"""
--- Day 18: Operation Order ---

As you look out the window and notice a heavily-forested continent slowly appear
over the horizon, you are interrupted by the child sitting next to you. They're
curious if you could help them with their math homework.

Unfortunately, it seems like this "math" follows different rules than you
remember.

The homework (your puzzle input) consists of a series of expressions that
consist of addition (+), multiplication (*), and parentheses ((...)). Just like
normal math, parentheses indicate that the expression inside must be evaluated
before it can be used by the surrounding expression. Addition still finds the
sum of the numbers on both sides of the operator, and multiplication still finds
the product.

However, the rules of operator precedence have changed. Rather than evaluating
multiplication before addition, the operators have the same precedence, and are
evaluated left-to-right regardless of the order in which they appear.

For example, the steps to evaluate the expression 1 + 2 * 3 + 4 * 5 + 6 are as
follows:

    1 + 2 * 3 + 4 * 5 + 6
      3   * 3 + 4 * 5 + 6
          9   + 4 * 5 + 6
             13   * 5 + 6
                 65   + 6
                     71

Parentheses can override this order; for example, here is what happens if
parentheses are added to form 1 + (2 * 3) + (4 * (5 + 6)):

    1 + (2 * 3) + (4 * (5 + 6))
    1 +    6    + (4 * (5 + 6))
         7      + (4 * (5 + 6))
         7      + (4 *   11   )
         7      +     44
                51

Here are a few more examples:

    2 * 3 + (4 * 5) becomes 26.
    5 + (8 * 3 + 9 + 3 * 4 * 3) becomes 437.
    5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4)) becomes 12240.
    ((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2 becomes 13632.

Before you can help with the homework, you need to understand it yourself.
Evaluate the expression on each line of the homework; what is the sum of the
resulting values?

--- Part Two ---

You manage to answer the child's questions and they finish part 1 of their
homework, but get stuck when they reach the next section: advanced math.

Now, addition and multiplication have different precedence levels, but they're
not the ones you're familiar with. Instead, addition is evaluated before
multiplication.

For example, the steps to evaluate the expression 1 + 2 * 3 + 4 * 5 + 6 are now
as follows:

    1 + 2 * 3 + 4 * 5 + 6
      3   * 3 + 4 * 5 + 6
      3   *   7   * 5 + 6
      3   *   7   *  11
         21       *  11
             231

Here are the other examples from above:

    1 + (2 * 3) + (4 * (5 + 6)) still becomes 51.
    2 * 3 + (4 * 5) becomes 46.
    5 + (8 * 3 + 9 + 3 * 4 * 3) becomes 1445.
    5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4)) becomes 669060.
    ((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2 becomes 23340.

What do you get if you add up the results of evaluating the homework problems
using these new rules?
"""

import argparse
from typing import Tuple
from functools import partial, reduce
from operator import add, mul

parser = argparse.ArgumentParser(epilog=__doc__,
                                 formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument('input', type=argparse.FileType('rt'))
parser.add_argument('--debug', action='store_true')
parser.add_argument('--part-two', action='store_true')
args = parser.parse_args()

expressions = [line.strip().replace(' ', '') for line in args.input]

def evaluate1(expression: str) -> Tuple[int, int]:
    value = None
    op = None

    consumed = 0
    while consumed < len(expression):
        char = expression[consumed]
        consumed += 1

        if char == '(':
            sub_value, sub_consumed = evaluate1(expression[consumed:])
            consumed += sub_consumed

            if op:
                value = reduce(op, [value, sub_value])
            else:
                value = sub_value
        elif char == ')':
            break
        elif char in '*+':
            op = add if char == '+' else mul
        else:
            if value is None:
                value = int(char)
            else:
                assert op
                value = reduce(op, [value, int(char)])

    return value, consumed


def parse_summand(s: str) -> Tuple[int, int]:
    char = s[0]
    consumed = 1

    if char == '(':
        value, sub_consumed = parse_expression(s[consumed:])
        consumed += sub_consumed

        assert s[consumed] == ')', 'closing parenthesis expected'
        consumed += 1
    else:
        # must be a number
        value = int(char)

    return value, consumed

def parse_factor(s: str) -> Tuple[int, int]:
    value, consumed = parse_summand(s)
    while consumed < len(s):
        if s[consumed] == '+':
            consumed += 1
            sub_value, sub_consumed = parse_summand(s[consumed:])
            value += sub_value
            consumed += sub_consumed
        else:
            break

    return value, consumed


def parse_expression(s: str) -> Tuple[int, int]:
    value, consumed = parse_factor(s)
    while consumed < len(s):
        if s[consumed] == '*':
            consumed += 1
            sub_value, sub_consumed = parse_factor(s[consumed:])
            value *= sub_value
            consumed += sub_consumed
        else:
            break

    return value, consumed


def evaluate(expression: str) -> int:
    if not args.part_two:
        value, consumed = evaluate1(expression)
    else:
        value, consumed = parse_expression(expression)

    assert len(expression) == consumed, 'not all of expression consumed'
    return value

if args.debug:
    for expression in expressions:
        print(expression, end=' = ')
        result = evaluate(expression)
        print(result)

print(sum(map(evaluate, expressions)))
