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
Contains classes for physical weapons.
"""

from math import ceil
from util import ceil_05

# Melee weapons
#
# Name, offensive BV formula, defensive BV, damage formula,
# weight formula, heat
#
# TODO: Chain Whip, Flail, Medium Shield, rules level
#
PHYSICAL = {
    "Hatchet" : [(lambda x : x * 1.5), 0, (lambda x : ceil(x / 5.0)),
                 (lambda x : ceil(x / 15.0)), 0],
    "Sword" : [(lambda x : x * 1.725), 0, (lambda x : ceil(x / 10.0) + 1),
               (lambda x : ceil_05(x / 20.0)), 0],
    "Retractable Blade" :
        [(lambda x : x * 1.725), 0, (lambda x : ceil(x / 10.0)),
         (lambda x : ceil_05(x / 2.0) + 0.5), 0], 
    "Claws" : [(lambda x : x * 1.275), 0, (lambda x : ceil(x / 7.0)),
               (lambda x : ceil(x / 15.0)), 0],
    "Mace" : [(lambda x : x * 1.0), 0, (lambda x : ceil(x / 4.0)),
              (lambda x : ceil(x / 10.0)), 0],
    "Lance" : [(lambda x : x * 1.0), 0, (lambda x : ceil(x / 5.0)),
               (lambda x : ceil_05(x / 20.0)), 0],
    "Small Vibroblade" : [(lambda x : 12), 0, (lambda x : 7.0),
                          (lambda x : 3.0), 3],
    "Medium Vibroblade" : [(lambda x : 17), 0, (lambda x : 10.0),
                           (lambda x : 5.0), 5],
    "Large Vibroblade" : [(lambda x : 24), 0, (lambda x : 14.0),
                          (lambda x : 7.0), 7],
    # Hack: Divide Talons BV multiplier by 2, because it is one item
    # being split up into two
    "Talons" : [(lambda x : x * 1.0), 0, (lambda x : ceil(x / 5.0) / 2.0),
                (lambda x : ceil(x / 15.0)), 0],
    "Spot Welder" : [(lambda x : 5), 0, (lambda x : 5),
                     (lambda x : 2), 2],
    # Defensive stuff
    "Small Shield" : [(lambda x : 0), 50, (lambda x : 0),
                      (lambda x : 2), 0],
    "Large Shield" : [(lambda x : 0), 263, (lambda x : 0),
                      (lambda x : 6), 0],
    "Spikes" : [(lambda x : 0), 4, (lambda x : 0),
                      (lambda x : 0.5), 0]
    }

class Physicallist:
    """
    Store list with physical weapons
    """
    def __init__(self, m_weight):
        self.list = []
        for phys in PHYSICAL.keys():
            self.list.append(Physical(phys, m_weight))
        self.name = "physcial"
        self.p_weight = 0

    def add(self, entry, loc):
        """
        Add a physical weapon
        """
        for phys in self.list:
            if (entry == phys.name):
                phys.addone(loc)
                self.p_weight += phys.get_weight()
                return True
        # No match found
        return False

class Physical:
    """
    A individual physical weapon type
    """
    def __init__(self, key, m_weight):
        self.name = key
        self.m_weight = m_weight
        self.bv_mult = PHYSICAL[key][0]
        self.heat = PHYSICAL[key][4]
        self.count = 0
        self.count_la = 0 # Needed for AES
        self.count_ra = 0

    def get_weight(self):
        """
        Return weight
        """
        return PHYSICAL[self.name][3](float(self.m_weight))

    def get_damage(self):
        """
        Return damage
        """
        return PHYSICAL[self.name][2](self.m_weight)

    def addone(self, loc):
        """
        Add a physical weapon
        """
        self.count = self.count + 1
        # Also keep track of arm locations
        if loc == "LA":
            self.count_la = self.count_la + 1
        elif loc == "RA":
            self.count_ra = self.count_ra + 1

    def get_bv(self):
        """
        Get offensive BV of physical weapon
        """
        dam = PHYSICAL[self.name][2](self.m_weight)
        return self.bv_mult(dam)

    def get_defensive_bv(self):
        """
        Get defensive BV of physical weapon
        """
        return PHYSICAL[self.name][1]
