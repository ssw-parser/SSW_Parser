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
Contains a base class to force common interfaces
"""

class Item:
    """
    A base class supposed to contains the interface elements shared by
    all item types.
    """
    def __init__(self):
        pass

    def get_type(self):
        """
        Return a string containing the type of the item
        """
        raise NotImplementedError

    def get_rules_level(self):
        """
        Return rules level
        0 = Intro-tech,
        1 = Tournament legal,
        2 = Advanced,
        3 = Experimental,
        4 = Primitive (special)
        """
        raise NotImplementedError

    def get_year(self):
        """
        Returns the earliest year the item is available
        Returns first year it is no longer experimental,
        if it is not an expermental item
        """
        raise NotImplementedError

    def get_weight(self):
        """
        Returns the weight of the item
        """
        raise NotImplementedError

    def summary_string(self):
        """
        Returns a summary string with type and weight
        """
        return self.get_type() + " " + str(self.get_weight()) + " tons"
