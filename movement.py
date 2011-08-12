#!/usr/bin/python

from math import ceil
from error import *
from util import *

# Engine and other propulsion related stuff, like fixed jumpjets and gyros.

# The following tables contain the engine weight for each rating

stdengine = {
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
    400 : 52.5
}

lgtengine = {
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
    400 : 39.5
}

xlengine = {
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
    400 : 26.5
}

cmpengine = {
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
# Name, techbase, year, BV multiplier, weight
#
# Where techbase 0 = IS, 1 = Clan, 2 = Both, 10 = unknown
#
# Missing: ICE, Fuel Cell, Fission
engine = [["Fusion Engine", 2, 2021, 1.0, (lambda x : stdengine[x])],
          ["XL Engine", 0, 2579, 0.5, (lambda x : xlengine[x])],
          ["XL Engine", 1, 2579, 0.75, (lambda x : xlengine[x])],
          ["Light Fusion Engine", 0, 3062, 0.75, (lambda x : lgtengine[x])],
          ["Compact Fusion Engine", 0, 3068, 1.0, (lambda x : cmpengine[x])],
          # Assume same year as Mackie
          ["Primitive Fusion Engine", 2, 2439, 1.0,
           (lambda x : stdengine[ceil_5(x * 1.2)])]]

# Gyro types
#
# Name, techbase, year, BV multiplier, weight multiplier
#
# Where techbase 0 = IS, 1 = Clan, 2 = Both, 10 = unknown
#
gyro = [["Standard Gyro", 2, 2439, 0.5, 1.0],
        ["Extra-Light Gyro", 0, 3067, 0.5, 0.5],
        ["Heavy-Duty Gyro", 0, 3067, 1.0, 2.0],
        ["Compact Gyro", 0, 3068, 0.5, 1.5]]

# Jump-jet types
#
# Name, year
#
jumpjet = [["Standard Jump Jet", 2471],
           ["Improved Jump Jet", 3069]]

# Myomer enhancement types
#
# Name, techbase, year, weight
#
# Where techbase 0 = IS, 1 = Clan, 2 = Both, 10 = unknown
#
enhancement = [["---", 2, 0, (lambda x : 0)], #None
               ["MASC", 0, 2740, (lambda x : round(x * 0.05))],
               ["MASC", 1, 2740, (lambda x : round(x * 0.04))],
               ["TSM", 0, 3050, (lambda x : 0)]]

# Cockpit types
#
# Name, techbase, year, weight
#
cockpit = [["Standard Cockpit", 2300, 3],
           ["Small Cockpit", 3067, 2],
          # Assume same year as Mackie
           ["Primitive Cockpit", 2439, 5]]



# A class to hold cockpit info
class Cockpit:
    def __init__(self, ctype, console):
        self.type = ctype
        self.console = console
        self.c_weight = 0

        # Check for legal cockpit type, save data
        id = 0
        for i in cockpit:
            if (i[0] == self.type):
                id = 1
                self.year = i[1]
                self.wgt = i[2]
        if id == 0:
            error_exit((self.type))

        # Hack: Add console year
        if (self.console == "TRUE" and self.year < 2631):
            self.year == 2631

        # Hack: Add console weight
        if self.console == "TRUE":
            self.c_weight = 3

    # Return earliest year cockpit is available
    def get_year(self):
        return self.year

    # Return weight
    def get_weight(self):
        return self.wgt

    # Return console weight
    def get_c_weight(self):
        return self.c_weight

class JumpJets:
    def __init__(self, weight, jump, jjtype):
        self.weight = weight # Mech weight, not JJ weight
        self.jump = jump
        self.jjtype = jjtype

        # Check for legal jump-jet type, if jump-jets are mounted, save data
        if self.jump > 0:
            id = 0
            for i in jumpjet:
                if i[0] == self.jjtype:
                    id = 1
                    self.jjyear = i[1]
            if id == 0:
                error_exit(self.jjtype)

    # Return earliest year jumpjet is available
    def get_year(self):
        return self.jjyear

    def get_weight(self):
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


    # Return distance
    def get_jump(self):
        return self.jump



# A class to hold motive info for a mech
#
class Motive:
    def __init__(self, weight, etype, erating, ebase, gtype, gbase, enh, etb):
        self.etype = etype
        self.erating = erating
        self.eb = int(ebase)
        self.gtype = gtype
        self.gb = int(gbase)
        self.enhancement = enh
        self.etb = int(etb)
        self.speed = self.erating / weight
        # A note on primitive engines:
        # It seems like using engine rating directly does give
        # the right speed, even if rules says otherwise
        # This looks like an internal SSW issue, so
        # assume that the weight of these engines are incorrect

        # Check for legal engine type, save data
        id = 0
        for i in engine:
            if (i[0] == self.etype and i[1] == self.eb):
                id = 1
                self.eyear = i[2]
                self.eBV = i[3]
                self.eweight = i[4](self.erating)
        if id == 0:
            error_exit((self.etype, self.eb))

        # Check for legal gyro type, save data
        id = 0
        for i in gyro:
            if (i[0] == self.gtype and i[1] == self.gb):
                id = 1
                self.gyear = i[2]
                self.gBV = i[3]
                self.gweightm = i[4]
        if id == 0:
            error_exit((self.gtype, self.gb))

        # Check for legal enhancement type, save data
        id = 0
        for i in enhancement:
            if (i[0] == self.enhancement and i[1] == self.etb):
                id = 1
                self.enhyear = i[2]
                self.enhweight = i[3](weight)
        if id == 0:
            error_exit((self.enhancement, self.etb))



    # Return earliest year engine is available
    def get_engine_year(self):
        return self.eyear

    # Return earliest year gyro is available
    def get_gyro_year(self):
        return self.gyear

    # Return earliest year enhancement is available
    def get_enh_year(self):
        return self.enhyear

    def get_engine_weight(self):
        return self.eweight

    def get_gyro_weight(self):
        rating = self.erating
        # Hack: Make sure Primitive Engines get right gyro weight
        if self.etype == "Primitive Fusion Engine":
            rating *= 1.2
            rating = ceil_5(rating)
        base_weight = ceil(float(rating) / 100.0)
        return self.gweightm * base_weight

    def get_enh_weight(self):
        return self.enhweight

    def get_engine_BVmod(self):
        return self.eBV

    def get_gyro_BVmod(self):
        return self.gBV

# TODO:
# - TO stuff: XXL, and Large engines
# - Add get jump heat function
