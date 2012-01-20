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
Contains classes for standard weapons.
"""

from util import calc_average

def hgr_damage(range):
    """
    Calculates Heavy Gauss Rifle damage.
    """
    if range <= 6:
        return 25
    elif range <= 13:
        return 20
    else:
        return 10

def sn_damage(range):
    """
    Calculates Snub-Nose PPC damage.
    """
    if range <= 9:
        return 10
    elif range <= 13:
        return 8
    else:
        return 5

def mml3_damage(range, art):
    """
    Calculates MML3 damage.
    We assumes a switch from LRM to SRM at range 6.
    """
    if range <= 6:
        return 2 * calc_average(3, art)
    else:
        return calc_average(3, art)

def mml5_damage(range, art):
    """
    Calculates MML5 damage.
    We assumes a switch from LRM to SRM at range 6.
    """
    if range <= 6:
        return 2 * calc_average(5, art)
    else:
        return calc_average(5, art)

def mml7_damage(range, art):
    """
    Calculates MML7 damage.
    We assumes a switch from LRM to SRM at range 6.
    """
    if range <= 6:
        return 2 * calc_average(7, art)
    else:
        return calc_average(7, art)

def mml9_damage(range, art):
    """
    Calculates MML9 damage.
    We assumes a switch from LRM to SRM at range 6.
    """
    if range <= 6:
        return 2 * calc_average(9, art)
    else:
        return calc_average(9, art)

def hag20_damage(range):
    """
    Calculates HAG20 damage.
    """
    if range <= 8:
        return calc_average(20, 2)
    elif range <= 16:
        return calc_average(20, 0)
    else:
        return calc_average(20, -2)


def hag30_damage(range):
    """
    Calculates HAG30 damage.
    """
    if range <= 8:
        return calc_average(30, 2)
    elif range <= 16:
        return calc_average(30, 0)
    else:
        return calc_average(30, -2)


def hag40_damage(range):
    """
    Calculates HAG40 damage.
    """
    if range <= 8:
        return calc_average(40, 2)
    elif range <= 16:
        return calc_average(40, 0)
    else:
        return calc_average(40, -2)

def atm3_damage(range):
    """
    Calculates ATM3 damage.
    We assumes a switch to HE at range 6, and normal at range 10.
    """
    if range <= 6:
        return 3 * calc_average(3, 2)
    elif range <= 10:
        return 2 * calc_average(3, 2)
    else:
        return calc_average(3, 2)


def atm6_damage(range):
    """
    Calculates ATM6 damage.
    We assumes a switch to HE at range 6, and normal at range 10.
    """
    if range <= 6:
        return 3 * calc_average(6, 2)
    elif range <= 10:
        return 2 * calc_average(6, 2)
    else:
        return calc_average(6, 2)


def atm9_damage(range):
    """
    Calculates ATM9 damage.
    We assumes a switch to HE at range 6, and normal at range 10.
    """
    if range <= 6:
        return 3 * calc_average(9, 2)
    elif range <= 10:
        return 2 * calc_average(9, 2)
    else:
        return calc_average(9, 2)


def atm12_damage(range):
    """
    Calculates ATM12 damage.
    We assumes a switch to HE at range 6, and normal at range 10.
    """
    if range <= 6:
        return 3 * calc_average(12, 2)
    elif range <= 10:
        return 2 * calc_average(12, 2)
    else:
        return calc_average(12, 2)

def svspl_damage(range):
    """
    Calculates Small VSPL damage.
    """
    if range <= 2:
        return 5
    elif range <= 4:
        return 4
    else:
        return 3

def mvspl_damage(range):
    """
    Calculates Medium VSPL damage.
    """
    if range <= 2:
        return 9
    elif range <= 5:
        return 7
    else:
        return 5

def lvspl_damage(range):
    """
    Calculates Large VSPL damage.
    """
    if range <= 4:
        return 11
    elif range <= 8:
        return 9
    else:
        return 7



# Weapons in the order of name, BV[main, ammo], rules level,
# heat (as used for BV calcs), damage as a function of range,
# range,  enhancement(A=artemis, T=tarcomp P=apollo),
# year, uses ammo rate?, weight, explosive slots
#
# Where rules level is:
#        0 = Intro-tech,
#        1 = Tournament legal,
#        2 = Advanced,
#        3 = Experimental,
#        4 = Primitive (special)
#
# To be loaded into the gear class
#
# TODO: IS: 2 MG, HMG, 2 HMG, 4 HMG, Flamer (Vehicle), One-shots
# TODO: Clan: 2 LMG, 4 LMG, 2 MG, 3 MG, 2 HMG, Flamer (Vehicle), One-shots
# TODO: New TL: Heavy Flamer, iHGR, Silver Bullet, VGL, NLRM10, NLRM15, NLRM20,
# Improved One-shot, Light Rifle, Medium Rifle, Heavy Rifle
# TODO: Advanced: Thumper, PMAC/2, PMAC/8, Fluid Gun, iHSL, iHLL, ERLPL,
# Mech Mortars, Imp OS, Artillery Cannons, HVACs, Chemical Lasers,
# SLRM-5, SLRM-15, SLRM-20, rest of PPC+cap
WEAPONS = {
    ### Inner Sphere, Tech Manual ###
    "(IS) Autocannon/2" : [[37, 5], 0,
                           1, (lambda x, y : 2),
                           "L", "T", 2300, 1, 6, 0],
    "(IS) Autocannon/5" : [[70, 9], 0,
                           1, (lambda x, y : 5),
                           "L", "T", 2250, 1, 8, 0],
    "(IS) Autocannon/10" : [[123, 15], 0,
                            3, (lambda x, y : 10),
                            "M", "T", 2460, 1, 12, 0],
    "(IS) Autocannon/20" : [[178, 22], 0,
                            7, (lambda x, y : 20),
                            "M", "T", 2500, 1, 14, 0],
    "(IS) LB 2-X AC" : [[42, 5], 1,
                        1, (lambda x, y : 2),
                        "L", "T", 3058, 1, 6, 0],
    "(IS) LB 5-X AC" : [[83, 10], 1,
                        1, (lambda x, y : 5),
                        "L", "T", 3058, 1, 8, 0],
    "(IS) LB 10-X AC" : [[148, 19], 1,
                         2, (lambda x, y : 10),
                         "L", "T", 2595, 1, 11, 0],
    "(IS) LB 20-X AC" : [[237, 30], 1,
                         6, (lambda x, y : 20),
                         "M", "T", 3058, 1, 14, 0],
    "(IS) Light AC/2" : [[30, 4], 1,
                         1, (lambda x, y : 2),
                         "L", "T", 3068, 1, 4, 0],
    "(IS) Light AC/5" : [[62, 8], 1,
                         1, (lambda x, y : 5),
                         "M", "T", 3068, 1, 5, 0],
    "(IS) Rotary AC/2" : [[118, 15], 1,
                          6, (lambda x, y : 2 * calc_average(6, 0)),
                          "L", "T", 3062, 6, 8, 0],
    "(IS) Rotary AC/5" : [[247, 31], 1,
                          6, (lambda x, y : 5 * calc_average(6, 0)),
                          "M", "T", 3062, 6, 10, 0],
    "(IS) Ultra AC/2" : [[56, 7], 1,
                         2, (lambda x, y : 2 * calc_average(2, 0)),
                         "L", "T", 3057, 2, 7, 0],
    "(IS) Ultra AC/5" : [[112, 14], 1,
                         2, (lambda x, y : 5 * calc_average(2, 0)),
                         "L", "T", 2640, 2, 9, 0],
    "(IS) Ultra AC/10" : [[210, 26], 1,
                          8, (lambda x, y : 10 * calc_average(2, 0)),
                          "L", "T", 3057, 2, 13, 0],
    "(IS) Ultra AC/20" : [[281, 35], 1,
                          16, (lambda x, y : 20 * calc_average(2, 0)),
                          "M", "T", 3060, 2, 15, 0],
    "(IS) Light Gauss Rifle" : [[159, 20], 1,
                                1, (lambda x, y : 8),
                                "L", "T", 3056, 1, 12, 5],
    "(IS) Gauss Rifle" : [[320, 40], 1,
                          1, (lambda x, y : 15),
                          "L", "T", 2590, 1, 15, 7],
    "(IS) Heavy Gauss Rifle" : [[346, 43], 1,
                                2, (lambda x, y : hgr_damage(x)),
                                "L", "T", 3061, 1, 18, 11],
    "(IS) Light Machine Gun" : [[5, 1], 1,
                                0, (lambda x, y : 1),
                                "M", "", 3068, 1, 0.5, 0],
    "(IS) MG Array (2 Light Machine Gun)" :
        [[16.7, 1], 1,
         0, (lambda x, y : 1 * calc_average(2, 0)),
         "M", "", 3068, 2, 1.5, 0],
    "(IS) MG Array (3 Light Machine Gun)" :
        [[25.05, 1], 1,
         0, (lambda x, y : 1 * calc_average(3, 0)),
         "M", "", 3068, 3, 2, 0],
    "(IS) MG Array (4 Light Machine Gun)" :
        [[33.4, 1], 1,
         0, (lambda x, y : 1 * calc_average(4, 0)),
         "M", "", 3068, 4, 2.5, 0],
    "(IS) Machine Gun" : [[5, 1], 0,
                          0, (lambda x, y : 2),
                          "S", "", 1900, 1, 0.5, 0],
    # MG 2
    "(IS) MG Array (3 Machine Gun)" :
        [[25.05, 1], 1,
         0, (lambda x, y : 2 * calc_average(3, 0)),
         "S", "", 3068, 3, 2, 0],
    "(IS) MG Array (4 Machine Gun)" :
        [[33.4, 1], 1,
         0, (lambda x, y : 2 * calc_average(4, 0)),
         "S", "", 3068, 4, 2.5, 0],
    # HMG
    # HMG 2
    "(IS) MG Array (3 Heavy Machine Gun)" :
        [[30.06, 1], 1,
         0, (lambda x, y : 3 * calc_average(3, 0)),
         "S", "", 3068, 3, 3.5, 0],
    # HMG 4
    "(IS) Flamer" : [[6, 0], 0,
                     3, (lambda x, y : 2),
                     "S", "", 2025, 0, 1, 0],
    # Flamer (Vehicle)
    "(IS) ER Small Laser" : [[17, 0], 1,
                             2, (lambda x, y : 3),
                             "M", "T", 3058, 0, 0.5, 0],
    "(IS) ER Medium Laser" : [[62, 0], 1,
                              5, (lambda x, y : 5),
                              "M", "T", 3058, 0, 1, 0],
    "(IS) ER Large Laser" : [[163, 0], 1,
                             12, (lambda x, y : 8),
                             "L", "T", 2620, 0, 5, 0],
    "(IS) Small Laser" : [[9, 0], 0,
                          1, (lambda x, y : 3),
                          "S", "T", 2300, 0, 0.5, 0],
    "(IS) Medium Laser" : [[46, 0], 0,
                           3, (lambda x, y : 5),
                           "M", "T", 2300, 0, 1, 0],
    "(IS) Large Laser" : [[123, 0], 0,
                          8, (lambda x, y : 8),
                          "M", "T", 2316, 0, 5, 0],
    "(IS) Small Pulse Laser" : [[12, 0], 1,
                                2, (lambda x, y : 3),
                                "S", "T", 2609, 0, 1, 0],
    "(IS) Medium Pulse Laser" : [[48, 0], 1,
                                 4, (lambda x, y : 6),
                                 "M", "T", 2609, 0, 2, 0],
    "(IS) Large Pulse Laser" : [[119, 0], 1,
                                10, (lambda x, y : 9),
                                "M", "T", 2609, 0, 7, 0],
    "(IS) Plasma Rifle" : [[210, 26], 1,
                           10, (lambda x, y : 10),
                           "M", "T", 3068, 1, 6, 0],
    "(IS) Light PPC" : [[88, 0], 1,
                        5, (lambda x, y : 5),
                        "L", "T", 3067, 0, 3, 0],
    "(IS) PPC" : [[176, 0], 0,
                  10, (lambda x, y : 10),
                  "L", "T", 2460, 0, 7, 0],
    "(IS) Heavy PPC" : [[317, 0], 1,
                        15, (lambda x, y : 15),
                        "L", "T", 3067, 0, 10, 0],
    "(IS) ER PPC" : [[229, 0], 1,
                     15, (lambda x, y : 10),
                     "L", "T", 2760, 0, 7, 0],
    "(IS) Snub-Nose PPC" : [[165, 0], 1,
                            10, (lambda x, y : sn_damage(x)),
                            "M", "T", 3067, 0, 6, 0],
    "(IS) LRM-5" : [[45, 6], 0,
                    2, (lambda x, y : calc_average(5, y)),
                    "L", "A", 2300, 1, 2, 0],
    "(IS) LRM-10" : [[90, 11], 0,
                     4, (lambda x, y : calc_average(10, y)),
                     "L", "A", 2305, 1, 5, 0],
    "(IS) LRM-15" : [[136, 17], 0,
                     5, (lambda x, y : calc_average(15, y)),
                     "L", "A", 2315, 1, 7, 0],
    "(IS) LRM-20" : [[181, 23], 0,
                     6, (lambda x, y : calc_average(20, y)),
                     "L", "A", 2322, 1, 10, 0],
    "(IS) MML-3" : [[29, 4], 1,
                    2, (lambda x, y : mml3_damage(x, y)),
                    "L", "A", 3068, 1, 1.5, 0],
    "(IS) MML-5" : [[45, 6], 1,
                    3, (lambda x, y : mml5_damage(x, y)),
                    "L", "A", 3068, 1, 3, 0],
    "(IS) MML-7" : [[67, 8], 1,
                    4, (lambda x, y : mml7_damage(x, y)),
                    "L", "A", 3068, 1, 4.5, 0],
    "(IS) MML-9" : [[86, 11], 1,
                    5, (lambda x, y : mml9_damage(x, y)),
                    "L", "A", 3068, 1, 6, 0],
    "(IS) SRM-2" : [[21, 3], 0,
                    2, (lambda x, y : 2 * calc_average(2, y)),
                    "M", "A", 2370, 1, 1, 0],
    "(IS) SRM-4" : [[39, 5], 0,
                    3, (lambda x, y : 2 * calc_average(4, y)),
                    "M", "A", 2370, 1, 2, 0],
    "(IS) SRM-6" : [[59, 7], 0,
                    4, (lambda x, y : 2 * calc_average(6, y)),
                    "M", "A", 2370, 1, 3, 0],
    "(IS) SRM-4 (OS)" : [[8, 0], 1,
                         0.75, (lambda x, y : 0), #TODO: OS damage
                         "M", "A", 2676, 0, 2.5, 0],
    "(IS) MRM-10" : [[56, 7], 1,
                     4, (lambda x, y : calc_average(10, y)),
                     "M", "P", 3058, 1, 3, 0],
    "(IS) MRM-20" : [[112, 14], 1,
                     6, (lambda x, y : calc_average(20, y)),
                     "M", "P", 3058, 1, 7, 0],
    "(IS) MRM-30" : [[168, 21], 1,
                     10, (lambda x, y : calc_average(30, y)),
                     "M", "P", 3058, 1, 10, 0],
    "(IS) MRM-40" : [[224, 28], 1,
                     12, (lambda x, y : calc_average(40, y)),
                     "M", "P", 3058, 1, 12, 0],
    "(IS) Rocket Launcher 10" : [[18, 0], 1,
                                 0.75, (lambda x, y : 0), #TODO: OS damage
                                 "L", "", 3064, 0, 0.5, 0],
    "(IS) Rocket Launcher 15" : [[23, 0], 1,
                                 1, 0, (lambda x, y : 0), #TODO: OS damage
                                 "M", "", 3064, 0, 1, 0],
    "(IS) Rocket Launcher 20" : [[24, 0], 1,
                                 1.25, (lambda x, y : 0), #TODO: OS damage
                                 "M", "", 3064, 0, 1.5, 0],
    "(IS) Streak SRM-2" : [[30, 4], 1,
                           1, (lambda x, y : 4),
                           "M", "", 2647, 1, 1.5, 0],
    "(IS) Streak SRM-4" : [[59, 7], 1,
                           1.5, (lambda x, y : 8),
                           "M", "", 3058, 1, 3, 0],
    "(IS) Streak SRM-6" : [[89, 11], 1,
                           2, (lambda x, y : 12),
                           "M", "", 3058, 1, 4.5, 0],
    "(IS) Streak SRM-2 (OS)" : [[6, 0], 1,
                                0.5, (lambda x, y : 0), #TODO: OS damage
                                "M", "", 2676, 0, 2, 0],
    "(IS) Narc Missile Beacon" : [[30, 0], 1,
                                  0, (lambda x, y : 0),
                                  "M", "", 2587, 1, 3, 0],
    "(IS) iNarc Launcher" : [[75, 0], 1,
                             0, (lambda x, y : 0),
                             "M", "", 3062, 1, 5, 0],
    ### Clan, Tech Manual ###
    "(CL) LB 2-X AC" : [[47, 6], 1,
                        1, (lambda x, y : 2),
                        "L", "T", 2826, 1, 5, 0],
    "(CL) LB 5-X AC" : [[93, 12], 1,
                        1, (lambda x, y : 5),
                        "L", "T", 2825, 1, 7, 0],
    "(CL) LB 10-X AC" : [[148, 19], 1,
                         2, (lambda x, y : 10),
                         "L", "T", 2595, 1, 10, 0],
    "(CL) LB 20-X AC" : [[237, 30], 1,
                         6, (lambda x, y : 20),
                         "M", "T", 2826, 1, 12, 0],
    "(CL) Ultra AC/2" : [[62, 8], 1,
                         2, (lambda x, y : 2 * calc_average(2, 0)),
                         "L", "T", 2827, 2, 5, 0],
    "(CL) Ultra AC/5" : [[122, 15], 1,
                         2, (lambda x, y : 5 * calc_average(2, 0)),
                         "L", "T", 2640, 2, 7, 0],
    "(CL) Ultra AC/10" : [[210, 26], 1,
                          6, (lambda x, y : 10 * calc_average(2, 0)),
                          "L", "T", 2825, 2, 10, 0],
    "(CL) Ultra AC/20" : [[335, 42], 1,
                          14, (lambda x, y : 20 * calc_average(2, 0)),
                          "M", "T", 2825, 2, 12, 0],
    "(CL) AP Gauss Rifle" : [[21, 3], 1,
                             1, (lambda x, y : 3),
                             "M", "T", 3069, 1, 0.5, 1],
    "(CL) Gauss Rifle" : [[320, 40], 1,
                          1, (lambda x, y : 15),
                          "L", "T", 2590, 1, 12, 6],
    "(CL) Hyper Assault Gauss 20" : [[267, 33], 1,
                                     4, (lambda x, y : hag20_damage(x)),
                                     "L", "T", 3068, 1, 10, 6],
    "(CL) Hyper Assault Gauss 30" : [[401, 50], 1,
                                     6, (lambda x, y : hag30_damage(x)),
                                     "L", "T", 3068, 1, 13, 8],
    "(CL) Hyper Assault Gauss 40" : [[535, 67], 1,
                                     8, (lambda x, y : hag40_damage(x)),
                                     "L", "T", 3069, 1, 16, 10],
    "(CL) Light Machine Gun" : [[5, 1], 1,
                                0, (lambda x, y : 1),
                                "M", "", 3060, 1, 0.25, 0],
    # LMG 2
    "(CL) MG Array (3 Light Machine Gun)" :
        [[25.05, 1], 1,
         0, (lambda x, y : 1 * calc_average(3, 0)),
         "M", "", 3069, 3, 1, 0],
    # LMG 4
    "(CL) Machine Gun" : [[5, 1], 1,
                          0, (lambda x, y : 2),
                          "S", "", 1900, 1, 0.25, 0],
    # MG 2
    # MG 3
    "(CL) MG Array (4 Machine Gun)" :
        [[33.4, 1], 1,
         0, (lambda x, y : 2 * calc_average(4, 0)),
         "S", "", 3069, 4, 1.25, 0],
    "(CL) Heavy Machine Gun" : [[6, 1], 1,
                                0, (lambda x, y : 3),
                                "S", "", 3059, 1, 0.5, 0],
    # HMG 2
    "(CL) MG Array (3 Heavy Machine Gun)" :
        [[30.06, 1], 1,
         0, (lambda x, y : 3 * calc_average(3, 0)),
         "S", "", 3069, 3, 1.75, 0],
    "(CL) MG Array (4 Heavy Machine Gun)" :
        [[40.08, 1], 1,
         0, (lambda x, y : 3 * calc_average(4, 0)),
         "S", "", 3069, 4, 2.25, 0],
    "(CL) Flamer" : [[6, 0], 1,
                     3, (lambda x, y : 2),
                     "S", "", 2025, 0, 0.5, 0],
    # Flamer (Vehicle)
    "(CL) ER Micro Laser" : [[7, 0], 1,
                             1, (lambda x, y : 2),
                             "M", "T", 3060, 0, 0.25, 0],
    "(CL) ER Small Laser" : [[31, 0], 1,
                             2, (lambda x, y : 5),
                             "M", "T", 2825, 0, 0.5, 0],
    "(CL) ER Medium Laser" : [[108, 0], 1,
                              5, (lambda x, y : 7),
                              "M", "T", 2824, 0, 1, 0],
    "(CL) ER Large Laser" : [[248, 0], 1,
                             12, (lambda x, y : 10),
                             "L", "T", 2620, 0, 4, 0],
    "(CL) Micro Pulse Laser" : [[12, 0], 1,
                                1, (lambda x, y : 3),
                                "S", "T", 3060, 0, 0.5, 0],
    "(CL) Small Pulse Laser" : [[24, 0], 1,
                                2, (lambda x, y : 3),
                                "M", "T", 2609, 0, 1, 0],
    "(CL) Medium Pulse Laser" : [[111, 0], 1,
                                 4, (lambda x, y : 7),
                                 "M", "T", 2609, 0, 2, 0],
    "(CL) Large Pulse Laser" : [[265, 0], 1,
                                10, (lambda x, y : 10),
                                "L", "T", 2609, 0, 6, 0],
    "(CL) Heavy Small Laser" : [[15, 0], 1,
                                3, (lambda x, y : 6),
                                "S", "T", 3059, 0, 0.5, 0],
    "(CL) Heavy Medium Laser" : [[76, 0], 1,
                                 7, (lambda x, y : 10),
                                 "M", "T", 3059, 0, 1, 0],
    "(CL) Heavy Large Laser" : [[244, 0], 1,
                                18, (lambda x, y : 16),
                                "M", "T", 3059, 0, 4, 0],
    "(CL) Plasma Cannon" : [[170, 21], 1,
                            7, (lambda x, y : 0),
                            "L", "T", 3069, 1, 3, 0],
    "(CL) ER PPC" : [[412, 0], 1,
                     15, (lambda x, y : 15),
                     "L", "T", 2760, 0, 6, 0],
    "(CL) ATM-3" : [[53, 14], 1,
                    2, (lambda x, y : atm3_damage(x)),
                    "M", "", 3054, 1, 1.5, 0],
    "(CL) ATM-6" : [[105, 26], 1,
                    4, (lambda x, y : atm6_damage(x)),
                    "M", "", 3054, 1, 3.5, 0],
    "(CL) ATM-9" : [[147, 36], 1,
                    6, (lambda x, y : atm9_damage(x)),
                    "M", "", 3054, 1, 5, 0],
    "(CL) ATM-12" : [[212, 52], 1,
                     8, (lambda x, y : atm12_damage(x)),
                     "M", "", 3055, 1, 7, 0],
    "(CL) LRM-5" : [[55, 7], 1,
                    2, (lambda x, y : calc_average(5, y)),
                    "L", "A", 2400, 1, 1, 0],
    "(CL) LRM-10" : [[109, 14], 1,
                     4, (lambda x, y : calc_average(10, y)),
                     "L", "A", 2400, 1, 2.5, 0],
    "(CL) LRM-15" : [[164, 21], 1,
                     5, (lambda x, y : calc_average(15, y)),
                     "L", "A", 2400, 1, 3.5, 0],
    "(CL) LRM-20" : [[220, 27], 1,
                     6, (lambda x, y : calc_average(20, y)),
                     "L", "A", 2400, 1, 5, 0],
    "(CL) SRM-2" : [[21, 3], 1,
                    2, (lambda x, y : 2 * calc_average(2, y)),
                    "M", "A", 2370, 1, 0.5, 0],
    "(CL) SRM-4" : [[39, 5], 1,
                    3, (lambda x, y : 2 * calc_average(4, y)),
                    "M", "A", 2370, 1, 1, 0],
    "(CL) SRM-6" : [[59, 7], 1,
                    4, (lambda x, y : 2 * calc_average(6, y)),
                    "M", "A", 2370, 1, 1.5, 0],
    "(CL) Streak SRM-2" : [[40, 5], 1,
                           1, (lambda x, y : 4),
                           "M", "", 2647, 1, 1, 0],
    "(CL) Streak SRM-4" : [[79, 10], 1,
                           1.5, (lambda x, y : 8),
                           "M", "", 2826, 1, 2, 0],
    "(CL) Streak SRM-6" : [[118, 15], 1,
                           2, (lambda x, y : 12),
                           "M", "", 2826, 1, 3, 0],
    "(CL) Streak SRM-4 (OS)" : [[16, 0], 1,
                                0.75, (lambda x, y : 0), #TODO: OS damage
                                "M", "", 2826, 0, 2.5, 0],
    "(CL) Narc Missile Beacon" : [[30, 0], 1,
                                  0, (lambda x, y : 0),
                                  "M", "", 2587, 1, 2, 0],
    ### New Tournament Legal ###
    "ER Flamer" : [[16, 0], 1,
                   4, (lambda x, y : 2),
                   "M", "", 3067, 0, 1, 0],
    # Heavy Flamer
    # iHGR
    "(IS) Magshot Gauss Rifle" : [[15, 2], 1,
                                  1, (lambda x, y : 2),
                                  "M", "T", 3072, 1, 0.5, 2],
    # Silver Bullet
    # VGL
    "(IS) Binary Laser Cannon" : [[222, 0], 1,
                                  16, (lambda x, y : 12),
                                  "M", "T", 2812, 0, 9, 0],
    "(IS) Enhanced LRM-5" : [[52, 7], 1,
                             2, (lambda x, y : calc_average(5, y)),
                             "L", "A", 3058, 1, 3, 0],
    # NLRM-10
    # NLRM-15
    # NLRM-20
    # Imp OS
    # Light Rifle
    # Medium Rifle
    # Heavy Rifle
    "(IS) Thunderbolt-5" : [[64, 8], 1,
                            3, (lambda x, y : 5),
                            "L", "", 3072, 1, 3, 0],
    "(IS) Thunderbolt-10" : [[127, 16], 1,
                             5, (lambda x, y : 10),
                             "L", "", 3072, 1, 7, 0],
    "(IS) Thunderbolt-15" : [[229, 29], 1,
                             7, (lambda x, y : 15),
                             "L", "", 3072, 1, 11, 0],
    "(IS) Thunderbolt-20" : [[305, 38], 1,
                             8, (lambda x, y : 20),
                             "L", "", 3072, 1, 15, 0],

    ### Advanced Weapons ###
    "(IS) Arrow IV Missile" : [[240, 30], 2,
                               10, (lambda x, y : 20),
                               "L", "", 2600, 1, 15, 0],
    "(CL) Arrow IV Missile" : [[240, 30], 2,
                               10, (lambda x, y : 20),
                               "L", "", 2600, 1, 12, 0],
    # Thumper
    "(IS) Sniper" : [[85, 11], 2,
                     10, (lambda x, y : 20),
                     "L", "", 1900, 1, 20, 0],
    # Artillery Cannons
    # HVACs
    # Protomech AC/2
    "(CL) Protomech AC/4" : [[49, 6], 2,
                             1, (lambda x, y : 4),
                             "M", "T", 3073, 1, 4.5, 0],
    # Protomech AC/8
    # Fluid Gun
    "(IS) Bombast Laser" : [[137, 0], 2,
                            12, (lambda x, y : 12),
                            "M", "T", 3064, 0, 7, 0],
    # Chemical Lasers
    "(CL) ER Small Pulse Laser" : [[36, 0], 2,
                                   3, (lambda x, y : 5),
                                   "M", "T", 3057, 0, 1.5, 0],
    "(CL) ER Medium Pulse Laser" : [[117, 0], 2,
                                    6, (lambda x, y : 7),
                                    "M", "T", 3057, 0, 2, 0],
    # ERLPL
    # iHSL
    "(CL) Improved Heavy Medium Laser" : [[93, 0], 2,
                                          7, (lambda x, y : 10),
                                          "M", "T", 3069, 0, 1, 2],
    # iHLL
    "(IS) Small Variable Speed Pulse Laser" :
        [[22, 0], 2,
         3, (lambda x, y : svspl_damage(x)),
         "M", "T", 3070, 0, 2, 0],
    "(IS) Medium Variable Speed Pulse Laser" :
        [[56, 0], 2,
         7, (lambda x, y : mvspl_damage(x)),
         "M", "T", 3070, 0, 4, 0],
    "(IS) Large Variable Speed Pulse Laser" :
        [[123, 0], 2,
         10, (lambda x, y : lvspl_damage(x)),
         "M", "T", 3070, 0, 9, 0],
    "(IS) Small X-Pulse Laser" : [[21, 0], 2,
                                  3, (lambda x, y : 3),
                                  "M", "T", 3057, 0, 1, 0],
    "(IS) Medium X-Pulse Laser" : [[71, 0], 2,
                                   6, (lambda x, y : 6),
                                   "M", "T", 3057, 0, 2, 0],
    "(IS) Large X-Pulse Laser" : [[178, 0], 2,
                                  14, (lambda x, y : 9),
                                  "M", "T", 3057, 0, 7, 0],
    # MM1
    # MM2
    # MM4
    # MM8-IS
    "(CL) Mech Mortar 8" : [[50, 6], 2,
                            10, (lambda x, y : 2 * calc_average(8, 0)),
                            "L", "", 2840, 1, 5, 0],
    # ERLMs
    # SLRM5
    "(CL) Streak LRM-10" : [[173, 22], 2,
                            2, (lambda x, y : 10),
                            "L", "", 3057, 1, 5, 0],
    # SLRM15
    # SLRM20
    "(IS) Light PPC + PPC Capacitor" : [[132, 0], 2,
                                        10, (lambda x, y : 10),
                                        "L", "T", 3067, 0, 4, 3],
    "(IS) Snub-Nose PPC + PPC Capacitor" :
        [[252, 0], 2,
         15, (lambda x, y : sn_damage(x) + 5),
         "M", "T", 3067, 0, 7, 3],
    # rest of +PPC cap
    "(IS) BattleMech Taser" : [[40, 5], 2,
                               6, (lambda x, y : 1),
                               "M", "", 3067, 1, 4, 3],

    ### Experimental Weapons ###
    "(CL) Rotary AC/2" : [[161, 20], 3,
                          6, (lambda x, y : 2 * calc_average(6, 0)),
                          "L", "T", 3073, 6, 8, 0],
    "(CL) Rotary AC/5" : [[345, 43], 3,
                          6, (lambda x, y : 5 * calc_average(6, 0)),
                          "L", "T", 3073, 6, 10, 0]
    }

# List of launcher names, shorthand and tubes
# Missing: NLRM-10, NLRM-15, NLRM-20
LAUNCHER_LIST = [["(IS) LRM-5", "i5:", 5],
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

class Weaponlist:
    """
    Store the list with weapons
    """
    def __init__(self, art4, art5, apollo):
        self.list = []
        for weap in WEAPONS.keys():
            self.list.append(Weapon(weap, art4, art5, apollo))

class Weapon:
    """
    An individual weapon type
    """
    def __init__(self, key, art4, art5, apollo):
        self.name = key
        self.batt_val = WEAPONS[key][0]
        self.range = WEAPONS[key][4]
        self.useammo = WEAPONS[key][7]
        self.explosive = WEAPONS[key][9]
        self.count = 0
        self.countrear = 0
        self.countarm = 0 # We count arm weapons also, to help with BV calcs
        self.ammocount = 0
        self.ammo_ton = 0

        # Deal with enhancements, Artemis
        self.enhance = ""
        if (WEAPONS[key][5] == "A"):
            if art5 == "TRUE":
                self.enhance = "A5"
            elif art4 == "TRUE":
                self.enhance = "A4"
        # Apollo
        elif (WEAPONS[key][5] == "P" and apollo == "TRUE"):
            self.enhance = "AP"
        # Tarcomp, we can not know if one is present right now
        elif (WEAPONS[key][5] == "T"):
            self.enhance = "TC"

    def get_weight(self):
        """
        Return weight
        """
        wgt = WEAPONS[self.name][8]
        if self.enhance == "A5":
            wgt += 1.5
        elif self.enhance == "A4":
            wgt += 1
        elif self.enhance == "AP":
            wgt += 1
        return wgt

    def get_heat(self):
        """
        Return heat
        """
        return WEAPONS[self.name][2]

    def get_damage(self, range):
        """
        Return damage
        """
        art = 0
        if self.enhance == "A5":
            art = 3
        elif self.enhance == "A4":
            art = 2
        elif self.enhance == "AP":
            art = -1
        return WEAPONS[self.name][3](range, art)

    def addone(self):
        """
        Add a normal-front facing weapon
        """
        self.count = self.count + 1

    def addone_rear(self):
        """
        Add a rear-facing weapon
        """
        self.countrear = self.countrear + 1

    def addone_arm(self):
        """
        Add a weapon to arms.
        Note that addone needs also to be called
        """
        self.countarm = self.countarm + 1

    # We need to track tonnage and rounds separately due to BV
    # calculations and how MML ammo works
    def add_ammo(self, count, amount):
        """
        Add ammo for the weapon
        """
        self.ammocount = self.ammocount + amount
        self.ammo_ton += count

    def get_bv(self, tarcomp):
        """
        Get the BV of an INDIVIDUAL weapon, not all of them
        """
        batt_val = self.batt_val[0]
        if (tarcomp > 0 and self.enhance == "TC"):
            batt_val *= 1.25
        if (self.enhance == "A4"):
            batt_val *= 1.2
        elif (self.enhance == "A5"):
            batt_val *= 1.3
        if (self.enhance == "AP"):
            batt_val *= 1.15
        return batt_val


    def get_ammo_bv(self):
        """
        Get the BV of the total ammo
        """
        bv_ammo = 0
        # Here we use BV of the unmodified weapons, of both facing
        bv_weapons = self.batt_val[0] * (self.count + self.countrear)
        # Handle ammo
        if (self.batt_val[1] > 0 and self.ammocount > 0):
            bv_ammo = self.batt_val[1] * self.ammo_ton
            # Disallow ammo BV to be greater than that of
            # the weapon itself
            if bv_ammo > bv_weapons:
                bv_ammo = bv_weapons

        return bv_ammo

    def get_ammo_per_weapon(self):
        """
        Get amount of ammo for each forward-facing weapon
        """
        if self.count > 0:
            return int(float(self.ammocount) / float(self.count))
        # For no weapons, ammo matters not
        else:
            return 0



