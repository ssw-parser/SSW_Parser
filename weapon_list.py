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
Contains the class that collects all weapons together.
"""

from weapons import Weapon, WEAPONS

# List of secondary weapons.
#
# These weapons are meant to be filtered out when considering a mech's main
# armaments.
#
SECONDARY_LIST = ["(IS) Small Laser", # 0.5t
                  "(IS) Flamer", # 1t
                  "(IS) Machine Gun", # 0.5t
                  "(IS) Medium Laser", # 1t
                  "(IS) Small Pulse Laser", # 1t
                  "(IS) ER Medium Laser", # 1t
                  "(IS) Medium Pulse Laser", # 2t
                  "(IS) ER Small Laser" # 0.5t
                  ]

# List of LRM launcher names, shorthand and tubes
# Missing: NLRM-10, NLRM-15, NLRM-20
LRM_LIST = [["(IS) LRM-5", "i5:", 5],
            ["(IS) LRM-10", "i10:", 10],
            ["(IS) LRM-15", "i15:", 15],
            ["(IS) LRM-20", "i20:", 20],
            ["(CL) LRM-5", "c5:", 5],
            ["(CL) LRM-10", "c10:", 10],
            ["(CL) LRM-15", "c15:", 15],
            ["(CL) LRM-20", "c20:", 20],
            ["(IS) Enhanced LRM-5", "n5:", 5],
            ["(IS) MML-3", "m3:", 3],
            ["(IS) MML-5", "m5:", 5],
            ["(IS) MML-7", "m7:", 7],
            ["(IS) MML-9", "m9:", 9]]

# List of SRM launcher names, shorthand and tubes
SRM_LIST = [["(IS) SRM-2", "i2:", 2],
            ["(IS) SRM-4", "i4:", 4],
            ["(IS) SRM-6", "i6:", 6],
            ["(CL) SRM-2", "c2:", 2],
            ["(CL) SRM-4", "c4:", 4],
            ["(CL) SRM-6", "c6:", 6],
            ["(IS) MML-3", "m3:", 3],
            ["(IS) MML-5", "m5:", 5],
            ["(IS) MML-7", "m7:", 7],
            ["(IS) MML-9", "m9:", 9]]


# List of autocannon names (that can use special ammo), and shorthand
AC_LIST = [["(IS) Autocannon/2", "ac2:"],
           ["(IS) Autocannon/5", "ac5:"],
           ["(IS) Autocannon/10", "ac10:"],
           ["(IS) Autocannon/20", "ac20:"],
           ["(IS) Light AC/2", "lac2:"],
           ["(IS) Light AC/5", "lac5:"]]



class Weaponlist:
    """
    Store the list with weapons
    """
    def __init__(self, art4, art5, apollo):
        self.list = {}
        for weap in WEAPONS.keys():
            self.list[weap] = Weapon(weap, art4, art5, apollo)

    def get_rules_level(self):
        """
        Return rules level for all weapons
        """
        r_level = 0
        for weap in self.list.itervalues():
            if weap.get_rules_level() > r_level and weap.count > 0:
                r_level = weap.get_rules_level()
        return r_level

    def count_damage(self, rnge):
        """
        Count total damage from weapons at a given range
        """
        dam = 0
        for weap in self.list.itervalues():
            if (weap.check_range(rnge) and weap.count > 0):
                dam += weap.get_damage(rnge) * weap.count

        return dam


    def count_srms(self):
        """
        Count number of SRM tubes that can fire special ammo
        """
        srms = 0
        for launcher in SRM_LIST:
            for weap in self.list.itervalues():
                if (weap.name == launcher[0]):
                    srms += launcher[2] * weap.count
        return srms

    def has_ac(self):
        """
        Check if a special ammo using autocannon is mounted
        """
        found = False
        for launcher in AC_LIST:
            for weap in self.list.itervalues():
                if (weap.name == launcher[0] and weap.count > 0):
                    found = True
        return found

    def all_summary(self):
        """
        Return a short description string for all weapons.
        """
        w_str = ""
        for weap in self.list.itervalues():
            if (weap.count > 0):
                w_str += weap.get_short_count() + " "

        return w_str


    def main_summary(self):
        """
        Return a short description string for main weapons.
        """
        w_str = ""
        for weap in self.list.itervalues():
            if (weap.count > 0):
                # Filter out secondary weapons
                found = False
                for sec in SECONDARY_LIST:
                    if sec == weap.name:
                        found = True
                if not found:
                    w_str += weap.get_short_count() + " "

        return w_str


    def std_summary(self, rnge):
        """
        Count total damage and heat from weapons at a given range.
        Also return a short description string.
        Return is in the form (string, damage, heat).
        """
        w_str = ""
        dam = 0
        heat = 0
        for weap in self.list.itervalues():
            if (weap.check_range(rnge) and weap.count > 0):
                w_str += weap.get_short_count() + " "
                dam += weap.get_damage(rnge) * weap.count
                heat += weap.get_heat() * weap.count

        return (w_str, dam, heat)


    def list_summary(self, w_list, rnge):
        """
        Count total damage and heat from weapons in w_list at a given range.
        Also return a short description string.
        Return is in the form (string, damage, heat).
        """
        w_str = ""
        dam = 0
        heat = 0
        for weap in self.list.itervalues():
            for launcher in w_list:
                if (weap.name == launcher[0] and weap.count > 0):
                    w_str += weap.get_short_count() + " "
                    dam += weap.get_damage(rnge) * weap.count
                    heat += weap.get_heat() * weap.count

        return (w_str, dam, heat)


