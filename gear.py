#!/usr/bin/python

from math import ceil
from error import *
from util import *

# A class to contain data about battlemech gear to allow for clearer code,
# by using named class members.

# Weapons in the order of name, BV[main, ammo], range,
# enhancement(A=artemis, T=tarcomp P=apollo),
# year, uses ammo rate?, weight, heat
#
# To be loaded into the gear class
#
# TODO1: IS: Flamer (Vehicle), HMG,  Clan: Flamer (Vehicle)
# TODO2: IS: MG Arrays: 2 HMG, 4 HMG, 2 MG, 3 MG
# Clan: 2 HMG, 2 LMG, 4 LMG, 2 MG, 3 MG
# TODO3: Artemis IV versions
weapons = [["(IS) Autocannon/2", [37, 5], "L", "T", 2300, 1, 6, 1],
           ["(IS) Autocannon/5", [70, 9], "L", "T", 2250, 1, 8, 1],
           ["(IS) Autocannon/10", [123, 15], "M", "T", 2460, 1, 12, 3],
           ["(IS) Autocannon/20", [178, 22], "M", "T", 2500, 1, 14, 7],
           ["(IS) Light Gauss Rifle", [159, 20], "L", "T", 3056, 1, 12, 1],
           ["(IS) Gauss Rifle", [320, 40], "L", "T", 2590, 1, 15, 1],
           ["(IS) Heavy Gauss Rifle", [346, 43], "L", "T", 3061, 1, 18, 2],
           ["(IS) LB 2-X AC", [42, 5], "L", "T", 3058, 1, 6, 1],
           ["(IS) LB 5-X AC", [83, 10], "L", "T", 3058, 1, 8, 1],
           ["(IS) LB 10-X AC", [148, 19], "L", "T", 2595, 1, 11, 2],
           ["(IS) LB 20-X AC", [237, 30], "M", "T", 3058, 1, 14, 6],
           ["(IS) Light AC/2", [30, 4], "L", "T", 3068, 1, 4, 1],
           ["(IS) Light AC/5", [62, 8], "M", "T", 3068, 1, 5, 1],
           ["(IS) Light Machine Gun", [5, 1], "M", "", 3068, 1, 0.5, 0],
           ["(IS) MG Array (2 Light Machine Gun)", [6.7, 1], "M", "", 3068, 2, 1.5, 0],
           ["(IS) MG Array (3 Light Machine Gun)", [10.05, 1], "M", "", 3068, 3, 2, 0],
           ["(IS) MG Array (4 Light Machine Gun)", [13.4, 1], "M", "", 3068, 4, 2.5, 0],
           ["(IS) Machine Gun", [5, 1], "S", "", 1900, 1, 0.5, 0],
           # MG 2
           # MG 3
           ["(IS) MG Array (4 Machine Gun)", [13.4, 1], "S", "", 3068, 4, 2.5, 0],
           # HMG
           # HMG 2
           ["(IS) MG Array (3 Heavy Machine Gun)", [12.06, 1], "S", "", 3068, 3, 3.5, 0],
           # HMG 4
           # Nail/rivet
           ["(IS) Rotary AC/2", [118, 15], "L", "T", 3062, 6, 8, 6],
           ["(IS) Rotary AC/5", [247, 31], "M", "T", 3062, 6, 10, 6],
           ["(IS) Ultra AC/2", [56, 7], "L", "T", 3057, 2, 7, 2],
           ["(IS) Ultra AC/5", [112, 14], "L", "T", 2640, 2, 9, 2],
           ["(IS) Ultra AC/10", [210, 26], "L", "T", 3057, 2, 13, 8],
           ["(IS) Ultra AC/20", [281, 35], "M", "T", 3060, 2, 15, 16],
           ["(IS) ER Large Laser", [163, 0], "L", "T", 2620, 0, 5, 12],
           ["(IS) ER Medium Laser", [62, 0], "M", "T", 3058, 0, 1, 5],
           ["(IS) ER Small Laser", [17, 0], "M", "T", 3058, 0, 0.5, 2],
           ["(IS) Flamer", [6, 0], "S", "", 2025, 0, 1, 3],
           # Flamer (Vehicle)
           ["(IS) Large Laser", [123, 0], "M", "T", 2316, 0, 5, 8],
           ["(IS) Medium Laser", [46, 0], "M", "T", 2300, 0, 1, 3],
           ["(IS) Small Laser", [9, 0], "S", "T", 2300, 0, 0.5, 1],
           ["(IS) Plasma Rifle", [210, 26], "M", "T", 3068, 1, 6, 10],
           ["(IS) Light PPC", [88, 0], "L", "T", 3067, 0, 3, 5],
           ["(IS) Light PPC + PPC Capacitor", [132, 0], "L", "T", 3067, 0, 4, 10],
           ["(IS) PPC", [176, 0], "L", "T", 2460, 0, 7, 10],
           ["(IS) Heavy PPC", [317, 0], "L", "T", 3067, 0, 10, 15],
           ["(IS) ER PPC", [229, 0], "L", "T", 2760, 0, 7, 15],
           ["(IS) Snub-Nose PPC", [165, 0], "M", "T", 3067, 0, 6, 10],
           ["(IS) Large Pulse Laser", [119, 0], "M", "T", 2609, 0, 7, 10],
           ["(IS) Medium Pulse Laser", [48, 0], "M", "T", 2609, 0, 2, 4],
           ["(IS) Small Pulse Laser", [12, 0], "S", "T", 2609, 0, 1, 2],
           ["(IS) LRM-5", [45, 6], "L", "A", 2300, 1, 2, 2],
           ["(IS) LRM-10", [90, 11], "L", "A", 2305, 1, 5, 4],
           ["(IS) LRM-15", [136, 17], "L", "A", 2315, 1, 7, 5],
           ["(IS) LRM-20", [181, 23], "L", "A", 2322, 1, 10, 6],
           ["(IS) MML-3", [29, 4], "L", "A", 3068, 1, 1.5, 2],
           ["(IS) MML-5", [45, 6], "L", "A", 3068, 1, 3, 3],
           ["(IS) MML-7", [67, 8], "L", "A", 3068, 1, 4.5, 4],
           ["(IS) MML-9", [86, 11], "L", "A", 3068, 1, 6, 5],
           ["(IS) MRM-10", [56, 7], "M", "P", 3058, 1, 3, 4],
           ["(IS) MRM-20", [112, 14], "M", "P", 3058, 1, 7, 6],
           ["(IS) MRM-30", [168, 21], "M", "P", 3058, 1, 10, 10],
           ["(IS) MRM-40", [224, 28], "M", "P", 3058, 1, 12, 12],
           ["(IS) Rocket Launcher 10", [18, 0], "L", "", 3064, 0, 0.5, 3],
           ["(IS) Rocket Launcher 15", [23, 0], "M", "", 3064, 0, 1, 4],
           ["(IS) Rocket Launcher 20", [24, 0], "M", "", 3064, 0, 1.5, 5],
           ["(IS) SRM-2", [21, 3], "M", "A", 2370, 1, 1, 2],
           ["(IS) SRM-4", [39, 5], "M", "A", 2370, 1, 2, 3],
           ["(IS) SRM-6", [59, 7], "M", "A", 2370, 1, 3, 4],
           ["(IS) Streak SRM-2", [30, 4], "M", "", 2647, 1, 1.5, 2],
           ["(IS) Streak SRM-4", [59, 7], "M", "", 3058, 1, 3, 3],
           ["(IS) Streak SRM-6", [89, 11], "M", "", 3058, 1, 4.5, 4],
           ["(IS) Streak SRM-2 (OS)", [6, 0], "M", "", 2676, 0, 2, 2],
           ["(IS) Narc Missile Beacon", [30, 0], "M", "", 2587, 1, 3, 0],
           ["(IS) iNarc Launcher", [75, 0], "M", "", 3062, 1, 5, 0],
           # Advanced Weapons
           ["(IS) Magshot Gauss Rifle", [15, 2], "M", "T", 3072, 1, 0.5, 1],
           ["(IS) Small Variable Speed Pulse Laser", [22, 0], "M", "T", 3070, 0, 2, 3],
           ["(IS) Medium Variable Speed Pulse Laser", [56, 0], "M", "T", 3070, 0, 4, 7],
           ["(IS) Large Variable Speed Pulse Laser", [123, 0], "M", "T", 3070, 0, 9, 10],
           ["(IS) Large X-Pulse Laser", [178, 0], "M", "T", 3057, 0, 7, 14],
           ["(IS) Bombast Laser", [137, 0], "M", "T", 3064, 0, 7, 12],
           ["(IS) Thunderbolt-15", [229, 29], "L", "", 3072, 1, 11, 7],
           ["(IS) Enhanced LRM-5", [52, 7], "L", "A", 3058, 1, 3, 2],
           ["ER Flamer", [16, 0], "M", "", 3067, 0, 1, 4],
           # Clan
           ["(CL) LB 2-X AC", [47, 6], "L", "T", 2826, 1, 5, 1],
           ["(CL) LB 5-X AC", [93, 12], "L", "T", 2825, 1, 7, 1],
           ["(CL) LB 10-X AC", [148, 19], "L", "T", 2595, 1, 10, 2],
           ["(CL) LB 20-X AC", [237, 30], "M", "T", 2826, 1, 12, 6],
           ["(CL) Ultra AC/2", [62, 8], "L", "T", 2827, 2, 5, 2],
           ["(CL) Ultra AC/5", [122, 15], "L", "T", 2640, 2, 7, 2],
           ["(CL) Ultra AC/10", [210, 26], "L", "T", 2825, 2, 10, 6],
           ["(CL) Ultra AC/20", [335, 42], "M", "T", 2825, 2, 12, 14],
           ["(CL) AP Gauss Rifle", [21, 3], "M", "T", 3069, 1, 0.5, 1],
           ["(CL) Gauss Rifle", [320, 40], "L", "T", 2590, 1, 12, 1],
           ["(CL) Hyper Assault Gauss 20", [267, 33], "L", "T", 3068, 1, 10, 4],
           ["(CL) Hyper Assault Gauss 30", [401, 50], "L", "T", 3068, 1, 13, 6],
           ["(CL) Hyper Assault Gauss 40", [535, 67], "L", "T", 3069, 1, 16, 8],
           ["(CL) Light Machine Gun", [5, 1], "M", "", 3060, 1, 0.25, 0],
           # LMG 2
           ["(CL) MG Array (3 Light Machine Gun)", [10.05, 1], "M", "", 3069, 3, 1, 0],
           # LMG 4
           ["(CL) Machine Gun", [5, 1], "S", "", 1900, 1, 0.25, 0],
           # MG 2
           # MG 3
           ["(CL) MG Array (4 Machine Gun)", [13.4, 1], "S", "", 3069, 4, 1.25, 0],
           ["(CL) Heavy Machine Gun", [6, 1], "S", "", 3059, 1, 0.5, 0],
           # HMG 2
           ["(CL) MG Array (3 Heavy Machine Gun)", [12.06, 1], "S", "", 3069, 3, 1.75, 0],
           ["(CL) MG Array (4 Heavy Machine Gun)", [16.08, 1], "S", "", 3069, 4, 2.25, 0],
           ["(CL) Flamer", [6, 0], "S", "", 2025, 0, 0.5, 3],
           # Flamer (Vehicle)
           ["(CL) ER Micro Laser", [7, 0], "M", "T", 3060, 0, 0.25, 1],
           ["(CL) ER Small Laser", [31, 0], "M", "T", 2825, 0, 0.5, 2],
           ["(CL) ER Medium Laser", [108, 0], "M", "T", 2824, 0, 1, 5],
           ["(CL) ER Large Laser", [248, 0], "L", "T", 2620, 0, 4, 12],
           ["(CL) Micro Pulse Laser", [12, 0], "S", "T", 3060, 0, 0.5, 1],
           ["(CL) Small Pulse Laser", [24, 0], "M", "T", 2609, 0, 1, 2],
           ["(CL) Medium Pulse Laser", [111, 0], "M", "T", 2609, 0, 2, 4],
           ["(CL) Large Pulse Laser", [265, 0], "L", "T", 2609, 0, 6, 10],
           ["(CL) Heavy Small Laser", [15, 0], "S", "T", 3059, 0, 0.5, 3],
           ["(CL) Heavy Medium Laser", [76, 0], "M", "T", 3059, 0, 1, 7],
           ["(CL) Heavy Large Laser", [244, 0], "M", "T", 3059, 0, 4, 18],
           ["(CL) Plasma Cannon", [170, 21], "L", "T", 3069, 1, 3, 7],
           ["(CL) ER PPC", [412, 0], "L", "T", 2760, 0, 6, 15],
           ["(CL) ATM-3", [53, 14], "M", "", 3054, 1, 1.5, 2],
           ["(CL) ATM-6", [105, 26], "M", "", 3054, 1, 3.5, 4],
           ["(CL) ATM-9", [147, 36], "M", "", 3054, 1, 5, 6],
           ["(CL) ATM-12", [212, 52], "M", "", 3055, 1, 7, 8],
           ["(CL) LRM-5", [55, 7], "L", "A", 2400, 1, 1, 2],
           ["(CL) LRM-10", [109, 14], "L", "A", 2400, 1, 2.5, 4],
           ["(CL) LRM-15", [164, 21], "L", "A", 2400, 1, 3.5, 5],
           ["(CL) LRM-20", [220, 27], "L", "A", 2400, 1, 5, 6],
           ["(CL) SRM-2", [21, 3], "M", "A", 2370, 1, 0.5, 2],
           ["(CL) SRM-4", [39, 5], "M", "A", 2370, 1, 1, 3],
           ["(CL) SRM-6", [59, 7], "M", "A", 2370, 1, 1.5, 4],
           ["(CL) Streak SRM-2", [40, 5], "M", "", 2647, 1, 1, 2],
           ["(CL) Streak SRM-4", [79, 10], "M", "", 2826, 1, 2, 3],
           ["(CL) Streak SRM-6", [118, 15], "M", "", 2826, 1, 3, 4],
           ["(CL) Streak SRM-4 (OS)", [16, 0], "M", "", 2826, 0, 2.5, 3],
           ["(CL) Narc Missile Beacon", [30, 0], "M", "", 2587, 1, 2, 0],
           # Advanced Weapons
           ["(CL) Rotary AC/2", [161, 20], "L", "T", 3073, 6, 8, 6],
           ["(CL) Rotary AC/5", [345, 43], "L", "T", 3073, 6, 10, 6],
           ["(CL) Protomech AC/4", [49, 6], "M", "T", 3073, 1, 4.5, 1],
           ["(CL) Improved Heavy Medium Laser", [93, 0], "M", "T", 3069, 0, 1, 7],
           ["(CL) ER Medium Pulse Laser", [117, 0], "M", "T", 3057, 0, 2, 6],
           ["(CL) ER Small Pulse Laser", [36, 0], "M", "T", 3057, 0, 1.5, 3],
           ["(CL) Mech Mortar 8", [50, 6], "L", "", 2840, 1, 5, 10],
           # Artillery
           ["(IS) Arrow IV Missile", [240, 30], "L", "", 2600, 1, 15, 10],
           ["(CL) Arrow IV Missile", [240, 30], "L", "", 2600, 1, 12, 10]]


