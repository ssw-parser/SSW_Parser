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


from math import ceil
from error import *
from util import ceil_05


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
# Name, techbase, year, BV multiplier, weight factor
#
# Where techbase 0 = IS, 1 = Clan, 2 = Both, 10 = unknown
#
# Missing: Industrial
STRUCTURE = [["Standard Structure", 2, 2439, 1.0, 0.1],
             ["Endo-Steel", 0, 2487, 1.0, 0.05],
             ["Endo-Steel", 1, 2487, 1.0, 0.05],
             # No year given for primitive structure,
             # assume it becomes available the same year as the Mackie
             ["Primitive Structure", 0, 2439, 1.0, 0.1]]


# Info on armor types
#
# Name, techbase, year, BV multiplier, armor multiplier
#
# Where techbase 0 = IS, 1 = Clan, 2 = Both, 10 = unknown
#
# Missing: Industrial, Heavy Industrial, Commericial, TO armor
ARMOR = [["Standard Armor", 2, 2470, 1.0, 1.0],
         ["Ferro-Fibrous", 0, 2571, 1.0, 1.12],
         ["Ferro-Fibrous", 1, 2571, 1.0, 1.2],
         ["Light Ferro-Fibrous", 0, 3067, 1.0, 1.06],
         ["Heavy Ferro-Fibrous", 0, 3069, 1.0, 1.24],
         ["Stealth Armor", 0, 3063, 1.0, 1.0],
         # No year given for primitive armor, assume it becomes available
         # the same year as the Mackie
         ["Primitive Armor", 0, 2439, 1.0, 0.67]]


class IS:
    """
    A class to hold info about the internal stucture
    """
    def __init__(self, istype, tech_base, weight, motive):
        self.type = istype
        self.tech_base = int(tech_base)
        wgt = weight

        # Check for legal structure type, save data
        ident = False
        for i in STRUCTURE:
            if (i[0] == self.type and i[1] == self.tech_base):
                ident = True
                self.year = i[2]
                self.is_bv = i[3]
                wgtf = i[4]
        if ident == False:
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
    def __init__(self, loc_name, armor, maximum):
        self.l_name = loc_name
        self.arm = armor
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

    def get_warning_string(self):
        """
        Used if an report of armor value should be added to warnings
        """
        msg = "  " + self.l_name + " armor: " + str(self.arm)
        return msg

