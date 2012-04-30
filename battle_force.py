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
Contains BattleForce data for a mech
"""

from mech import Mech

class BattleForce:
    """
    A master class to hold data specific to BattleForce.
    """
    def __init__(self, mech, load):
        # Save pointers to data
        self.mech = mech
        self.load = load
 
    def get_weight_class(self):
        """
        Get BattleForce weight class
        """
        if self.mech.weight < 40:
            return 1
        elif self.mech.weight < 60:
            return 2
        elif self.mech.weight < 80:
            return 3
        else:
            return 4

    def get_point_value(self):
        """
        Get BattleForce point value
        """
        batt_val = round(self.mech.get_bv(self.load) / 100.0)
        if batt_val < 1:
            batt_val = 1
        return batt_val
