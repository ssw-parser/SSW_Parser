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
# heat (as used for BV calcs), damage as a function of range,
# range (min, short, med, long),
# enhancement(A=artemis, T=tarcomp P=apollo),
# uses ammo rate?, weight, slots, explosive?
#
# Where rules level is:
#        0 = Intro-tech,
#        1 = Tournament legal,
#        2 = Advanced,
#        3 = Experimental,
#        4 = Primitive (special)
#
# Use damage * 0.1 for one-shot weapons
#
# To be loaded into the gear class
#
# TODO: IS: 2 MG, HMG, 2 HMG, 4 HMG, Flamer (Vehicle), One-shots, LRT-20,
# SRT-2, SRT-6
# TODO: Clan: 2 LMG, 2 MG, 3 MG, 2 HMG, Flamer (Vehicle), One-shots, LRT-20
# TODO: New TL: VGL, NLRM10, NLRM15, NLRM20,
# Improved One-shot, Light Rifle, Medium Rifle, Heavy Rifle
# TODO: Advanced: Thumper, PMAC/2, iHSL, iHLL,
# Mech Mortars, Imp OS, Thumper & Sniper Artillery Cannon, HVAC2, HVAC5,
# Chemical Lasers, ELRM5, ELRM15, SLRM-5, SLRM-20
WEAPONS = {
    ### Inner Sphere, Tech Manual ###
    "(IS) Autocannon/2" : ["AC2", [37, 5], 0, 75000,
                           1, (lambda x, y : 2), [4, 8, 16, 24],
                           "T", 1, 6, 1, ""],
    "(IS) Autocannon/5" : ["AC5", [70, 9], 0, 125000,
                           1, (lambda x, y : 5), [3, 6, 12, 18],
                           "T", 1, 8, 4, ""],
    "(IS) Autocannon/10" : ["AC10", [123, 15], 0, 200000,
                            3, (lambda x, y : 10), [0, 5, 10, 15],
                            "T", 1, 12, 7, ""],
    "(IS) Autocannon/20" : ["AC20", [178, 22], 0, 300000,
                            7, (lambda x, y : 20), [0, 3, 6, 9],
                            "T", 1, 14, 10, ""],
    "(IS) LB 2-X AC" : ["LB2", [42, 5], 1, 150000,
                        1, (lambda x, y : 2), [4, 9, 18, 27],
                        "T", 1, 6, 4, ""],
    "(IS) LB 5-X AC" : ["LB5", [83, 10], 1, 250000,
                        1, (lambda x, y : 5), [3, 7, 14, 21],
                        "T", 1, 8, 5, ""],
    "(IS) LB 10-X AC" : ["LB10", [148, 19], 1, 400000,
                         2, (lambda x, y : 10), [0, 6, 12, 18],
                         "T", 1, 11, 6, ""],
    "(IS) LB 20-X AC" : ["LB20", [237, 30], 1, 600000,
                         6, (lambda x, y : 20), [0, 4, 8, 12],
                         "T", 1, 14, 11, ""],
    "(IS) Light AC/2" : ["LAC2", [30, 4], 1, 100000,
                         1, (lambda x, y : 2), [0, 6, 12, 18],
                         "T", 1, 4, 1, ""],
    "(IS) Light AC/5" : ["LAC5", [62, 8], 1, 150000,
                         1, (lambda x, y : 5), [0, 5, 10, 15],
                         "T", 1, 5, 2, ""],
    "(IS) Rotary AC/2" :
        ["RAC2", [118, 15], 1, 175000,
         6, (lambda x, y : 2 * calc_average(6, 0)), [0, 6, 12, 18],
         "T", 6, 8, 3, ""],
    "(IS) Rotary AC/5" :
        ["RAC5", [247, 31], 1, 275000,
         6, (lambda x, y : 5 * calc_average(6, 0)), [0, 5, 10, 15],
         "T", 6, 10, 6, ""],
    "(IS) Ultra AC/2" :
        ["UAC2", [56, 7], 1, 120000,
         2, (lambda x, y : 2 * calc_average(2, 0)), [3, 8, 17, 25],
         "T", 2, 7, 3, ""],
    "(IS) Ultra AC/5" :
        ["UAC5", [112, 14], 1, 200000,
         2, (lambda x, y : 5 * calc_average(2, 0)), [2, 6, 13, 20],
         "T", 2, 9, 5, ""],
    "(IS) Ultra AC/10" :
        ["UAC10", [210, 26], 1, 320000,
         8, (lambda x, y : 10 * calc_average(2, 0)), [0, 6, 12, 18],
         "T", 2, 13, 7, ""],
    "(IS) Ultra AC/20" :
        ["UAC20", [281, 35], 1, 480000,
         16, (lambda x, y : 20 * calc_average(2, 0)), [0, 3, 7, 10],
         "T", 2, 15, 10, ""],
    "(IS) Light Gauss Rifle" : ["LGR", [159, 20], 1, 275000,
                                1, (lambda x, y : 8), [3, 8, 17, 25],
                                "T", 1, 12, 5, "X"],
    "(IS) Gauss Rifle" : ["GR", [320, 40], 1, 300000,
                          1, (lambda x, y : 15), [2, 7, 15, 22],
                          "T", 1, 15, 7, "X"],
    "(IS) Heavy Gauss Rifle" :
        ["HGR", [346, 43], 1, 500000,
         2, (lambda x, y : hgr_damage(x)), [4, 6, 13, 20],
         "T", 1, 18, 11, "X"],
    "(IS) Light Machine Gun" : ["LMG", [5, 1], 1, 5000,
                                0, (lambda x, y : 1), [0, 2, 4, 6],
                                "", 1, 0.5, 1, ""],
    "(IS) MG Array (2 Light Machine Gun)" :
        ["LMG2A", [16.7, 1], 1, 11250,
         0, (lambda x, y : 1 * calc_average(2, 0)), [0, 2, 4, 6],
         "", 2, 1.5, 3, ""],
    "(IS) MG Array (3 Light Machine Gun)" :
        ["LMG3A", [25.05, 1], 1, 16250,
         0, (lambda x, y : 1 * calc_average(3, 0)), [0, 2, 4, 6],
         "", 3, 2, 4, ""],
    "(IS) MG Array (4 Light Machine Gun)" :
        ["LMG4A", [33.4, 1], 1, 21250,
         0, (lambda x, y : 1 * calc_average(4, 0)), [0, 2, 4, 6],
         "", 4, 2.5, 5, ""],
    "(IS) Machine Gun" : ["MG", [5, 1], 0, 5000,
                          0, (lambda x, y : 2), [0, 1, 2, 3],
                          "", 1, 0.5, 1, ""],
    # MG 2
    "(IS) MG Array (3 Machine Gun)" :
        ["MG3A", [25.05, 1], 1, 16250,
         0, (lambda x, y : 2 * calc_average(3, 0)), [0, 1, 2, 3],
         "", 3, 2, 4, ""],
    "(IS) MG Array (4 Machine Gun)" :
        ["MG4A", [33.4, 1], 1, 21250,
         0, (lambda x, y : 2 * calc_average(4, 0)), [0, 1, 2, 3],
         "", 4, 2.5, 5, ""],
    # HMG
    # HMG 2
    "(IS) MG Array (3 Heavy Machine Gun)" :
        ["HMG3A", [30.06, 1], 1, 23750,
         0, (lambda x, y : 3 * calc_average(3, 0)), [0, 1, 2, 2],
         "", 3, 3.5, 4, ""],
    # HMG 4
    "(IS) Flamer" : ["Flmr", [6, 0], 0, 7500,
                     3, (lambda x, y : 2), [0, 1, 2, 3],
                     "", 0, 1, 1, ""],
    # Flamer (Vehicle)
    "(IS) ER Small Laser" : ["ERSL", [17, 0], 1, 11250,
                             2, (lambda x, y : 3), [0, 2, 4, 5],
                             "T", 0, 0.5, 1, ""],
    "(IS) ER Medium Laser" : ["ERML", [62, 0], 1, 80000,
                              5, (lambda x, y : 5), [0, 4, 8, 12],
                              "T", 0, 1, 1, ""],
    "(IS) ER Large Laser" : ["ERLL", [163, 0], 1, 200000,
                             12, (lambda x, y : 8), [0, 7, 14, 19],
                             "T", 0, 5, 2, ""],
    "(IS) Small Laser" : ["SL", [9, 0], 0, 11250,
                          1, (lambda x, y : 3), [0, 1, 2, 3],
                          "T", 0, 0.5, 1, ""],
    "(IS) Medium Laser" : ["ML", [46, 0], 0, 40000,
                           3, (lambda x, y : 5), [0, 3, 6, 9],
                           "T", 0, 1, 1, ""],
    "(IS) Large Laser" : ["LL", [123, 0], 0, 100000,
                          8, (lambda x, y : 8), [0, 5, 10, 15],
                          "T", 0, 5, 2, ""],
    "(IS) Small Pulse Laser" : ["SPL", [12, 0], 1, 16000,
                                2, (lambda x, y : 3), [0, 1, 2, 3],
                                "T", 0, 1, 1, ""],
    "(IS) Medium Pulse Laser" : ["MPL", [48, 0], 1, 60000,
                                 4, (lambda x, y : 6), [0, 2, 4, 6],
                                 "T", 0, 2, 1, ""],
    "(IS) Large Pulse Laser" : ["LPL", [119, 0], 1, 175000,
                                10, (lambda x, y : 9), [0, 3, 7, 10],
                                "T", 0, 7, 2, ""],
    "(IS) Plasma Rifle" : ["PR", [210, 26], 1, 260000,
                           10, (lambda x, y : 10), [0, 5, 10, 15],
                           "T", 1, 6, 2, ""],
    "(IS) Light PPC" : ["LPPC", [88, 0], 1, 150000,
                        5, (lambda x, y : 5), [3, 6, 12, 18],
                        "T", 0, 3, 2, ""],
    "(IS) PPC" : ["PPC", [176, 0], 0, 200000,
                  10, (lambda x, y : 10), [3, 6, 12, 18],
                  "T", 0, 7, 3, ""],
    "(IS) Heavy PPC" : ["HPPC", [317, 0], 1, 250000,
                        15, (lambda x, y : 15), [3, 6, 12, 18],
                        "T", 0, 10, 4, ""],
    "(IS) ER PPC" : ["ERPPC", [229, 0], 1, 300000,
                     15, (lambda x, y : 10), [0, 7, 14, 23],
                     "T", 0, 7, 3, ""],
    "(IS) Snub-Nose PPC" :
        ["SNPPC", [165, 0], 1, 300000,
         10, (lambda x, y : sn_damage(x)), [0, 9, 13, 15],
         "T", 0, 6, 2, ""],
    "(IS) LRM-5" :
        ["LRM5", [45, 6], 0, 30000,
         2, (lambda x, y : calc_average(5, y)), [6, 7, 14, 21],
         "A", 1, 2, 1, ""],
    "(IS) LRM-10" :
        ["LRM10", [90, 11], 0, 100000,
         4, (lambda x, y : calc_average(10, y)), [6, 7, 14, 21],
         "A", 1, 5, 2, ""],
    "(IS) LRM-15" :
        ["LRM15", [136, 17], 0, 175000,
         5, (lambda x, y : calc_average(15, y)), [6, 7, 14, 21],
         "A", 1, 7, 3, ""],
    "(IS) LRM-20" :
        ["LRM20", [181, 23], 0, 250000,
         6, (lambda x, y : calc_average(20, y)), [6, 7, 14, 21],
         "A", 1, 10, 5, ""],
    "(IS) LRT-5" :
        ["LRT5", [45, 6], 0, 30000,
         2, (lambda x, y : calc_average(5, y)), [6, 7, 14, 21],
         "A", 1, 2, 1, ""],
    "(IS) LRT-10" :
        ["LRT10", [90, 11], 0, 100000,
         4, (lambda x, y : calc_average(10, y)), [6, 7, 14, 21],
         "A", 1, 5, 2, ""],
    "(IS) LRT-15" :
        ["LRT15", [136, 17], 0, 175000,
         5, (lambda x, y : calc_average(15, y)), [6, 7, 14, 21],
         "A", 1, 7, 3, ""],
    # LRT-20
    "(IS) MML-3" :
        ["MML3", [29, 4], 1, 45000,
         2, (lambda x, y : mml3_damage(x, y)), [0, 3, 14, 21],
         "A", 1, 1.5, 2, ""],
    "(IS) MML-5" :
        ["MML5", [45, 6], 1, 75000,
         3, (lambda x, y : mml5_damage(x, y)), [0, 3, 14, 21],
         "A", 1, 3, 3, ""],
    "(IS) MML-7" :
        ["MML7", [67, 8], 1, 105000,
         4, (lambda x, y : mml7_damage(x, y)), [0, 3, 14, 21],
         "A", 1, 4.5, 4, ""],
    "(IS) MML-9" :
        ["MML9", [86, 11], 1, 125000,
         5, (lambda x, y : mml9_damage(x, y)), [0, 3, 14, 21],
         "A", 1, 6, 5, ""],
    "(IS) SRM-2" :
        ["SRM2", [21, 3], 0, 10000,
         2, (lambda x, y : 2 * calc_average(2, y)), [0, 3, 6, 9],
         "A", 1, 1, 1, ""],
    "(IS) SRM-4" :
        ["SRM4", [39, 5], 0, 60000,
         3, (lambda x, y : 2 * calc_average(4, y)), [0, 3, 6, 9],
         "A", 1, 2, 1, ""],
    "(IS) SRM-6" :
        ["SRM6", [59, 7], 0, 80000,
         4, (lambda x, y : 2 * calc_average(6, y)), [0, 3, 6, 9],
         "A", 1, 3, 2, ""],
    "(IS) SRM-4 (OS)" :
        ["SRM4OS", [8, 0], 1, 30000,
         0.75, (lambda x, y : 2 * calc_average(4, y) * 0.1), [0, 3, 6, 9],
         "A", 0, 2.5, 1, ""],
    # SRT-2
    "(IS) SRT-4" :
        ["SRT4", [39, 5], 0, 60000,
         3, (lambda x, y : 2 * calc_average(4, y)), [0, 3, 6, 9],
         "A", 1, 2, 1, ""],
    # SRT-6
    "(IS) MRM-10" :
        ["MRM10", [56, 7], 1, 50000,
         4, (lambda x, y : calc_average(10, y)), [0, 3, 8, 15],
         "P", 1, 3, 2, ""],
    "(IS) MRM-20" :
        ["MRM20", [112, 14], 1, 125000,
         6, (lambda x, y : calc_average(20, y)), [0, 3, 8, 15],
         "P", 1, 7, 3, ""],
    "(IS) MRM-30" :
        ["MRM30", [168, 21], 1, 225000,
         10, (lambda x, y : calc_average(30, y)), [0, 3, 8, 15],
         "P", 1, 10, 5,""],
    "(IS) MRM-40" :
        ["MRM40", [224, 28], 1, 350000,
         12, (lambda x, y : calc_average(40, y)), [0, 3, 8, 15],
         "P", 1, 12, 7, ""],
    "(IS) Rocket Launcher 10" :
        ["RL10", [18, 0], 1, 15000,
         0.75, (lambda x, y : calc_average(10, 0) * 0.1), [0, 5, 11, 18],
         "", 0, 0.5, 1, ""],
    "(IS) Rocket Launcher 15" :
        ["RL15", [23, 0], 1, 30000,
         1, (lambda x, y : calc_average(15, 0) * 0.1), [0, 4, 9, 15],
         "", 0, 1, 2, ""],
    "(IS) Rocket Launcher 20" :
        ["RL20", [24, 0], 1, 45000,
         1.25, (lambda x, y : calc_average(20, 0) * 0.1), [0, 3, 7, 12],
         "", 0, 1.5, 3, ""],
    "(IS) Streak SRM-2" : ["SSRM2", [30, 4], 1, 15000,
                           1, (lambda x, y : 4), [0, 3, 6, 9],
                           "", 1, 1.5, 1, ""],
    "(IS) Streak SRM-4" : ["SSRM4", [59, 7], 1, 90000,
                           1.5, (lambda x, y : 8), [0, 3, 6, 9],
                           "", 1, 3, 1, ""],
    "(IS) Streak SRM-6" : ["SSRM6", [89, 11], 1, 120000,
                           2, (lambda x, y : 12), [0, 3, 6, 9],
                           "", 1, 4.5, 2, ""],
    "(IS) Streak SRM-2 (OS)" : ["SSRM2OS", [6, 0], 1, 7500,
                                0.5, (lambda x, y : 4 * 0.1), [0, 3, 6, 9],
                                "", 0, 2, 1, ""],
    "(IS) Narc Missile Beacon" : ["Narc", [30, 0], 1, 100000,
                                  0, (lambda x, y : 0), [0, 3, 6, 9],
                                  "", 1, 3, 2, ""],
    "(IS) iNarc Launcher" : ["iNarc", [75, 0], 1, 250000,
                             0, (lambda x, y : 0), [0, 4, 9, 15],
                             "", 1, 5, 3, ""],
    ### Clan, Tech Manual ###
    "(CL) LB 2-X AC" : ["LB2", [47, 6], 1, 150000,
                        1, (lambda x, y : 2), [4, 10, 20, 30],
                        "T", 1, 5, 3, ""],
    "(CL) LB 5-X AC" : ["LB5", [93, 12], 1, 250000,
                        1, (lambda x, y : 5), [3, 8, 15, 24],
                        "T", 1, 7, 4, ""],
    "(CL) LB 10-X AC" : ["LB10", [148, 19], 1, 400000,
                         2, (lambda x, y : 10), [0, 6, 12, 18],
                         "T", 1, 10, 5, ""],
    "(CL) LB 20-X AC" : ["LB20", [237, 30], 1, 600000,
                         6, (lambda x, y : 20), [0, 4, 8, 12],
                         "T", 1, 12, 9, ""],
    "(CL) Ultra AC/2" :
        ["UAC2", [62, 8], 1, 120000,
         2, (lambda x, y : 2 * calc_average(2, 0)), [2, 9, 18, 27],
         "T", 2, 5, 2, ""],
    "(CL) Ultra AC/5" :
        ["UAC5", [122, 15], 1, 200000,
         2, (lambda x, y : 5 * calc_average(2, 0)), [0, 7, 14, 21],
         "T", 2, 7, 3, ""],
    "(CL) Ultra AC/10" :
        ["UAC10", [210, 26], 1, 320000,
         6, (lambda x, y : 10 * calc_average(2, 0)), [0, 6, 12, 18],
         "T", 2, 10, 4, ""],
    "(CL) Ultra AC/20" :
        ["UAC20", [335, 42], 1, 480000,
         14, (lambda x, y : 20 * calc_average(2, 0)), [0, 4, 8, 12],
         "T", 2, 12, 8, ""],
    "(CL) AP Gauss Rifle" : ["APGR", [21, 3], 1, 10000,
                             1, (lambda x, y : 3), [0, 3, 6, 9],
                             "T", 1, 0.5, 1, "X"],
    "(CL) Gauss Rifle" : ["GR", [320, 40], 1, 300000,
                          1, (lambda x, y : 15), [2, 7, 15, 22],
                          "T", 1, 12, 6, "X"],
    "(CL) Hyper Assault Gauss 20" :
        ["HAG20", [267, 33], 1, 400000,
         4, (lambda x, y : hag20_damage(x)), [2, 8, 16, 24],
         "T", 1, 10, 6, "X"],
    "(CL) Hyper Assault Gauss 30" :
        ["HAG30", [401, 50], 1, 500000,
         6, (lambda x, y : hag30_damage(x)), [2, 8, 16, 24],
         "T", 1, 13, 8, "X"],
    "(CL) Hyper Assault Gauss 40" :
        ["HAG40", [535, 67], 1, 600000,
         8, (lambda x, y : hag40_damage(x)), [2, 8, 16, 24],
         "T", 1, 16, 10, "X"],
    "(CL) Light Machine Gun" : ["LMG", [5, 1], 1, 5000,
                                0, (lambda x, y : 1), [0, 2, 4, 6],
                                "", 1, 0.25, 1, ""],
    # LMG 2
    "(CL) MG Array (3 Light Machine Gun)" :
        ["LMG3A", [25.05, 1], 1, 16250,
         0, (lambda x, y : 1 * calc_average(3, 0)), [0, 2, 4, 6],
         "", 3, 1, 4, ""],
    "(CL) MG Array (4 Light Machine Gun)" :
        ["LMG4A", [33.4, 1], 1, 21250,
         0, (lambda x, y : 1 * calc_average(4, 0)), [0, 2, 4, 6],
         "", 4, 1.25, 5, ""],
    "(CL) Machine Gun" : ["MG", [5, 1], 1, 5000,
                          0, (lambda x, y : 2), [0, 1, 2, 3],
                          "", 1, 0.25, 1, ""],
    # MG 2
    # MG 3
    "(CL) MG Array (4 Machine Gun)" :
        ["MG4A", [33.4, 1], 1, 21250,
         0, (lambda x, y : 2 * calc_average(4, 0)), [0, 1, 2, 3],
         "", 4, 1.25, 5, ""],
    "(CL) Heavy Machine Gun" : ["HMG", [6, 1], 1, 7500,
                                0, (lambda x, y : 3), [0, 1, 2, 2],
                                "", 1, 0.5, 1, ""],
    # HMG 2
    "(CL) MG Array (3 Heavy Machine Gun)" :
        ["HMG3A", [30.06, 1], 1, 23750,
         0, (lambda x, y : 3 * calc_average(3, 0)), [0, 1, 2, 2],
         "", 3, 1.75, 4, ""],
    "(CL) MG Array (4 Heavy Machine Gun)" :
        ["HMG4A", [40.08, 1], 1, 31250,
         0, (lambda x, y : 3 * calc_average(4, 0)), [0, 1, 2, 2],
         "", 4, 2.25, 5, ""],
    "(CL) Flamer" : ["Flmr", [6, 0], 1, 7500,
                     3, (lambda x, y : 2), [0, 1, 2, 3],
                     "", 0, 0.5, 1, ""],
    # Flamer (Vehicle)
    "(CL) ER Micro Laser" : ["ERMcL", [7, 0], 1, 10000,
                             1, (lambda x, y : 2), [0, 1, 2, 4],
                             "T", 0, 0.25, 1, ""],
    "(CL) ER Small Laser" : ["ERSL", [31, 0], 1, 11250,
                             2, (lambda x, y : 5), [0, 2, 4, 6],
                             "T", 0, 0.5, 1, ""],
    "(CL) ER Medium Laser" : ["ERML", [108, 0], 1, 80000,
                              5, (lambda x, y : 7), [0, 5, 10, 15],
                              "T", 0, 1, 1, ""],
    "(CL) ER Large Laser" : ["ERLL", [248, 0], 1, 200000,
                             12, (lambda x, y : 10), [0, 8, 15, 25],
                             "T", 0, 4, 1, ""],
    "(CL) Micro Pulse Laser" : ["McPL", [12, 0], 1, 12500,
                                1, (lambda x, y : 3), [0, 1, 2, 3],
                                "T", 0, 0.5, 1, ""],
    "(CL) Small Pulse Laser" : ["SPL", [24, 0], 1, 16000,
                                2, (lambda x, y : 3), [0, 2, 4, 6],
                                "T", 0, 1, 1, ""],
    "(CL) Medium Pulse Laser" : ["MPL", [111, 0], 1, 60000,
                                 4, (lambda x, y : 7), [0, 4, 8, 12],
                                 "T", 0, 2, 1, ""],
    "(CL) Large Pulse Laser" : ["LPL", [265, 0], 1, 175000,
                                10, (lambda x, y : 10), [0, 6, 14, 20],
                                "T", 0, 6, 2, ""],
    "(CL) Heavy Small Laser" : ["HSL", [15, 0], 1, 20000,
                                3, (lambda x, y : 6), [0, 1, 2, 3],
                                "T", 0, 0.5, 1, ""],
    "(CL) Heavy Medium Laser" : ["HML", [76, 0], 1, 100000,
                                 7, (lambda x, y : 10), [0, 3, 6, 9],
                                 "T", 0, 1, 2, ""],
    "(CL) Heavy Large Laser" : ["HLL", [244, 0], 1, 250000,
                                18, (lambda x, y : 16), [0, 5, 10, 15],
                                "T", 0, 4, 3, ""],
    "(CL) Plasma Cannon" : ["PC", [170, 21], 1, 320000,
                            7, (lambda x, y : 0), [0, 6, 12, 18],
                            "T", 1, 3, 1, ""],
    "(CL) ER PPC" : ["ERPPC", [412, 0], 1, 300000,
                     15, (lambda x, y : 15), [0, 7, 14, 23],
                     "T", 0, 6, 2, ""],
    "(CL) ATM-3" : ["ATM3", [53, 14], 1, 50000,
                    2, (lambda x, y : atm3_damage(x)), [0, 3, 18, 27],
                    "", 1, 1.5, 2, ""],
    "(CL) ATM-6" : ["ATM6", [105, 26], 1, 125000,
                    4, (lambda x, y : atm6_damage(x)), [0, 3, 18, 27],
                    "", 1, 3.5, 3, ""],
    "(CL) ATM-9" : ["ATM9", [147, 36], 1, 225000,
                    6, (lambda x, y : atm9_damage(x)), [0, 3, 18, 27],
                    "", 1, 5, 4, ""],
    "(CL) ATM-12" : ["ATM12", [212, 52], 1, 350000,
                     8, (lambda x, y : atm12_damage(x)), [0, 3, 18, 27],
                     "", 1, 7, 5, ""],
    "(CL) LRM-5" : ["LRM5", [55, 7], 1, 30000,
                    2, (lambda x, y : calc_average(5, y)), [0, 7, 14, 21],
                    "A", 1, 1, 1, ""],
    "(CL) LRM-10" : ["LRM10", [109, 14], 1, 100000,
                     4, (lambda x, y : calc_average(10, y)), [0, 7, 14, 21],
                     "A", 1, 2.5, 1, ""],
    "(CL) LRM-15" : ["LRM15", [164, 21], 1, 175000,
                     5, (lambda x, y : calc_average(15, y)), [0, 7, 14, 21],
                     "A", 1, 3.5, 2, ""],
    "(CL) LRM-20" : ["LRM20", [220, 27], 1, 250000,
                     6, (lambda x, y : calc_average(20, y)), [0, 7, 14, 21],
                     "A", 1, 5, 4, ""],
    "(CL) LRT-5" : ["LRT5", [55, 7], 1, 30000,
                    2, (lambda x, y : calc_average(5, y)), [0, 7, 14, 21],
                    "A", 1, 1, 1, ""],
    "(CL) LRT-10" : ["LRT10", [109, 14], 1, 100000,
                     4, (lambda x, y : calc_average(10, y)), [0, 7, 14, 21],
                     "A", 1, 2.5, 1, ""],
    "(CL) LRT-15" : ["LRT15", [164, 21], 1, 175000,
                     5, (lambda x, y : calc_average(15, y)), [0, 7, 14, 21],
                     "A", 1, 3.5, 2, ""],
    # LRT-20
    "(CL) SRM-2" : ["SRM2", [21, 3], 1, 10000,
                    2, (lambda x, y : 2 * calc_average(2, y)), [0, 3, 6, 9],
                    "A", 1, 0.5, 1, ""],
    "(CL) SRM-4" : ["SRM4", [39, 5], 1, 60000,
                    3, (lambda x, y : 2 * calc_average(4, y)), [0, 3, 6, 9],
                    "A", 1, 1, 1, ""],
    "(CL) SRM-6" : ["SRM6", [59, 7], 1, 80000,
                    4, (lambda x, y : 2 * calc_average(6, y)), [0, 3, 6, 9],
                    "A", 1, 1.5, 1, ""],
    "(CL) SRT-2" : ["SRT2", [21, 3], 1, 10000,
                    2, (lambda x, y : 2 * calc_average(2, y)), [0, 3, 6, 9],
                    "A", 1, 0.5, 1, ""],
    "(CL) SRT-4" : ["SRT4", [39, 5], 1, 60000,
                    3, (lambda x, y : 2 * calc_average(4, y)), [0, 3, 6, 9],
                    "A", 1, 1, 1, ""],
    "(CL) SRT-6" : ["SRT6", [59, 7], 1, 80000,
                    4, (lambda x, y : 2 * calc_average(6, y)), [0, 3, 6, 9],
                    "A", 1, 1.5, 1, ""],
    "(CL) Streak SRM-2" : ["SSRM2", [40, 5], 1, 15000,
                           1, (lambda x, y : 4), [0, 4, 8, 12],
                           "", 1, 1, 1, ""],
    "(CL) Streak SRM-4" : ["SSRM4", [79, 10], 1, 90000,
                           1.5, (lambda x, y : 8), [0, 4, 8, 12],
                           "", 1, 2, 1, ""],
    "(CL) Streak SRM-6" : ["SSRM6", [118, 15], 1, 120000,
                           2, (lambda x, y : 12), [0, 4, 8, 12],
                           "", 1, 3, 2, ""],
    "(CL) Streak SRM-4 (OS)" : ["SSRM4OS", [16, 0], 1, 45000,
                                0.75, (lambda x, y : 8 * 0.1), [0, 4, 8, 12],
                                "", 0, 2.5, 1, ""],
    "(CL) Narc Missile Beacon" : ["Narc", [30, 0], 1, 100000,
                                  0, (lambda x, y : 0), [0, 4, 8, 12],
                                  "", 1, 2, 1, ""],
    ### New Tournament Legal ###
    "ER Flamer" : ["ERFlmr", [16, 0], 1, 15000,
                   4, (lambda x, y : 2), [0, 3, 5, 7],
                   "", 0, 1, 1, ""],
    "Heavy Flamer" : ["Hflmr", [15, 2], 1, 11250,
                      5, (lambda x, y : 4), [0, 2, 3, 4],
                      "", 1, 1.5, 1, ""],
    "(IS) Improved Heavy Gauss Rifle" :
        ["iHGR", [385, 48], 1, 700000,
         2, (lambda x, y : 22), [3, 6, 12, 19],
         "T", 1, 20, 11, "X"],
    "(IS) Magshot Gauss Rifle" : ["MSGR", [15, 2], 1, 8500,
                                  1, (lambda x, y : 2), [0, 3, 6, 9],
                                  "T", 1, 0.5, 2, "X"],
    "(IS) Silver Bullet Gauss" :
        ["SBGR", [198, 25], 1, 350000,
         1, (lambda x, y : calc_average(15, 0)), [2, 7, 15, 22],
         "", 1, 15, 7, "X"],
    # VGL
    "(IS) Binary Laser Cannon" : ["BLC", [222, 0], 1, 200000,
                                  16, (lambda x, y : 12), [0, 5, 10, 15],
                                  "T", 0, 9, 4, ""],
    "(IS) Enhanced LRM-5" :
        ["NLRM5", [52, 7], 1, 37500,
         2, (lambda x, y : calc_average(5, y)), [3, 7, 14, 21],
         "A", 1, 3, 2, ""],
    # NLRM-10
    # NLRM-15
    # NLRM-20
    # Imp OS
    "(CL) Narc Missile Beacon (iOS)" : ["NarciOS", [6, 0], 1, 80000,
                                        0, (lambda x, y : 0), [0, 4, 8, 12],
                                        "", 0, 1.5, 1, ""],
                                        
    # Light Rifle
    # Medium Rifle
    # Heavy Rifle
    "(IS) Thunderbolt-5" : ["Tbolt5", [64, 8], 1, 50000,
                            3, (lambda x, y : 5), [5, 6, 12, 18],
                            "", 1, 3, 1, ""],
    "(IS) Thunderbolt-10" : ["Tbolt10", [127, 16], 1, 175000,
                             5, (lambda x, y : 10), [5, 6, 12, 18],
                             "", 1, 7, 2, ""],
    "(IS) Thunderbolt-15" : ["Tbolt15", [229, 29], 1, 325000,
                             7, (lambda x, y : 15), [5, 6, 12, 18],
                             "", 1, 11, 3, ""],
    "(IS) Thunderbolt-20" : ["Tbolt20", [305, 38], 1, 450000,
                             8, (lambda x, y : 20), [5, 6, 12, 18],
                             "", 1, 15, 5, ""],

    ### Advanced Weapons ###
    "(IS) Arrow IV Missile" : ["ArwIV", [240, 30], 2, 450000,
                               10, (lambda x, y : 20), [6, 120, 120, 120],
                               "", 1, 15, 15, ""],
    "(CL) Arrow IV Missile" : ["ArwIV", [240, 30], 2, 450000,
                               10, (lambda x, y : 20), [6, 135, 135, 135],
                               "", 1, 12, 12, ""],
    # Thumper
    "(IS) Sniper" : ["Snpr", [85, 11], 2, 300000,
                     10, (lambda x, y : 20), [6, 270, 270, 270],
                     "", 1, 20, 20, ""],
    # Thumper Cannon
    # Sniper Cannon
    "Long Tom Artillery Cannon" : ["LTArtC", [329, 41], 2, 650000,
                                   20, (lambda x, y : 20), [4, 6, 13, 20],
                                   "", 1, 20, 15, ""],
    # HVAC2
    # HVAC5
    "(IS) Hyper-Velocity Autocannon/10" :
        ["HVAC10", [158, 20], 2, 230000,
         7, (lambda x, y : 10), [0, 6, 12, 20],
         "T", 1, 14, 6, "X"],
    # Protomech AC/2
    "(CL) Protomech AC/4" : ["PAC4", [49, 6], 2, 133000,
                             1, (lambda x, y : 4), [0, 5, 10, 15],
                             "T", 1, 4.5, 3, ""],
    "(CL) Protomech AC/8" : ["PAC8", [66, 8], 2, 175000,
                             2, (lambda x, y : 8), [0, 3, 7, 10],
                             "T", 1, 5.5, 4, ""],
    "(IS) Fluid Gun" : ["Fluid", [6, 1], 2, 35000,
                        0, (lambda x, y : 0), [0, 1, 2, 3],
                        "", 1, 2, 2, ""],
    "(IS) Bombast Laser" : ["BmbL", [137, 0], 2, 200000,
                            12, (lambda x, y : 12), [0, 5, 10, 15],
                            "T", 0, 7, 3, ""],
    # Chemical Lasers
    "(CL) ER Small Pulse Laser" : ["ERSPL", [36, 0], 2, 30000,
                                   3, (lambda x, y : 5), [0, 2, 4, 6],
                                   "T", 0, 1.5, 1, ""],
    "(CL) ER Medium Pulse Laser" : ["ERMPL", [117, 0], 2, 150000,
                                    6, (lambda x, y : 7), [0, 5, 9, 14],
                                    "T", 0, 2, 2, ""],
    "(CL) ER Large Pulse Laser" : ["ERLPL", [272, 0], 2, 400000,
                                   13, (lambda x, y : 10), [0, 7, 15, 23],
                                   "T", 0, 6, 3, ""],
    # iHSL
    "(CL) Improved Heavy Medium Laser" : ["iHML", [93, 0], 2, 150000,
                                          7, (lambda x, y : 10), [0, 3, 6, 9],
                                          "T", 0, 1, 2, "X"],
    # iHLL
    "(IS) Small Variable Speed Pulse Laser" :
        ["SVSPL", [22, 0], 2, 60000,
         3, (lambda x, y : svspl_damage(x)), [0, 2, 4, 6],
         "T", 0, 2, 1, ""],
    "(IS) Medium Variable Speed Pulse Laser" :
        ["MVSPL", [56, 0], 2, 200000,
         7, (lambda x, y : mvspl_damage(x)), [0, 2, 5, 9],
         "T", 0, 4, 2, ""],
    "(IS) Large Variable Speed Pulse Laser" :
        ["LVSPL", [123, 0], 2, 465000,
         10, (lambda x, y : lvspl_damage(x)), [0, 4, 8, 15],
         "T", 0, 9, 4, ""],
    "(IS) Small X-Pulse Laser" : ["SXPL", [21, 0], 2, 31000,
                                  3, (lambda x, y : 3), [0, 2, 4, 5],
                                  "T", 0, 1, 1, ""],
    "(IS) Medium X-Pulse Laser" : ["MXPL", [71, 0], 2, 110000,
                                   6, (lambda x, y : 6), [0, 3, 6, 9],
                                   "T", 0, 2, 1, ""],
    "(IS) Large X-Pulse Laser" : ["LXPL", [178, 0], 2, 275000,
                                  14, (lambda x, y : 9), [0, 5, 10, 15],
                                  "T", 0, 7, 2, ""],
    # MM1
    # MM2
    # MM4
    # MM8-IS
    "(CL) Mech Mortar 8" :
        ["Mrtr8", [50, 6], 2, 70000,
         10, (lambda x, y : 2 * calc_average(8, 0)), [6, 7, 14, 21],
         "", 1, 5, 3, ""],
    # ELRM 5
    "(IS) Extended LRM-10" :
        ["ELRM10", [133, 17], 2, 200000,
         6, (lambda x, y : calc_average(10, 0)), [10, 12, 22, 38],
         "", 1, 8, 4, ""],
    # ELRM 15
    "(IS) Extended LRM-20" :
        ["ELRM20", [268, 34], 2, 500000,
         12, (lambda x, y : calc_average(20, 0)), [10, 12, 22, 38],
         "", 1, 18, 8, ""],
    # SLRM5
    "(CL) Streak LRM-10" : ["SLRM10", [173, 22], 2, 225000,
                            2, (lambda x, y : 10), [0, 7, 14, 21],
                            "", 1, 5, 2, ""],
    "(CL) Streak LRM-15" : ["SLRM15", [259, 32], 2, 400000,
                            2.5, (lambda x, y : 15), [0, 7, 14, 21],
                            "", 1, 7, 3, ""],
    # SLRM20
    "(IS) Light PPC + PPC Capacitor" : ["LPPC+", [132, 0], 2, 300000,
                                        10, (lambda x, y : 10), [3, 6, 12, 18],
                                        "T", 0, 4, 3, "X"],
    "(IS) PPC + PPC Capacitor" : ["PPC+", [264, 0], 2, 350000,
                  15, (lambda x, y : 15), [3, 6, 12, 18],
                  "T", 0, 8, 4, "X"],
    "(IS) Heavy PPC + PPC Capacitor" : ["HPPC+", [370, 0], 2, 400000,
                        20, (lambda x, y : 20), [3, 6, 12, 18],
                        "T", 0, 11, 5, "X"],
    "(IS) ER PPC + PPC Capacitor" : ["ERPPC+", [343, 0], 2, 450000,
                     20, (lambda x, y : 15), [0, 7, 14, 23],
                     "T", 0, 8, 4, "X"],
    "(IS) Snub-Nose PPC + PPC Capacitor" :
        ["SNPPC+", [252, 0], 2, 450000,
         15, (lambda x, y : sn_damage(x) + 5), [0, 9, 13, 15],
         "T", 0, 7, 3, "X"],
    "(IS) BattleMech Taser" : ["TSR", [40, 5], 2, 200000,
                               6, (lambda x, y : 1), [0, 1, 2, 4],
                               "", 1, 4, 3, "X"],

    ### Experimental Weapons ###
    "(CL) Rotary AC/2" :
        ["RAC2", [161, 20], 3, 175000,
         6, (lambda x, y : 2 * calc_average(6, 0)), [0, 8, 17, 25],
         "T", 6, 8, 4, ""],
    "(CL) Rotary AC/5" :
        ["RAC5", [345, 43], 3, 275000,
         6, (lambda x, y : 5 * calc_average(6, 0)), [0, 7, 14, 21],
         "T", 6, 10, 8, ""],
    "(IS) Bombast Laser (Insulated)" : ["BmbL", [137, 0], 3, 203000,
                            11, (lambda x, y : 12), [0, 5, 10, 15],
                            "T", 0, 7.5, 4, ""],
   "(IS) Medium Variable Speed Pulse Laser (Insulated)" :
        ["MVSPL", [56, 0], 3, 203000,
         6, (lambda x, y : mvspl_damage(x)), [0, 2, 5, 9],
         "T", 0, 4.5, 3, ""],
    "(CL) Heavy Large Laser (Insulated)" :
        ["HLL", [244, 0], 3, 253000,
         17, (lambda x, y : 16), [0, 5, 10, 15],
         "T", 0, 4.5, 4, ""],
    "(CL) ER Medium Pulse Laser (Insulated)" :
        ["ERMPL", [117, 0], 3, 153000,
         5, (lambda x, y : 7), [0, 5, 9, 14],
         "T", 0, 2.5, 3, ""],
    "(CL) ER Large Pulse Laser (Insulated)" :
        ["ERLPL", [272, 0], 3, 403000,
         12, (lambda x, y : 10), [0, 7, 15, 23],
         "T", 0, 6.5, 4, ""]
    }

