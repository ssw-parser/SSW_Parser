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

def hgr_damage(rnge):
    """
    Calculates Heavy Gauss Rifle damage.
    """
    if rnge <= 6:
        return 25
    elif rnge <= 13:
        return 20
    else:
        return 10

def sn_damage(rnge):
    """
    Calculates Snub-Nose PPC damage.
    """
    if rnge <= 9:
        return 10
    elif rnge <= 13:
        return 8
    else:
        return 5

def mml3_damage(rnge, art):
    """
    Calculates MML3 damage.
    We assumes a switch from LRM to SRM at range 6.
    """
    if rnge <= 6:
        return 2 * calc_average(3, art)
    else:
        return calc_average(3, art)

def mml5_damage(rnge, art):
    """
    Calculates MML5 damage.
    We assumes a switch from LRM to SRM at range 6.
    """
    if rnge <= 6:
        return 2 * calc_average(5, art)
    else:
        return calc_average(5, art)

def mml7_damage(rnge, art):
    """
    Calculates MML7 damage.
    We assumes a switch from LRM to SRM at range 6.
    """
    if rnge <= 6:
        return 2 * calc_average(7, art)
    else:
        return calc_average(7, art)

def mml9_damage(rnge, art):
    """
    Calculates MML9 damage.
    We assumes a switch from LRM to SRM at range 6.
    """
    if rnge <= 6:
        return 2 * calc_average(9, art)
    else:
        return calc_average(9, art)

def hag20_damage(rnge):
    """
    Calculates HAG20 damage.
    """
    if rnge <= 8:
        return calc_average(20, 2)
    elif rnge <= 16:
        return calc_average(20, 0)
    else:
        return calc_average(20, -2)


def hag30_damage(rnge):
    """
    Calculates HAG30 damage.
    """
    if rnge <= 8:
        return calc_average(30, 2)
    elif rnge <= 16:
        return calc_average(30, 0)
    else:
        return calc_average(30, -2)


def hag40_damage(rnge):
    """
    Calculates HAG40 damage.
    """
    if rnge <= 8:
        return calc_average(40, 2)
    elif rnge <= 16:
        return calc_average(40, 0)
    else:
        return calc_average(40, -2)

def atm3_damage(rnge):
    """
    Calculates ATM3 damage.
    We assumes a switch to HE at range 6, and normal at range 10.
    """
    if rnge <= 6:
        return 3 * calc_average(3, 2)
    elif rnge <= 10:
        return 2 * calc_average(3, 2)
    else:
        return calc_average(3, 2)


def atm6_damage(rnge):
    """
    Calculates ATM6 damage.
    We assumes a switch to HE at range 6, and normal at range 10.
    """
    if rnge <= 6:
        return 3 * calc_average(6, 2)
    elif rnge <= 10:
        return 2 * calc_average(6, 2)
    else:
        return calc_average(6, 2)


def atm9_damage(rnge):
    """
    Calculates ATM9 damage.
    We assumes a switch to HE at range 6, and normal at range 10.
    """
    if rnge <= 6:
        return 3 * calc_average(9, 2)
    elif rnge <= 10:
        return 2 * calc_average(9, 2)
    else:
        return calc_average(9, 2)


def atm12_damage(rnge):
    """
    Calculates ATM12 damage.
    We assumes a switch to HE at range 6, and normal at range 10.
    """
    if rnge <= 6:
        return 3 * calc_average(12, 2)
    elif rnge <= 10:
        return 2 * calc_average(12, 2)
    else:
        return calc_average(12, 2)

def svspl_damage(rnge):
    """
    Calculates Small VSPL damage.
    """
    if rnge <= 2:
        return 5
    elif rnge <= 4:
        return 4
    else:
        return 3

def mvspl_damage(rnge):
    """
    Calculates Medium VSPL damage.
    """
    if rnge <= 2:
        return 9
    elif rnge <= 5:
        return 7
    else:
        return 5

def lvspl_damage(rnge):
    """
    Calculates Large VSPL damage.
    """
    if rnge <= 4:
        return 11
    elif rnge <= 8:
        return 9
    else:
        return 7



