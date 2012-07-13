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

"""
Utility functions

ceil_05 rounds up to nearest half-ton
ceil_5 rounds up to nearest five ton
gettext, get_child, and get_child_data are used for parsing xml
"""

import sys
from math import ceil

CLUSTER_TABLE = {
    2: [1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2],
    3: [1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3],
    4: [1, 2, 2, 2, 2, 3, 3, 3, 3, 4, 4],
    5: [1, 2, 2, 3, 3, 3, 3, 4, 4, 5, 5],
    6: [2, 2, 3, 3, 4, 4, 4, 5, 5, 6, 6],
    7: [2, 2, 3, 4, 4, 4, 4, 6, 6, 7, 7],
    8: [3, 3, 4, 4, 5, 5, 5, 6, 6, 8, 8],
    9: [3, 3, 4, 5, 5, 5, 5, 7, 7, 9, 9],
    10: [3, 3, 4, 6, 6, 6, 6, 8, 8, 10, 10],
    12: [4, 4, 5, 8, 8, 8, 8, 10, 10, 12, 12],
    15: [5, 5, 6, 9, 9, 9, 9, 12, 12, 15, 15],
    20: [6, 6, 9, 12, 12, 12, 12, 16, 16, 20, 20],
    30: [10, 10, 12, 18, 18, 18, 18, 24, 24, 30, 30],
    40: [12, 12, 18, 24, 24, 24, 24, 32, 32, 40, 40]
    }


def cluster(size, col):
    """
    Access cluster table with adjustment
    """
    if col < 0:
        col = 0
    elif col > 10:
        col = 10
    return CLUSTER_TABLE[size][col]


def calc_average(size, adj):
    """
    Calculate average cluster.
    """
    total = 0
    total += cluster(size, 0 + adj)
    total += cluster(size, 1 + adj) * 2
    total += cluster(size, 2 + adj) * 3
    total += cluster(size, 3 + adj) * 4
    total += cluster(size, 4 + adj) * 5
    total += cluster(size, 5 + adj) * 6
    total += cluster(size, 6 + adj) * 5
    total += cluster(size, 7 + adj) * 4
    total += cluster(size, 8 + adj) * 3
    total += cluster(size, 9 + adj) * 2
    total += cluster(size, 10 + adj)
    return float(total) / 36.0


def conv_era(era):
    """
    Convert era to string
    """
    conv = {
        0: "AoW",
        1: "SL",
        2: "SW-E",
        3: "SW-L",
        4: "Clan",
        5: "CW",
        6: "Jihad",
        7: "Rep",
        8: "DA"
        }
    return conv[era]


def get_move_target_modifier(speed):
    """
    Get target movement modifier for a specific speed.
    """
    if (speed < 3):
        mod = 0
    elif (speed < 5):
        mod = 1
    elif (speed < 7):
        mod = 2
    elif (speed < 10):
        mod = 3
    elif (speed < 18):
        mod = 4
    elif (speed < 25):
        mod = 5
    else:
        mod = 6

    return mod


def year_era_test(year, era, name):
    """
    Test if years and production eras are conpatible,
    exit if not.
    """
    if (year <= 2570 and era != 0):
        print name
        print "Year-Era mis-match!", year, conv_era(era)
        sys.exit(1)

    if (year >= 2571 and year <= 2780 and era != 1):
        print name
        print "Year-Era mis-match!", year, conv_era(era)
        sys.exit(1)

    if (year >= 2781 and year <= 2900 and era != 2):
        print name
        print "Year-Era mis-match!", year, conv_era(era)
        sys.exit(1)

    if (year >= 2901 and year <= 3048 and era != 3):
        print name
        print "Year-Era mis-match!", year, conv_era(era)
        sys.exit(1)

    if (year >= 3049 and year <= 3061 and era != 4):
        print name
        print "Year-Era mis-match!", year, conv_era(era)
        sys.exit(1)

    if (year >= 3062 and year <= 3067 and era != 5):
        print name
        print "Year-Era mis-match!", year, conv_era(era)
        sys.exit(1)

    if (year >= 3068 and year <= 3085 and era != 6):
        print name
        print "Year-Era mis-match!", year, conv_era(era)
        sys.exit(1)

    if (year >= 3086 and year <= 3130 and era != 7):
        print name
        print "Year-Era mis-match!", year, conv_era(era)
        sys.exit(1)

    if (year >= 3131 and era != 8):
        print name
        print "Year-Era mis-match!", year, conv_era(era)
        sys.exit(1)


def ceil_05(value):
    """
    Round up to nearest half-ton

    We do this by multiplying with two, rounding up to nearest ton,
    and finally dividing the result with two
    """
    calc = value
    calc *= 2
    calc = ceil(calc)
    calc /= 2
    return calc


def ceil_5(value):
    """
    Round up to nearest five ton

    We do this by dividing with five, rounding up to nearest ton,
    and finally multiplying the result with five
    """
    calc = value
    calc /= 5.0
    calc = ceil(calc)
    calc *= 5
    return calc


def gettext(nodes):
    """
    Get a text node data
    """
    for node in nodes:
        if node.nodeType == node.TEXT_NODE:
            return node.data


def get_child(parent, name):
    """
    Get first child node
    """
    return parent.getElementsByTagName(name)[0]


def get_child_data(parent, name):
    """
    Get first child node data
    """
    child = parent.getElementsByTagName(name)[0]
    return gettext(child.childNodes)
