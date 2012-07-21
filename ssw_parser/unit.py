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
unit.py
=======
Contains a base class for units to force common interfaces
"""

from math import ceil


class Unit:
    """
    A base class supposed to contains the interface elements shared by
    all unit types.
    """
    def __init__(self):
        # Declare some variables to shut up error checkers
        self.year = 0
        self.omni = "FALSE"

    def get_year(self, load):
        """
        Get year
        """
        if self.omni == "TRUE":
            return load.year
        else:
            return self.year

    def get_off_speed_factor(self, load, printq):
        """
        Calculates offensive speed factor for BV calculations.
        """
        speed_factor = self.get_max_run() + ceil(load.get_jump() / 2.0)
        if (printq):
            print "Speed Factor: ", speed_factor
        adj_sf = ((speed_factor - 5.0) / 10.0) + 1.0
        off_speed_factor = round(pow(adj_sf, 1.2), 2)
        if (printq):
            print "Offensive Speed Factor: ", off_speed_factor

        return off_speed_factor

    def get_max_run(self):
        """
        Get maximum running speed
        """
        raise NotImplementedError

    def get_rules_level(self, load):
        """
        Return rules level
        0 = Intro-tech,
        1 = Tournament legal,
        2 = Advanced,
        3 = Experimental,
        4 = Primitive (special)
        """
        raise NotImplementedError