# Weapons in the order of name, shorthand, BV[main, ammo], rules level,
# heat (as used for BV calcs), damage as a function of range, max range,
# enhancement(A=artemis, T=tarcomp P=apollo),
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
    "(IS) Autocannon/2" : ["AC2", [37, 5], 0,
                           1, (lambda x, y : 2), 24,
                           "T", 2300, 1, 6, 0],
    "(IS) Autocannon/5" : ["AC5", [70, 9], 0,
                           1, (lambda x, y : 5), 18,
                           "T", 2250, 1, 8, 0],
    "(IS) Autocannon/10" : ["AC10", [123, 15], 0,
                            3, (lambda x, y : 10), 15,
                            "T", 2460, 1, 12, 0],
    "(IS) Autocannon/20" : ["AC20", [178, 22], 0,
                            7, (lambda x, y : 20), 9,
                            "T", 2500, 1, 14, 0],
    "(IS) LB 2-X AC" : ["LB2", [42, 5], 1,
                        1, (lambda x, y : 2), 27,
                        "T", 3058, 1, 6, 0],
    "(IS) LB 5-X AC" : ["LB5", [83, 10], 1,
                        1, (lambda x, y : 5), 21,
                        "T", 3058, 1, 8, 0],
    "(IS) LB 10-X AC" : ["LB10", [148, 19], 1,
                         2, (lambda x, y : 10), 18,
                         "T", 2595, 1, 11, 0],
    "(IS) LB 20-X AC" : ["LB20", [237, 30], 1,
                         6, (lambda x, y : 20), 12,
                         "T", 3058, 1, 14, 0],
    "(IS) Light AC/2" : ["LAC2", [30, 4], 1,
                         1, (lambda x, y : 2), 18,
                         "T", 3068, 1, 4, 0],
    "(IS) Light AC/5" : ["LAC5", [62, 8], 1,
                         1, (lambda x, y : 5), 15,
                         "T", 3068, 1, 5, 0],
    "(IS) Rotary AC/2" : ["RAC2", [118, 15], 1,
                          6, (lambda x, y : 2 * calc_average(6, 0)), 18,
                          "T", 3062, 6, 8, 0],
    "(IS) Rotary AC/5" : ["RAC5", [247, 31], 1,
                          6, (lambda x, y : 5 * calc_average(6, 0)), 15,
                          "T", 3062, 6, 10, 0],
    "(IS) Ultra AC/2" : ["UAC2", [56, 7], 1,
                         2, (lambda x, y : 2 * calc_average(2, 0)), 25,
                         "T", 3057, 2, 7, 0],
    "(IS) Ultra AC/5" : ["UAC5", [112, 14], 1,
                         2, (lambda x, y : 5 * calc_average(2, 0)), 20,
                         "T", 2640, 2, 9, 0],
    "(IS) Ultra AC/10" : ["UAC10", [210, 26], 1,
                          8, (lambda x, y : 10 * calc_average(2, 0)), 18,
                          "T", 3057, 2, 13, 0],
    "(IS) Ultra AC/20" : ["UAC20", [281, 35], 1,
                          16, (lambda x, y : 20 * calc_average(2, 0)), 10,
                          "T", 3060, 2, 15, 0],
    "(IS) Light Gauss Rifle" : ["LGR", [159, 20], 1,
                                1, (lambda x, y : 8), 25,
                                "T", 3056, 1, 12, 5],
    "(IS) Gauss Rifle" : ["GR", [320, 40], 1,
                          1, (lambda x, y : 15), 22,
                          "T", 2590, 1, 15, 7],
    "(IS) Heavy Gauss Rifle" : ["HGR", [346, 43], 1,
                                2, (lambda x, y : hgr_damage(x)), 20,
                                "T", 3061, 1, 18, 11],
    "(IS) Light Machine Gun" : ["LMG", [5, 1], 1,
                                0, (lambda x, y : 1), 6,
                                "", 3068, 1, 0.5, 0],
    "(IS) MG Array (2 Light Machine Gun)" :
        ["LMG2A", [16.7, 1], 1,
         0, (lambda x, y : 1 * calc_average(2, 0)), 6,
         "", 3068, 2, 1.5, 0],
    "(IS) MG Array (3 Light Machine Gun)" :
        ["LMG3A", [25.05, 1], 1,
         0, (lambda x, y : 1 * calc_average(3, 0)), 6,
         "", 3068, 3, 2, 0],
    "(IS) MG Array (4 Light Machine Gun)" :
        ["LMG4A", [33.4, 1], 1,
         0, (lambda x, y : 1 * calc_average(4, 0)), 6,
         "", 3068, 4, 2.5, 0],
    "(IS) Machine Gun" : ["MG", [5, 1], 0,
                          0, (lambda x, y : 2), 3,
                          "", 1900, 1, 0.5, 0],
    # MG 2
    "(IS) MG Array (3 Machine Gun)" :
        ["MG3A", [25.05, 1], 1,
         0, (lambda x, y : 2 * calc_average(3, 0)), 3,
         "", 3068, 3, 2, 0],
    "(IS) MG Array (4 Machine Gun)" :
        ["MG4A", [33.4, 1], 1,
         0, (lambda x, y : 2 * calc_average(4, 0)), 3,
         "", 3068, 4, 2.5, 0],
    # HMG
    # HMG 2
    "(IS) MG Array (3 Heavy Machine Gun)" :
        ["HMG3A", [30.06, 1], 1,
         0, (lambda x, y : 3 * calc_average(3, 0)), 2,
         "", 3068, 3, 3.5, 0],
    # HMG 4
    "(IS) Flamer" : ["Flmr", [6, 0], 0,
                     3, (lambda x, y : 2), 3,
                     "", 2025, 0, 1, 0],
    # Flamer (Vehicle)
    "(IS) ER Small Laser" : ["ERSL", [17, 0], 1,
                             2, (lambda x, y : 3), 5,
                             "T", 3058, 0, 0.5, 0],
    "(IS) ER Medium Laser" : ["ERML", [62, 0], 1,
                              5, (lambda x, y : 5), 12,
                              "T", 3058, 0, 1, 0],
    "(IS) ER Large Laser" : ["ERLL", [163, 0], 1,
                             12, (lambda x, y : 8), 19,
                             "T", 2620, 0, 5, 0],
    "(IS) Small Laser" : ["SL", [9, 0], 0,
                          1, (lambda x, y : 3), 3,
                          "T", 2300, 0, 0.5, 0],
    "(IS) Medium Laser" : ["ML", [46, 0], 0,
                           3, (lambda x, y : 5), 9,
                           "T", 2300, 0, 1, 0],
    "(IS) Large Laser" : ["LL", [123, 0], 0,
                          8, (lambda x, y : 8), 15,
                          "T", 2316, 0, 5, 0],
    "(IS) Small Pulse Laser" : ["SPL", [12, 0], 1,
                                2, (lambda x, y : 3), 3,
                                "T", 2609, 0, 1, 0],
    "(IS) Medium Pulse Laser" : ["MPL", [48, 0], 1,
                                 4, (lambda x, y : 6), 6,
                                 "T", 2609, 0, 2, 0],
    "(IS) Large Pulse Laser" : ["LPL", [119, 0], 1,
                                10, (lambda x, y : 9), 10,
                                "T", 2609, 0, 7, 0],
    "(IS) Plasma Rifle" : ["PR", [210, 26], 1,
                           10, (lambda x, y : 10), 15,
                           "T", 3068, 1, 6, 0],
    "(IS) Light PPC" : ["LPPC", [88, 0], 1,
                        5, (lambda x, y : 5), 18,
                        "T", 3067, 0, 3, 0],
    "(IS) PPC" : ["PPC", [176, 0], 0,
                  10, (lambda x, y : 10), 18,
                  "T", 2460, 0, 7, 0],
    "(IS) Heavy PPC" : ["HPPC", [317, 0], 1,
                        15, (lambda x, y : 15), 18,
                        "T", 3067, 0, 10, 0],
    "(IS) ER PPC" : ["ERPPC", [229, 0], 1,
                     15, (lambda x, y : 10), 23,
                     "T", 2760, 0, 7, 0],
    "(IS) Snub-Nose PPC" : ["SNPPC", [165, 0], 1,
                            10, (lambda x, y : sn_damage(x)), 15,
                            "T", 3067, 0, 6, 0],
    "(IS) LRM-5" : ["LRM5", [45, 6], 0,
                    2, (lambda x, y : calc_average(5, y)), 21,
                    "A", 2300, 1, 2, 0],
    "(IS) LRM-10" : ["LRM10", [90, 11], 0,
                     4, (lambda x, y : calc_average(10, y)), 21,
                     "A", 2305, 1, 5, 0],
    "(IS) LRM-15" : ["LRM15", [136, 17], 0,
                     5, (lambda x, y : calc_average(15, y)), 21,
                     "A", 2315, 1, 7, 0],
    "(IS) LRM-20" : ["LRM20", [181, 23], 0,
                     6, (lambda x, y : calc_average(20, y)), 21,
                     "A", 2322, 1, 10, 0],
    "(IS) MML-3" : ["MML3", [29, 4], 1,
                    2, (lambda x, y : mml3_damage(x, y)), 21,
                    "A", 3068, 1, 1.5, 0],
    "(IS) MML-5" : ["MML5", [45, 6], 1,
                    3, (lambda x, y : mml5_damage(x, y)), 21,
                    "A", 3068, 1, 3, 0],
    "(IS) MML-7" : ["MML7", [67, 8], 1,
                    4, (lambda x, y : mml7_damage(x, y)), 21,
                    "A", 3068, 1, 4.5, 0],
    "(IS) MML-9" : ["MML9", [86, 11], 1,
                    5, (lambda x, y : mml9_damage(x, y)), 21,
                    "A", 3068, 1, 6, 0],
    "(IS) SRM-2" : ["SRM2", [21, 3], 0,
                    2, (lambda x, y : 2 * calc_average(2, y)), 9,
                    "A", 2370, 1, 1, 0],
    "(IS) SRM-4" : ["SRM4", [39, 5], 0,
                    3, (lambda x, y : 2 * calc_average(4, y)), 9,
                    "A", 2370, 1, 2, 0],
    "(IS) SRM-6" : ["SRM6", [59, 7], 0,
                    4, (lambda x, y : 2 * calc_average(6, y)), 9,
                    "A", 2370, 1, 3, 0],
    "(IS) SRM-4 (OS)" : ["SRM4OS", [8, 0], 1,
                         0.75, (lambda x, y : 0), 9, #TODO: OS damage
                         "A", 2676, 0, 2.5, 0],
    "(IS) MRM-10" : ["MRM10", [56, 7], 1,
                     4, (lambda x, y : calc_average(10, y)), 15,
                     "P", 3058, 1, 3, 0],
    "(IS) MRM-20" : ["MRM20", [112, 14], 1,
                     6, (lambda x, y : calc_average(20, y)), 15,
                     "P", 3058, 1, 7, 0],
    "(IS) MRM-30" : ["MRM30", [168, 21], 1,
                     10, (lambda x, y : calc_average(30, y)), 15,
                     "P", 3058, 1, 10, 0],
    "(IS) MRM-40" : ["MRM40", [224, 28], 1,
                     12, (lambda x, y : calc_average(40, y)), 15,
                     "P", 3058, 1, 12, 0],
    "(IS) Rocket Launcher 10" : ["RL10", [18, 0], 1,
                                 0.75, (lambda x, y : 0), 18, #TODO: OS damage
                                 "", 3064, 0, 0.5, 0],
    "(IS) Rocket Launcher 15" : ["RL15", [23, 0], 1,
                                 1, 0, (lambda x, y : 0), 15, #TODO: OS damage
                                 "", 3064, 0, 1, 0],
    "(IS) Rocket Launcher 20" : ["RL20", [24, 0], 1,
                                 1.25, (lambda x, y : 0), 12, #TODO: OS damage
                                 "", 3064, 0, 1.5, 0],
    "(IS) Streak SRM-2" : ["SSRM2", [30, 4], 1,
                           1, (lambda x, y : 4), 9,
                           "", 2647, 1, 1.5, 0],
    "(IS) Streak SRM-4" : ["SSRM4", [59, 7], 1,
                           1.5, (lambda x, y : 8), 9,
                           "", 3058, 1, 3, 0],
    "(IS) Streak SRM-6" : ["SSRM6", [89, 11], 1,
                           2, (lambda x, y : 12), 9,
                           "", 3058, 1, 4.5, 0],
    "(IS) Streak SRM-2 (OS)" : ["SSRM2OS", [6, 0], 1,
                                0.5, (lambda x, y : 0), 9, #TODO: OS damage
                                "", 2676, 0, 2, 0],
    "(IS) Narc Missile Beacon" : ["Narc", [30, 0], 1,
                                  0, (lambda x, y : 0), 9,
                                  "", 2587, 1, 3, 0],
    "(IS) iNarc Launcher" : ["iNarc", [75, 0], 1,
                             0, (lambda x, y : 0), 15,
                             "", 3062, 1, 5, 0],
    ### Clan, Tech Manual ###
    "(CL) LB 2-X AC" : ["LB2", [47, 6], 1,
                        1, (lambda x, y : 2), 30,
                        "T", 2826, 1, 5, 0],
    "(CL) LB 5-X AC" : ["LB5", [93, 12], 1,
                        1, (lambda x, y : 5), 24,
                        "T", 2825, 1, 7, 0],
    "(CL) LB 10-X AC" : ["LB10", [148, 19], 1,
                         2, (lambda x, y : 10), 18,
                         "T", 2595, 1, 10, 0],
    "(CL) LB 20-X AC" : ["LB20", [237, 30], 1,
                         6, (lambda x, y : 20), 12,
                         "T", 2826, 1, 12, 0],
    "(CL) Ultra AC/2" : ["UAC2", [62, 8], 1,
                         2, (lambda x, y : 2 * calc_average(2, 0)), 27,
                         "T", 2827, 2, 5, 0],
    "(CL) Ultra AC/5" : ["UAC5", [122, 15], 1,
                         2, (lambda x, y : 5 * calc_average(2, 0)), 21,
                         "T", 2640, 2, 7, 0],
    "(CL) Ultra AC/10" : ["UAC10", [210, 26], 1,
                          6, (lambda x, y : 10 * calc_average(2, 0)), 18,
                          "T", 2825, 2, 10, 0],
    "(CL) Ultra AC/20" : ["UAC20", [335, 42], 1,
                          14, (lambda x, y : 20 * calc_average(2, 0)), 12,
                          "T", 2825, 2, 12, 0],
    "(CL) AP Gauss Rifle" : ["APGR", [21, 3], 1,
                             1, (lambda x, y : 3), 9,
                             "T", 3069, 1, 0.5, 1],
    "(CL) Gauss Rifle" : ["GR", [320, 40], 1,
                          1, (lambda x, y : 15), 22,
                          "T", 2590, 1, 12, 6],
    "(CL) Hyper Assault Gauss 20" : ["HAG20", [267, 33], 1,
                                     4, (lambda x, y : hag20_damage(x)), 24,
                                     "T", 3068, 1, 10, 6],
    "(CL) Hyper Assault Gauss 30" : ["HAG30", [401, 50], 1,
                                     6, (lambda x, y : hag30_damage(x)), 24,
                                     "T", 3068, 1, 13, 8],
    "(CL) Hyper Assault Gauss 40" : ["HAG40", [535, 67], 1,
                                     8, (lambda x, y : hag40_damage(x)), 24,
                                     "T", 3069, 1, 16, 10],
    "(CL) Light Machine Gun" : ["LMG", [5, 1], 1,
                                0, (lambda x, y : 1), 6,
                                "", 3060, 1, 0.25, 0],
    # LMG 2
    "(CL) MG Array (3 Light Machine Gun)" :
        ["LMG3A", [25.05, 1], 1,
         0, (lambda x, y : 1 * calc_average(3, 0)), 6,
         "", 3069, 3, 1, 0],
    # LMG 4
    "(CL) Machine Gun" : ["MG", [5, 1], 1,
                          0, (lambda x, y : 2), 3,
                          "", 1900, 1, 0.25, 0],
    # MG 2
    # MG 3
    "(CL) MG Array (4 Machine Gun)" :
        ["MG4A", [33.4, 1], 1,
         0, (lambda x, y : 2 * calc_average(4, 0)), 3,
         "", 3069, 4, 1.25, 0],
    "(CL) Heavy Machine Gun" : ["HMG", [6, 1], 1,
                                0, (lambda x, y : 3), 2,
                                "", 3059, 1, 0.5, 0],
    # HMG 2
    "(CL) MG Array (3 Heavy Machine Gun)" :
        ["HMG3A", [30.06, 1], 1,
         0, (lambda x, y : 3 * calc_average(3, 0)), 2,
         "", 3069, 3, 1.75, 0],
    "(CL) MG Array (4 Heavy Machine Gun)" :
        ["HMG4A", [40.08, 1], 1,
         0, (lambda x, y : 3 * calc_average(4, 0)), 2,
         "", 3069, 4, 2.25, 0],
    "(CL) Flamer" : ["Flmr", [6, 0], 1,
                     3, (lambda x, y : 2), 3,
                     "", 2025, 0, 0.5, 0],
    # Flamer (Vehicle)
    "(CL) ER Micro Laser" : ["ERMcL", [7, 0], 1,
                             1, (lambda x, y : 2), 4,
                             "T", 3060, 0, 0.25, 0],
    "(CL) ER Small Laser" : ["ERSL", [31, 0], 1,
                             2, (lambda x, y : 5), 6,
                             "T", 2825, 0, 0.5, 0],
    "(CL) ER Medium Laser" : ["ERML", [108, 0], 1,
                              5, (lambda x, y : 7), 15,
                              "T", 2824, 0, 1, 0],
    "(CL) ER Large Laser" : ["ERLL", [248, 0], 1,
                             12, (lambda x, y : 10), 25,
                             "T", 2620, 0, 4, 0],
    "(CL) Micro Pulse Laser" : ["McPL", [12, 0], 1,
                                1, (lambda x, y : 3), 3,
                                "T", 3060, 0, 0.5, 0],
    "(CL) Small Pulse Laser" : ["SPL", [24, 0], 1,
                                2, (lambda x, y : 3), 6,
                                "T", 2609, 0, 1, 0],
    "(CL) Medium Pulse Laser" : ["MPL", [111, 0], 1,
                                 4, (lambda x, y : 7), 12,
                                 "T", 2609, 0, 2, 0],
    "(CL) Large Pulse Laser" : ["LPL", [265, 0], 1,
                                10, (lambda x, y : 10), 20,
                                "T", 2609, 0, 6, 0],
    "(CL) Heavy Small Laser" : ["HSL", [15, 0], 1,
                                3, (lambda x, y : 6), 3,
                                "T", 3059, 0, 0.5, 0],
    "(CL) Heavy Medium Laser" : ["HML", [76, 0], 1,
                                 7, (lambda x, y : 10), 9,
                                 "T", 3059, 0, 1, 0],
    "(CL) Heavy Large Laser" : ["HLL", [244, 0], 1,
                                18, (lambda x, y : 16), 15,
                                "T", 3059, 0, 4, 0],
    "(CL) Plasma Cannon" : ["PC", [170, 21], 1,
                            7, (lambda x, y : 0), 18,
                            "T", 3069, 1, 3, 0],
    "(CL) ER PPC" : ["ERPPC", [412, 0], 1,
                     15, (lambda x, y : 15), 23,
                     "T", 2760, 0, 6, 0],
    "(CL) ATM-3" : ["ATM3", [53, 14], 1,
                    2, (lambda x, y : atm3_damage(x)), 27,
                    "", 3054, 1, 1.5, 0],
    "(CL) ATM-6" : ["ATM6", [105, 26], 1,
                    4, (lambda x, y : atm6_damage(x)), 27,
                    "", 3054, 1, 3.5, 0],
    "(CL) ATM-9" : ["ATM9", [147, 36], 1,
                    6, (lambda x, y : atm9_damage(x)), 27,
                    "", 3054, 1, 5, 0],
    "(CL) ATM-12" : ["ATM12", [212, 52], 1,
                     8, (lambda x, y : atm12_damage(x)), 27,
                     "", 3055, 1, 7, 0],
    "(CL) LRM-5" : ["LRM5", [55, 7], 1,
                    2, (lambda x, y : calc_average(5, y)), 21,
                    "A", 2400, 1, 1, 0],
    "(CL) LRM-10" : ["LRM10", [109, 14], 1,
                     4, (lambda x, y : calc_average(10, y)), 21,
                     "A", 2400, 1, 2.5, 0],
    "(CL) LRM-15" : ["LRM15", [164, 21], 1,
                     5, (lambda x, y : calc_average(15, y)), 21,
                     "A", 2400, 1, 3.5, 0],
    "(CL) LRM-20" : ["LRM20", [220, 27], 1,
                     6, (lambda x, y : calc_average(20, y)), 21,
                     "A", 2400, 1, 5, 0],
    "(CL) SRM-2" : ["SRM2", [21, 3], 1,
                    2, (lambda x, y : 2 * calc_average(2, y)), 9,
                    "A", 2370, 1, 0.5, 0],
    "(CL) SRM-4" : ["SRM4", [39, 5], 1,
                    3, (lambda x, y : 2 * calc_average(4, y)), 9,
                    "A", 2370, 1, 1, 0],
    "(CL) SRM-6" : ["SRM6", [59, 7], 1,
                    4, (lambda x, y : 2 * calc_average(6, y)), 9,
                    "A", 2370, 1, 1.5, 0],
    "(CL) Streak SRM-2" : ["SSRM2", [40, 5], 1,
                           1, (lambda x, y : 4), 12,
                           "", 2647, 1, 1, 0],
    "(CL) Streak SRM-4" : ["SSRM4", [79, 10], 1,
                           1.5, (lambda x, y : 8), 12,
                           "", 2826, 1, 2, 0],
    "(CL) Streak SRM-6" : ["SSRM6", [118, 15], 1,
                           2, (lambda x, y : 12), 12,
                           "", 2826, 1, 3, 0],
    "(CL) Streak SRM-4 (OS)" : ["SSRM4OS", [16, 0], 1,
                                0.75, (lambda x, y : 0), 12, #TODO: OS damage
                                "", 2826, 0, 2.5, 0],
    "(CL) Narc Missile Beacon" : ["Narc", [30, 0], 1,
                                  0, (lambda x, y : 0), 12,
                                  "", 2587, 1, 2, 0],
    ### New Tournament Legal ###
    "ER Flamer" : ["ERFlmr", [16, 0], 1,
                   4, (lambda x, y : 2), 7,
                   "", 3067, 0, 1, 0],
    # Heavy Flamer
    # iHGR
    "(IS) Magshot Gauss Rifle" : ["MSGR", [15, 2], 1,
                                  1, (lambda x, y : 2), 9,
                                  "T", 3072, 1, 0.5, 2],
    # Silver Bullet
    # VGL
    "(IS) Binary Laser Cannon" : ["BLC", [222, 0], 1,
                                  16, (lambda x, y : 12), 15,
                                  "T", 2812, 0, 9, 0],
    "(IS) Enhanced LRM-5" : ["NLRM5", [52, 7], 1,
                             2, (lambda x, y : calc_average(5, y)), 21,
                             "A", 3058, 1, 3, 0],
    # NLRM-10
    # NLRM-15
    # NLRM-20
    # Imp OS
    # Light Rifle
    # Medium Rifle
    # Heavy Rifle
    "(IS) Thunderbolt-5" : ["Tbolt5", [64, 8], 1,
                            3, (lambda x, y : 5), 18,
                            "", 3072, 1, 3, 0],
    "(IS) Thunderbolt-10" : ["Tbolt10", [127, 16], 1,
                             5, (lambda x, y : 10), 18,
                             "", 3072, 1, 7, 0],
    "(IS) Thunderbolt-15" : ["Tbolt15", [229, 29], 1,
                             7, (lambda x, y : 15), 18,
                             "", 3072, 1, 11, 0],
    "(IS) Thunderbolt-20" : ["Tbolt20", [305, 38], 1,
                             8, (lambda x, y : 20), 18,
                             "", 3072, 1, 15, 0],

    ### Advanced Weapons ###
    "(IS) Arrow IV Missile" : ["ArwIV", [240, 30], 2,
                               10, (lambda x, y : 20), 120,
                               "", 2600, 1, 15, 0],
    "(CL) Arrow IV Missile" : ["ArwIV", [240, 30], 2,
                               10, (lambda x, y : 20), 135,
                               "", 2600, 1, 12, 0],
    # Thumper
    "(IS) Sniper" : ["Snpr", [85, 11], 2,
                     10, (lambda x, y : 20), 270,
                     "", 1900, 1, 20, 0],
    # Artillery Cannons
    # HVACs
    # Protomech AC/2
    "(CL) Protomech AC/4" : ["PAC4", [49, 6], 2,
                             1, (lambda x, y : 4), 15,
                             "T", 3073, 1, 4.5, 0],
    # Protomech AC/8
    # Fluid Gun
    "(IS) Bombast Laser" : ["BmbL", [137, 0], 2,
                            12, (lambda x, y : 12), 15,
                            "T", 3064, 0, 7, 0],
    # Chemical Lasers
    "(CL) ER Small Pulse Laser" : ["ERSPL", [36, 0], 2,
                                   3, (lambda x, y : 5), 6,
                                   "T", 3057, 0, 1.5, 0],
    "(CL) ER Medium Pulse Laser" : ["ERMPL", [117, 0], 2,
                                    6, (lambda x, y : 7), 14,
                                    "T", 3057, 0, 2, 0],
    # ERLPL
    # iHSL
    "(CL) Improved Heavy Medium Laser" : ["iHML", [93, 0], 2,
                                          7, (lambda x, y : 10), 9,
                                          "T", 3069, 0, 1, 2],
    # iHLL
    "(IS) Small Variable Speed Pulse Laser" :
        ["SVSPL", [22, 0], 2,
         3, (lambda x, y : svspl_damage(x)), 6,
         "T", 3070, 0, 2, 0],
    "(IS) Medium Variable Speed Pulse Laser" :
        ["MVSPL", [56, 0], 2,
         7, (lambda x, y : mvspl_damage(x)), 9,
         "T", 3070, 0, 4, 0],
    "(IS) Large Variable Speed Pulse Laser" :
        ["LVSPL", [123, 0], 2,
         10, (lambda x, y : lvspl_damage(x)), 15,
         "T", 3070, 0, 9, 0],
    "(IS) Small X-Pulse Laser" : ["SXPL", [21, 0], 2,
                                  3, (lambda x, y : 3), 5,
                                  "T", 3057, 0, 1, 0],
    "(IS) Medium X-Pulse Laser" : ["MXPL", [71, 0], 2,
                                   6, (lambda x, y : 6), 9,
                                   "T", 3057, 0, 2, 0],
    "(IS) Large X-Pulse Laser" : ["LXPL", [178, 0], 2,
                                  14, (lambda x, y : 9), 15,
                                  "T", 3057, 0, 7, 0],
    # MM1
    # MM2
    # MM4
    # MM8-IS
    "(CL) Mech Mortar 8" : ["Mrtr8", [50, 6], 2,
                            10, (lambda x, y : 2 * calc_average(8, 0)), 21,
                            "", 2840, 1, 5, 0],
    # ERLMs
    # SLRM5
    "(CL) Streak LRM-10" : ["SLRM10", [173, 22], 2,
                            2, (lambda x, y : 10), 21,
                            "", 3057, 1, 5, 0],
    # SLRM15
    # SLRM20
    "(IS) Light PPC + PPC Capacitor" : ["LPPC+", [132, 0], 2,
                                        10, (lambda x, y : 10), 18,
                                        "T", 3067, 0, 4, 3],
    "(IS) Snub-Nose PPC + PPC Capacitor" :
        ["SNPPC+", [252, 0], 2,
         15, (lambda x, y : sn_damage(x) + 5), 15,
         "T", 3067, 0, 7, 3],
    # rest of +PPC cap
    "(IS) BattleMech Taser" : ["TSR", [40, 5], 2,
                               6, (lambda x, y : 1), 4,
                               "", 3067, 1, 4, 3],

    ### Experimental Weapons ###
    "(CL) Rotary AC/2" : ["RAC2", [161, 20], 3,
                          6, (lambda x, y : 2 * calc_average(6, 0)), 25,
                          "T", 3073, 6, 8, 0],
    "(CL) Rotary AC/5" : ["RAC5", [345, 43], 3,
                          6, (lambda x, y : 5 * calc_average(6, 0)), 21,
                          "T", 3073, 6, 10, 0]
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
        self.batt_val = WEAPONS[key][1]
        self.range = WEAPONS[key][5]
        self.useammo = WEAPONS[key][8]
        self.explosive = WEAPONS[key][10]
        self.count = 0
        self.countrear = 0
        self.countarm = 0 # We count arm weapons also, to help with BV calcs
        self.ammocount = 0
        self.ammo_ton = 0

        # Deal with enhancements, Artemis
        self.enhance = ""
        if (WEAPONS[key][6] == "A"):
            if art5 == "TRUE":
                self.enhance = "A5"
            elif art4 == "TRUE":
                self.enhance = "A4"
        # Apollo
        elif (WEAPONS[key][6] == "P" and apollo == "TRUE"):
            self.enhance = "AP"
        # Tarcomp, we can not know if one is present right now
        elif (WEAPONS[key][6] == "T"):
            self.enhance = "TC"

    def get_weight(self):
        """
        Return weight
        """
        wgt = WEAPONS[self.name][9]
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
        return WEAPONS[self.name][3]

    def get_short(self):
        """
        Return short name
        """
        return WEAPONS[self.name][0]

    def get_damage(self, rnge):
        """
        Return damage
        """

        # No damage if out of range
        if rnge > WEAPONS[self.name][5]:
            return 0

        # Check for cluster adjustments from Artemis & Apollo
        art = 0
        if self.enhance == "A5":
            art = 3
        elif self.enhance == "A4":
            art = 2
        elif self.enhance == "AP":
            art = -1

        return WEAPONS[self.name][4](rnge, art)

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