# Ammo
#
# Name, weapon, ammount, weight
#
# TODO: Vehicle flamer
# TODO: Advanced weapons
ammo = [["(IS) @ AC/2", ["(IS) Autocannon/2"], 45, 1],
        ["(IS) @ AC/5", ["(IS) Autocannon/5"], 20, 1],
        ["(IS) @ AC/10", ["(IS) Autocannon/10"], 10, 1],
        ["(IS) @ AC/20", ["(IS) Autocannon/20"], 5, 1],
        ["(IS) @ Light Gauss Rifle", ["(IS) Light Gauss Rifle"], 16, 1],
        ["@ Gauss Rifle", ["(IS) Gauss Rifle", "(CL) Gauss Rifle"], 8, 1],
        ["(IS) @ Heavy Gauss Rifle", ["(IS) Heavy Gauss Rifle"], 4, 1],
        ["(IS) @ LB 2-X AC (Slug)", ["(IS) LB 2-X AC"], 45, 1],
        ["(IS) @ LB 5-X AC (Slug)", ["(IS) LB 5-X AC"], 20, 1],
        ["(IS) @ LB 5-X AC (Cluster)", ["(IS) LB 5-X AC"], 20, 1],
        ["(IS) @ LB 10-X AC (Slug)", ["(IS) LB 10-X AC"], 10, 1],
        ["(IS) @ LB 10-X AC (Cluster)", ["(IS) LB 10-X AC"], 10, 1],
        ["(IS) @ LB 20-X AC (Slug)", ["(IS) LB 20-X AC"], 5, 1],
        ["(IS) @ LB 20-X AC (Cluster)", ["(IS) LB 20-X AC"], 5, 1],
        ["(IS) @ Light AC/2", ["(IS) Light AC/2"], 45, 1],
        ["@ Light Machine Gun",
         ["(IS) Light Machine Gun", "(CL) Light Machine Gun",
          "(IS) MG Array (2 Light Machine Gun)",
          "(IS) MG Array (3 Light Machine Gun)",
          "(IS) MG Array (4 Light Machine Gun)",
          "(CL) MG Array (3 Light Machine Gun)"], 200, 1],
        ["@ Light Machine Gun (1/2)",
         ["(IS) Light Machine Gun", "(CL) Light Machine Gun",
          "(IS) MG Array (2 Light Machine Gun)",
          "(IS) MG Array (3 Light Machine Gun)",
          "(IS) MG Array (4 Light Machine Gun)",
          "(CL) MG Array (3 Light Machine Gun)"], 100, 0.5],
        ["@ Machine Gun",
         ["(IS) Machine Gun", "(CL) Machine Gun",
          "(IS) MG Array (4 Machine Gun)",
          "(CL) MG Array (4 Machine Gun)"], 200, 1],
        ["@ Machine Gun (1/2)",
         ["(IS) Machine Gun", "(CL) Machine Gun",
          "(IS) MG Array (4 Machine Gun)",
          "(CL) MG Array (4 Machine Gun)"], 100, 0.5],
        ["@ Heavy Machine Gun",
         ["(CL) Heavy Machine Gun",
          "(IS) MG Array (3 Heavy Machine Gun)",
          "(CL) MG Array (3 Heavy Machine Gun)",
          "(CL) MG Array (4 Heavy Machine Gun)"], 100, 1],
       ["@ Heavy Machine Gun (1/2)",
         ["(CL) Heavy Machine Gun",
          "(IS) MG Array (3 Heavy Machine Gun)",
          "(CL) MG Array (3 Heavy Machine Gun)",
          "(CL) MG Array (4 Heavy Machine Gun)"], 50, 0.5],
        ["(IS) @ Rotary AC/2", ["(IS) Rotary AC/2"], 45, 1],
        ["(IS) @ Rotary AC/5", ["(IS) Rotary AC/5"], 20, 1],
        ["(IS) @ Ultra AC/2", ["(IS) Ultra AC/2"], 45, 1],
        ["(IS) @ Ultra AC/5", ["(IS) Ultra AC/5"], 20, 1],
        ["(IS) @ Ultra AC/10", ["(IS) Ultra AC/10"], 10, 1],
        ["(IS) @ Ultra AC/20", ["(IS) Ultra AC/20"], 5, 1],
        ["(IS) @ Plasma Rifle", ["(IS) Plasma Rifle"], 10, 1],
        ["(IS) @ LRM-5", ["(IS) LRM-5"], 24, 1],
        ["(IS) @ LRM-10", ["(IS) LRM-10"], 12, 1],
        ["(IS) @ LRM-15", ["(IS) LRM-15"], 8, 1],
        ["(IS) @ LRM-20", ["(IS) LRM-20"], 6, 1],
        ["(IS) @ LRM-5 (Artemis IV Capable)", ["(IS) LRM-5"], 24, 1],
        ["(IS) @ LRM-10 (Artemis IV Capable)", ["(IS) LRM-10"], 12, 1],
        ["(IS) @ LRM-15 (Artemis IV Capable)", ["(IS) LRM-15"], 8, 1],
        ["(IS) @ LRM-20 (Artemis IV Capable)", ["(IS) LRM-20"], 6, 1],
        ["(IS) @ MML-3 (LRM)", ["(IS) MML-3"], 40, 1],
        ["(IS) @ MML-3 (SRM)", ["(IS) MML-3"], 33, 1],
        ["(IS) @ MML-5 (LRM)", ["(IS) MML-5"], 24, 1],
        ["(IS) @ MML-5 (SRM)", ["(IS) MML-5"], 20, 1],
        ["(IS) @ MML-7 (LRM)", ["(IS) MML-7"], 17, 1],
        ["(IS) @ MML-7 (SRM)", ["(IS) MML-7"], 14, 1],
        ["(IS) @ MML-9 (LRM)", ["(IS) MML-9"], 13, 1],
        ["(IS) @ MML-9 (SRM)", ["(IS) MML-9"], 11, 1],
        ["(IS) @ MML-3 (LRM Artemis IV Capable)", ["(IS) MML-3"], 40, 1],
        ["(IS) @ MML-3 (SRM Artemis IV Capable)", ["(IS) MML-3"], 33, 1],
        ["(IS) @ MML-7 (LRM Artemis IV Capable)", ["(IS) MML-7"], 17, 1],
        ["(IS) @ MML-7 (SRM Artemis IV Capable)", ["(IS) MML-7"], 14, 1],
        ["(IS) @ MRM-10", ["(IS) MRM-10"], 24, 1],
        ["(IS) @ MRM-20", ["(IS) MRM-20"], 12, 1],
        ["(IS) @ MRM-30", ["(IS) MRM-30"], 8, 1],
        ["(IS) @ MRM-40", ["(IS) MRM-40"], 6, 1],
        ["@ SRM-2", ["(IS) SRM-2", "(CL) SRM-2"], 50, 1],
        ["@ SRM-4", ["(IS) SRM-4", "(CL) SRM-4"], 25, 1],
        ["@ SRM-6", ["(IS) SRM-6", "(CL) SRM-6"], 15, 1],
        ["@ SRM-6 (Artemis IV Capable)", ["(IS) SRM-6", "(CL) SRM-6"], 15, 1],
        ["@ SRM-4 (Narc Capable)", ["(IS) SRM-4", "(CL) SRM-4"], 25, 1],
        ["@ SRM-6 (Narc Capable)", ["(IS) SRM-6", "(CL) SRM-6"], 15, 1],
        ["(IS) @ Streak SRM-2", ["(IS) Streak SRM-2"], 50, 1],
        ["(IS) @ Streak SRM-4", ["(IS) Streak SRM-4"], 25, 1],
        ["(IS) @ Streak SRM-6", ["(IS) Streak SRM-6"], 15, 1],
        ["(IS) @ Narc (Homing)", ["(IS) Narc Missile Beacon"], 6, 1],
        ["(IS) @ iNarc (Homing)", ["(IS) iNarc Launcher"], 4, 1],
        ["(IS) @ Anti-Missile System", ["(IS) Anti-Missile System"], 12, 1],
        # Advanced
        ["(IS) @ Magshot Gauss Rifle", ["(IS) Magshot Gauss Rifle"], 50, 1],
        ["(IS) @ Thunderbolt-15", ["(IS) Thunderbolt-15"], 4, 1],
        ["(IS) @ NLRM-5", ["(IS) Enhanced LRM-5"], 24, 1],
        # Clan
        ["(CL) @ LB 2-X AC (Slug)", ["(CL) LB 2-X AC"], 45, 1],
        ["(CL) @ LB 2-X AC (Cluster)", ["(CL) LB 2-X AC"], 45, 1],
        ["(CL) @ LB 5-X AC (Slug)", ["(CL) LB 5-X AC"], 20, 1],
        ["(CL) @ LB 5-X AC (Cluster)", ["(CL) LB 5-X AC"], 20, 1],
        ["(CL) @ LB 10-X AC (Slug)", ["(CL) LB 10-X AC"], 10, 1],
        ["(CL) @ LB 10-X AC (Cluster)", ["(CL) LB 10-X AC"], 10, 1],
        ["(CL) @ LB 20-X AC (Slug)", ["(CL) LB 20-X AC"], 5, 1],
        ["(CL) @ LB 20-X AC (Cluster)", ["(CL) LB 20-X AC"], 5, 1],
        ["(CL) @ Ultra AC/2", ["(CL) Ultra AC/2"], 45, 1],
        ["(CL) @ Ultra AC/5", ["(CL) Ultra AC/5"], 20, 1],
        ["(CL) @ Ultra AC/10", ["(CL) Ultra AC/10"], 10, 1],
        ["(CL) @ Ultra AC/20", ["(CL) Ultra AC/20"], 5, 1],
        ["(CL) @ AP Gauss Rifle", ["(CL) AP Gauss Rifle"], 40, 1],
        ["(CL) @ Hyper Assault Gauss 20", ["(CL) Hyper Assault Gauss 20"], 6, 1],
        ["(CL) @ Hyper Assault Gauss 30", ["(CL) Hyper Assault Gauss 30"], 4, 1],
        ["(CL) @ Hyper Assault Gauss 40", ["(CL) Hyper Assault Gauss 40"], 3, 1],
        ["(CL) @ Plasma Cannon", ["(CL) Plasma Cannon"], 10, 1],
        ["(CL) @ ATM-3", ["(CL) ATM-3"], 20, 1],
        ["(CL) @ ATM-3 (ER)", ["(CL) ATM-3"], 20, 1],
        ["(CL) @ ATM-3 (HE)", ["(CL) ATM-3"], 20, 1],
        ["(CL) @ ATM-6", ["(CL) ATM-6"], 10, 1],
        ["(CL) @ ATM-6 (ER)", ["(CL) ATM-6"], 10, 1],
        ["(CL) @ ATM-6 (HE)", ["(CL) ATM-6"], 10, 1],
        ["(CL) @ ATM-9", ["(CL) ATM-9"], 7, 1],
        ["(CL) @ ATM-9 (ER)", ["(CL) ATM-9"], 7, 1],
        ["(CL) @ ATM-9 (HE)", ["(CL) ATM-9"], 7, 1],
        ["(CL) @ ATM-12", ["(CL) ATM-12"], 5, 1],
        ["(CL) @ ATM-12 (ER)", ["(CL) ATM-12"], 5, 1],
        ["(CL) @ ATM-12 (HE)", ["(CL) ATM-12"], 5, 1],
        ["(CL) @ LRM-5", ["(CL) LRM-5"], 24, 1],
        ["(CL) @ LRM-10", ["(CL) LRM-10"], 12, 1],
        ["(CL) @ LRM-15", ["(CL) LRM-15"], 8, 1],
        ["(CL) @ LRM-20", ["(CL) LRM-20"], 6, 1],
        ["(CL) @ LRM-10 (Artemis IV Capable)", ["(CL) LRM-10"], 12, 1],
        ["(CL) @ LRM-15 (Artemis IV Capable)", ["(CL) LRM-15"], 8, 1],
        ["(CL) @ LRM-20 (Artemis IV Capable)", ["(CL) LRM-20"], 6, 1],
        ["(CL) @ LRM-15 (Artemis V)", ["(CL) LRM-15"], 8, 1],        
        ["(CL) @ LRM-20 (Artemis V)", ["(CL) LRM-20"], 6, 1],        
        ["(CL) @ Streak SRM-2", ["(CL) Streak SRM-2"], 50, 1],
        ["(CL) @ Streak SRM-4", ["(CL) Streak SRM-4"], 25, 1],
        ["(CL) @ Streak SRM-6", ["(CL) Streak SRM-6"], 15, 1],
        ["(CL) @ Narc (Homing)", ["(CL) Narc Missile Beacon"], 6, 1],
        ["(CL) @ Anti-Missile System", ["(CL) Anti-Missile System"], 24, 1],
        # Advanced
        ["(CL) @ Rotary AC/2", ["(CL) Rotary AC/2"], 45, 1],
        ["(CL) @ Rotary AC/5", ["(CL) Rotary AC/5"], 20, 1],
        ["(CL) @ Protomech AC/4", ["(CL) Protomech AC/4"], 20, 1],
        ["(CL) @ 'Mech Mortar 8 (Anti-Personnel)", ["(CL) Mech Mortar 8"], 4, 1],
        # Artillery
        ["(IS) @ Arrow IV (Non-Homing)", ["(IS) Arrow IV Missile"], 5, 1],
        ["(IS) @ Arrow IV (Homing)", ["(IS) Arrow IV Missile"], 5, 1],
        ["(CL) @ Arrow IV (Homing)", ["(CL) Arrow IV Missile"], 5, 1]]

