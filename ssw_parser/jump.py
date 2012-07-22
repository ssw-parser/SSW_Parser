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
jump.py
=======
Contains objects related to jump movement

This includes jumpjets, partial wings, jump boosters.
"""

from math import ceil
from error import error_exit
from util import ceil_05, gettext
from item import Item

# Jump-jet types
#
# Name, heat generated, rules level, cost factor
#
# Where rules level is: 0 = intro, 1 = TL, 2 = advanced, 3 = experimental
#
JUMP_JET = [["Standard Jump Jet", 1, 0, 200],
            ["Improved Jump Jet", 0.5, 1, 500],
            ["Mech UMU", 1, 2, 200]]


class JumpJets(Item):
    """
    A class to hold info about jump-jets

    :param jets: XML node that contains jump-jet info.
    :type jets: xml node
    :param weight: Mech weight.
    :type weight: int
    """
    def __init__(self, jets, weight):
        Item.__init__(self)
        self.weight = weight  # Mech weight, not JJ weight
        # Handle default
        if jets is None:
            self.jump = 0
            self.jjtype = ""
            self.r_level = 0
        else:
            self.jump = int(jets.attributes["number"].value)
            jnode = jets.getElementsByTagName("type")[0]
            self.jjtype = gettext(jnode.childNodes)

        # Check for legal jump-jet type, if jump-jets are mounted, save data
        if self.jump > 0:
            ident = False
            for i in JUMP_JET:
                if i[0] == self.jjtype:
                    ident = True
                    self.heat = i[1]
                    self.r_level = i[2]
                    self.cost = i[3]
            if not ident:
                error_exit(self.jjtype)

    def get_type(self):
        """
        Return jump-jet type description

        :return: jump distance + jump-jet type
        :rtype: string
        """
        return str(self.jump) + " " + self.jjtype

    def get_rules_level(self):
        """
        Return jump-jet rules level

        :return: rules level of jump-jets
        :rtype: int
        """
        return self.r_level

    def get_weight(self):
        """
        Get weight of jumpjets

        :return: the total weight of jump-jets
        :rtype: float
        """
        if self.jump == 0:
            return 0
        if self.weight < 60:
            base = 0.5
        elif self.weight < 90:
            base = 1.0
        else:
            base = 2.0
        if self.jjtype == "Standard Jump Jet" or self.jjtype == "Mech UMU":
            base = base * 1.0
        elif self.jjtype == "Improved Jump Jet":
            base = base * 2.0
        else:
            error_exit(self.jjtype)
        return base * self.jump

    def get_cost(self):
        """
        Get jump-jets cost

        :return: Total cost of all jump-jets
        :rtype: int
        """
        if self.jump == 0:
            return 0
        else:
            return (self.weight * self.jump * self.jump * self.cost)

    def get_jump(self):
        """
        Returns max jump distance

        :return: max jump distance
        :rtype: int
        """
        return self.jump

    def get_heat(self, mech):
        """
        Get jumping heat, minimum 3

        :return: Maximum jumping heat
        :rtype: int
        """
        # No jump jets generate no heat
        if self.jump == 0:
            return 0
        # UMUs generate 1 heat in total
        elif self.jjtype == "Mech UMU":
            return 1
        else:
            heat = self.jump * self.heat
            minimum = 3
            if mech.engine.etype == "XXL Engine":
                heat *= 2
                minimum = 6
            return max(minimum, ceil(heat))


class JumpBoosters(Item):
    """
    A class to hold info about jump boosters.

    :param weight: Mech weight.
    :type weight: int
    :param jump: Booster jump distance.
    :type jump: int

    Unlike some Items, this one requires the xml processing to be done before
    creation.
    """
    def __init__(self, weight, jump):
        Item.__init__(self)
        self.weight = weight  # Mech weight, not JJ weight
        self.jump = jump

    def get_type(self):
        """
        Returns type description

        :return: the string "Mechanical jump boosters"
        :rtype: string
        """
        return "Mechanical jump boosters"

    def get_rules_level(self):
        """
        Jump boosters are advanced rules

        :return: The rules level of jump boosters, or zero if none exists.
        :rtype: int
        """
        if self.jump:
            return 2
        else:
            return 0

    def get_weight(self):
        """
        Get weight of jump-boosters

        :return: weight
        :rtype: float
        """
        return ceil_05(0.05 * self.weight * self.jump)

    def get_cost(self):
        """
        Get cost of jump boosters

        :return: cost
        :rtype: int
        """
        return (self.weight * self.jump * self.jump * 150)

    def get_jump(self):
        """
        Returns jump distance

        :return: maximum jump distance
        :rtype: int
        """
        return self.jump


class PartialWing(Item):
    """
    A class to hold information about partial wings

    :param weight: Mech weight.
    :type weight: int
    :param wing: Status of partial wings.
    :type wing: bool
    :param tech: Partial wing tech base.
    :type tech: int

    Unlike some Items, this one requires the xml processing to be done before
    creation.
    """
    def __init__(self, weight, wing, tech):
        Item.__init__(self)
        self.weight = weight  # Mech weight, not JJ weight
        self.wing = wing  # Bool: Do we mount a partial wing?
        self.tech = tech

    def get_type(self):
        """
        Return partial wing type description

        :return: the string "Partial Wing"
        :rtype: string
        """
        return "Partial Wing"

    def get_rules_level(self):
        """
        Partial wing are advanced rules

        :return: partial wing rules level
        :rtype: int
        """
        if self.wing:
            return 2
        else:
            return 0

    def get_weight(self):
        """
        Get weight of partial wing

        :return: Weight of partial wing
        :rtype: float
        """
        # Clan
        if self.wing and self.tech == 1:
            return ceil_05(0.05 * self.weight)
        # IS
        elif self.wing and self.tech == 0:
            return ceil_05(0.07 * self.weight)
        else:
            return 0.0

    def get_cost(self):
        """
        Get cost of partial wing

        :return: Cost of partial wing
        :rtype: int
        """
        if self.wing:
            return (self.get_weight() * 50000)
        else:
            return 0

    def has_wing(self):
        """
        Return true if we have a wing

        :return: True if a partial wing is mounted, False otherwise.
        :rtype: bool
        """
        return self.wing
