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
Contains objects related to moving a mech: cockpit, engine, gyro, myomer,
jumpjets, partial wing, jump boosters.
"""

from math import ceil
from error import error_exit
from util import ceil_05, ceil_5, gettext
from item import Item

# Engine and other propulsion related stuff, like fixed jumpjets and gyros.

# The following tables contain the engine weight for each rating

STD_ENGINE = {
    10 : 0.5,
    15 : 0.5,
    20 : 0.5,
    25 : 0.5,
    30 : 1.0,
    35 : 1.0,
    40 : 1.0,
    45 : 1.0,
    50 : 1.5,
    55 : 1.5,
    60 : 1.5,
    65 : 2.0,
    70 : 2.0,
    75 : 2.0,
    80 : 2.5,
    85 : 2.5,
    90 : 3.0,
    95 : 3.0,
    100 : 3.0,
    105 : 3.5,
    110 : 3.5,
    115 : 4.0,
    120 : 4.0,
    125 : 4.0,
    130 : 4.5,
    135 : 4.5,
    140 : 5.0,
    145 : 5.0,
    150 : 5.5,
    155 : 5.5,
    160 : 6.0,
    165 : 6.0,
    170 : 6.0,
    175 : 7.0,
    180 : 7.0,
    185 : 7.5,
    190 : 7.5,
    195 : 8.0,
    200 : 8.5,
    205 : 8.5,
    210 : 9.0,
    215 : 9.5,
    220 : 10.0,
    225 : 10.0,
    230 : 10.5,
    235 : 11.0,
    240 : 11.5,
    245 : 12.0,
    250 : 12.5,
    255 : 13.0,
    260 : 13.5,
    265 : 14.0,
    270 : 14.5,
    275 : 15.5,
    280 : 16.0,
    285 : 16.5,
    290 : 17.5,
    295 : 18.0,
    300 : 19.0,
    305 : 19.5,
    310 : 20.5,
    315 : 21.5,
    320 : 22.5,
    325 : 23.5,
    330 : 24.5,
    335 : 25.5,
    340 : 27.0,
    345 : 28.5,
    350 : 29.5,
    355 : 31.5,
    360 : 33.0,
    365 : 34.5,
    370 : 36.5,
    375 : 38.5,
    380 : 41.0,
    385 : 43.5,
    390 : 46.0,
    395 : 49.0,
    400 : 52.5,
    405 : 56.5,
    410 : 61.0,
    415 : 66.5,
    420 : 72.5,
    425 : 79.5,
    430 : 87.5,
    435 : 97.0,
    440 : 107.5,
    445 : 119.5,
    450 : 133.5,
    455 : 150.0,
    460 : 168.5,
    465 : 190.0,
    470 : 214.5,
    475 : 243.0,
    480 : 275.5,
    485 : 313.0,
    490 : 356.0,
    495 : 405.5,
    500 : 462.5
}

LGT_ENGINE = {
    10 : 0.5,
    15 : 0.5,
    20 : 0.5,
    25 : 0.5,
    30 : 1.0,
    35 : 1.0,
    40 : 1.0,
    45 : 1.0,
    50 : 1.5,
    55 : 1.5,
    60 : 1.5,
    65 : 1.5,
    70 : 1.5,
    75 : 1.5,
    80 : 2.0,
    85 : 2.0,
    90 : 2.5,
    95 : 2.5,
    100 : 2.5,
    105 : 3.0,
    110 : 3.0,
    115 : 3.0,
    120 : 3.0,
    125 : 3.0,
    130 : 3.5,
    135 : 3.5,
    140 : 4.0,
    145 : 4.0,
    150 : 4.5,
    155 : 4.5,
    160 : 4.5,
    165 : 4.5,
    170 : 4.5,
    175 : 5.5,
    180 : 5.5,
    185 : 6.0,
    190 : 6.0,
    195 : 6.0,
    200 : 6.5,
    205 : 6.5,
    210 : 7.0,
    215 : 7.5,
    220 : 7.5,
    225 : 7.5,
    230 : 8.0,
    235 : 8.5,
    240 : 9.0,
    245 : 9.0,
    250 : 9.5,
    255 : 10.0,
    260 : 10.5,
    265 : 10.5,
    270 : 11.0,
    275 : 12.0,
    280 : 12.0,
    285 : 12.5,
    290 : 13.5,
    295 : 13.5,
    300 : 14.5,
    305 : 15.0,
    310 : 15.5,
    315 : 16.5,
    320 : 17.0,
    325 : 18.0,
    330 : 18.5,
    335 : 19.5,
    340 : 20.5,
    345 : 21.5,
    350 : 22.5,
    355 : 24.0,
    360 : 25.0,
    365 : 26.0,
    370 : 27.5,
    375 : 29.0,
    380 : 31.0,
    385 : 33.0,
    390 : 34.5,
    395 : 37.0,
    400 : 39.5,
    405 : 42.5,
    410 : 46.0,
    415 : 50.0,
    420 : 54.5,
    425 : 60.0,
    430 : 66.0,
    435 : 73.0,
    440 : 81.0,
    445 : 90.0,
    450 : 100.5,
    455 : 112.5,
    460 : 126.5,
    465 : 142.5,
    470 : 161.0,
    475 : 182.5,
    480 : 207.0,
    485 : 235.0,
    490 : 267.0,
    495 : 304.5,
    500 : 347.0
}

XL_ENGINE = {
    10 : 0.5,
    15 : 0.5,
    20 : 0.5,
    25 : 0.5,
    30 : 0.5,
    35 : 0.5,
    40 : 0.5,
    45 : 0.5,
    50 : 1.0,
    55 : 1.0,
    60 : 1.0,
    65 : 1.0,
    70 : 1.0,
    75 : 1.0,
    80 : 1.5,
    85 : 1.5,
    90 : 1.5,
    95 : 1.5,
    100 : 1.5,
    105 : 2.0,
    110 : 2.0,
    115 : 2.0,
    120 : 2.0,
    125 : 2.0,
    130 : 2.5,
    135 : 2.5,
    140 : 2.5,
    145 : 2.5,
    150 : 3.0,
    155 : 3.0,
    160 : 3.0,
    165 : 3.0,
    170 : 3.0,
    175 : 3.5,
    180 : 3.5,
    185 : 4.0,
    190 : 4.0,
    195 : 4.0,
    200 : 4.5,
    205 : 4.5,
    210 : 4.5,
    215 : 5.0,
    220 : 5.0,
    225 : 5.0,
    230 : 5.5,
    235 : 5.5,
    240 : 6.0,
    245 : 6.0,
    250 : 6.5,
    255 : 6.5,
    260 : 7.0,
    265 : 7.0,
    270 : 7.5,
    275 : 8.0,
    280 : 8.0,
    285 : 8.5,
    290 : 9.0,
    295 : 9.0,
    300 : 9.5,
    305 : 10.0,
    310 : 10.5,
    315 : 11.0,
    320 : 11.5,
    325 : 12.0,
    330 : 12.5,
    335 : 13.0,
    340 : 13.5,
    345 : 14.5,
    350 : 15.0,
    355 : 16.0,
    360 : 16.5,
    365 : 17.5,
    370 : 18.5,
    375 : 19.5,
    380 : 20.5,
    385 : 22.0,
    390 : 23.0,
    395 : 24.5,
    400 : 26.5,
    405 : 28.5,
    410 : 30.5,
    415 : 33.5,
    420 : 36.5,
    425 : 40.0,
    430 : 44.0,
    435 : 48.5,
    440 : 54.0,
    445 : 60.0,
    450 : 67.0,
    455 : 75.0,
    460 : 84.5,
    465 : 95.0,
    470 : 107.5,
    475 : 121.5,
    480 : 138.0,
    485 : 156.5,
    490 : 178.0,
    495 : 203.0,
    500 : 231.5
}

CMP_ENGINE = {
    10 : 1.0,
    15 : 1.0,
    20 : 1.0,
    25 : 1.0,
    30 : 1.5,
    35 : 1.5,
    40 : 1.5,
    45 : 1.5,
    50 : 2.5,
    55 : 2.5,
    60 : 2.5,
    65 : 3.0,
    70 : 3.0,
    75 : 3.0,
    80 : 4.0,
    85 : 4.0,
    90 : 4.5,
    95 : 4.5,
    100 : 4.5,
    105 : 5.5,
    110 : 5.5,
    115 : 6.0,
    120 : 6.0,
    125 : 6.0,
    130 : 7.0,
    135 : 7.0,
    140 : 7.5,
    145 : 7.5,
    150 : 8.5,
    155 : 8.5,
    160 : 9.0,
    165 : 9.0,
    170 : 9.0,
    175 : 10.5,
    180 : 10.5,
    185 : 11.5,
    190 : 11.5,
    195 : 12.0,
    200 : 13.0,
    205 : 13.0,
    210 : 13.5,
    215 : 14.5,
    220 : 15.0,
    225 : 15.0,
    230 : 16.0,
    235 : 16.5,
    240 : 17.5,
    245 : 18.0,
    250 : 19.0,
    255 : 19.5,
    260 : 20.5,
    265 : 21.0,
    270 : 22.0,
    275 : 23.5,
    280 : 24.0,
    285 : 25.0,
    290 : 26.5,
    295 : 27.0,
    300 : 28.5,
    305 : 29.5,
    310 : 31.0,
    315 : 32.5,
    320 : 34.0,
    325 : 35.5,
    330 : 37.0,
    335 : 38.5,
    340 : 40.5,
    345 : 43.0,
    350 : 44.5,
    355 : 47.5,
    360 : 49.5,
    365 : 52.0,
    370 : 55.0,
    375 : 58.0,
    380 : 61.5,
    385 : 65.5,
    390 : 69.0,
    395 : 73.5,
    400 : 79.0
}

# Engine types
#
# Name, techbase, BV multiplier, weight, rules level
#
# Where techbase 0 = IS, 1 = Clan, 2 = Both, 10 = unknown
# Where rules level is: 0 = intro, 1 = TL, 2 = advanced, 3 = experimental,
# 4 = primitive
#
# Missing: ICE, Fuel Cell, Fission
ENGINE = [["Fusion Engine", 2, 1.0, (lambda x : STD_ENGINE[x]), 0],
          ["XL Engine", 0, 0.5, (lambda x : XL_ENGINE[x]), 1],
          ["XL Engine", 1, 0.75, (lambda x : XL_ENGINE[x]), 1],
          ["Light Fusion Engine", 0, 0.75, (lambda x : LGT_ENGINE[x]), 1],
          ["Compact Fusion Engine", 0, 1.0,
           (lambda x : CMP_ENGINE[x]), 1],
          # Advanced
          # XXL Engine (IS): Old BV factor 0.5, new 0.25
          ["XXL Engine", 0, 0.5,
           (lambda x : ceil_05(STD_ENGINE[x] * 0.333)), 3],
          ["XXL Engine", 1, 0.5,
           (lambda x : ceil_05(STD_ENGINE[x] * 0.333)), 3],
          ["Primitive Fusion Engine", 2, 1.0,
           (lambda x : STD_ENGINE[ceil_5(x * 1.2)]), 4]]

# Gyro types
#
# Name, techbase, BV multiplier, weight multiplier, rules level
#
# Where techbase 0 = IS, 1 = Clan, 2 = Both, 10 = unknown
# Where rules level is: 0 = intro, 1 = TL, 2 = advanced, 3 = experimental
#
GYRO = [["Standard Gyro", 2, 0.5, 1.0, 0],
        ["Extra-Light Gyro", 0, 0.5, 0.5, 1],
        ["Heavy-Duty Gyro", 0, 1.0, 2.0, 1],
        ["Compact Gyro", 0, 0.5, 1.5, 1]]

# Jump-jet types
#
# Name, heat generated, rules level
#
# Where rules level is: 0 = intro, 1 = TL, 2 = advanced, 3 = experimental
#
JUMP_JET = [["Standard Jump Jet", 1, 0],
            ["Improved Jump Jet", 0.5, 1],
            ["Mech UMU", 1, 2]]

# Myomer enhancement types
#
# Name, techbase, weight
#
# Where techbase 0 = IS, 1 = Clan, 2 = Both, 10 = unknown
#
ENHANCEMENT = [["---", 2, (lambda x : 0)], #None
               ["MASC", 0, (lambda x : round(x * 0.05))],
               ["MASC", 1, (lambda x : round(x * 0.04))],
               ["TSM", 0, (lambda x : 0)]]

# Cockpit types
#
# Name, weight, rules level
#
# Where rules level is: 0 = intro, 1 = TL, 2 = advanced, 3 = experimental,
# 4 = primitive
#
COCKPIT = [["Standard Cockpit", 3, 0],
           ["Small Cockpit", 2, 1],
           ["Primitive Cockpit", 5, 4]]



class Cockpit(Item):
    """
    A class to hold cockpit (and command console) info
    """
    def __init__(self, cpt):
        Item.__init__(self)
        cnode = cpt.getElementsByTagName("type")[0]
        self.console = cnode.attributes["commandconsole"].value
        self.type = gettext(cnode.childNodes)
        self.c_weight = 0

        # Check for legal cockpit type, save data
        ident = False
        for i in COCKPIT:
            if (i[0] == self.type):
                ident = True
                self.wgt = i[1]
                self.r_level = i[2]
        if not ident:
            error_exit((self.type))

        # Hack: Add console weight
        if self.console == "TRUE":
            self.c_weight = 3

    def get_type(self):
        """
        Return cockpit type
        """
        msg = self.type
        if self.console == "TRUE":
            msg += " (Command Console)"
        return msg

    def get_rules_level(self):
        """
        Return rules level of cockpit
        Command console is advanced
        """
        r_lev = self.r_level
        if self.console == "TRUE":
            return max(2, r_lev)
        else:
            return r_lev

    def get_weight(self):
        """
        Return weight
        """
        return self.wgt + self.c_weight

class JumpJets(Item):
    """
    A class to hold info about jump-jets
    """
    def __init__(self, jets, weight):
        Item.__init__(self)
        self.weight = weight # Mech weight, not JJ weight
        # Handle default
        if jets is None:
            self.jump = 0
            self.jjtype = ""
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
            if not ident:
                error_exit(self.jjtype)

    def get_type(self):
        """
        Return jump-jet type
        """
        return str(self.jump) + " " + self.jjtype

    def get_rules_level(self):
        """
        Return jump-jet rules level
        """
        return self.r_level

    def get_weight(self):
        """
        Get weight of jumpjets
        """
        if self.jump == 0:
            return 0
        if self.weight < 60:
            base = 0.5
        elif self.weight < 90:
            base = 1.0
        else:
            base = 2.0
        if self.jjtype == "Standard Jump Jet":
            base = base * 1.0
        elif self.jjtype == "Improved Jump Jet":
            base = base * 2.0
        else:
            error_exit(self.jjtype)
        return base * self.jump

    def get_jump(self):
        """
        Return distance
        """
        return self.jump

    def get_heat(self, mech):
        """
        Get jumping heat, minimum 3
        """
        # No jump jets generate no heat
        if self.jump == 0:
            return 0
        # UMUs generate 1 heat in total
        elif self.jjtype == "Mech UMU":
            return 1
        else:
            heat = ceil(self.jump * self.heat)
            minimum = 3
            if mech.engine.etype == "XXL Engine":
                heat *= 2
                minimum = 6
            return max(minimum, heat)


class JumpBoosters(Item):
    """
    A class to hold info about jump booster
    """
    def __init__(self, weight, jump):
        Item.__init__(self)
        self.weight = weight # Mech weight, not JJ weight
        self.jump = jump

    def get_type(self):
        """
        Return type
        """
        return "Mechanical jump boosters"

    def get_rules_level(self):
        """
        Jump boosters are advanced rules
        """
        if self.jump:
            return 2
        else:
            return 0

    def get_weight(self):
        """
        Get weight of jump-boosters
        """
        base = ceil_05(0.05 * self.weight)
        return base * self.jump

    def get_jump(self):
        """
        Return distance
        """
        return self.jump


class PartialWing(Item):
    """
    A class to hold information about partial wings
    """
    def __init__(self, weight, wing):
        Item.__init__(self)
        self.weight = weight # Mech weight, not JJ weight
        self.wing = wing # Bool: Do we mount a partial wing?

    def get_type(self):
        """
        Return partial wing
        """
        return "Partial Wing"

    def get_rules_level(self):
        """
        Partial wing are advanced rules
        """
        if self.wing:
            return 2
        else:
            return 0

    def get_weight(self):
        """
        Get weight of partial wing
        """
        if self.wing:
            return ceil_05(0.05 * self.weight)
        else:
            return 0

    def has_wing(self):
        """
        Return true if we have a wing 
        """
        return self.wing

class Enhancement(Item):
    """
    A class to hold information about myomer enhancements
    """
    def __init__(self, enh, weight):
        Item.__init__(self)
        if enh is None:
            self.etb = 2
            self.enhancement = "---"
        else:
            enode = enh.getElementsByTagName("type")[0]
            self.enhancement = gettext(enode.childNodes)
            self.etb = int(enh.attributes["techbase"].value)

        # Check for legal enhancement type, save data
        ident = False
        for i in ENHANCEMENT:
            if (i[0] == self.enhancement and i[1] == self.etb):
                ident = True
                self.enhweight = i[2](weight)
        if not ident:
            error_exit((self.enhancement, self.etb))

    def get_type(self):
        """
        Return myomer enhancement type
        """
        if self.enhancement == "---":
            return ""
        else:
            return self.enhancement

    def get_rules_level(self):
        """
        Everything is tournament legal, none is intro
        """
        if self.enhancement == "---":
            return 0
        else:
            return 1

    def get_weight(self):
        """
        Return weight of myomer enhancement
        """
        return self.enhweight

    def is_tsm(self):
        """
        Check if the enhancemetn is TSM
        """
        if self.enhancement == "TSM":
            return True
        else:
            return False

    def is_masc(self):
        """
        Check if the enhancement is MASC
        """
        if self.enhancement == "MASC":
            return True
        else:
            return False

class Gyro(Item):
    """
    A class to hold gyroscope information
    """
    def __init__(self, gyr, etype, erating):
        Item.__init__(self)
        # We need engine info for calculations
        self.gtype = gettext(gyr.childNodes)
        self.g_base = int(gyr.attributes["techbase"].value)

        # Check for legal gyro type, save data
        ident = False
        for i in GYRO:
            if (i[0] == self.gtype and i[1] == self.g_base):
                ident = True
                self.gyro_bv = i[2]
                gweightm = i[3]
                self.r_level = i[4]
        if not ident:
            error_exit((self.gtype, self.g_base))

        # Calculate weight
        rating = erating
        # Hack: Make sure Primitive Engines get right gyro weight
        if etype == "Primitive Fusion Engine":
            rating *= 1.2
            rating = ceil_5(rating)
        base_weight = ceil(float(rating) / 100.0)
        self.weight = gweightm * base_weight

    def get_type(self):
        """
        Return gyro type
        """
        return self.gtype

    def get_rules_level(self):
        """
        Return gyro rules level
        """
        return self.r_level

    def get_weight(self):
        """
        Return weight of gyro
        """
        return self.weight

    def get_bv_mod(self):
        """
        Get BV factor for gyro
        """
        return self.gyro_bv


class Engine(Item):
    """
    A class to hold engine info for a mech
    """
    def __init__(self, eng, weight):
        Item.__init__(self)
        self.erating = int(eng.attributes["rating"].value)
        self.e_base = int(eng.attributes["techbase"].value)
        self.etype = gettext(eng.childNodes)
        self.speed = self.erating / weight
        # A note on primitive engines:
        # It seems like using engine rating directly does give
        # the right speed, even if rules says otherwise
        # This looks like an internal SSW issue, so
        # assume that the weight of these engines are incorrect

        # Check for legal engine type, save data
        ident = False
        for i in ENGINE:
            if (i[0] == self.etype and i[1] == self.e_base):
                ident = True
                self.eng_bv = i[2]
                self.eweight = i[3](self.erating)
                self.r_level = i[4]
        if not ident:
            error_exit((self.etype, self.e_base))


    def get_type(self):
        """
        Return engine type
        """
        return str(self.erating) + " " + self.etype

    def get_rules_level(self):
        """
        Return engine rules level
        """
        r_lev = self.r_level
        # Large engines are advanced
        if self.erating > 400:
            r_lev = max(r_lev, 2)
        return r_lev

    def get_weight(self):
        """
        Return weight of engine
        """
        return self.eweight

    def get_bv_mod(self):
        """
        Get BV factor for engine
        """
        return self.eng_bv

    def vulnerable(self):
        """
        Returns false if CASE protects from engine shutdown,
        true if explosions in a side torso causes shutdown
        """
        # Inner Sphere XL engines are vulnerable
        if self.etype == "XL Engine" and self.e_base == 0:
            return True
        # and so is all XXL engines
        elif self.etype == "XXL Engine":
            return True
        # the rest are safe
        else:
            return False