# Equipment, spilt into offensive, and defensive
#
# Name, BV, year, uses ammo rate, weight
#
o_equipment = [["C3 Computer (Slave)", 0, 3050, 0, 1],
               ["C3 Computer (Master)", 0, 3050, 0, 5],
               ["Improved C3 Computer", 0, 3062, 0, 2.5],
               ["TAG", 0, 2600, 0, 1],
               ["Light TAG", 0, 3054, 0, 0.5],
               # Experimental
               ["Collapsible Command Module (CCM)", 0, 2710, 0, 16],
               ["Coolant Pod", 0, 3049, 0, 1]]


d_equipment = [["A-Pod", 1, 3055, 0, 0.5],
               ["B-Pod", 2, 3069, 0, 1],
               ["(IS) Anti-Missile System", 32, 2617, 1, 0.5],
               ["Guardian ECM Suite", 61, 2597, 0, 1.5],
               ["Beagle Active Probe", 10, 2576, 0, 1.5],
               ["ECM Suite", 61, 2597, 0, 1], # Clan
               ["Active Probe", 12, 2576, 0, 1], # Clan
               ["Light Active Probe", 7, 2576, 0, 0.5], # No year found
               ["(CL) Anti-Missile System", 32, 2617, 1, 0.5],
               ["CASE", 0, 2476, 0, 0.5], # HACK: CASE
               # Experimental
               ["Angel ECM", 100, 3057, 0, 2],
               ["Bloodhound Active Probe", 25, 3058, 0, 2],
               ["Electronic Warfare Equipment", 39, 3025, 0, 7.5],
               ["(CL) CASE II", 0, 3062, 0, 0.5]]

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
physical = [["Hatchet", 3022, 1.5, (lambda x : ceil(x / 5)), (lambda x : ceil(x / 15))],
            ["Sword", 3058, 1.725, (lambda x : ceil(x / 10) + 1), (lambda x : ceil_05(x / 20))],
            ["Claws", 3060, 1.275, (lambda x : ceil(x / 7)), (lambda x : ceil(x / 15))],
            ["Mace", 3061, 1.0, (lambda x : ceil(x / 4)), (lambda x : ceil(x / 10))],
            ["Talons", 3072, 1.0, (lambda x : ceil((x / 5) * 1.5)), (lambda x : ceil(x / 15))]]

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
        self.count = 0
        self.countrear = 0
        self.ammocount = 0

    def addone(self):
        self.count = self.count + 1

    def addone_rear(self):
        self.countrear = self.countrear + 1

    def add_ammo(self, amount):
        self.ammocount = self.ammocount + amount

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
        self.count = 0
        self.ammocount = 0

    def addone(self):
        self.count = self.count + 1

    def add_ammo(self, amount):
        self.ammocount = self.ammocount + amount

