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
item.py
=======
Contains a base class for items to force common interfaces
"""


class Item:
    """
    A base class supposed to contains the interface elements shared by
    all item types.

    Note that this class only intended to be used on bigger items like engines,
    armor, jump-jets and similar. Things that falls under gear should be
    handled differently.
    """
    def __init__(self):
        pass

    def get_type(self):
        """
        Return a string describing the type of the item.
        Note that it is not intended to be used in any conditionals,
        this is just for textual output.
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

    def get_weight(self):
        """
        Returns the weight of the item
        """
        raise NotImplementedError

    def get_cost(self):
        """
        Returns the cost of the item
        """
        raise NotImplementedError

    def summary_string(self):
        """
        Returns a summary string with type and weight.
        """
        return self.get_type() + " " + str(self.get_weight()) + " tons"