class Weapon:
    """
    An individual weapon type
    """
    def __init__(self, key, art4, art5, apollo):
        self.name = key
        self.entry = WEAPONS[key]
        self.batt_val = self.entry[1]
        self.count = 0
        self.countrear = 0
        self.count_la = 0 # We count arm weapons also, to help with BV calcs
        self.count_ra = 0 # and A.E.S.
        self.ammocount = 0
        self.ammo_ton = 0

        # Deal with enhancements, Artemis
        self.enhance = ""
        if (self.entry[7] == "A"):
            if art5 == "TRUE":
                self.enhance = "A5"
            elif art4 == "TRUE":
                self.enhance = "A4"
        # Apollo
        elif (self.entry[7] == "P" and apollo == "TRUE"):
            self.enhance = "AP"
        # Tarcomp, we can not know if one is present right now
        elif (self.entry[7] == "T"):
            self.enhance = "TC"

    def explosive_slots(self):
        """
        Return how many explosive slots a weapon has
        """
        if self.entry[11] == "X":
            return self.entry[10]
        else:
            return 0

    def get_rules_level(self):
        """
        Return rules level
        """
        rule = self.entry[2]
        # Handle artemis & apollo
        if self.enhance == "A4" and rule < 1:
            rule = 1
        elif self.enhance == "A5" and rule < 2:
            rule = 2
        elif self.enhance == "AP" and rule < 2:
            rule = 2
        return rule

    def get_weight(self):
        """
        Return weight
        """
        wgt = self.entry[9]
        if self.enhance == "A5":
            wgt += 1.5
        elif self.enhance == "A4":
            wgt += 1
        elif self.enhance == "AP":
            wgt += 1
        return wgt

    def get_cost(self):
        """
        Return the cost of an item
        """
        cost = self.entry[3]
        if self.enhance == "A5":
            cost += 250000
        elif self.enhance == "A4":
            cost += 100000
        elif self.enhance == "AP":
            cost += 125000
        return cost

    def get_range(self):
        """
        Return maximum (long) range
        """
        return self.entry[6][3]

    def get_med_range(self):
        """
        Return medium range
        """
        return self.entry[6][2]

    def get_short_range(self):
        """
        Return short range
        """
        return self.entry[6][1]

    def get_min_range(self):
        """
        Return minimum range
        """
        return self.entry[6][0]

    def check_range(self, rng):
        """
        Check if in range
        """
        if (rng > self.entry[6][0] and rng <= self.entry[6][3]):
            return True
        else:
            return False

    def get_heat(self):
        """
        Return heat
        """
        return self.entry[4]

    def get_short(self):
        """
        Return short name
        """
        return self.entry[0]

    def count_string(self):
        """
        Return count string with ammo
        """
        report = str(self.count)
        if self.entry[8] > 0:
            report += "/" + str(self.get_ammo_per_weapon())

        return report

    def get_short_count(self):
        """
        Return short name, with weapon and ammo count
        """
        name = self.entry[0].lower() + ":" + str(self.count)
        if self.entry[8] > 0:
            name += "/" + str(self.get_ammo_per_weapon())
            
        return name

    def get_damage(self, rnge):
        """
        Return damage
        """

        # No damage if out of range
        if rnge > self.entry[6][3]:
            return 0

        # Check for cluster adjustments from Artemis & Apollo
        art = 0
        if self.enhance == "A5":
            art = 3
        elif self.enhance == "A4":
            art = 2
        elif self.enhance == "AP":
            art = -1

        return self.entry[5](rnge, art)

    def addone(self, loc):
        """
        Add a normal-front facing weapon
        """
        self.count = self.count + 1
        # Also keep track of arm locations
        if loc == "LA":
            self.count_la = self.count_la + 1
        elif loc == "RA":
            self.count_ra = self.count_ra + 1

    def addone_rear(self):
        """
        Add a rear-facing weapon
        """
        self.countrear = self.countrear + 1

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



