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
type.py
===============
Contains definitions of mech types
"""

from battle_force import BattleForce


class Type:
    """
    A master class to hold specification of mech types.
    """
    def __init__(self, mech, load):
        # Save pointers to data
        self.mech = mech
        self.load = load

    ### Mech type tests ###

    def is_juggernaut(self):
        """
        Check if a mech is a juggernaut

        Definition:
        - Walking and jump speed no more than 4
        - BF armor at least 5
        - Able to do 30 damage at range 6
        - Do less than 20 damage at range 18
        """
        if self.mech.get_walk() > 4 or self.load.get_jump() > 4:
            return False

        batt_f = BattleForce(self.mech, self.load)
        if batt_f.get_armor() < 5:
            return False

        if self.load.gear.weaponlist.count_damage(6) < 30:
            return False

        if self.load.gear.weaponlist.count_damage(18) >= 20:
            return False

        return True

    def is_sniper(self):
        """
        Check if a mech is a sniper

        Definition:
        - Able to do 10 damage at range 18
        - Do same (or less) damage at range 15 than range 18
          or is slower than walk or jump 4
        """
        dam18 = self.load.gear.weaponlist.count_damage(18)
        if dam18 < 10:
            return False

        if (self.load.gear.weaponlist.count_damage(15) > dam18 and
            (self.mech.get_walk() > 3 or self.load.get_jump() > 4)):
            return False

        return True

    def is_missile_boat(self):
        """
        Check if a mech is a missile boat

        Definition:
        - Has at least 20 LRM tubes
        """
        if self.load.gear.weaponlist.lrms < 20:
            return False

        return True

    def is_striker(self):
        """
        Check if a mech is a striker

        Definition:
        - Speed at least walk 5 or jump 5
        - Able to do 15 damage at range 3
        """
        if self.mech.get_walk() < 5 and self.load.get_jump() < 5:
            return False

        if self.load.gear.weaponlist.count_damage(3) < 15:
            return False

        return True

    def is_skirmisher(self):
        """
        Check if a mech is a skirmisher

        Definition:
        - Speed at least walk 5 or jump 5
        - BF armor at least 3
        - Able to do 5 damage at range 15
        """
        if self.mech.get_walk() < 5 and self.load.get_jump() < 5:
            return False

        batt_f = BattleForce(self.mech, self.load)
        if batt_f.get_armor() < 3:
            return False

        if self.load.gear.weaponlist.count_damage(15) < 5:
            return False

        return True

    def is_scout(self):
        """
        Check if a mech is a scout

        Definition:
        - Speed at least walk 6 or jump 6
        """
        if self.mech.get_walk() < 6 and self.load.get_jump() < 6:
            return False

        return True

    def is_brawler(self):
        """
        Check if a mech is a brawler

        Definition:
        - Speed at least walk 4 or jump 4
        - BF armor at least 4
        - Able to do 10 damage at range 15
        - Do more damage at range 15 than range 18
        """
        if self.mech.get_walk() < 4 and self.load.get_jump() < 4:
            return False

        batt_f = BattleForce(self.mech, self.load)
        if batt_f.get_armor() < 4:
            return False

        dam15 = self.load.gear.weaponlist.count_damage(15)
        if dam15 < 10:
            return False

        if self.load.gear.weaponlist.count_damage(18) >= dam15:
            return False

        return True