class Physicallist:
    def __init__(self):
        self.list = []
        for p in physical:
            self.list.append(Physical(p))
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

# Store Gear
#
# Take in lists of front and rear facing gears
class Gear:
    def __init__(self, weight, a4, equip, equiprear):
        self.a4 = a4 # Artemis IV
        self.equip = equip
        self.equiprear = equiprear

        # We need to create local lists for avoid trouble with Omni-mechs
        self.weaponlist = Weaponlist()
        self.o_equiplist = O_Equiplist()
        self.d_equiplist = D_Equiplist()
        self.physicallist = Physicallist()
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

        # Count gear
        for name in self.equip:
            # Go through weapon list
            id = 0
            for w in self.weaponlist.list:
                if name[0] == w.name:
                    w.addone()
                    self.w_weight += w.weight
                    if w.enhance == "T":
                        self.tcw_weight += w.weight
                    id = 1
                    # Artemis IV
                    if (self.a4 == "TRUE" and w.enhance == "A"):
                        self.w_weight += 1

            # Handle non-weapon equipment
            # HACK: Handle CASE
            for e in self.o_equiplist.list:
                if (name[0] == e.name and 
                    (name[1] == 'equipment' or name[1] == 'CASE')):
                    e.addone()
                    self.o_weight += e.weight
                    id = 1

            # Hack, handle targeting computer
            if (name[0] == "(IS) Targeting Computer" and name[1] =='TargetingComputer'):
                self.tarcomp = 1
                id = 1
            if (name[0] == "(CL) Targeting Computer" and name[1] =='TargetingComputer'):
                self.tarcomp = 2
                id = 1

            # Handle non-weapon equipment
            # HACK: Handle CASE
            for e in self.d_equiplist.list:
                if (name[0] == e.name and 
                    (name[1] == 'equipment' or name[1] == 'CASE' or name[1] == 'CASEII')):
                    e.addone()
                    self.d_weight += e.weight
                    id = 1

            for p in self.physicallist.list:
                if (name[0] == p.name and name[1] == 'physical'):
                    p.addone()
                    id = 1
                    # Use float to avoid rounding errors
                    self.p_weight += p.weight(float(weight))
                    self.phys = 1

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
                            w.add_ammo(a.count * a.amount)
                            id = 1
                # We need to do defensive equipment also due to AMS
                for e in self.d_equiplist.list:
                    for i in a.wname:
                        if e.name == i:
                            e.add_ammo(a.count * a.amount)
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
                BV += e.count * e.BV
        # TODO AMS ammo
        return BV

# TODO:
# - tarcomp year, and other years
# - rest of ammo
# - Make AMS ammo count as defensive BV wise
# - Coolant pod heat effect, coolant pod explosive effect
