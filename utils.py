from itertools import tee


# from more-itertools:
# https://more-itertools.readthedocs.io/en/stable/_modules/more_itertools/recipes.html#pairwise
def pairwise(iterable):
    "s -> (s0,s1), (s1,s2), (s2, s3), ..."
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)
