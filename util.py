#!/usr/bin/python
# coding: utf-8

#    SSW-file parser: Prints mech summaries
#    Copyright (C) 2011  Christer Nyfält
#
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 2 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License along
#    with this program; if not, write to the Free Software Foundation, Inc.,
#    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.



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
