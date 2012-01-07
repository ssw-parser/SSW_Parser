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
Mech internal structure and armor classes
"""

from error import error_exit
from util import ceil_05, get_child_data
from item import Item

# These four tables lists internal structure for each weight class in
# 1st: center torso, 2nd: side torsos, 3rd: arms, and 4th: legs
CT_IS = {
    20 : 6,
    25 : 8,
    30 : 10,
    35 : 11,
    40 : 12,
    45 : 14,
    50 : 16,
    55 : 18,
    60 : 20,
    65 : 21,
    70 : 22,
    75 : 23,
    80 : 25,
    85 : 27,
    90 : 29,
    95 : 30,
    100 : 31
    }

ST_IS = {
    20 : 5,
    25 : 6,
    30 : 7,
    35 : 8,
    40 : 10,
    45 : 11,
    50 : 12,
    55 : 13,
    60 : 14,
    65 : 15,
    70 : 15,
    75 : 16,
    80 : 17,
    85 : 18,
    90 : 19,
    95 : 20,
    100 : 21
    }

ARM_IS = {
    20 : 3,
    25 : 4,
    30 : 5,
    35 : 6,
    40 : 6,
    45 : 7,
    50 : 8,
    55 : 9,
    60 : 10,
    65 : 10,
    70 : 11,
    75 : 12,
    80 : 13,
    85 : 14,
    90 : 15,
    95 : 16,
    100 : 17
    }

LEG_IS = {
    20 : 4,
    25 : 6,
    30 : 7,
    35 : 8,
    40 : 10,
    45 : 11,
    50 : 12,
    55 : 13,
    60 : 14,
    65 : 15,
    70 : 15,
    75 : 16,
    80 : 17,
    85 : 18,
    90 : 19,
    95 : 20,
    100 : 21
    }

# Info on internal structure types
#
# Name, techbase, year, BV multiplier, weight factor, rules level
#
# Where techbase 0 = IS, 1 = Clan, 2 = Both, 10 = unknown
# Where rules level is 0 = intro, 1 = TL, 2 = advanced, 3 = experimental,
# 4 = primitive
#
# Missing: Industrial
STRUCTURE = [["Standard Structure", 2, 2439, 1.0, 0.1, 0],
             ["Endo-Steel", 0, 2487, 1.0, 0.05, 1],
             ["Endo-Steel", 1, 2487, 1.0, 0.05, 1],
             # No year given for primitive structure,
             # assume it becomes available the same year as the Mackie
             ["Primitive Structure", 0, 2439, 1.0, 0.1, 4]]


# Info on armor types
#
# Name, techbase, year, BV multiplier, armor multiplier, rules level
#
# Where techbase 0 = IS, 1 = Clan, 2 = Both, 10 = unknown
# Where rules level is 0 = intro, 1 = TL, 2 = advanced, 3 = experimental,
# 4 = primitive
#
# Missing: Industrial, Heavy Industrial, Commericial, TO armor
ARMOR = [["Standard Armor", 2, 2470, 1.0, 1.0, 0],
         ["Ferro-Fibrous", 0, 2571, 1.0, 1.12, 1],
         ["Ferro-Fibrous", 1, 2571, 1.0, 1.2, 1],
         ["Light Ferro-Fibrous", 0, 3067, 1.0, 1.06, 1],
         ["Heavy Ferro-Fibrous", 0, 3069, 1.0, 1.24, 1],
         ["Stealth Armor", 0, 3063, 1.0, 1.0, 1],
         # No year given for primitive armor, assume it becomes available
         # the same year as the Mackie
         ["Primitive Armor", 0, 2439, 1.0, 0.67, 4]]


class IS(Item):
    """
    A class to hold info about the internal stucture
    """
    def __init__(self, stru, weight, motive):
        Item.__init__(self)
        self.tech_base = int(stru.attributes["techbase"].value)
        self.type = get_child_data(stru, "type")
        wgt = weight

        # Check for legal structure type, save data
        ident = False
        for i in STRUCTURE:
            if (i[0] == self.type and i[1] == self.tech_base):
                ident = True
                self.year = i[2]
                self.is_bv = i[3]
                wgtf = i[4]
                self.r_level = i[5]
        if not ident:
            error_exit((self.type, self.tech_base))

        # Calculate IS weight
        wgt *= wgtf
        # hack to get half-ton rounding up
        wgt = ceil_05(wgt)
        self.wgt = wgt

        # Calculate IS points
        self.points = 0

        # Head always have 3 IS
        self.points += 3

        # Otherwise get from table
        self.points += CT_IS[weight]
        self.points += ST_IS[weight] * 2
        self.points += LEG_IS[weight] * 2

        # The arms/front legs need to check if mech is Biped or Quad
        if motive == "Quad":
            self.points += LEG_IS[weight] * 2
        elif motive == "Biped":
            self.points += ARM_IS[weight] * 2
        else:
            error_exit(motive)

    def get_type(self):
        """
        Return internal structure type
        """
        return self.type

    def get_rules_level(self):
        """
        Return armor rules level
        0 = intro, 1 = tournament legal, 2 = advanced, 3 = experimental
        """
        return self.r_level

    def get_year(self):
        """
        Return earliest year structure is available
        """
        return self.year

    def get_weight(self):
        """
        Return structure weight
        """
        return self.wgt

    def get_bv_factor(self):
        """
        Return IS BV factor
        """
        return self.points * 1.5 * self.is_bv

class ArmorLoc:
    """
    A class to hold info about the armor in one location
    """
    def __init__(self, loc_name, armor, i_struct, maximum):
        self.l_name = loc_name
        self.arm = armor
        self.i_struct = i_struct
        self.max = maximum
        assert self.arm <= self.max, "More than maximum armor!"

    def check_value(self, value):
        """
        Check if armor is at least value
        """
        return self.arm >= value

    def check_percent(self, percent):
        """
        Check if armor is at least percent of max
        """
        return (self.arm >= self.max * percent)

    def check_armor_is(self, value):
        """
        Check if armor and IS is at least value
        """
        return ((self.arm + self.i_struct) >= value)

    def get_warning_string(self):
        """
        Used if an report of armor value should be added to warnings
        """
        msg = "  " + self.l_name + " armor: " + str(self.arm)
        return msg

    def get_report(self):
        """
        Print a report of the armor in a cetain location in the form:
        Location: armor/max xx%
        """
        ratio = float(self.arm) / float(self.max)
        msg = ("%-18s: %3d/%3d %3d %%" % (self.l_name, self.arm, self.max,
                                          int(ratio * 100)))
        return msg


class TorsoArmor:
    """
    A class to hold info about the armor in a torso location
    """
    def __init__(self, loc_name, front, rear, i_struct):
        self.front = ArmorLoc(loc_name + " front", front, i_struct,
                              i_struct * 2)
        self.rear = ArmorLoc(loc_name + " rear", rear, i_struct, i_struct * 2)
        self.total = ArmorLoc(loc_name + " total", front + rear, i_struct,
                              i_struct * 2)

    def report(self):
        """
        Report for torso armor: front, rear and total
        """
        print self.front.get_report()
        print self.rear.get_report()
        print self.total.get_report()

    def get_total(self):
        """
        Get total armor, both front and rear for this location
        """
        return self.total.arm

    def get_max(self):
        """
        Get maximum possible armor for this location
        """
        return self.total.max


class Armor(Item):
    """
    A class to hold armor info for a mech
    """
    def __init__(self, arm, weight, motive):
        Item.__init__(self)
        self.tech_base = int(arm.attributes["techbase"].value)
        self.atype = get_child_data(arm, "type")
        head = int(get_child_data(arm, "hd"))
        c_torso = int(get_child_data(arm, "ct"))
        ctr = int(get_child_data(arm, "ctr"))
        l_torso = int(get_child_data(arm, "lt"))
        ltr = int(get_child_data(arm, "ltr"))
        r_torso = int(get_child_data(arm, "rt"))
        rtr = int(get_child_data(arm, "rtr"))
        l_arm = int(get_child_data(arm, "la"))
        r_arm = int(get_child_data(arm, "ra"))
        l_leg = int(get_child_data(arm, "ll"))
        r_leg = int(get_child_data(arm, "rl"))

        # Check for legal armor type, save data
        ident = False
        for i in ARMOR:
            if (i[0] == self.atype and i[1] == self.tech_base):
                ident = True
                self.year = i[2]
                self.armor_bv = i[3]
                self.armor_multipler = i[4]
                self.r_level = i[5]
        if not ident:
            error_exit((self.atype, self.tech_base))


        # Head always have max 9 armor
        self.head = ArmorLoc("Head", head, 3, 9)

        # Otherwise 2 times Internal Structure
        self.c_torso = TorsoArmor("Center Torso", c_torso, ctr, CT_IS[weight])
        self.l_torso = TorsoArmor("Left Torso", l_torso, ltr, ST_IS[weight])
        self.r_torso = TorsoArmor("Right Torso", r_torso, rtr, ST_IS[weight])

        # The arms/front legs need to check if mech is Biped or Quad
        if motive == "Quad":
            self.l_arm = ArmorLoc("Front Left Leg", l_arm, LEG_IS[weight],
                                  LEG_IS[weight] * 2)
            self.r_arm = ArmorLoc("Front Right Leg", r_arm, LEG_IS[weight],
                                  LEG_IS[weight] * 2)
            self.l_leg = ArmorLoc("Rear Left Leg", l_leg, LEG_IS[weight],
                                  LEG_IS[weight] * 2)
            self.r_leg = ArmorLoc("Rear Right Leg", r_leg, LEG_IS[weight],
                                  LEG_IS[weight] * 2)
        elif motive == "Biped":
            self.l_arm = ArmorLoc("Left Arm", l_arm, ARM_IS[weight],
                                  ARM_IS[weight] * 2)
            self.r_arm = ArmorLoc("Right Arm", r_arm, ARM_IS[weight],
                                  ARM_IS[weight] * 2)
            self.l_leg = ArmorLoc("Left Leg", l_leg, LEG_IS[weight],
                                  LEG_IS[weight] * 2)
            self.r_leg = ArmorLoc("Right Leg", r_leg, LEG_IS[weight],
                                  LEG_IS[weight] * 2)
        else:
            error_exit(motive)

        # Last sum up total
        armortotal = (self.head.arm + self.c_torso.get_total() +
                      self.l_torso.get_total() +
                      self.r_torso.get_total() + self.l_arm.arm +
                      self.r_arm.arm +
                      self.l_leg.arm + self.r_leg.arm)
        maxtotal = (self.head.max + self.c_torso.get_max() +
                    self.l_torso.get_max() +
                    self.r_torso.get_max() + self.l_arm.max + self.r_arm.max +
                    self.l_leg.max + self.r_leg.max)
        self.total = ArmorLoc("Total", armortotal, (maxtotal - 9) / 2 + 3,
                              maxtotal)

    def get_armor_bv(self):
        """
        Return armor BV
        """
        return (self.armor_bv * 2.5 * self.total.arm)
       

    def get_type(self):
        """
        Return armor type
        """
        if self.tech_base == 0:
            base = "(IS)"
        elif self.tech_base == 1:
            base = "(Clan)"
        elif self.tech_base == 2:
            base = ""
        return self.atype + " " + base

    def get_rules_level(self):
        """
        Return armor rules level
        0 = intro, 1 = tournament legal, 2 = advanced, 3 = experimental
        """
        return self.r_level

    def get_year(self):
        """
        Return earliest year armor is available
        """
        return self.year

    def get_weight(self):
        """
        Return armor weight
        """
        wgt = self.total.arm / (16 * self.armor_multipler)
        # hack to get half-ton rounding up
        wgt = ceil_05(wgt)
        return wgt

    def get_armor_percent(self):
        """
        Return armor percent
        """
        ratio = float(self.total.arm) / float(self.total.max)
        return (ratio * 100)

    def armor_total_report(self):
        """
        Report total armor
        """
        print self.summary_string()
        print self.total.get_report()

    def parse_armor(self):
        """
        Print out all armor reports
        """
        self.armor_total_report()
        print self.head.get_report()
        self.c_torso.report()
        self.l_torso.report()
        self.r_torso.report()
        print self.l_leg.get_report()
        print self.r_leg.get_report()
        print self.l_arm.get_report()
        print self.r_arm.get_report()

