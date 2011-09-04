#!/usr/bin/python

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



from math import ceil
from error import *
from util import *

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
weapons = [["(IS) Autocannon/2", [37, 5], "L", "T", 2300, 1, 6, 1, 0],
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
           ["(IS) MG Array (2 Light Machine Gun)", [16.7, 1], "M", "", 3068, 2, 1.5, 0, 0],
           ["(IS) MG Array (3 Light Machine Gun)", [25.05, 1], "M", "", 3068, 3, 2, 0, 0],
           ["(IS) MG Array (4 Light Machine Gun)", [33.4, 1], "M", "", 3068, 4, 2.5, 0, 0],
           ["(IS) Machine Gun", [5, 1], "S", "", 1900, 1, 0.5, 0, 0],
           # MG 2
           # MG 3
           ["(IS) MG Array (4 Machine Gun)", [33.4, 1], "S", "", 3068, 4, 2.5, 0, 0],
           # HMG
           # HMG 2
           ["(IS) MG Array (3 Heavy Machine Gun)", [30.06, 1], "S", "", 3068, 3, 3.5, 0, 0],
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
           ["(IS) Light PPC + PPC Capacitor", [132, 0], "L", "T", 3067, 0, 4, 10, 3],
           ["(IS) PPC", [176, 0], "L", "T", 2460, 0, 7, 10, 0],
           ["(IS) Heavy PPC", [317, 0], "L", "T", 3067, 0, 10, 15, 0],
           ["(IS) ER PPC", [229, 0], "L", "T", 2760, 0, 7, 15, 0],
           ["(IS) Snub-Nose PPC", [165, 0], "M", "T", 3067, 0, 6, 10, 0],
           ["(IS) Snub-Nose PPC + PPC Capacitor", [252, 0], "M", "T", 3067, 0, 7, 15, 3],
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
           ["(IS) Small Variable Speed Pulse Laser", [22, 0], "M", "T", 3070, 0, 2, 3, 0],
           ["(IS) Medium Variable Speed Pulse Laser", [56, 0], "M", "T", 3070, 0, 4, 7, 0],
           ["(IS) Large Variable Speed Pulse Laser", [123, 0], "M", "T", 3070, 0, 9, 10, 0],
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
           ["(CL) Hyper Assault Gauss 20", [267, 33], "L", "T", 3068, 1, 10, 4, 6],
           ["(CL) Hyper Assault Gauss 30", [401, 50], "L", "T", 3068, 1, 13, 6, 8],
           ["(CL) Hyper Assault Gauss 40", [535, 67], "L", "T", 3069, 1, 16, 8, 10],
           ["(CL) Light Machine Gun", [5, 1], "M", "", 3060, 1, 0.25, 0, 0],
           # LMG 2
           ["(CL) MG Array (3 Light Machine Gun)", [25.05, 1], "M", "", 3069, 3, 1, 0, 0],
           # LMG 4
           ["(CL) Machine Gun", [5, 1], "S", "", 1900, 1, 0.25, 0, 0],
           # MG 2
           # MG 3
           ["(CL) MG Array (4 Machine Gun)", [33.4, 1], "S", "", 3069, 4, 1.25, 0, 0],
           ["(CL) Heavy Machine Gun", [6, 1], "S", "", 3059, 1, 0.5, 0, 0],
           # HMG 2
           ["(CL) MG Array (3 Heavy Machine Gun)", [30.06, 1], "S", "", 3069, 3, 1.75, 0, 0],
           ["(CL) MG Array (4 Heavy Machine Gun)", [40.08, 1], "S", "", 3069, 4, 2.25, 0, 0],
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
           ["(CL) Improved Heavy Medium Laser", [93, 0], "M", "T", 3069, 0, 1, 7, 2],
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
ammo = [["(IS) @ AC/2", ["(IS) Autocannon/2"], 45, 1, "X"],
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
        ["@ SRM-6 (Artemis IV Capable)", ["(IS) SRM-6", "(CL) SRM-6"], 15, 1, "X"],
        ["@ SRM-4 (Narc Capable)", ["(IS) SRM-4", "(CL) SRM-4"], 25, 1, "X"],
        ["@ SRM-6 (Narc Capable)", ["(IS) SRM-6", "(CL) SRM-6"], 15, 1, "X"],
        ["(IS) @ Streak SRM-2", ["(IS) Streak SRM-2"], 50, 1, "X"],
        ["(IS) @ Streak SRM-4", ["(IS) Streak SRM-4"], 25, 1, "X"],
        ["(IS) @ Streak SRM-6", ["(IS) Streak SRM-6"], 15, 1, "X"],
        ["(IS) @ Narc (Homing)", ["(IS) Narc Missile Beacon"], 6, 1, "X"],
        ["(IS) @ iNarc (Homing)", ["(IS) iNarc Launcher"], 4, 1, "X"],
        ["(IS) @ Anti-Missile System", ["(IS) Anti-Missile System"], 12, 1, "X"],
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
        ["(CL) @ Hyper Assault Gauss 20", ["(CL) Hyper Assault Gauss 20"], 6, 1, ""],
        ["(CL) @ Hyper Assault Gauss 30", ["(CL) Hyper Assault Gauss 30"], 4, 1, ""],
        ["(CL) @ Hyper Assault Gauss 40", ["(CL) Hyper Assault Gauss 40"], 3, 1, ""],
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
        ["(CL) @ Anti-Missile System", ["(CL) Anti-Missile System"], 24, 1, "X"],
        # Advanced
        ["(CL) @ Rotary AC/2", ["(CL) Rotary AC/2"], 45, 1, "X"],
        ["(CL) @ Rotary AC/5", ["(CL) Rotary AC/5"], 20, 1, "X"],
        ["(CL) @ Protomech AC/4", ["(CL) Protomech AC/4"], 20, 1, "X"],
        ["(CL) @ Streak LRM-10", ["(CL) Streak LRM-10"], 12, 1, "X"],
        ["(CL) @ 'Mech Mortar 8 (Anti-Personnel)", ["(CL) Mech Mortar 8"], 4, 1, "X"],
        # Artillery
        ["(IS) @ Arrow IV (Non-Homing)", ["(IS) Arrow IV Missile"], 5, 1, "X"],
        ["(IS) @ Arrow IV (Homing)", ["(IS) Arrow IV Missile"], 5, 1, "X"],
        ["(CL) @ Arrow IV (Homing)", ["(CL) Arrow IV Missile"], 5, 1, "X"],
        ["@ Sniper", ["(IS) Sniper"], 10, 1, "X"]]

# Equipment, spilt into offensive, and defensive
#
# Name, BV, year, uses ammo rate, weight, explosive slots
#
o_equipment = [["C3 Computer (Slave)", [0, 0], 3050, 0, 1, 0],
               ["C3 Computer (Master)", [0, 0], 3050, 0, 5, 0],
               ["Improved C3 Computer", [0, 0], 3062, 0, 2.5, 0],
               ["TAG", [0, 0], 2600, 0, 1, 0],
               ["Light TAG", [0, 0], 3054, 0, 0.5, 0],
               ["Cargo, Liquid", [0, 0], 1900, 0, 1, 0],
               # Experimental
               ["Collapsible Command Module (CCM)", [0, 0], 2710, 0, 16, 0],
               ["Coolant Pod", [0, 0], 3049, 0, 1, 1]]


d_equipment = [["A-Pod", [1, 0], 3055, 0, 0.5, 0],
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

d_physical = [["Small Shield", [50, 0], 3067, 0, 2, 0]]

# Targeting computers, currently not used
#
# TODO: fix this
tarcomps = [["(IS) Targeting Computer", 0, 3062, 0],
            ["(CL) Targeting Computer", 0, 2860, 0]]

# Info on heatsink types
#
# Name, techbase, year, sinking capability
#
# Where techbase 0 = IS, 1 = Clan, 2 = Both, 10 = unknown
#
heatsink = [["Single Heat Sink", 2, 2022, 1],
            ["Double Heat Sink", 0, 2567, 2],
            ["Double Heat Sink", 1, 2567, 2],
            ["Laser Heat Sink", 1, 3051, 2]]

# Not used.
missile_ench = [["Artemis IV", 2598],
                ["Apollo", 3071]]

# Melee weapons
#
# Name, year, BV multiplier, damage formula, weight
#
physical = [["Hatchet", 3022, 1.5, (lambda x : ceil(x / 5.0)), (lambda x : ceil(x / 15.0))],
            ["Sword", 3058, 1.725, (lambda x : ceil(x / 10.0) + 1), (lambda x : ceil_05(x / 20.0))],
            ["Retractable Blade", 2420, 1.725, (lambda x : ceil(x / 10.0)), (lambda x : ceil_05(x / 2.0) + 0.5)], 
            ["Claws", 3060, 1.275, (lambda x : ceil(x / 7.0)), (lambda x : ceil(x / 15.0))],
            ["Mace", 3061, 1.0, (lambda x : ceil(x / 4.0)), (lambda x : ceil(x / 10.0))],
            ["Lance", 3064, 1.0, (lambda x : ceil(x / 5.0)), (lambda x : ceil_05(x / 20.0))],
            # Hack: Divide Talons BV multiplier by 2, because it is one item
            # being split up into two
            ["Talons", 3072, 1.0, (lambda x : ceil(x / 5.0) / 2.0), (lambda x : ceil(x / 15.0))]]


class Heatsinks:
    def __init__(self, hstype, tb, nr):
        self.type = hstype
        self.tb = int(tb)
        self.nr = nr

        # Check for heatsink type, save data
        id = 0
        for i in heatsink:
            if (i[0] == self.type and i[1] == self.tb):
                id = 1
                self.year = i[2]
                self.cap = i[3]
        if id == 0:
            error_exit((self.type, self.tb))

    # Return earliest year heatsink is available
    def get_year(self):
        return self.year

    # Return heatsink weight
    # 1 ton/sink, 10 free
    def get_weight(self):
        return self.nr - 10

    # Return sinking capability
    def get_sink(self):
        return self.nr * self.cap

class Weaponlist:
    def __init__(self):
        self.list = []
        for w in weapons:
            self.list.append(Weapon(w))

class Weapon:
    def __init__(self, ginfo):
        self.name = ginfo[0]
        self.BV = ginfo[1]
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
        self.count = self.count + 1

    def addone_rear(self):
        self.countrear = self.countrear + 1

    def addone_arm(self):
        self.countarm = self.countarm + 1

    # We need to track tonnage and rounds separately due to BV
    # calculations and how MML ammo works
    def add_ammo(self, count, amount):
        self.ammocount = self.ammocount + amount
        self.ammo_ton += count

    # Get the BV of an INDIVIDUAL weapon, not all of them
    # TODO: Artemis V, Apollo
    def get_BV(self, tarcomp, a4, a5, ap):
        BV = self.BV[0]
        if (tarcomp > 0 and self.enhance == "T"):
            BV *= 1.25
        if (a4 == "TRUE" and self.enhance == "A"):
            BV *= 1.2
        elif (a5 == "TRUE" and self.enhance == "A"):
            BV *= 1.3
        if (ap == "TRUE" and self.enhance == "P"):
            BV *= 1.15
        return BV


    # Get the BV of the total ammo
    def get_ammo_BV(self):
        BV_ammo = 0
        # Here we use BV of the unmodified weapons, of both facing
        BV_weapons = self.BV[0] * (self.count + self.countrear)
        # Handle ammo
        if (self.BV[1] > 0 and self.ammocount > 0):
            BV_ammo = self.BV[1] * self.ammo_ton
            # Disallow ammo BV to be greater than that of
            # the weapon itself
            if BV_ammo > BV_weapons:
                BV_ammo = BV_weapons

        return BV_ammo


class Ammolist:
    def __init__(self):
        self.list = []
        for a in ammo:
            self.list.append(Ammo(a))

class Ammo:
    def __init__(self, ginfo):
        self.name = ginfo[0]
        self.wname = ginfo[1]
        self.amount = ginfo[2]
        self.weight = ginfo[3]
        self.explosive = ginfo[4]
        self.count = 0

    def addone(self):
        self.count = self.count + 1

class O_Equiplist:
    def __init__(self):
        self.list = []
        for e in o_equipment:
            self.list.append(Equipment(e))

class D_Equiplist:
    def __init__(self):
        self.list = []
        for e in d_equipment:
            self.list.append(Equipment(e))

class Equipment:
    def __init__(self, ginfo):
        self.name = ginfo[0]
        self.BV = ginfo[1]
        self.year = ginfo[2]
        self.useammo = ginfo[3]
        self.weight = ginfo[4]
        self.explosive = ginfo[5]
        self.count = 0
        self.ammocount = 0
        self.ammo_ton = 0

    def addone(self):
        self.count = self.count + 1

    # We need to track tonnage and rounds separately due to BV
    # calculations and how MML ammo works
    def add_ammo(self, count, amount):
        self.ammocount = self.ammocount + amount
        self.ammo_ton += count

class Physicallist:
    def __init__(self):
        self.list = []
        for p in physical:
            self.list.append(Physical(p))
        self.name = "physcial"

class D_Physicallist:
    def __init__(self):
        self.list = []
        for p in d_physical:
            self.list.append(Equipment(p))
        self.name = "physcial"

class Physical:
    def __init__(self, pinfo):
        self.name = pinfo[0]
        self.year = pinfo[1]
        self.BVmult = pinfo[2]
        self.dam = pinfo[3]
        self.weight = pinfo[4]
        self.count = 0

    def addone(self):
        self.count = self.count + 1

    def get_BV(self, weight):
        return self.dam(weight) * self.BVmult

# Store Gear
#
# Take in lists of front and rear facing gears
class Gear:
    def __init__(self, weight, a4, a5, ap, equip, equiprear, cc):
        self.a4 = a4 # Artemis IV
        self.a5 = a5 # Artemis V
        self.ap = ap # Apollo
        self.equip = equip
        self.equiprear = equiprear
        self.cc = cc # Clan CASE

        # We need to create local lists for avoid trouble with Omni-mechs
        self.weaponlist = Weaponlist()
        self.o_equiplist = O_Equiplist()
        self.d_equiplist = D_Equiplist()
        self.physicallist = Physicallist()
        self.d_physicallist = D_Physicallist()
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

        # Count gear
        for name in self.equip:
            # Go through weapon list
            id = 0
            for w in self.weaponlist.list:
                if name[0] == w.name:
                    w.addone()
                    # Arm weapons
                    if name[2] == "RA" or name[2] == "LA":
                        w.addone_arm()
                    self.w_weight += w.weight
                    if w.enhance == "T":
                        self.tcw_weight += w.weight
                    id = 1
                    # Artemis IV
                    if (self.a4 == "TRUE" and w.enhance == "A"):
                        self.w_weight += 1
                    # Artemis V
                    elif (self.a5 == "TRUE" and w.enhance == "A"):
                        self.w_weight += 1.5
                    # Apollo
                    if (self.ap == "TRUE" and w.enhance == "P"):
                        self.w_weight += 1
                    # Hack - Narc
                    if name[0] == "(IS) Narc Missile Beacon" or name[0] == "(IS) iNarc Launcher" or name[0] == "(CL) Narc Missile Beacon":
                        self.has_narc = True
                    # Add explosive weapon to location
                    if w.explosive > 0:
                        # Split weapons, assign to innermost
                        if type(name[2]).__name__ == 'list':
                            j = ""
                            loc = ""
                            for i in name[2]:
                                # First part
                                if (j == ""):
                                    j = i[0]
                                    continue
                                elif (i[0] == "CT" and (j == "RT" or j == "LT")):
                                    loc = "CT"
                                elif (j == "CT" and (i[0] == "RT" or i[0] == "LT")):
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
                            expl += w.explosive
                            self.exp_weapon[loc] = expl
                        else:
                            expl = self.exp_weapon.get(name[2], 0)
                            expl += w.explosive
                            self.exp_weapon[name[2]] = expl

            # Handle non-weapon equipment
            # HACK: Handle CASE
            for e in self.o_equiplist.list:
                if (name[0] == e.name and 
                    (name[1] == 'equipment' or name[1] == 'CASE')):
                    e.addone()
                    self.o_weight += e.weight
                    id = 1
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
                    if e.explosive > 0:
                        expl = self.exp_weapon.get(name[2], 0)
                        expl += e.explosive
                        self.exp_weapon[name[2]] = expl

            # Hack, handle targeting computer
            if (name[0] == "(IS) Targeting Computer" and name[1] =='TargetingComputer'):
                self.tarcomp = 1
                id = 1
            if (name[0] == "(CL) Targeting Computer" and name[1] =='TargetingComputer'):
                self.tarcomp = 2
                id = 1

            # Hack, supercharger
            if (name[0] == "Supercharger" and name[1] == "Supercharger"):
                self.supercharger = True
                id = 1

            # Handle non-weapon equipment
            # HACK: Handle CASE
            for e in self.d_equiplist.list:
                # non-CASE
                if (name[0] == e.name and name[1] == 'equipment'):
                    e.addone()
                    self.d_weight += e.weight
                    id = 1
                    # Add explosive weapon to location
                    if e.explosive > 0:
                        expl = self.exp_weapon.get(name[2], 0)
                        expl += e.explosive
                        self.exp_weapon[name[2]] = expl
                # CASE
                if (name[0] == e.name and
                    (name[1] == 'CASE' or name[1] == 'CASEII')):
                    e.addone()
                    self.d_weight += e.weight
                    id = 1
                    # Save CASE status
                    self.case[name[2]] = name[1]



            for p in self.physicallist.list:
                if (name[0] == p.name and name[1] == 'physical'):
                    p.addone()
                    id = 1
                    # Use float to avoid rounding errors
                    self.p_weight += p.weight(float(weight))
                    self.phys = 1

            for p in self.d_physicallist.list:
                # non-CASE
                if (name[0] == p.name and name[1] == 'physical'):
                    p.addone()
                    self.d_weight += p.weight
                    id = 1

            for a in self.ammolist.list:
                if (name[0] == a.name and name[1] == 'ammunition'):
                    a.addone()
                    # Special case, AMS ammo count as defensive equipment
                    if (name[0] == "(IS) @ Anti-Missile System"):
                        self.d_weight += a.weight
                    elif (name[0] == "(CL) @ Anti-Missile System"):
                        self.d_weight += a.weight
                    else:
                        self.a_weight += a.weight
                    id = 1
                    # Add explosive ammo to location
                    if a.explosive == "X":
                        expl = self.exp_ammo.get(name[2], 0)
                        expl += 1
                        self.exp_ammo[name[2]] = expl
            # Not found
            if id == 0:
                print "Unidentified:", name
                error_exit("gear")

        for name in self.equiprear:
            # Go through weapon list
            id = 0
            for w in self.weaponlist.list:
                if name[0] == w.name:
                    w.addone_rear()
                    self.w_weight += w.weight
                    if w.enhance == "T":
                        self.tcw_weight += w.weight
                    id = 1
                    # Artemis IV
                    if (self.a4 == "TRUE" and w.enhance == "A"):
                        self.w_weight += 1
                    # Artemis V
                    elif (self.a5 == "TRUE" and w.enhance == "A"):
                        self.w_weight += 1.5
                    # Apollo
                    if (self.ap == "TRUE" and w.enhance == "P"):
                        self.w_weight += 1
                    # Add explosive weapon to location
                    if w.explosive > 0:
                        expl = self.exp_weapon.get(name[2], 0)
                        expl += w.explosive
                        self.exp_weapon[name[2]] = expl
            # Not found
            if (id == 0):
                print "Unidentified:", name
                error_exit("gear")

        # Calculate tarcomp weight
        if self.tarcomp == 1:  #IS
            self.o_weight += ceil(self.tcw_weight / 4.0)
        if self.tarcomp == 2:  #Clan
            self.o_weight += ceil(self.tcw_weight / 5.0)

        # Add ammo to weapon
        for a in self.ammolist.list:
            if a.count > 0:
                id = 0
                for w in self.weaponlist.list:
                    for i in a.wname:
                        if w.name == i:
                            w.add_ammo(a.count * a.weight, a.count * a.amount)
                            id = 1
                # We need to do defensive equipment also due to AMS
                for e in self.d_equiplist.list:
                    for i in a.wname:
                        if e.name == i:
                            e.add_ammo(a.count * a.weight, a.count * a.amount)
                            id = 1
                if (id == 0):
                    print "ERROR: Unknown weapon:", a.wname
                    error_exit("weapon")



    # Get weapons weight
    def get_w_weight(self):
        return self.w_weight

    # Get ammo weight
    def get_a_weight(self):
        return self.a_weight

    # Get offensive gear weight
    def get_o_weight(self):
        return self.o_weight

    # Get defensive gear weight
    def get_d_weight(self):
        return self.d_weight

    # Get physical weapon weight
    def get_p_weight(self):
        return self.p_weight

    # Get defensive gear BV
    def get_def_BV(self):
        BV = 0.0
        for e in self.d_equiplist.list:
            if (e.count > 0):
                BV_gear = e.count * e.BV[0]
                BV += BV_gear
                # Handle AMS ammo (and possible other ammo)
                if (e.BV[1] > 0 and e.ammocount > 0):
                    BV_ammo = e.BV[1] * e.ammo_ton
                    # Disallow ammo BV to be greater than that of
                    # the system itself
                    if BV_ammo > BV_gear:
                        BV_ammo = BV_gear
                    BV += BV_ammo
        for p in self.d_physicallist.list:
            if (p.count > 0):
                BV_gear = p.count * p.BV[0]
                BV += BV_gear
        return BV

    # Return how much BV is reduced by explosive ammo
    def get_ammo_exp_BV(self, engine):
        neg_BV = 0.0
        # Check each ammo location
        for i in self.exp_ammo.keys():
            cas = self.case.get(i, "")
            # Head and center torso always
            if i == "HD":
                neg_BV -= 15.0 * self.exp_ammo[i]
            elif i == "CT":
                neg_BV -= 15.0 * self.exp_ammo[i]
            # So are legs
            elif (i == "LL" or i == "RL" or i == "RLL" or i == "RRL"):
                neg_BV -= 15.0 * self.exp_ammo[i]
            # Side torsos depends on several factors
            elif (i == "LT" or i == "RT"):
                # Inner Sphere XL Engines means that side torsos are vulnerable
                if ((engine.etype == "XL Engine" and engine.eb == 0) or
                    engine.etype == "XXL Engine"):
                    if (cas != "CASEII"):
                        neg_BV -= 15.0 * self.exp_ammo[i]
                # Otherwise we check for CASE
                elif (self.cc == "FALSE"):
                    # No CASE
                    if (cas != "CASE" and cas != "CASEII"):
                        neg_BV -= 15.0 * self.exp_ammo[i]
            # Arms are complicated
            elif (i == "LA" or i == "FLL"):
                # Inner Sphere XL Engines means that side torsos are vulnerable
                if ((engine.etype == "XL Engine" and engine.eb == 0) or
                    engine.etype == "XXL Engine"):
                    if (cas != "CASEII" and self.cc == "FALSE"):
                        neg_BV -= 15.0 * self.exp_ammo[i]
                # Otherwise we check for CASE
                elif (self.cc == "FALSE"):
                    # we can use torso CASE
                    cas2 = self.case.get("LT", "")
                    # No CASE
                    if ((cas != "CASE" and cas != "CASEII") and (cas2 != "CASE" and cas2 != "CASEII")):
                        neg_BV -= 15.0 * self.exp_ammo[i]
            elif (i == "RA" or i == "FRL"):
                # Inner Sphere XL Engines means that side torsos are vulnerable
                if ((engine.etype == "XL Engine" and engine.eb == 0) or
                    engine.etype == "XXL Engine"):
                    if (cas != "CASEII" and self.cc == "FALSE"):
                        neg_BV -= 15.0 * self.exp_ammo[i]
                # Otherwise we check for CASE
                elif (self.cc == "FALSE"):
                    # we can use torso CASE
                    cas2 = self.case.get("RT", "")
                    # No CASE
                    if ((cas != "CASE" and cas != "CASEII") and (cas2 != "CASE" and cas2 != "CASEII")):
                        neg_BV -= 15.0 * self.exp_ammo[i]

        return neg_BV

    # Return how much BV is reduced by explosive weapons
    def get_weapon_exp_BV(self, engine):
        neg_BV = 0.0
        # Check each ammo location
        for i in self.exp_weapon.keys():
            cas = self.case.get(i, "")
            # Head and center torso always
            if i == "HD":
                neg_BV -= self.exp_weapon[i]
            elif i == "CT":
                neg_BV -= self.exp_weapon[i]
            # So are legs
            elif (i == "LL" or i == "RL" or i == "RLL" or i == "RRL"):
                neg_BV -= self.exp_weapon[i]
            # Side torsos depends on several factors
            elif (i == "LT" or i == "RT"):
                # Inner Sphere XL Engines means that side torsos are vulnerable
                if ((engine.etype == "XL Engine" and engine.eb == 0) or
                    engine.etype == "XXL Engine"):
                    if (cas != "CASEII"):
                        neg_BV -= self.exp_weapon[i]
                # Otherwise we check for CASE
                elif (self.cc == "FALSE"):
                    # No CASE
                    if (cas != "CASE" and cas != "CASEII"):
                        neg_BV -= self.exp_weapon[i]
            # Arms are complicated
            elif (i == "LA" or i == "FLL"):
                # Inner Sphere XL Engines means that side torsos are vulnerable
                if ((engine.etype == "XL Engine" and engine.eb == 0) or
                    engine.etype == "XXL Engine"):
                    if (cas != "CASEII" and self.cc == "FALSE"):
                        neg_BV -= self.exp_weapon[i]
                # Otherwise we check for CASE
                elif (self.cc == "FALSE"):
                    # we can use torso CASE
                    cas2 = self.case.get("LT", "")
                    # No CASE
                    if ((cas != "CASE" and cas != "CASEII") and (cas2 != "CASE" and cas2 != "CASEII")):
                        neg_BV -= self.exp_weapon[i]
            elif (i == "RA" or i == "FRL"):
                # Inner Sphere XL Engines means that side torsos are vulnerable
                if ((engine.etype == "XL Engine" and engine.eb == 0) or
                    engine.etype == "XXL Engine"):
                    if (cas != "CASEII" and self.cc == "FALSE"):
                        neg_BV -= self.exp_weapon[i]
                # Otherwise we check for CASE
                elif (self.cc == "FALSE"):
                    # we can use torso CASE
                    cas2 = self.case.get("RT", "")
                    # No CASE
                    if ((cas != "CASE" and cas != "CASEII") and (cas2 != "CASE" and cas2 != "CASEII")):
                        neg_BV -= self.exp_weapon[i]

        return neg_BV

    def check_weapon_BV_flip(self):
        BV_front = 0.0
        BV_rear = 0.0
        # Weapons
        for w in self.weaponlist.list:
            if (w.count - w.countarm) > 0:
                BV_front += w.get_BV(self.tarcomp, self.a4, self.a5, self.ap) * (w.count - w.countarm)

            if w.countrear > 0:
                BV_rear += w.get_BV(self.tarcomp, self.a4, self.a5, self.ap) * w.countrear
 
        if (BV_rear > BV_front):
            return True
        else:
            return False
        

