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
# weight formula, heat, rules level, cost
#
# Where rules level is:
#        0 = Intro-tech,
#        1 = Tournament legal,
#        2 = Advanced,
#        3 = Experimental,
#        4 = Primitive (special)
#
# TODO: Medium Shield, industrial equipment
#
PHYSICAL = {
    # Total Warfare
    "Hatchet" : [(lambda x : x * 1.5), 0, (lambda x : ceil(x / 5.0)),
                 (lambda x : ceil(x / 15.0)), 0, 0, (lambda x, y : x * 5000)],
    "Sword" : [(lambda x : x * 1.725), 0, (lambda x : ceil(x / 10.0) + 1),
               (lambda x : ceil_05(x / 20.0)), 0, 1, (lambda x, y : x * 10000)],
    "Retractable Blade" :
        [(lambda x : x * 1.725), 0, (lambda x : ceil(x / 10.0)),
         (lambda x : ceil_05(x / 2.0) + 0.5), 0, 1,
         (lambda x, y : x * 10000 + 10000)], 
    "Backhoe" : [(lambda x : 8), 0, (lambda x: 6),
                 (lambda x : 5), 0, 1, (lambda x, y : 50000)],
    "Spot Welder" : [(lambda x : 5), 0, (lambda x : 5),
                     (lambda x : 2), 2, 1, (lambda x, y : 75000)],
    # Advanced stuff
    "Claws" : [(lambda x : x * 1.275), 0, (lambda x : ceil(x / 7.0)),
               (lambda x : ceil(x / 15.0)), 0, 2, (lambda x, y : y * 200)],
    "Mace" : [(lambda x : x * 1.0), 0, (lambda x : ceil(x / 4.0)),
              (lambda x : ceil(x / 10.0)), 0, 1, (lambda x, y : 130000)],
    "Lance" : [(lambda x : x * 1.0), 0, (lambda x : ceil(x / 5.0)),
               (lambda x : ceil_05(x / 20.0)), 0, 2, (lambda x, y : y * 150)],
    "Small Vibroblade" : [(lambda x : 12), 0, (lambda x : 7.0),
                          (lambda x : 3.0), 3, 3, (lambda x, y : 150000)],
    "Medium Vibroblade" : [(lambda x : 17), 0, (lambda x : 10.0),
                           (lambda x : 5.0), 5, 3, (lambda x, y : 400000)],
    "Large Vibroblade" : [(lambda x : 24), 0, (lambda x : 14.0),
                          (lambda x : 7.0), 7, 3, (lambda x, y : 750000)],
    "Chain Whip" : [(lambda x : 1.725), 0, (lambda x : 3.0),
                    (lambda x : 3.0), 0, 2, (lambda x, y : 120000)],
    "Flail" : [(lambda x : 11.0), 0, (lambda x : 9.0),
               (lambda x : 5.0), 0, 1, (lambda x, y : 110000)],
    # Hack: Divide Talons BV multiplier by 2, because it is one item
    # being split up into two
    "Talons" : [(lambda x : x * 1.0), 0, (lambda x : ceil(x / 5.0) / 2.0),
                (lambda x : ceil(x / 30.0)), 0, 3, (lambda x, y : y * 150)],
    # Defensive stuff
    "Small Shield" : [(lambda x : 0), 50, (lambda x : 0),
                      (lambda x : 2), 0, 3, (lambda x, y : 50000)],
    "Large Shield" : [(lambda x : 0), 263, (lambda x : 0),
                      (lambda x : 6), 0, 3, (lambda x, y : 300000)],
    "Spikes" : [(lambda x : 0), 4, (lambda x : 0),
                      (lambda x : 0.5), 0, 2, (lambda x, y : y * 50)]
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
        self.p_speed = 0

    def get_rules_level(self):
        """
        Return rules level for all weapons
        """
        r_level = 0
        for phys in self.list:
            if phys.get_rules_level() > r_level and phys.count > 0:
                r_level = phys.get_rules_level()
        return r_level

    def get_cost(self):
        """
        Return the cost of all physical weapons
        """
        cost = 0
        for phys in self.list:
            if phys.count > 0:
                cost += phys.count * phys.get_cost()
        return cost

    def add(self, entry, loc):
        """
        Add a physical weapon
        """
        for phys in self.list:
            if (entry == phys.name):
                phys.addone(loc)
                self.p_weight += phys.get_weight()
                # Speed reduction from shields
                if phys.name == "Large Shield":
                    self.p_speed = -1
                return True
        # No match found
        return False

    def get_speed_adj(self):
        """
        Return possible speed adjustment
        """
        return self.p_speed

    def get_def_bv(self):
        """
        Return defensive BV of all physical weapons
        """
        batt_val = 0.0
        for phys in self.list:
            if (phys.count > 0 and phys.get_defensive_bv() > 0):
                bv_gear = phys.count * phys.get_defensive_bv()
                batt_val += bv_gear
        return batt_val


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

    def get_rules_level(self):
        """
        Return rules level
        """
        return PHYSICAL[self.name][5]

    def get_cost(self):
        """
        Return the cost of one item
        """
        return PHYSICAL[self.name][6](self.get_weight(), self.m_weight)

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
