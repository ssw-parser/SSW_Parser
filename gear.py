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
Contains classes for weapons and other gear.
"""

from math import ceil
from error import error_exit
from util import ceil_05, gettext
from item import Item

# A class to contain data about battlemech gear to allow for clearer code,
# by using named class members.

# Weapons in the order of name, BV[main, ammo], range,
# enhancement(A=artemis, T=tarcomp P=apollo),
# year, uses ammo rate?, weight, heat(as used for BV calcs), explosive slots
#
# To be loaded into the gear class
#
# TODO1: IS: Flamer (Vehicle), HMG,  Clan: Flamer (Vehicle)
# TODO2: IS: MG Arrays: 2 HMG, 4 HMG, 2 MG, 3 MG
# Clan: 2 HMG, 2 LMG, 4 LMG, 2 MG, 3 MG
# TODO3: Artemis IV versions
WEAPONS = [["(IS) Autocannon/2", [37, 5], "L", "T", 2300, 1, 6, 1, 0],
           ["(IS) Autocannon/5", [70, 9], "L", "T", 2250, 1, 8, 1, 0],
           ["(IS) Autocannon/10", [123, 15], "M", "T", 2460, 1, 12, 3, 0],
           ["(IS) Autocannon/20", [178, 22], "M", "T", 2500, 1, 14, 7, 0],
           ["(IS) Light Gauss Rifle", [159, 20], "L", "T", 3056, 1, 12, 1, 5],
           ["(IS) Gauss Rifle", [320, 40], "L", "T", 2590, 1, 15, 1, 7],
           ["(IS) Heavy Gauss Rifle", [346, 43], "L", "T", 3061, 1, 18, 2, 11],
           ["(IS) LB 2-X AC", [42, 5], "L", "T", 3058, 1, 6, 1, 0],
           ["(IS) LB 5-X AC", [83, 10], "L", "T", 3058, 1, 8, 1, 0],
           ["(IS) LB 10-X AC", [148, 19], "L", "T", 2595, 1, 11, 2, 0],
           ["(IS) LB 20-X AC", [237, 30], "M", "T", 3058, 1, 14, 6, 0],
           ["(IS) Light AC/2", [30, 4], "L", "T", 3068, 1, 4, 1, 0],
           ["(IS) Light AC/5", [62, 8], "M", "T", 3068, 1, 5, 1, 0],
           ["(IS) Light Machine Gun", [5, 1], "M", "", 3068, 1, 0.5, 0, 0],
           ["(IS) MG Array (2 Light Machine Gun)", [16.7, 1], "M", "", 3068,
            2, 1.5, 0, 0],
           ["(IS) MG Array (3 Light Machine Gun)", [25.05, 1], "M", "", 3068,
            3, 2, 0, 0],
           ["(IS) MG Array (4 Light Machine Gun)", [33.4, 1], "M", "", 3068,
            4, 2.5, 0, 0],
           ["(IS) Machine Gun", [5, 1], "S", "", 1900, 1, 0.5, 0, 0],
           # MG 2
           # MG 3
           ["(IS) MG Array (4 Machine Gun)", [33.4, 1], "S", "", 3068,
            4, 2.5, 0, 0],
           # HMG
           # HMG 2
           ["(IS) MG Array (3 Heavy Machine Gun)", [30.06, 1], "S", "", 3068,
            3, 3.5, 0, 0],
           # HMG 4
           # Nail/rivet
           ["(IS) Rotary AC/2", [118, 15], "L", "T", 3062, 6, 8, 6, 0],
           ["(IS) Rotary AC/5", [247, 31], "M", "T", 3062, 6, 10, 6, 0],
           ["(IS) Ultra AC/2", [56, 7], "L", "T", 3057, 2, 7, 2, 0],
           ["(IS) Ultra AC/5", [112, 14], "L", "T", 2640, 2, 9, 2, 0],
           ["(IS) Ultra AC/10", [210, 26], "L", "T", 3057, 2, 13, 8, 0],
           ["(IS) Ultra AC/20", [281, 35], "M", "T", 3060, 2, 15, 16, 0],
           ["(IS) ER Large Laser", [163, 0], "L", "T", 2620, 0, 5, 12, 0],
           ["(IS) ER Medium Laser", [62, 0], "M", "T", 3058, 0, 1, 5, 0],
           ["(IS) ER Small Laser", [17, 0], "M", "T", 3058, 0, 0.5, 2, 0],
           ["(IS) Flamer", [6, 0], "S", "", 2025, 0, 1, 3, 0],
           # Flamer (Vehicle)
           ["(IS) Large Laser", [123, 0], "M", "T", 2316, 0, 5, 8, 0],
           ["(IS) Medium Laser", [46, 0], "M", "T", 2300, 0, 1, 3, 0],
           ["(IS) Small Laser", [9, 0], "S", "T", 2300, 0, 0.5, 1, 0],
           ["(IS) Plasma Rifle", [210, 26], "M", "T", 3068, 1, 6, 10, 0],
           ["(IS) Light PPC", [88, 0], "L", "T", 3067, 0, 3, 5, 0],
           ["(IS) Light PPC + PPC Capacitor", [132, 0], "L", "T", 3067,
            0, 4, 10, 3],
           ["(IS) PPC", [176, 0], "L", "T", 2460, 0, 7, 10, 0],
           ["(IS) Heavy PPC", [317, 0], "L", "T", 3067, 0, 10, 15, 0],
           ["(IS) ER PPC", [229, 0], "L", "T", 2760, 0, 7, 15, 0],
           ["(IS) Snub-Nose PPC", [165, 0], "M", "T", 3067, 0, 6, 10, 0],
           ["(IS) Snub-Nose PPC + PPC Capacitor", [252, 0], "M", "T", 3067,
            0, 7, 15, 3],
           ["(IS) Large Pulse Laser", [119, 0], "M", "T", 2609, 0, 7, 10, 0],
           ["(IS) Medium Pulse Laser", [48, 0], "M", "T", 2609, 0, 2, 4, 0],
           ["(IS) Small Pulse Laser", [12, 0], "S", "T", 2609, 0, 1, 2, 0],
           ["(IS) LRM-5", [45, 6], "L", "A", 2300, 1, 2, 2, 0],
           ["(IS) LRM-10", [90, 11], "L", "A", 2305, 1, 5, 4, 0],
           ["(IS) LRM-15", [136, 17], "L", "A", 2315, 1, 7, 5, 0],
           ["(IS) LRM-20", [181, 23], "L", "A", 2322, 1, 10, 6, 0],
           ["(IS) MML-3", [29, 4], "L", "A", 3068, 1, 1.5, 2, 0],
           ["(IS) MML-5", [45, 6], "L", "A", 3068, 1, 3, 3, 0],
           ["(IS) MML-7", [67, 8], "L", "A", 3068, 1, 4.5, 4, 0],
           ["(IS) MML-9", [86, 11], "L", "A", 3068, 1, 6, 5, 0],
           ["(IS) MRM-10", [56, 7], "M", "P", 3058, 1, 3, 4, 0],
           ["(IS) MRM-20", [112, 14], "M", "P", 3058, 1, 7, 6, 0],
           ["(IS) MRM-30", [168, 21], "M", "P", 3058, 1, 10, 10, 0],
           ["(IS) MRM-40", [224, 28], "M", "P", 3058, 1, 12, 12, 0],
           ["(IS) Rocket Launcher 10", [18, 0], "L", "", 3064, 0, 0.5, 0.75, 0],
           ["(IS) Rocket Launcher 15", [23, 0], "M", "", 3064, 0, 1, 1, 0],
           ["(IS) Rocket Launcher 20", [24, 0], "M", "", 3064, 0, 1.5, 1.25, 0],
           ["(IS) SRM-2", [21, 3], "M", "A", 2370, 1, 1, 2, 0],
           ["(IS) SRM-4", [39, 5], "M", "A", 2370, 1, 2, 3, 0],
           ["(IS) SRM-6", [59, 7], "M", "A", 2370, 1, 3, 4, 0],
           ["(IS) Streak SRM-2", [30, 4], "M", "", 2647, 1, 1.5, 1, 0],
           ["(IS) Streak SRM-4", [59, 7], "M", "", 3058, 1, 3, 1.5, 0],
           ["(IS) Streak SRM-6", [89, 11], "M", "", 3058, 1, 4.5, 2, 0],
           ["(IS) Streak SRM-2 (OS)", [6, 0], "M", "", 2676, 0, 2, 0.5, 0],
           ["(IS) Narc Missile Beacon", [30, 0], "M", "", 2587, 1, 3, 0, 0],
           ["(IS) iNarc Launcher", [75, 0], "M", "", 3062, 1, 5, 0, 0],
           # Advanced Weapons
           ["(IS) Magshot Gauss Rifle", [15, 2], "M", "T", 3072, 1, 0.5, 1, 2],
           ["(IS) BattleMech Taser", [40, 5], "M", "", 3067, 1, 4, 6, 3],
           ["(IS) Small Variable Speed Pulse Laser", [22, 0], "M", "T", 3070,
            0, 2, 3, 0],
           ["(IS) Medium Variable Speed Pulse Laser", [56, 0], "M", "T", 3070,
            0, 4, 7, 0],
           ["(IS) Large Variable Speed Pulse Laser", [123, 0], "M", "T", 3070,
            0, 9, 10, 0],
           ["(IS) Medium X-Pulse Laser", [71, 0], "M", "T", 3057, 0, 2, 6, 0],
           ["(IS) Large X-Pulse Laser", [178, 0], "M", "T", 3057, 0, 7, 14, 0],
           ["(IS) Binary Laser Cannon", [222, 0], "M", "T", 2812, 0, 9, 16, 0],
           ["(IS) Bombast Laser", [137, 0], "M", "T", 3064, 0, 7, 12, 0],
           ["(IS) Thunderbolt-5", [64, 8], "L", "", 3072, 1, 3, 3, 0],
           ["(IS) Thunderbolt-10", [127, 16], "L", "", 3072, 1, 7, 5, 0],
           ["(IS) Thunderbolt-15", [229, 29], "L", "", 3072, 1, 11, 7, 0],
           ["(IS) Thunderbolt-20", [305, 38], "L", "", 3072, 1, 15, 8, 0],
           ["(IS) Enhanced LRM-5", [52, 7], "L", "A", 3058, 1, 3, 2, 0],
           ["ER Flamer", [16, 0], "M", "", 3067, 0, 1, 4, 0],
           # Clan
           ["(CL) LB 2-X AC", [47, 6], "L", "T", 2826, 1, 5, 1, 0],
           ["(CL) LB 5-X AC", [93, 12], "L", "T", 2825, 1, 7, 1, 0],
           ["(CL) LB 10-X AC", [148, 19], "L", "T", 2595, 1, 10, 2, 0],
           ["(CL) LB 20-X AC", [237, 30], "M", "T", 2826, 1, 12, 6, 0],
           ["(CL) Ultra AC/2", [62, 8], "L", "T", 2827, 2, 5, 2, 0],
           ["(CL) Ultra AC/5", [122, 15], "L", "T", 2640, 2, 7, 2, 0],
           ["(CL) Ultra AC/10", [210, 26], "L", "T", 2825, 2, 10, 6, 0],
           ["(CL) Ultra AC/20", [335, 42], "M", "T", 2825, 2, 12, 14, 0],
           ["(CL) AP Gauss Rifle", [21, 3], "M", "T", 3069, 1, 0.5, 1, 1],
           ["(CL) Gauss Rifle", [320, 40], "L", "T", 2590, 1, 12, 1, 6],
           ["(CL) Hyper Assault Gauss 20", [267, 33], "L", "T", 3068,
            1, 10, 4, 6],
           ["(CL) Hyper Assault Gauss 30", [401, 50], "L", "T", 3068,
            1, 13, 6, 8],
           ["(CL) Hyper Assault Gauss 40", [535, 67], "L", "T", 3069,
            1, 16, 8, 10],
           ["(CL) Light Machine Gun", [5, 1], "M", "", 3060, 1, 0.25, 0, 0],
           # LMG 2
           ["(CL) MG Array (3 Light Machine Gun)", [25.05, 1], "M", "", 3069,
            3, 1, 0, 0],
           # LMG 4
           ["(CL) Machine Gun", [5, 1], "S", "", 1900, 1, 0.25, 0, 0],
           # MG 2
           # MG 3
           ["(CL) MG Array (4 Machine Gun)", [33.4, 1], "S", "", 3069,
            4, 1.25, 0, 0],
           ["(CL) Heavy Machine Gun", [6, 1], "S", "", 3059, 1, 0.5, 0, 0],
           # HMG 2
           ["(CL) MG Array (3 Heavy Machine Gun)", [30.06, 1], "S", "", 3069,
            3, 1.75, 0, 0],
           ["(CL) MG Array (4 Heavy Machine Gun)", [40.08, 1], "S", "", 3069,
            4, 2.25, 0, 0],
           ["(CL) Flamer", [6, 0], "S", "", 2025, 0, 0.5, 3, 0],
           # Flamer (Vehicle)
           ["(CL) ER Micro Laser", [7, 0], "M", "T", 3060, 0, 0.25, 1, 0],
           ["(CL) ER Small Laser", [31, 0], "M", "T", 2825, 0, 0.5, 2, 0],
           ["(CL) ER Medium Laser", [108, 0], "M", "T", 2824, 0, 1, 5, 0],
           ["(CL) ER Large Laser", [248, 0], "L", "T", 2620, 0, 4, 12, 0],
           ["(CL) Micro Pulse Laser", [12, 0], "S", "T", 3060, 0, 0.5, 1, 0],
           ["(CL) Small Pulse Laser", [24, 0], "M", "T", 2609, 0, 1, 2, 0],
           ["(CL) Medium Pulse Laser", [111, 0], "M", "T", 2609, 0, 2, 4, 0],
           ["(CL) Large Pulse Laser", [265, 0], "L", "T", 2609, 0, 6, 10, 0],
           ["(CL) Heavy Small Laser", [15, 0], "S", "T", 3059, 0, 0.5, 3, 0],
           ["(CL) Heavy Medium Laser", [76, 0], "M", "T", 3059, 0, 1, 7, 0],
           ["(CL) Heavy Large Laser", [244, 0], "M", "T", 3059, 0, 4, 18, 0],
           ["(CL) Plasma Cannon", [170, 21], "L", "T", 3069, 1, 3, 7, 0],
           ["(CL) ER PPC", [412, 0], "L", "T", 2760, 0, 6, 15, 0],
           ["(CL) ATM-3", [53, 14], "M", "", 3054, 1, 1.5, 2, 0],
           ["(CL) ATM-6", [105, 26], "M", "", 3054, 1, 3.5, 4, 0],
           ["(CL) ATM-9", [147, 36], "M", "", 3054, 1, 5, 6, 0],
           ["(CL) ATM-12", [212, 52], "M", "", 3055, 1, 7, 8, 0],
           ["(CL) LRM-5", [55, 7], "L", "A", 2400, 1, 1, 2, 0],
           ["(CL) LRM-10", [109, 14], "L", "A", 2400, 1, 2.5, 4, 0],
           ["(CL) LRM-15", [164, 21], "L", "A", 2400, 1, 3.5, 5, 0],
           ["(CL) LRM-20", [220, 27], "L", "A", 2400, 1, 5, 6, 0],
           ["(CL) SRM-2", [21, 3], "M", "A", 2370, 1, 0.5, 2, 0],
           ["(CL) SRM-4", [39, 5], "M", "A", 2370, 1, 1, 3, 0],
           ["(CL) SRM-6", [59, 7], "M", "A", 2370, 1, 1.5, 4, 0],
           ["(CL) Streak SRM-2", [40, 5], "M", "", 2647, 1, 1, 1, 0],
           ["(CL) Streak SRM-4", [79, 10], "M", "", 2826, 1, 2, 1.5, 0],
           ["(CL) Streak SRM-6", [118, 15], "M", "", 2826, 1, 3, 2, 0],
           ["(CL) Streak SRM-4 (OS)", [16, 0], "M", "", 2826, 0, 2.5, 0.75, 0],
           ["(CL) Narc Missile Beacon", [30, 0], "M", "", 2587, 1, 2, 0, 0],
           # Advanced Weapons
           ["(CL) Rotary AC/2", [161, 20], "L", "T", 3073, 6, 8, 6, 0],
           ["(CL) Rotary AC/5", [345, 43], "L", "T", 3073, 6, 10, 6, 0],
           ["(CL) Protomech AC/4", [49, 6], "M", "T", 3073, 1, 4.5, 1, 0],
           ["(CL) Improved Heavy Medium Laser", [93, 0], "M", "T", 3069,
            0, 1, 7, 2],
           ["(CL) ER Medium Pulse Laser", [117, 0], "M", "T", 3057, 0, 2, 6, 0],
           ["(CL) ER Small Pulse Laser", [36, 0], "M", "T", 3057, 0, 1.5, 3, 0],
           ["(CL) Streak LRM-10", [173, 22], "L", "", 3057, 1, 5, 2, 0],
           ["(CL) Mech Mortar 8", [50, 6], "L", "", 2840, 1, 5, 10, 0],
           # Artillery
           ["(IS) Arrow IV Missile", [240, 30], "L", "", 2600, 1, 15, 10, 0],
           ["(CL) Arrow IV Missile", [240, 30], "L", "", 2600, 1, 12, 10, 0],
           ["(IS) Sniper", [85, 11], "L", "", 1900, 1, 20, 10, 0]]


# Ammo
#
# Name, weapon, ammount, weight, explosive?
#
# TODO: Vehicle flamer
# TODO: Advanced weapons
AMMO = [["(IS) @ AC/2", ["(IS) Autocannon/2"], 45, 1, "X"],
        ["(IS) @ AC/5", ["(IS) Autocannon/5"], 20, 1, "X"],
        ["(IS) @ AC/10", ["(IS) Autocannon/10"], 10, 1, "X"],
        ["(IS) @ AC/20", ["(IS) Autocannon/20"], 5, 1, "X"],
        ["(IS) @ Light Gauss Rifle", ["(IS) Light Gauss Rifle"], 16, 1, ""],
        ["@ Gauss Rifle", ["(IS) Gauss Rifle", "(CL) Gauss Rifle"], 8, 1, ""],
        ["(IS) @ Heavy Gauss Rifle", ["(IS) Heavy Gauss Rifle"], 4, 1, ""],
        ["(IS) @ LB 2-X AC (Slug)", ["(IS) LB 2-X AC"], 45, 1, "X"],
        ["(IS) @ LB 5-X AC (Slug)", ["(IS) LB 5-X AC"], 20, 1, "X"],
        ["(IS) @ LB 5-X AC (Cluster)", ["(IS) LB 5-X AC"], 20, 1, "X"],
        ["(IS) @ LB 10-X AC (Slug)", ["(IS) LB 10-X AC"], 10, 1, "X"],
        ["(IS) @ LB 10-X AC (Cluster)", ["(IS) LB 10-X AC"], 10, 1, "X"],
        ["(IS) @ LB 20-X AC (Slug)", ["(IS) LB 20-X AC"], 5, 1, "X"],
        ["(IS) @ LB 20-X AC (Cluster)", ["(IS) LB 20-X AC"], 5, 1, "X"],
        ["(IS) @ Light AC/2", ["(IS) Light AC/2"], 45, 1, "X"],
        ["(IS) @ Light AC/5", ["(IS) Light AC/5"], 20, 1, "X"],
        ["@ Light Machine Gun",
         ["(IS) Light Machine Gun", "(CL) Light Machine Gun",
          "(IS) MG Array (2 Light Machine Gun)",
          "(IS) MG Array (3 Light Machine Gun)",
          "(IS) MG Array (4 Light Machine Gun)",
          "(CL) MG Array (3 Light Machine Gun)"], 200, 1, "X"],
        ["@ Light Machine Gun (1/2)",
         ["(IS) Light Machine Gun", "(CL) Light Machine Gun",
          "(IS) MG Array (2 Light Machine Gun)",
          "(IS) MG Array (3 Light Machine Gun)",
          "(IS) MG Array (4 Light Machine Gun)",
          "(CL) MG Array (3 Light Machine Gun)"], 100, 0.5, "X"],
        ["@ Machine Gun",
         ["(IS) Machine Gun", "(CL) Machine Gun",
          "(IS) MG Array (4 Machine Gun)",
          "(CL) MG Array (4 Machine Gun)"], 200, 1, "X"],
        ["@ Machine Gun (1/2)",
         ["(IS) Machine Gun", "(CL) Machine Gun",
          "(IS) MG Array (4 Machine Gun)",
          "(CL) MG Array (4 Machine Gun)"], 100, 0.5, "X"],
        ["@ Heavy Machine Gun",
         ["(CL) Heavy Machine Gun",
          "(IS) MG Array (3 Heavy Machine Gun)",
          "(CL) MG Array (3 Heavy Machine Gun)",
          "(CL) MG Array (4 Heavy Machine Gun)"], 100, 1, "X"],
       ["@ Heavy Machine Gun (1/2)",
         ["(CL) Heavy Machine Gun",
          "(IS) MG Array (3 Heavy Machine Gun)",
          "(CL) MG Array (3 Heavy Machine Gun)",
          "(CL) MG Array (4 Heavy Machine Gun)"], 50, 0.5, "X"],
        ["(IS) @ Rotary AC/2", ["(IS) Rotary AC/2"], 45, 1, "X"],
        ["(IS) @ Rotary AC/5", ["(IS) Rotary AC/5"], 20, 1, "X"],
        ["(IS) @ Ultra AC/2", ["(IS) Ultra AC/2"], 45, 1, "X"],
        ["(IS) @ Ultra AC/5", ["(IS) Ultra AC/5"], 20, 1, "X"],
        ["(IS) @ Ultra AC/10", ["(IS) Ultra AC/10"], 10, 1, "X"],
        ["(IS) @ Ultra AC/20", ["(IS) Ultra AC/20"], 5, 1, "X"],
        ["(IS) @ Plasma Rifle", ["(IS) Plasma Rifle"], 10, 1, ""],
        ["(IS) @ LRM-5", ["(IS) LRM-5"], 24, 1, "X"],
        ["(IS) @ LRM-10", ["(IS) LRM-10"], 12, 1, "X"],
        ["(IS) @ LRM-15", ["(IS) LRM-15"], 8, 1, "X"],
        ["(IS) @ LRM-20", ["(IS) LRM-20"], 6, 1, "X"],
        ["(IS) @ LRM-5 (Artemis IV Capable)", ["(IS) LRM-5"], 24, 1, "X"],
        ["(IS) @ LRM-10 (Artemis IV Capable)", ["(IS) LRM-10"], 12, 1, "X"],
        ["(IS) @ LRM-15 (Artemis IV Capable)", ["(IS) LRM-15"], 8, 1, "X"],
        ["(IS) @ LRM-20 (Artemis IV Capable)", ["(IS) LRM-20"], 6, 1, "X"],
        ["(IS) @ LRM-15 (Narc Capable)", ["(IS) LRM-15"], 8, 1, "X"],
        ["(IS) @ MML-3 (LRM)", ["(IS) MML-3"], 40, 1, "X"],
        ["(IS) @ MML-3 (SRM)", ["(IS) MML-3"], 33, 1, "X"],
        ["(IS) @ MML-5 (LRM)", ["(IS) MML-5"], 24, 1, "X"],
        ["(IS) @ MML-5 (SRM)", ["(IS) MML-5"], 20, 1, "X"],
        ["(IS) @ MML-7 (LRM)", ["(IS) MML-7"], 17, 1, "X"],
        ["(IS) @ MML-7 (SRM)", ["(IS) MML-7"], 14, 1, "X"],
        ["(IS) @ MML-9 (LRM)", ["(IS) MML-9"], 13, 1, "X"],
        ["(IS) @ MML-9 (SRM)", ["(IS) MML-9"], 11, 1, "X"],
        ["(IS) @ MML-3 (LRM Artemis IV Capable)", ["(IS) MML-3"], 40, 1, "X"],
        ["(IS) @ MML-3 (SRM Artemis IV Capable)", ["(IS) MML-3"], 33, 1, "X"],
        ["(IS) @ MML-5 (LRM Artemis IV Capable)", ["(IS) MML-5"], 24, 1, "X"],
        ["(IS) @ MML-5 (SRM Artemis IV Capable)", ["(IS) MML-5"], 20, 1, "X"],
        ["(IS) @ MML-7 (LRM Artemis IV Capable)", ["(IS) MML-7"], 17, 1, "X"],
        ["(IS) @ MML-7 (SRM Artemis IV Capable)", ["(IS) MML-7"], 14, 1, "X"],
        ["(IS) @ MML-9 (LRM Artemis IV Capable)", ["(IS) MML-9"], 13, 1, "X"],
        ["(IS) @ MML-9 (SRM Artemis IV Capable)", ["(IS) MML-9"], 11, 1, "X"],
        ["(IS) @ MRM-10", ["(IS) MRM-10"], 24, 1, "X"],
        ["(IS) @ MRM-20", ["(IS) MRM-20"], 12, 1, "X"],
        ["(IS) @ MRM-30", ["(IS) MRM-30"], 8, 1, "X"],
        ["(IS) @ MRM-40", ["(IS) MRM-40"], 6, 1, "X"],
        ["@ SRM-2", ["(IS) SRM-2", "(CL) SRM-2"], 50, 1, "X"],
        ["@ SRM-4", ["(IS) SRM-4", "(CL) SRM-4"], 25, 1, "X"],
        ["@ SRM-6", ["(IS) SRM-6", "(CL) SRM-6"], 15, 1, "X"],
        ["@ SRM-6 (Artemis IV Capable)",
         ["(IS) SRM-6", "(CL) SRM-6"], 15, 1, "X"],
        ["@ SRM-4 (Narc Capable)", ["(IS) SRM-4", "(CL) SRM-4"], 25, 1, "X"],
        ["@ SRM-6 (Narc Capable)", ["(IS) SRM-6", "(CL) SRM-6"], 15, 1, "X"],
        ["(IS) @ Streak SRM-2", ["(IS) Streak SRM-2"], 50, 1, "X"],
        ["(IS) @ Streak SRM-4", ["(IS) Streak SRM-4"], 25, 1, "X"],
        ["(IS) @ Streak SRM-6", ["(IS) Streak SRM-6"], 15, 1, "X"],
        ["(IS) @ Narc (Homing)", ["(IS) Narc Missile Beacon"], 6, 1, "X"],
        ["(IS) @ iNarc (Homing)", ["(IS) iNarc Launcher"], 4, 1, "X"],
        ["(IS) @ Anti-Missile System",
         ["(IS) Anti-Missile System"], 12, 1, "X"],
        # Advanced
        ["(IS) @ Magshot Gauss Rifle", ["(IS) Magshot Gauss Rifle"], 50, 1, ""],
        ["(IS) @ BattleMech Taser", ["(IS) BattleMech Taser"], 5, 1, "X"],
        ["(IS) @ Thunderbolt-5", ["(IS) Thunderbolt-5"], 12, 1, "X"],
        ["(IS) @ Thunderbolt-10", ["(IS) Thunderbolt-10"], 6, 1, "X"],
        ["(IS) @ Thunderbolt-15", ["(IS) Thunderbolt-15"], 4, 1, "X"],
        ["(IS) @ Thunderbolt-20", ["(IS) Thunderbolt-20"], 3, 1, "X"],
        ["(IS) @ NLRM-5", ["(IS) Enhanced LRM-5"], 24, 1, "X"],
        # Clan
        ["(CL) @ LB 2-X AC (Slug)", ["(CL) LB 2-X AC"], 45, 1, "X"],
        ["(CL) @ LB 2-X AC (Cluster)", ["(CL) LB 2-X AC"], 45, 1, "X"],
        ["(CL) @ LB 5-X AC (Slug)", ["(CL) LB 5-X AC"], 20, 1, "X"],
        ["(CL) @ LB 5-X AC (Cluster)", ["(CL) LB 5-X AC"], 20, 1, "X"],
        ["(CL) @ LB 10-X AC (Slug)", ["(CL) LB 10-X AC"], 10, 1, "X"],
        ["(CL) @ LB 10-X AC (Cluster)", ["(CL) LB 10-X AC"], 10, 1, "X"],
        ["(CL) @ LB 20-X AC (Slug)", ["(CL) LB 20-X AC"], 5, 1, "X"],
        ["(CL) @ LB 20-X AC (Cluster)", ["(CL) LB 20-X AC"], 5, 1, "X"],
        ["(CL) @ Ultra AC/2", ["(CL) Ultra AC/2"], 45, 1, "X"],
        ["(CL) @ Ultra AC/5", ["(CL) Ultra AC/5"], 20, 1, "X"],
        ["(CL) @ Ultra AC/10", ["(CL) Ultra AC/10"], 10, 1, "X"],
        ["(CL) @ Ultra AC/20", ["(CL) Ultra AC/20"], 5, 1, "X"],
        ["(CL) @ AP Gauss Rifle", ["(CL) AP Gauss Rifle"], 40, 1, ""],
        ["(CL) @ Hyper Assault Gauss 20",
         ["(CL) Hyper Assault Gauss 20"], 6, 1, ""],
        ["(CL) @ Hyper Assault Gauss 30",
         ["(CL) Hyper Assault Gauss 30"], 4, 1, ""],
        ["(CL) @ Hyper Assault Gauss 40",
         ["(CL) Hyper Assault Gauss 40"], 3, 1, ""],
        ["(CL) @ Plasma Cannon", ["(CL) Plasma Cannon"], 10, 1, ""],
        ["(CL) @ ATM-3", ["(CL) ATM-3"], 20, 1, "X"],
        ["(CL) @ ATM-3 (ER)", ["(CL) ATM-3"], 20, 1, "X"],
        ["(CL) @ ATM-3 (HE)", ["(CL) ATM-3"], 20, 1, "X"],
        ["(CL) @ ATM-6", ["(CL) ATM-6"], 10, 1, "X"],
        ["(CL) @ ATM-6 (ER)", ["(CL) ATM-6"], 10, 1, "X"],
        ["(CL) @ ATM-6 (HE)", ["(CL) ATM-6"], 10, 1, "X"],
        ["(CL) @ ATM-9", ["(CL) ATM-9"], 7, 1, "X"],
        ["(CL) @ ATM-9 (ER)", ["(CL) ATM-9"], 7, 1, "X"],
        ["(CL) @ ATM-9 (HE)", ["(CL) ATM-9"], 7, 1, "X"],
        ["(CL) @ ATM-12", ["(CL) ATM-12"], 5, 1, "X"],
        ["(CL) @ ATM-12 (ER)", ["(CL) ATM-12"], 5, 1, "X"],
        ["(CL) @ ATM-12 (HE)", ["(CL) ATM-12"], 5, 1, "X"],
        ["(CL) @ LRM-5", ["(CL) LRM-5"], 24, 1, "X"],
        ["(CL) @ LRM-10", ["(CL) LRM-10"], 12, 1, "X"],
        ["(CL) @ LRM-15", ["(CL) LRM-15"], 8, 1, "X"],
        ["(CL) @ LRM-20", ["(CL) LRM-20"], 6, 1, "X"],
        ["(CL) @ LRM-10 (Artemis IV Capable)", ["(CL) LRM-10"], 12, 1, "X"],
        ["(CL) @ LRM-15 (Artemis IV Capable)", ["(CL) LRM-15"], 8, 1, "X"],
        ["(CL) @ LRM-20 (Artemis IV Capable)", ["(CL) LRM-20"], 6, 1, "X"],
        ["(CL) @ LRM-15 (Artemis V)", ["(CL) LRM-15"], 8, 1, "X"],        
        ["(CL) @ LRM-20 (Artemis V)", ["(CL) LRM-20"], 6, 1, "X"],        
        ["(CL) @ Streak SRM-2", ["(CL) Streak SRM-2"], 50, 1, "X"],
        ["(CL) @ Streak SRM-4", ["(CL) Streak SRM-4"], 25, 1, "X"],
        ["(CL) @ Streak SRM-6", ["(CL) Streak SRM-6"], 15, 1, "X"],
        ["(CL) @ Narc (Homing)", ["(CL) Narc Missile Beacon"], 6, 1, "X"],
        ["(CL) @ Anti-Missile System",
         ["(CL) Anti-Missile System"], 24, 1, "X"],
        # Advanced
        ["(CL) @ Rotary AC/2", ["(CL) Rotary AC/2"], 45, 1, "X"],
        ["(CL) @ Rotary AC/5", ["(CL) Rotary AC/5"], 20, 1, "X"],
        ["(CL) @ Protomech AC/4", ["(CL) Protomech AC/4"], 20, 1, "X"],
        ["(CL) @ Streak LRM-10", ["(CL) Streak LRM-10"], 12, 1, "X"],
        ["(CL) @ 'Mech Mortar 8 (Anti-Personnel)",
         ["(CL) Mech Mortar 8"], 4, 1, "X"],
        # Artillery
        ["(IS) @ Arrow IV (Non-Homing)", ["(IS) Arrow IV Missile"], 5, 1, "X"],
        ["(IS) @ Arrow IV (Homing)", ["(IS) Arrow IV Missile"], 5, 1, "X"],
        ["(CL) @ Arrow IV (Homing)", ["(CL) Arrow IV Missile"], 5, 1, "X"],
        ["@ Sniper", ["(IS) Sniper"], 10, 1, "X"]]

# Equipment, spilt into offensive, and defensive
#
# Name, BV, year, uses ammo rate, weight, explosive slots
#
O_EQUIPMENT = [["C3 Computer (Slave)", [0, 0], 3050, 0, 1, 0],
               ["C3 Computer (Master)", [0, 0], 3050, 0, 5, 0],
               ["Improved C3 Computer", [0, 0], 3062, 0, 2.5, 0],
               ["TAG", [0, 0], 2600, 0, 1, 0],
               ["Light TAG", [0, 0], 3054, 0, 0.5, 0],
               ["Cargo, Liquid", [0, 0], 1900, 0, 1, 0],
               # Experimental
               ["Collapsible Command Module (CCM)", [0, 0], 2710, 0, 16, 0],
               ["Coolant Pod", [0, 0], 3049, 0, 1, 1]]


D_EQUIPMENT = [["A-Pod", [1, 0], 3055, 0, 0.5, 0],
               ["B-Pod", [2, 0], 3069, 0, 1, 0],
               ["(IS) Anti-Missile System", [32, 11], 2617, 1, 0.5, 0],
               ["Guardian ECM Suite", [61, 0], 2597, 0, 1.5, 0],
               ["Beagle Active Probe", [10, 0], 2576, 0, 1.5, 0],
               ["ECM Suite", [61, 0], 2597, 0, 1, 0], # Clan
               ["Active Probe", [12, 0], 2576, 0, 1, 0], # Clan
               ["Light Active Probe", [7, 0], 2576, 0, 0.5, 0], # No year found
               ["(CL) Anti-Missile System", [32, 22], 2617, 1, 0.5, 0],
               ["CASE", [0, 0], 2476, 0, 0.5, 0], # HACK: CASE
               # Experimental
               ["Angel ECM", [100, 0], 3057, 0, 2, 0],
               ["Bloodhound Active Probe", [25, 0], 3058, 0, 2, 0],
               ["Electronic Warfare Equipment", [39, 0], 3025, 0, 7.5, 0],
               ["(CL) Laser Anti-Missile System", [45, 0], 3048, 0, 1, 0],
               ["(IS) CASE II", [0, 0], 3064, 0, 1, 0],
               ["(CL) CASE II", [0, 0], 3062, 0, 0.5, 0]]

D_PHYSICAL = [["Small Shield", [50, 0], 3067, 0, 2, 0]]

# Targeting computers, currently not used
#
# TODO: fix this
TARCOMPS = [["(IS) Targeting Computer", 0, 3062, 0],
            ["(CL) Targeting Computer", 0, 2860, 0]]

# Info on heatsink types
#
# Name, techbase, year, sinking capability, rules level
#
# Where techbase 0 = IS, 1 = Clan, 2 = Both, 10 = unknown
# Where rules level is 0 = intro, 1 = TL, 2 = advanced, 3 = experimental
#
HEATSINK = [["Single Heat Sink", 2, 2022, 1, 0],
            ["Double Heat Sink", 0, 2567, 2, 1],
            ["Double Heat Sink", 1, 2567, 2, 1],
            ["Laser Heat Sink", 1, 3051, 2, 2]]

# Not used.
MISSILE_ENCH = [["Artemis IV", 2598],
                ["Apollo", 3071]]

# Melee weapons
#
# Name, year, BV multiplier, damage formula, weight
#
PHYSICAL = [["Hatchet", 3022, 1.5, (lambda x : ceil(x / 5.0)),
             (lambda x : ceil(x / 15.0))],
            ["Sword", 3058, 1.725, (lambda x : ceil(x / 10.0) + 1),
             (lambda x : ceil_05(x / 20.0))],
            ["Retractable Blade", 2420, 1.725, (lambda x : ceil(x / 10.0)),
             (lambda x : ceil_05(x / 2.0) + 0.5)], 
            ["Claws", 3060, 1.275, (lambda x : ceil(x / 7.0)),
             (lambda x : ceil(x / 15.0))],
            ["Mace", 3061, 1.0, (lambda x : ceil(x / 4.0)),
             (lambda x : ceil(x / 10.0))],
            ["Lance", 3064, 1.0, (lambda x : ceil(x / 5.0)),
             (lambda x : ceil_05(x / 20.0))],
            # Hack: Divide Talons BV multiplier by 2, because it is one item
            # being split up into two
            ["Talons", 3072, 1.0, (lambda x : ceil(x / 5.0) / 2.0),
             (lambda x : ceil(x / 15.0))]]


class Heatsinks(Item):
    """
    Heatsinks for a mech
    """
    def __init__(self, hstype, tech_b, number):
        self.type = hstype
        self.tech_b = int(tech_b)
        self.number = number

        # Check for heatsink type, save data
        ident = False
        for i in HEATSINK:
            if (i[0] == self.type and i[1] == self.tech_b):
                ident = True
                self.year = i[2]
                self.cap = i[3]
                self.r_level = i[4]
        if not ident:
            error_exit((self.type, self.tech_b))

    def get_type(self):
        """
        Return heat-sink type
        """
        return self.type

    def get_rules_level(self):
        """
        Return heat-sink rules level
        0 = intro, 1 = tournament legal, 2 = advanced, 3 = experimental
        """
        return self.r_level

    def get_year(self):
        """
        Return earliest year heatsink is available
        """
        return self.year

    def get_weight(self):
        """
        Return heatsink weight
        1 ton/sink, 10 free
        """
        return self.number - 10

    def get_sink(self):
        """
        Return sinking capability
        """
        return self.number * self.cap


class Equip:
    """
    The new equipment class being tested out
    """
    # TODO: Make a real item
    # TODO: Make this a parent class, and split according to type?
    def __init__(self, node):
        nnode = node.getElementsByTagName("name")[0]
        self.name = gettext(nnode.childNodes)
        tnode = node.getElementsByTagName("type")[0]
        self.typ = gettext(tnode.childNodes)
        self.rear = False
        self.turret = False
        lnd = node.getElementsByTagName("location")
        # Normal case, no split
        if (lnd):
            lnode = lnd[0]
            self.loc = gettext(lnode.childNodes)
        # Split location
        else:
            self.loc = []
        lnd = node.getElementsByTagName("splitlocation")
        for lnode in lnd:
            lnr = int(lnode.attributes["number"].value)
            loc_temp = gettext(lnode.childNodes)
            self.loc.append((loc_temp, lnr))
        # Check for rear-mounted stuff
        if self.name[0:4] == "(R) ":
            self.rear = True
            self.name = self.name[4:]
        # Hack -- also check for turreted
        elif self.name[0:4] == "(T) ":
            self.turret = True
            self.name = self.name[4:]



class Weaponlist:
    """
    Store the list with weapons
    """
    def __init__(self):
        self.list = []
        for weap in WEAPONS:
            self.list.append(Weapon(weap))

class Weapon:
    """
    An individual weapon type
    """
    def __init__(self, ginfo):
        self.name = ginfo[0]
        self.batt_val = ginfo[1]
        self.range = ginfo[2]
        self.enhance = ginfo[3]
        self.year = ginfo[4]
        self.useammo = ginfo[5]
        self.weight = ginfo[6]
        self.heat = ginfo[7]
        self.explosive = ginfo[8]
        self.count = 0
        self.countrear = 0
        self.countarm = 0 # We count arm weapons also, to help with BV calcs
        self.ammocount = 0
        self.ammo_ton = 0

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

    def get_bv(self, tarcomp, art4, art5, apollo):
        """
        Get the BV of an INDIVIDUAL weapon, not all of them
        """
        batt_val = self.batt_val[0]
        if (tarcomp > 0 and self.enhance == "T"):
            batt_val *= 1.25
        if (art4 == "TRUE" and self.enhance == "A"):
            batt_val *= 1.2
        elif (art5 == "TRUE" and self.enhance == "A"):
            batt_val *= 1.3
        if (apollo == "TRUE" and self.enhance == "P"):
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


class Ammolist:
    """
    Store the list with weapon types
    """
    def __init__(self):
        self.list = []
        for ammo in AMMO:
            self.list.append(Ammo(ammo))

class Ammo:
    """
    An individual ammo type
    """
    def __init__(self, ginfo):
        self.name = ginfo[0]
        self.wname = ginfo[1]
        self.amount = ginfo[2]
        self.weight = ginfo[3]
        self.explosive = ginfo[4]
        self.count = 0

    def addone(self):
        """
        Add one ammo item
        """
        self.count = self.count + 1

class OffEquiplist:
    """
    Store the list with offensive equipment types
    """
    def __init__(self):
        self.list = []
        for equip in O_EQUIPMENT:
            self.list.append(Equipment(equip))

class DefEquiplist:
    """
    Store the list with defensive equipment types
    """
    def __init__(self):
        self.list = []
        for equip in D_EQUIPMENT:
            self.list.append(Equipment(equip))

class Equipment:
    """
    An equipment type
    """
    def __init__(self, ginfo):
        self.name = ginfo[0]
        self.batt_val = ginfo[1]
        self.year = ginfo[2]
        self.useammo = ginfo[3]
        self.weight = ginfo[4]
        self.explosive = ginfo[5]
        self.count = 0
        self.ammocount = 0
        self.ammo_ton = 0

    def addone(self):
        """
        Add one piece of equipment
        """
        self.count = self.count + 1

    # We need to track tonnage and rounds separately due to BV
    # calculations and how MML ammo works
    def add_ammo(self, count, amount):
        """
        Add ammo to equipment
        """
        self.ammocount = self.ammocount + amount
        self.ammo_ton += count

class Physicallist:
    """
    Store list with physical weapons
    """
    def __init__(self):
        self.list = []
        for phys in PHYSICAL:
            self.list.append(Physical(phys))
        self.name = "physcial"

class DefPhysicallist:
    """
    Store list with defensive physical items
    """
    def __init__(self):
        self.list = []
        for phys in D_PHYSICAL:
            self.list.append(Equipment(phys))
        self.name = "physcial"

class Physical:
    """
    A individual physical weapon type
    """
    def __init__(self, pinfo):
        self.name = pinfo[0]
        self.year = pinfo[1]
        self.bv_mult = pinfo[2]
        self.dam = pinfo[3]
        self.weight = pinfo[4]
        self.count = 0

    def addone(self):
        """
        Add a physical weapon
        """
        self.count = self.count + 1

    def get_bv(self, weight):
        """
        Get BV of physical weapon
        """
        return self.dam(weight) * self.bv_mult

class Gear:
    """
    Store Gear

    Take in lists of front and rear facing gears
    """
    def __init__(self, weight, art4, art5, apollo, equip, equiprear, clan_case):
        self.art4 = art4 # Artemis IV
        self.art5 = art5 # Artemis V
        self.apollo = apollo # Apollo
        self.equip = equip
        self.equiprear = equiprear
        self.cc = clan_case # Clan CASE

        # We need to create local lists for avoid trouble with Omni-mechs
        self.weaponlist = Weaponlist()
        self.o_equiplist = OffEquiplist()
        self.d_equiplist = DefEquiplist()
        self.physicallist = Physicallist()
        self.d_physicallist = DefPhysicallist()
        self.ammolist = Ammolist()
        # Keep track of tarcomp
        self.tarcomp = 0
        # Mech has a physical weapon?
        self.phys = 0
        # Gear weight
        self.w_weight = 0.0
        self.a_weight = 0.0
        self.o_weight = 0.0
        self.d_weight = 0.0
        self.p_weight = 0.0
        # Weight of targeting computer weapons
        self.tcw_weight = 0.0
        # Track explosive ammo by locations
        self.exp_ammo = {}
        self.exp_weapon = {}
        self.case = {}
        # Track coolant pods
        self.coolant = 0
        self.has_narc = False
        self.has_tag = False
        self.has_c3 = False
        self.has_c3m = False
        self.has_c3i = False
        self.supercharger = False
        # Track LRM tubes (IS, Clan, NLRM, MMLs)
        # no ATMs, no streaks and no ELRMs
        # only launchers that can use special ammo
        self.lrms = 0

        ### Count gear ###
        for name in self.equip:
            ### Weapons ###
            # Go through weapon list
            ident = False
            for weap in self.weaponlist.list:
                # Weapon identified
                if name[0] == weap.name:
                    # Add weapon
                    weap.addone()

                    # Arm weapons
                    if name[2] == "RA" or name[2] == "LA":
                        weap.addone_arm()

                    # track weapons weight
                    self.w_weight += weap.weight
                    # track weight for targeting computer
                    if weap.enhance == "T":
                        self.tcw_weight += weap.weight

                    # We have found a valid weapon
                    ident = True

                    # Missile fire control systems require extra weight
                    # Artemis IV
                    if (self.art4 == "TRUE" and weap.enhance == "A"):
                        self.w_weight += 1
                    # Artemis V
                    elif (self.art5 == "TRUE" and weap.enhance == "A"):
                        self.w_weight += 1.5
                    # Apollo
                    if (self.apollo == "TRUE" and weap.enhance == "P"):
                        self.w_weight += 1
                    # Hack - track Narc
                    if (name[0] == "(IS) Narc Missile Beacon" or
                        name[0] == "(IS) iNarc Launcher" or
                        name[0] == "(CL) Narc Missile Beacon"):
                        self.has_narc = True

                    # Count LRM tubes that can fire special ammo
                    # Missing: NLRM-10, NLRM-15, NLRM-20
                    if name[0] == "(IS) MML-3":
                        self.lrms += 3

                    if (name[0] == "(IS) LRM-5" or name[0] == "(CL) LRM-5" or
                        name[0] == "(IS) MML-5" or
                        name[0] == "(IS) Enhanced LRM-5"):
                        self.lrms += 5

                    if name[0] == "(IS) MML-7":
                        self.lrms += 7

                    if name[0] == "(IS) MML-9":
                        self.lrms += 9

                    if name[0] == "(IS) LRM-10" or name[0] == "(CL) LRM-10":
                        self.lrms += 10

                    if name[0] == "(IS) LRM-15" or name[0] == "(CL) LRM-15":
                        self.lrms += 15

                    if name[0] == "(IS) LRM-20" or name[0] == "(CL) LRM-20":
                        self.lrms += 20

                    # Add explosive weapon to location
                    if weap.explosive > 0:
                        # Split weapons, assign to innermost
                        if type(name[2]).__name__ == 'list':
                            j = ""
                            loc = ""
                            for i in name[2]:
                                # First part
                                if (j == ""):
                                    j = i[0]
                                    continue
                                elif (i[0] == "CT" and
                                      (j == "RT" or j == "LT")):
                                    loc = "CT"
                                elif (j == "CT" and
                                      (i[0] == "RT" or i[0] == "LT")):
                                    loc = "CT"
                                    print i[0], j
                                elif (i[0] == "RA" and j == "RT"):
                                    loc = "RT"
                                elif (j == "RA" and i[0] == "RT"):
                                    loc = "RT"
                                elif (i[0] == "LA" and j == "LT"):
                                    loc = "LT"
                                elif (j == "LA" and i[0] == "LT"):
                                    loc = "LT"
                            assert loc, "Split weapon location failed!"
                            expl = self.exp_weapon.get(loc, 0)
                            expl += weap.explosive
                            self.exp_weapon[loc] = expl
                        # No split, easy to handle
                        else:
                            expl = self.exp_weapon.get(name[2], 0)
                            expl += weap.explosive
                            self.exp_weapon[name[2]] = expl

            # Handle non-weapon equipment
            # HACK: Handle CASE
            for equip in self.o_equiplist.list:
                if (name[0] == equip.name and 
                    (name[1] == 'equipment' or name[1] == 'CASE')):
                    equip.addone()
                    self.o_weight += equip.weight
                    ident = True
                    # Hack, coolant pods
                    if name[0] == "Coolant Pod":
                        self.coolant += 1
                    # Hack -- C3
                    elif name[0] == "C3 Computer (Slave)":
                        self.has_c3 = True
                    elif name[0] == "C3 Computer (Master)":
                        self.has_c3m = True
                        # Master computers can work as TAG
                        self.has_tag = True
                    elif name[0] == "Improved C3 Computer":
                        self.has_c3i = True
                    elif name [0] == "TAG" or name[0] == "Light TAG":
                        self.has_tag = True
                    # Add explosive weapon to location
                    if equip.explosive > 0:
                        expl = self.exp_weapon.get(name[2], 0)
                        expl += equip.explosive
                        self.exp_weapon[name[2]] = expl

            # Hack, handle targeting computer
            if (name[0] == "(IS) Targeting Computer" and
                name[1] =='TargetingComputer'):
                self.tarcomp = 1
                ident = True
            if (name[0] == "(CL) Targeting Computer" and
                name[1] =='TargetingComputer'):
                self.tarcomp = 2
                ident = True

            # Hack, supercharger
            if (name[0] == "Supercharger" and name[1] == "Supercharger"):
                self.supercharger = True
                ident = True

            # Handle non-weapon equipment
            # HACK: Handle CASE
            for equip in self.d_equiplist.list:
                # non-CASE
                if (name[0] == equip.name and name[1] == 'equipment'):
                    equip.addone()
                    self.d_weight += equip.weight
                    ident = True
                    # Add explosive weapon to location
                    if equip.explosive > 0:
                        expl = self.exp_weapon.get(name[2], 0)
                        expl += equip.explosive
                        self.exp_weapon[name[2]] = expl
                # CASE
                if (name[0] == equip.name and
                    (name[1] == 'CASE' or name[1] == 'CASEII')):
                    equip.addone()
                    self.d_weight += equip.weight
                    ident = True
                    # Save CASE status
                    self.case[name[2]] = name[1]



            for phys in self.physicallist.list:
                if (name[0] == phys.name and name[1] == 'physical'):
                    phys.addone()
                    ident = True
                    # Use float to avoid rounding errors
                    self.p_weight += phys.weight(float(weight))
                    self.phys = 1

            for phys in self.d_physicallist.list:
                # non-CASE
                if (name[0] == phys.name and name[1] == 'physical'):
                    phys.addone()
                    self.d_weight += phys.weight
                    ident = True

            for ammo in self.ammolist.list:
                if (name[0] == ammo.name and name[1] == 'ammunition'):
                    ammo.addone()
                    # Special case, AMS ammo count as defensive equipment
                    if (name[0] == "(IS) @ Anti-Missile System"):
                        self.d_weight += ammo.weight
                    elif (name[0] == "(CL) @ Anti-Missile System"):
                        self.d_weight += ammo.weight
                    else:
                        self.a_weight += ammo.weight
                    ident = True
                    # Add explosive ammo to location
                    if ammo.explosive == "X":
                        expl = self.exp_ammo.get(name[2], 0)
                        expl += 1
                        self.exp_ammo[name[2]] = expl
            # Not found
            if not ident:
                print "Unidentified:", name
                error_exit("gear")

        for name in self.equiprear:
            # Go through weapon list
            ident = False
            for weap in self.weaponlist.list:
                if name[0] == weap.name:
                    weap.addone_rear()
                    self.w_weight += weap.weight
                    if weap.enhance == "T":
                        self.tcw_weight += weap.weight
                    ident = True
                    # Artemis IV
                    if (self.art4 == "TRUE" and weap.enhance == "A"):
                        self.w_weight += 1
                    # Artemis V
                    elif (self.art5 == "TRUE" and weap.enhance == "A"):
                        self.w_weight += 1.5
                    # Apollo
                    if (self.apollo == "TRUE" and weap.enhance == "P"):
                        self.w_weight += 1
                    # Add explosive weapon to location
                    if weap.explosive > 0:
                        expl = self.exp_weapon.get(name[2], 0)
                        expl += weap.explosive
                        self.exp_weapon[name[2]] = expl
            # Not found
            if (not ident):
                print "Unidentified:", name
                error_exit("gear")

        # Calculate tarcomp weight
        if self.tarcomp == 1:  #IS
            self.o_weight += ceil(self.tcw_weight / 4.0)
        if self.tarcomp == 2:  #Clan
            self.o_weight += ceil(self.tcw_weight / 5.0)

        # Add ammo to weapon
        for ammo in self.ammolist.list:
            if ammo.count > 0:
                ident = False
                for weap in self.weaponlist.list:
                    for i in ammo.wname:
                        if weap.name == i:
                            weap.add_ammo(ammo.count * ammo.weight,
                                          ammo.count * ammo.amount)
                            ident = True
                # We need to do defensive equipment also due to AMS
                for equip in self.d_equiplist.list:
                    for i in ammo.wname:
                        if equip.name == i:
                            equip.add_ammo(ammo.count * ammo.weight,
                                           ammo.count * ammo.amount)
                            ident = True
                if (not ident):
                    print "ERROR: Unknown weapon:", ammo.wname
                    error_exit("weapon")



    def get_w_weight(self):
        """
        Get weapons weight
        """
        return self.w_weight

    def get_a_weight(self):
        """
        Get ammo weight
        """
        return self.a_weight

    def get_o_weight(self):
        """
        Get offensive gear weight
        """
        return self.o_weight

    def get_d_weight(self):
        """
        Get defensive gear weight
        """
        return self.d_weight

    def get_p_weight(self):
        """
        Get physical weapon weight
        """
        return self.p_weight

    def get_def_bv(self):
        """
        Get defensive gear BV
        """
        batt_val = 0.0
        for equip in self.d_equiplist.list:
            if (equip.count > 0):
                bv_gear = equip.count * equip.batt_val[0]
                batt_val += bv_gear
                # Handle AMS ammo (and possible other ammo)
                if (equip.batt_val[1] > 0 and equip.ammocount > 0):
                    bv_ammo = equip.batt_val[1] * equip.ammo_ton
                    # Disallow ammo BV to be greater than that of
                    # the system itself
                    if bv_ammo > bv_gear:
                        bv_ammo = bv_gear
                    batt_val += bv_ammo
        for phys in self.d_physicallist.list:
            if (phys.count > 0):
                bv_gear = phys.count * phys.batt_val[0]
                batt_val += bv_gear
        return batt_val

    def get_ammo_exp_bv(self, engine):
        """
        Return how much BV is reduced by explosive ammo
        """
        neg_bv = 0.0
        # Check each ammo location
        for i in self.exp_ammo.keys():
            cas = self.case.get(i, "")
            # Head and center torso always
            if i == "HD":
                neg_bv -= 15.0 * self.exp_ammo[i]
            elif i == "CT":
                neg_bv -= 15.0 * self.exp_ammo[i]
            # So are legs
            elif (i == "LL" or i == "RL" or i == "RLL" or i == "RRL"):
                neg_bv -= 15.0 * self.exp_ammo[i]
            # Side torsos depends on several factors
            elif (i == "LT" or i == "RT"):
                # Inner Sphere XL Engines means that side torsos are vulnerable
                if engine.vulnerable():
                    if (cas != "CASEII"):
                        neg_bv -= 15.0 * self.exp_ammo[i]
                # Otherwise we check for CASE
                elif (self.cc == "FALSE"):
                    # No CASE
                    if (cas != "CASE" and cas != "CASEII"):
                        neg_bv -= 15.0 * self.exp_ammo[i]
            # Arms are complicated
            elif (i == "LA" or i == "FLL"):
                # Inner Sphere XL Engines means that side torsos are vulnerable
                if engine.vulnerable():
                    if (cas != "CASEII" and self.cc == "FALSE"):
                        neg_bv -= 15.0 * self.exp_ammo[i]
                # Otherwise we check for CASE
                elif (self.cc == "FALSE"):
                    # we can use torso CASE
                    cas2 = self.case.get("LT", "")
                    # No CASE
                    if ((cas != "CASE" and cas != "CASEII") and
                        (cas2 != "CASE" and cas2 != "CASEII")):
                        neg_bv -= 15.0 * self.exp_ammo[i]
            elif (i == "RA" or i == "FRL"):
                # Inner Sphere XL Engines means that side torsos are vulnerable
                if engine.vulnerable():
                    if (cas != "CASEII" and self.cc == "FALSE"):
                        neg_bv -= 15.0 * self.exp_ammo[i]
                # Otherwise we check for CASE
                elif (self.cc == "FALSE"):
                    # we can use torso CASE
                    cas2 = self.case.get("RT", "")
                    # No CASE
                    if ((cas != "CASE" and cas != "CASEII") and
                        (cas2 != "CASE" and cas2 != "CASEII")):
                        neg_bv -= 15.0 * self.exp_ammo[i]

        return neg_bv

    def get_weapon_exp_bv(self, engine):
        """
        Return how much BV is reduced by explosive weapons
        """
        neg_bv = 0.0
        # Check each ammo location
        for i in self.exp_weapon.keys():
            cas = self.case.get(i, "")
            # Head and center torso always
            if i == "HD":
                neg_bv -= self.exp_weapon[i]
            elif i == "CT":
                neg_bv -= self.exp_weapon[i]
            # So are legs
            elif (i == "LL" or i == "RL" or i == "RLL" or i == "RRL"):
                neg_bv -= self.exp_weapon[i]
            # Side torsos depends on several factors
            elif (i == "LT" or i == "RT"):
                # Inner Sphere XL Engines means that side torsos are vulnerable
                if engine.vulnerable():
                    if (cas != "CASEII"):
                        neg_bv -= self.exp_weapon[i]
                # Otherwise we check for CASE
                elif (self.cc == "FALSE"):
                    # No CASE
                    if (cas != "CASE" and cas != "CASEII"):
                        neg_bv -= self.exp_weapon[i]
            # Arms are complicated
            elif (i == "LA" or i == "FLL"):
                # Inner Sphere XL Engines means that side torsos are vulnerable
                if engine.vulnerable():
                    if (cas != "CASEII" and self.cc == "FALSE"):
                        neg_bv -= self.exp_weapon[i]
                # Otherwise we check for CASE
                elif (self.cc == "FALSE"):
                    # we can use torso CASE
                    cas2 = self.case.get("LT", "")
                    # No CASE
                    if ((cas != "CASE" and cas != "CASEII") and
                        (cas2 != "CASE" and cas2 != "CASEII")):
                        neg_bv -= self.exp_weapon[i]
            elif (i == "RA" or i == "FRL"):
                # Inner Sphere XL Engines means that side torsos are vulnerable
                if engine.vulnerable():
                    if (cas != "CASEII" and self.cc == "FALSE"):
                        neg_bv -= self.exp_weapon[i]
                # Otherwise we check for CASE
                elif (self.cc == "FALSE"):
                    # we can use torso CASE
                    cas2 = self.case.get("RT", "")
                    # No CASE
                    if ((cas != "CASE" and cas != "CASEII") and
                        (cas2 != "CASE" and cas2 != "CASEII")):
                        neg_bv -= self.exp_weapon[i]

        return neg_bv

    def check_weapon_bv_flip(self):
        """
        Check if front and rear weapons needs to be flipped for BV calculations
        """
        bv_front = 0.0
        bv_rear = 0.0
        # Weapons
        for weap in self.weaponlist.list:
            if (weap.count - weap.countarm) > 0:
                bv_front += weap.get_bv(self.tarcomp, self.art4, self.art5,
                                        self.apollo) * (weap.count - weap.countarm)

            if weap.countrear > 0:
                bv_rear += weap.get_bv(self.tarcomp, self.art4, self.art5,
                                       self.apollo) * weap.countrear
 
        if (bv_rear > bv_front):
            return True
        else:
            return False
        

