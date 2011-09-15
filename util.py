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
"""

from math import ceil


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

def get_child_data(parent, name):
    """
    Get first child node data
    """
    child = parent.getElementsByTagName(name)[0]
    return gettext(child.childNodes)