class Armor:
    """
    A class to hold armor info for a mech
    """
    def __init__(self, weight, motive, atype, tech_base,
                 hd, ct, ctr, lt, ltr, rt, rtr, la, ra, ll, rl):
        # Save type of armor
        self.atype = atype
        # and its techbase
        self.tech_base = int(tech_base)

        # Check for legal armor type, save data
        ident = False
        for i in ARMOR:
            if (i[0] == self.atype and i[1] == self.tech_base):
                ident = True
                self.year = i[2]
                self.armor_bv = i[3]
                self.armor_multipler = i[4]
        if ident == False:
            error_exit((self.atype, self.tech_base))


        # Head always have max 9 armor
        self.head = ArmorLoc("Head", hd, 9)

        # Otherwise 2 times Internal Structure
        # We store three different values for each torso part
        # to simplify the interface. Front, rear and total
        self.ctf = ArmorLoc("Center Torso front", ct, CT_IS[weight] * 2)
        self.ctr = ArmorLoc("Center Torso rear", ctr, CT_IS[weight] * 2)
        self.ct = ArmorLoc("Center Torso total", ct + ctr, CT_IS[weight] * 2)
        self.ltf = ArmorLoc("Left Torso front", lt, ST_IS[weight] * 2)
        self.ltr = ArmorLoc("Left Torso rear", ltr, ST_IS[weight] * 2)
        self.lt = ArmorLoc("Left Torso total", lt + ltr, ST_IS[weight] * 2)
        self.rtf = ArmorLoc("Right Torso front", rt, ST_IS[weight] * 2)
        self.rtr = ArmorLoc("Right Torso rear", rtr, ST_IS[weight] * 2)
        self.rt = ArmorLoc("Right Torso total", rt + rtr, ST_IS[weight] * 2)

        # The arms/front legs need to check if mech is Biped or Quad
        if motive == "Quad":
            self.l_arm = ArmorLoc("Front Left Leg", la, LEG_IS[weight] * 2)
        elif motive == "Biped":
            self.l_arm = ArmorLoc("Left Arm", la, ARM_IS[weight] * 2)
        else:
            error_exit(motive)

        if motive == "Quad":
            self.r_arm = ArmorLoc("Front Right Leg", ra, LEG_IS[weight] * 2)
        elif motive == "Biped":
            self.r_arm = ArmorLoc("Right Arm", ra, ARM_IS[weight] * 2)
        else:
            error_exit(motive)

        if motive == "Quad":
            self.l_leg = ArmorLoc("Rear Left Leg", ll, LEG_IS[weight] * 2)
        elif motive == "Biped":
            self.l_leg = ArmorLoc("Left Leg", ll, LEG_IS[weight] * 2)
        else:
            error_exit(motive)

        if motive == "Quad":
            self.r_leg = ArmorLoc("Rear Right Leg", rl, LEG_IS[weight] * 2)
        elif motive == "Biped":
            self.r_leg = ArmorLoc("Right Leg", rl, LEG_IS[weight] * 2)
        else:
            error_exit(motive)

        # Last sum up total
        armortotal = self.head.arm + self.ct.arm + self.lt.arm + self.rt.arm + self.l_arm.arm + self.r_arm.arm + self.l_leg.arm + self.r_leg.arm
        maxtotal = self.head.max + self.ct.max + self.lt.max + self.rt.max + self.l_arm.max + self.r_arm.max + self.l_leg.max + self.r_leg.max
        self.total = ArmorLoc("Total", armortotal, maxtotal)

        # Store potential falling damage
        self.fall_dam = ceil(weight / 10.0)


    def get_armor_bv(self):
        """
        Return armor BV
        """
        return (self.armor_bv * 2.5 * self.total.arm)
       

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

    def print_report(self, armor):
        """
        Print a report of the armor in a cetain location in the form:
        Location: armor/max xx%
        """
        ratio = float(armor.arm) / float(armor.max)
        msg = ("%-18s: %3d/%3d %3d %%" % (armor.l_name, armor.arm, armor.max,
                                          int(ratio * 100)))
        print msg

    def head_report(self):
        """
        Head armor report
        """
        self.print_report(self.head)
        if (not self.head.check_value(8)):
            st1 = "WARNING: 10-points hits will head-cap!"
            st2 = self.head.get_warning_string()
            warnings.add((st1, st2))
            print_warning((st1, st2))

    def report_fall(self, a_loc):
        """
        Falling damage armor report
        """
        if (a_loc.arm < self.fall_dam):
            st1 = "WARNING: Falling damage might go internal on " + a_loc.l_name + " armor!"
            st2 = "  Damage: " + str(self.fall_dam) + ", armor: " + str(a_loc.arm)
            warnings.add((st1, st2))
            print_warning((st1, st2))

    def report_standard(self, a_loc):
        """
        Standard armor location report, should be used in most cases
        Considers an armor value of less than 50% of max to be too weak
        """
        self.print_report(a_loc)
        if (not a_loc.check_percent(0.5)):
            st1 = "WARNING: Weak " + a_loc.l_name + " armor!"
            st2 = a_loc.get_warning_string()
            warnings.add((st1, st2))
            print_warning((st1, st2))
        # Also check for falling damage, just in case
        self.report_fall(a_loc)

    def center_torso_report(self):
        """
        Center torso armor report
        """
        # Standard for front armor
        self.report_standard(self.ctf)
        # Only falling damage check for rear
        self.print_report(self.ctr)
        self.report_fall(self.ctr)
        # No checks for total armor
        self.print_report(self.ct)

    def left_torso_report(self):
        """
        Left torso armor report
        """
        # Standard for front armor
        self.report_standard(self.ltf)
        # Only falling damage check for rear
        self.print_report(self.ltr)
        self.report_fall(self.ltr)
        # No checks for total armor
        self.print_report(self.lt)

    def right_torso_report(self):
        """
        Right torso armor report
        """
        # Standard for front armor
        self.report_standard(self.rtf)
        # Only falling damage check for rear
        self.print_report(self.rtr)
        self.report_fall(self.rtr)
        # No checks for total armor
        self.print_report(self.rt)

    def armor_total_report(self):
        """
        Report total armor
        """
        if self.tech_base == 0:
            base = "(Inner Sphere)"
        elif self.tech_base == 1:
            base = "(Clan)"
        elif self.tech_base == 2:
            base = ""
        print str(self.get_weight()) + " tons " + self.atype + " " + base
        self.print_report(self.total)

    def parse_armor(self):
        self.armor_total_report()
        self.head_report()
        self.center_torso_report()
        self.left_torso_report()
        self.right_torso_report()
        self.report_standard(self.l_leg)
        self.report_standard(self.r_leg)
        self.report_standard(self.l_arm)
        self.report_standard(self.r_arm)


