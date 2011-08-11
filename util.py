#!/usr/bin/python

from math import ceil

# Utility functions

# Round up to nearest half-ton
#
# We do this by multiplying with two, rounding up to nearest ton,
# and finally dividing the result with two
def ceil_05(value):
    calc = value
    calc *= 2
    calc = ceil(calc)
    calc /= 2
    return calc

# Round up to nearest five ton
#
# We do this by dividing with five, rounding up to nearest ton,
# and finally multiplying the result with five
def ceil_5(value):
    calc = value
    calc /= 5.0
    calc = ceil(calc)
    calc *= 5
    return calc
