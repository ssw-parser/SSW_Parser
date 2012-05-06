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
from util import gettext, get_child_data
from item import Item
from weapon_list import Weaponlist
from physical import Physicallist

# A class to contain data about battlemech gear to allow for clearer code,
# by using named class members.

# Ammo
#
# Name, weapon, amount, weight, explosive?, cost
#
AMMO = {
    "(IS) @ AC/2" : [["(IS) Autocannon/2"], 45, 1, "X", 1000],
    "(IS) @ AC/5" : [["(IS) Autocannon/5"], 20, 1, "X", 4500],
    "(IS) @ AC/10" : [["(IS) Autocannon/10"], 10, 1, "X", 6000],
    "(IS) @ AC/20" : [["(IS) Autocannon/20"], 5, 1, "X", 10000],
    "(IS) @ Light Gauss Rifle" : [["(IS) Light Gauss Rifle"], 16, 1, "", 20000],
    "@ Gauss Rifle" :
        [["(IS) Gauss Rifle", "(CL) Gauss Rifle"], 8, 1, "", 20000],
    "(IS) @ Heavy Gauss Rifle" : [["(IS) Heavy Gauss Rifle"], 4, 1, "", 20000],
    "(IS) @ LB 2-X AC (Slug)" : [["(IS) LB 2-X AC"], 45, 1, "X", 2000],
    "(IS) @ LB 2-X AC (Cluster)" : [["(IS) LB 2-X AC"], 45, 1, "X", 3300],
    "(IS) @ LB 5-X AC (Slug)" : [["(IS) LB 5-X AC"], 20, 1, "X", 9000],
    "(IS) @ LB 5-X AC (Cluster)" : [["(IS) LB 5-X AC"], 20, 1, "X", 15000],
    "(IS) @ LB 10-X AC (Slug)" : [["(IS) LB 10-X AC"], 10, 1, "X", 12000],
    "(IS) @ LB 10-X AC (Cluster)" : [["(IS) LB 10-X AC"], 10, 1, "X", 20000],
    "(IS) @ LB 20-X AC (Slug)" : [["(IS) LB 20-X AC"], 5, 1, "X", 20000],
    "(IS) @ LB 20-X AC (Cluster)" : [["(IS) LB 20-X AC"], 5, 1, "X", 34000],
    "(IS) @ Light AC/2" : [["(IS) Light AC/2"], 45, 1, "X", 1000],
    "(IS) @ Light AC/5" : [["(IS) Light AC/5"], 20, 1, "X", 4500],
    "@ Light Machine Gun" :
        [["(IS) Light Machine Gun", "(CL) Light Machine Gun",
          "(IS) MG Array (2 Light Machine Gun)",
          "(IS) MG Array (3 Light Machine Gun)",
          "(IS) MG Array (4 Light Machine Gun)",
          "(CL) MG Array (3 Light Machine Gun)",
          "(CL) MG Array (4 Light Machine Gun)"], 200, 1, "X", 500],
    "@ Light Machine Gun (1/2)" :
        [["(IS) Light Machine Gun", "(CL) Light Machine Gun",
          "(IS) MG Array (2 Light Machine Gun)",
          "(IS) MG Array (3 Light Machine Gun)",
          "(IS) MG Array (4 Light Machine Gun)",
          "(CL) MG Array (3 Light Machine Gun)",
          "(CL) MG Array (4 Light Machine Gun)"], 100, 0.5, "X", 250],
    "@ Machine Gun" :
        [["(IS) Machine Gun", "(CL) Machine Gun",
          "(IS) MG Array (3 Machine Gun)",
          "(IS) MG Array (4 Machine Gun)",
          "(CL) MG Array (4 Machine Gun)"], 200, 1, "X", 1000],
    "@ Machine Gun (1/2)" :
        [["(IS) Machine Gun", "(CL) Machine Gun",
          "(IS) MG Array (3 Machine Gun)",
          "(IS) MG Array (4 Machine Gun)",
          "(CL) MG Array (4 Machine Gun)"], 100, 0.5, "X", 500],
    "@ Heavy Machine Gun" :
        [["(CL) Heavy Machine Gun",
          "(IS) MG Array (3 Heavy Machine Gun)",
          "(CL) MG Array (3 Heavy Machine Gun)",
          "(CL) MG Array (4 Heavy Machine Gun)"], 100, 1, "X", 1000],
    "@ Heavy Machine Gun (1/2)" :
        [["(CL) Heavy Machine Gun",
          "(IS) MG Array (3 Heavy Machine Gun)",
          "(CL) MG Array (3 Heavy Machine Gun)",
          "(CL) MG Array (4 Heavy Machine Gun)"], 50, 0.5, "X", 500],
    "(IS) @ Rotary AC/2" : [["(IS) Rotary AC/2"], 45, 1, "X", 3000],
    "(IS) @ Rotary AC/5" : [["(IS) Rotary AC/5"], 20, 1, "X", 12000],
    "(IS) @ Ultra AC/2" : [["(IS) Ultra AC/2"], 45, 1, "X", 1000],
    "(IS) @ Ultra AC/5" : [["(IS) Ultra AC/5"], 20, 1, "X", 9000],
    "(IS) @ Ultra AC/10" : [["(IS) Ultra AC/10"], 10, 1, "X", 12000],
    "(IS) @ Ultra AC/20" : [["(IS) Ultra AC/20"], 5, 1, "X", 20000],
    "(IS) @ Plasma Rifle" : [["(IS) Plasma Rifle"], 10, 1, "", 10000],
    "(IS) @ LRM-5" : [["(IS) LRM-5"], 24, 1, "X", 30000],
    "(IS) @ LRM-10" : [["(IS) LRM-10"], 12, 1, "X", 30000],
    "(IS) @ LRM-15" : [["(IS) LRM-15"], 8, 1, "X", 30000],
    "(IS) @ LRM-20" : [["(IS) LRM-20"], 6, 1, "X", 30000],
    "(IS) @ LRM-5 (Artemis IV Capable)" : [["(IS) LRM-5"], 24, 1, "X", 60000],
    "(IS) @ LRM-10 (Artemis IV Capable)" : [["(IS) LRM-10"], 12, 1, "X", 60000],
    "(IS) @ LRM-15 (Artemis IV Capable)" : [["(IS) LRM-15"], 8, 1, "X", 60000],
    "(IS) @ LRM-20 (Artemis IV Capable)" : [["(IS) LRM-20"], 6, 1, "X", 60000],
    "(IS) @ LRM-5 (Narc Capable)" : [["(IS) LRM-5"], 24, 1, "X", 60000],
    "(IS) @ LRM-10 (Narc Capable)" : [["(IS) LRM-10"], 12, 1, "X", 60000],
    "(IS) @ LRM-15 (Narc Capable)" : [["(IS) LRM-15"], 8, 1, "X", 60000],
    "(IS) @ LRM-20 (Narc Capable)" : [["(IS) LRM-20"], 6, 1, "X", 60000],
    "(IS) @ LRT-5 (Torpedo)" : [["(IS) LRT-5"], 24, 1, "X", 30000],
    "(IS) @ LRT-10 (Torpedo)" : [["(IS) LRT-10"], 12, 1, "X", 30000],
    "(IS) @ LRT-15 (Torpedo)" : [["(IS) LRT-15"], 8, 1, "X", 30000],
    "(IS) @ MML-3 (LRM)" : [["(IS) MML-3"], 40, 1, "X", 30000],
    "(IS) @ MML-3 (SRM)" : [["(IS) MML-3"], 33, 1, "X", 27000],
    "(IS) @ MML-5 (LRM)" : [["(IS) MML-5"], 24, 1, "X", 30000],
    "(IS) @ MML-5 (SRM)" : [["(IS) MML-5"], 20, 1, "X", 27000],
    "(IS) @ MML-7 (LRM)" : [["(IS) MML-7"], 17, 1, "X", 30000],
    "(IS) @ MML-7 (SRM)" : [["(IS) MML-7"], 14, 1, "X", 27000],
    "(IS) @ MML-9 (LRM)" : [["(IS) MML-9"], 13, 1, "X", 30000],
    "(IS) @ MML-9 (SRM)" : [["(IS) MML-9"], 11, 1, "X", 27000],
    "(IS) @ MML-3 (LRM Artemis IV Capable)" :
        [["(IS) MML-3"], 40, 1, "X", 60000],
    "(IS) @ MML-3 (SRM Artemis IV Capable)" :
        [["(IS) MML-3"], 33, 1, "X", 54000],
    "(IS) @ MML-5 (LRM Artemis IV Capable)" :
        [["(IS) MML-5"], 24, 1, "X", 60000],
    "(IS) @ MML-5 (SRM Artemis IV Capable)" :
        [["(IS) MML-5"], 20, 1, "X", 54000],
    "(IS) @ MML-7 (LRM Artemis IV Capable)" :
        [["(IS) MML-7"], 17, 1, "X", 60000],
    "(IS) @ MML-7 (SRM Artemis IV Capable)" :
        [["(IS) MML-7"], 14, 1, "X", 54000],
    "(IS) @ MML-9 (LRM Artemis IV Capable)" :
        [["(IS) MML-9"], 13, 1, "X", 60000],
    "(IS) @ MML-9 (SRM Artemis IV Capable)" :
        [["(IS) MML-9"], 11, 1, "X", 54000],
    "(IS) @ MRM-10" : [["(IS) MRM-10"], 24, 1, "X", 5000],
    "(IS) @ MRM-20" : [["(IS) MRM-20"], 12, 1, "X", 5000],
    "(IS) @ MRM-30" : [["(IS) MRM-30"], 8, 1, "X", 5000],
    "(IS) @ MRM-40" : [["(IS) MRM-40"], 6, 1, "X", 5000],
    "@ SRM-2" : [["(IS) SRM-2", "(CL) SRM-2"], 50, 1, "X", 27000],
    "@ SRM-4" : [["(IS) SRM-4", "(CL) SRM-4"], 25, 1, "X", 27000],
    "@ SRM-6" : [["(IS) SRM-6", "(CL) SRM-6"], 15, 1, "X", 27000],
    "@ SRM-4 (Artemis IV Capable)" :
        [["(IS) SRM-4", "(CL) SRM-4"], 25, 1, "X", 54000],
    "@ SRM-6 (Artemis IV Capable)" :
        [["(IS) SRM-6", "(CL) SRM-6"], 15, 1, "X", 54000],
    "@ SRM-2 (Narc Capable)" :
        [["(IS) SRM-2", "(CL) SRM-2"], 50, 1, "X", 54000],
    "@ SRM-4 (Narc Capable)" :
        [["(IS) SRM-4", "(CL) SRM-4"], 25, 1, "X", 54000],
    "@ SRM-6 (Narc Capable)" :
        [["(IS) SRM-6", "(CL) SRM-6"], 15, 1, "X", 54000],
    "@ SRT-2 (Torpedo)" : [["(CL) SRT-2"], 50, 1, "X", 27000],
    "@ SRT-4 (Torpedo)" : [["(IS) SRT-4", "(CL) SRT-4"], 25, 1, "X", 27000],
    "@ SRT-6 (Torpedo)" : [["(CL) SRT-6"], 15, 1, "X", 27000],
    "(IS) @ Streak SRM-2" : [["(IS) Streak SRM-2"], 50, 1, "X", 54000],
    "(IS) @ Streak SRM-4" : [["(IS) Streak SRM-4"], 25, 1, "X", 54000],
    "(IS) @ Streak SRM-6" : [["(IS) Streak SRM-6"], 15, 1, "X", 54000],
    "(IS) @ Narc (Homing)" : [["(IS) Narc Missile Beacon"], 6, 1, "X", 6000],
    "(IS) @ iNarc (Homing)" : [["(IS) iNarc Launcher"], 4, 1, "X", 7500],
    "(IS) @ Anti-Missile System" :
        [["(IS) Anti-Missile System"], 12, 1, "X", 2000],
    # Clan
    "(CL) @ LB 2-X AC (Slug)" : [["(CL) LB 2-X AC"], 45, 1, "X", 2000],
    "(CL) @ LB 2-X AC (Cluster)" : [["(CL) LB 2-X AC"], 45, 1, "X", 3300],
    "(CL) @ LB 5-X AC (Slug)" : [["(CL) LB 5-X AC"], 20, 1, "X", 9000],
    "(CL) @ LB 5-X AC (Cluster)" : [["(CL) LB 5-X AC"], 20, 1, "X", 15000],
    "(CL) @ LB 10-X AC (Slug)" : [["(CL) LB 10-X AC"], 10, 1, "X", 12000],
    "(CL) @ LB 10-X AC (Cluster)" : [["(CL) LB 10-X AC"], 10, 1, "X", 20000],
    "(CL) @ LB 20-X AC (Slug)" : [["(CL) LB 20-X AC"], 5, 1, "X", 20000],
    "(CL) @ LB 20-X AC (Cluster)" : [["(CL) LB 20-X AC"], 5, 1, "X", 34000],
    "(CL) @ Ultra AC/2" : [["(CL) Ultra AC/2"], 45, 1, "X", 1000],
    "(CL) @ Ultra AC/5" : [["(CL) Ultra AC/5"], 20, 1, "X", 9000],
    "(CL) @ Ultra AC/10" : [["(CL) Ultra AC/10"], 10, 1, "X", 12000],
    "(CL) @ Ultra AC/20" : [["(CL) Ultra AC/20"], 5, 1, "X", 20000],
    "(CL) @ AP Gauss Rifle" : [["(CL) AP Gauss Rifle"], 40, 1, "", 3000],
    "(CL) @ Hyper Assault Gauss 20" :
        [["(CL) Hyper Assault Gauss 20"], 6, 1, "", 30000],
    "(CL) @ Hyper Assault Gauss 30" :
        [["(CL) Hyper Assault Gauss 30"], 4, 1, "", 30000],
    "(CL) @ Hyper Assault Gauss 40" :
        [["(CL) Hyper Assault Gauss 40"], 3, 1, "", 30000],
    "(CL) @ Plasma Cannon" : [["(CL) Plasma Cannon"], 10, 1, "", 12000],
    "(CL) @ ATM-3" : [["(CL) ATM-3"], 20, 1, "X", 75000],
    "(CL) @ ATM-3 (ER)" : [["(CL) ATM-3"], 20, 1, "X", 75000],
    "(CL) @ ATM-3 (HE)" : [["(CL) ATM-3"], 20, 1, "X", 75000],
    "(CL) @ ATM-6" : [["(CL) ATM-6"], 10, 1, "X", 75000],
    "(CL) @ ATM-6 (ER)" : [["(CL) ATM-6"], 10, 1, "X", 75000],
    "(CL) @ ATM-6 (HE)" : [["(CL) ATM-6"], 10, 1, "X", 75000],
    "(CL) @ ATM-9" : [["(CL) ATM-9"], 7, 1, "X", 75000],
    "(CL) @ ATM-9 (ER)" : [["(CL) ATM-9"], 7, 1, "X", 75000],
    "(CL) @ ATM-9 (HE)" : [["(CL) ATM-9"], 7, 1, "X", 75000],
    "(CL) @ ATM-12" : [["(CL) ATM-12"], 5, 1, "X", 75000],
    "(CL) @ ATM-12 (ER)" : [["(CL) ATM-12"], 5, 1, "X", 75000],
    "(CL) @ ATM-12 (HE)" : [["(CL) ATM-12"], 5, 1, "X", 75000],
    "(CL) @ LRM-5" : [["(CL) LRM-5"], 24, 1, "X", 30000],
    "(CL) @ LRM-10" : [["(CL) LRM-10"], 12, 1, "X", 30000],
    "(CL) @ LRM-15" : [["(CL) LRM-15"], 8, 1, "X", 30000],
    "(CL) @ LRM-20" : [["(CL) LRM-20"], 6, 1, "X", 30000],
    "(CL) @ LRM-5 (Artemis IV Capable)" : [["(CL) LRM-5"], 24, 1, "X", 60000],
    "(CL) @ LRM-10 (Artemis IV Capable)" : [["(CL) LRM-10"], 12, 1, "X", 60000],
    "(CL) @ LRM-15 (Artemis IV Capable)" : [["(CL) LRM-15"], 8, 1, "X", 60000],
    "(CL) @ LRM-20 (Artemis IV Capable)" : [["(CL) LRM-20"], 6, 1, "X", 60000],
    "(CL) @ LRM-15 (Artemis V)" : [["(CL) LRM-15"], 8, 1, "X", 150000],        
    "(CL) @ LRM-20 (Artemis V)" : [["(CL) LRM-20"], 6, 1, "X", 150000],        
    "(CL) @ LRM-5 (Narc Capable)" : [["(CL) LRM-5"], 24, 1, "X", 60000],
    "(CL) @ LRM-15 (Narc Capable)" : [["(CL) LRM-15"], 8, 1, "X", 60000],
    "(CL) @ LRM-20 (Narc Capable)" : [["(CL) LRM-20"], 6, 1, "X", 60000],
    "(CL) @ LRT-5 (Torpedo)" : [["(CL) LRT-5"], 24, 1, "X", 30000],
    "(CL) @ LRT-10 (Torpedo)" : [["(CL) LRT-10"], 12, 1, "X", 30000],
    "(CL) @ LRT-15 (Torpedo)" : [["(CL) LRT-15"], 8, 1, "X", 30000],
    "(CL) @ Streak SRM-2" : [["(CL) Streak SRM-2"], 50, 1, "X", 54000],
    "(CL) @ Streak SRM-4" : [["(CL) Streak SRM-4"], 25, 1, "X", 54000],
    "(CL) @ Streak SRM-6" : [["(CL) Streak SRM-6"], 15, 1, "X", 54000],
    "(CL) @ Narc (Homing)" : [["(CL) Narc Missile Beacon"], 6, 1, "X", 6000],
    "(CL) @ Anti-Missile System" :
        [["(CL) Anti-Missile System"], 24, 1, "X", 2000],
    # Advanced
    "(IS) @ Magshot Gauss Rifle" :
        [["(IS) Magshot Gauss Rifle"], 50, 1, "", 1000],
    "(IS) @ BattleMech Taser" : [["(IS) BattleMech Taser"], 5, 1, "X", 2000],
    "(IS) @ Thunderbolt-5" : [["(IS) Thunderbolt-5"], 12, 1, "X", 50000],
    "(IS) @ Thunderbolt-10" : [["(IS) Thunderbolt-10"], 6, 1, "X", 50000],
    "(IS) @ Thunderbolt-15" : [["(IS) Thunderbolt-15"], 4, 1, "X", 50000],
    "(IS) @ Thunderbolt-20" : [["(IS) Thunderbolt-20"], 3, 1, "X", 50000],
    "(IS) @ NLRM-5" : [["(IS) Enhanced LRM-5"], 24, 1, "X", 31000],
    "(IS) @ ELRM-10" : [["(IS) Extended LRM-10"], 9, 1, "X", 35000],
    "(IS) @ ELRM-20" : [["(IS) Extended LRM-20"], 4, 1, "X", 35000],
    "@ Fluid Gun (Water)" : [["(IS) Fluid Gun"], 20, 1, "", 500],
    "@ C3 Remote Launcher" : [["C3 Remote Sensor Launcher"], 4, 1, "X", 100000],
    "(CL) @ Rotary AC/2" : [["(CL) Rotary AC/2"], 45, 1, "X", 3000],
    "(CL) @ Rotary AC/5" : [["(CL) Rotary AC/5"], 20, 1, "X", 12000],
    "(CL) @ Protomech AC/4" : [["(CL) Protomech AC/4"], 20, 1, "X", 4800],
    "(CL) @ Protomech AC/8" : [["(CL) Protomech AC/8"], 10, 1, "X", 6300],
    "(CL) @ Streak LRM-10" : [["(CL) Streak LRM-10"], 12, 1, "X", 60000],
    "(CL) @ Streak LRM-15" : [["(CL) Streak LRM-15"], 8, 1, "X", 60000],
    "(CL) @ 'Mech Mortar 8 (Anti-Personnel)" :
        [["(CL) Mech Mortar 8"], 4, 1, "X", 24000],
    "@ Heavy Flamer" : [["Heavy Flamer"], 10, 1, "X", 2000],
    "(IS) @ HVAC/10" :
        [["(IS) Hyper-Velocity Autocannon/10"], 8, 1, "X", 20000],
    "(IS) @ Improved Heavy Gauss Rifle" :
        [["(IS) Improved Heavy Gauss Rifle"], 4, 1, "", 20000],
    "(IS) @ Silver Bullet Gauss" :
        [["(IS) Silver Bullet Gauss"], 8, 1, "", 25000],
    "@ Long Tom Cannon" :
        [["Long Tom Artillery Cannon"], 5, 1, "X", 20000],
    # Artillery
    "(IS) @ Arrow IV (Non-Homing)" :
        [["(IS) Arrow IV Missile"], 5, 1, "X", 10000],
    "(IS) @ Arrow IV (Homing)" : [["(IS) Arrow IV Missile"], 5, 1, "X", 15000],
    "(CL) @ Arrow IV (Non-Homing)" :
        [["(CL) Arrow IV Missile"], 5, 1, "X", 10000],
    "(CL) @ Arrow IV (Homing)" : [["(CL) Arrow IV Missile"], 5, 1, "X", 15000],
    "@ Sniper" : [["(IS) Sniper"], 10, 1, "X", 6000]
    }

# Equipment
#
# Name : off BV, def BV, rules level, weight, uses ammo rate, explosive slots,
# cost
#
# Where rules level is: 0 = intro, 1 = tournament legal, 2 = advanced,
# 3 = experimental, 4 = primitive
#

EQUIPMENT = {
    # Tournament legal, TM
    "C3 Computer (Slave)" : [[0, 0], [0, 0], 1, 1, 0, 0, 250000],
    "C3 Computer (Master)" : [[0, 0], [0, 0], 1, 5, 0, 0, 1500000],
    "Improved C3 Computer" : [[0, 0], [0, 0], 1, 2.5, 0, 0, 750000],
    "TAG" : [[0, 0], [0, 0], 1, 1, 0, 0, 50000],
    "Light TAG" : [[0, 0], [0, 0], 1, 0.5, 0, 0, 40000],
    "A-Pod" : [[0, 0], [1, 0], 1, 0.5, 0, 0, 1500],
    "B-Pod" : [[0, 0], [2, 0], 1, 1, 0, 0, 2500],
    "(IS) Anti-Missile System" : [[0, 0], [32, 11], 1, 0.5, 1, 0, 100000],
    "Guardian ECM Suite" : [[0, 0], [61, 0], 1, 1.5, 0, 0, 200000],
    "Beagle Active Probe" : [[0, 0], [10, 0], 1, 1.5, 0, 0, 200000],
    "ECM Suite" : [[0, 0], [61, 0], 1, 1, 0, 0, 200000], # Clan
    "Active Probe" : [[0, 0], [12, 0], 1, 1, 0, 0, 200000], # Clan
    "Light Active Probe" : [[0, 0], [7, 0], 1, 0.5, 0, 0, 50000],
    "(CL) Anti-Missile System" : [[0, 0], [32, 22], 1, 0.5, 1, 0, 100000],
    # Industrial gear, TM
    "Cargo, Liquid" : [[0, 0], [0, 0], 1, 1, 0, 0, 100],
    "Communications Equipment" : [[0, 0], [0, 0], 1, 1, 0, 0, 10000],
    "Remote Sensor Dispenser" : [[0, 0], [0, 0], 1, 0.5, 1, 0, 30000],
    "Lift Hoist" : [[0, 0], [0, 0], 1, 3, 0, 0, 50000],
    # New TL
    "Watchdog CEWS" : [[0, 0], [68, 0], 1, 1.5, 0, 0, 600000],

    # Advandced
    "Angel ECM" : [[0, 0], [100, 0], 2, 2, 0, 0, 750000],
    "Bloodhound Active Probe" : [[0, 0], [25, 0], 2, 2, 0, 0, 500000],
    "Chaff Pod" : [[0, 0], [19, 0], 2, 1, 0, 1, 2000],
    "Coolant Pod" : [[0, 0], [0, 0], 2, 1, 0, 1, 50000],
    "(IS) Laser Anti-Missile System" : [[0, 0], [45, 0], 2, 1.5, 0, 0, 225000],
    "(CL) Laser Anti-Missile System" : [[0, 0], [45, 0], 2, 1, 0, 0, 225000],
    "M-Pod" : [[5, 0], [0, 0], 2, 1, 0, 1, 6000],
    "MW Aquatic Survival System" : [[0, 0], [9, 0], 2, 1.5, 0, 0, 4000],
    # Experimental
    "Collapsible Command Module (CCM)" : [[0, 0], [0, 0], 3, 16, 0, 0, 500000],
    "C3 Boosted Computer (Slave)" : [[0, 0], [0, 0], 3, 3, 0, 0, 500000],
    "C3 Boosted Computer (Master)" : [[0, 0], [0, 0], 3, 6, 0, 0, 3000000], 
    "Electronic Warfare Equipment" : [[0, 0], [39, 0], 3, 7.5, 0, 0, 500000],
    "HarJel" : [[0, 0], [0, 0], 3, 1, 0, 0, 120000],
    "C3 Remote Sensor Launcher" : [[30, 6], [0, 0], 3, 4, 1, 0, 400000],
    }

# CASE
#
# Name : rules level, weight
#
# Where rules level is: 0 = intro, 1 = tournament legal, 2 = advanced,
# 3 = experimental, 4 = primitive
#

CASE = {
    "CASE" : [1, 0.5],
    "(IS) CASE II" : [2, 1],
    "(CL) CASE II" : [2, 0.5]
    }

# Targeting computers
#
# rules level
#
TARCOMPS = {
    "(IS) Targeting Computer" : [1],
    "(CL) Targeting Computer" : [1]
    }

# Info on heatsink types
#
# Name, techbase, sinking capability, rules level, cost factor
#
# Where techbase 0 = IS, 1 = Clan, 2 = Both, 10 = unknown
# Where rules level is 0 = intro, 1 = TL, 2 = advanced, 3 = experimental
#
HEATSINK = [["Single Heat Sink", 2, 1, 0, 2000],
            ["Double Heat Sink", 0, 2, 1, 6000],
            ["Double Heat Sink", 1, 2, 1, 6000],
            ["Laser Heat Sink", 1, 2, 2, 6000]]

class Heatsinks(Item):
    """
    Heatsinks for a mech

    Warning: fusion engine with 10 free sinks is assumed
    """
    def __init__(self, heat):
        Item.__init__(self)
        # Handle default
        if heat is None:
            self.number = 0
            self.tech_b = 2
            self.type = "Single Heat Sink"
        else:
            self.number = int(heat.attributes["number"].value)
            self.tech_b = int(heat.attributes["techbase"].value)
            self.type = get_child_data(heat, "type")
        
        # Check for heatsink type, save data
        ident = False
        for i in HEATSINK:
            if (i[0] == self.type and i[1] == self.tech_b):
                ident = True
                self.cap = i[2]
                self.r_level = i[3]
                self.cost = i[4]
        if not ident:
            error_exit((self.type, self.tech_b))

    def get_type(self):
        """
        Return heat-sink type
        """
        return str(self.number) + " " + self.type

    def get_rules_level(self):
        """
        Return heat-sink rules level
        0 = intro, 1 = tournament legal, 2 = advanced, 3 = experimental
        """
        return self.r_level

    def get_weight(self):
        """
        Return heatsink weight
        1 ton/sink, 10 free
        """
        return self.number - 10

    def get_cost(self):
        """
        Return heatsink cost
        10 single heat sinks in fusion engine costs nothing
        """
        if self.type == "Single Heat Sink":
            return (self.number - 10) * self.cost
        else:
            return self.number * self.cost

    def get_sink(self):
        """
        Return sinking capability
        """
        return self.number * self.cap


class Equip:
    """
    A class used to extract raw gear and format its data
    """
    def __init__(self, node):
        self.name = get_child_data(node, "name")
        self.typ = get_child_data(node, "type")
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


class Ammolist:
    """
    Store the list with weapon types
    """
    def __init__(self):
        self.list = []
        for ammo in AMMO.keys():
            self.list.append(Ammo(ammo))

class Ammo:
    """
    An individual ammo type
    """
    def __init__(self, key):
        self.name = key
        self.wname = AMMO[key][0]
        self.amount = AMMO[key][1]
        self.weight = AMMO[key][2]
        self.explosive = AMMO[key][3]
        self.count = 0

    def addone(self):
        """
        Add one ammo item
        """
        self.count = self.count + 1

    def get_weight(self):
        """
        Return ammo weight for one item
        """
        return AMMO[self.name][2]



class Equiplist:
    """
    Store the list with equipment
    """
    def __init__(self):
        self.list = []
        for equip in EQUIPMENT.keys():
            self.list.append(Equipment(equip))

    def get_rules_level(self):
        """
        Return rules level for all equipment
        """
        r_level = 0
        for equip in self.list:
            if equip.get_rules_level() > r_level and equip.count > 0:
                r_level = equip.get_rules_level()
        return r_level

    def get_cost(self):
        """
        Return the cost of all equipment
        """
        cost = 0
        for equip in self.list:
            if equip.count > 0:
                cost += equip.count * equip.get_cost()
        return cost

    def get_def_bv(self):
        """
        Get defensive gear BV
        """
        batt_val = 0.0
        for equip in self.list:
            if (equip.count > 0):
                bv_gear = equip.count * equip.def_bv[0]
                batt_val += bv_gear
                # Handle AMS ammo (and possible other ammo)
                if (equip.def_bv[1] > 0 and equip.ammocount > 0):
                    bv_ammo = equip.def_bv[1] * equip.ammo_ton
                    # Disallow ammo BV to be greater than that of
                    # the system itself
                    if bv_ammo > bv_gear:
                        bv_ammo = bv_gear
                    batt_val += bv_ammo
        return batt_val

class Equipment:
    """
    An equipment type
    """
    def __init__(self, key):
        self.name = key
        self.off_bv = EQUIPMENT[key][0]
        self.def_bv = EQUIPMENT[key][1]
        self.useammo = EQUIPMENT[key][4]
        self.expl = EQUIPMENT[key][5]
        self.count = 0
        self.ammocount = 0
        self.ammo_ton = 0

    def get_rules_level(self):
        """
        Get rules level of equipment
        """
        return EQUIPMENT[self.name][2]

    def get_weight(self):
        """
        Get weight of equipment
        """
        return EQUIPMENT[self.name][3]

    def get_cost(self):
        """
        Get cost of one piece of equipment
        """
        return EQUIPMENT[self.name][6]

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

class Gear:
    """
    Store Gear

    Take in lists of front and rear facing gears
    """
    def __init__(self, weight, art4, art5, apollo, equip, clan_case):
        self.equip = equip
        self.c_case = clan_case # Clan CASE

        # We need to create local lists for avoid trouble with Omni-mechs
        self.weaponlist = Weaponlist(art4, art5, apollo)
        self.equiplist = Equiplist()
        self.physicallist = Physicallist(weight)
        self.ammolist = Ammolist()
        # Keep track of tarcomp
        self.tarcomp = 0
        # Gear weight
        self.a_weight = 0.0
        self.e_weight = 0.0
        self.tc_weight = 0.0
        # Track explosive ammo by locations
        self.exp_ammo = {}
        # Save reference to explosive weapon count
        self.exp_weapon = self.weaponlist.exp_weapon
        self.case = {}
        # Track coolant pods
        self.coolant = 0
        self.supercharger = False
        # Track modular armor
        self.mod_armor = {}
        self.has_mod_armor = False
        # Track CASE rules level
        self.case_rule = 0

        ### Count gear ###
        for name in self.equip:
            ### Weapons ###
            # Go through weapon list
            ident = False
            # A weapon
            if (name.typ == 'ballistic' or name.typ == 'energy' or
                name.typ == 'missile' or name.typ == 'artillery' or
                name.typ == 'mgarray'):
                found = self.weaponlist.add(name.name, name.loc, name.rear)
                if found:
                    ident = True

            # Handle non-weapon equipment
            elif (name.typ == 'equipment'):
                for equip in self.equiplist.list:
                    if (name.name == equip.name):
                        equip.addone()
                        self.e_weight += equip.get_weight()
                        ident = True
                        # Hack, coolant pods
                        if name.name == "Coolant Pod":
                            self.coolant += 1
                        # Add explosive equipment to location
                        if equip.expl > 0:
                            self.exp_weapon.add_weapon(name.loc, equip.expl)
            # Hack, CASE
            elif (name.typ == 'CASE' or name.typ == 'CASEII'):
                for cas in CASE.keys():
                    if (name.name == cas):
                        self.e_weight += CASE[cas][1]
                        ident = True
                        # Save CASE status
                        self.case[name.loc] = name.typ
                        # Hack CASE rules level
                        if self.case_rule < CASE[cas][0]:
                            self.case_rule = CASE[cas][0]

            # Hack, handle targeting computer
            elif (name.name == "(IS) Targeting Computer" and
                name.typ =='TargetingComputer'):
                self.tarcomp = 1
                ident = True
            elif (name.name == "(CL) Targeting Computer" and
                name.typ =='TargetingComputer'):
                self.tarcomp = 2
                ident = True

            # Hack, supercharger
            elif (name.name == "Supercharger" and name.typ == "Supercharger"):
                self.supercharger = True
                ident = True

            # A possible physical weapon
            elif (name.typ == 'physical'):
                found = self.physicallist.add(name.name, name.loc)
                if found:
                    ident = True

            # Modular armor
            elif (name.typ == 'miscellaneous'):
                if name.name == "Modular Armor":
                    ident = True
                    mod = self.mod_armor.get(name.loc, 0)
                    mod += 10
                    self.mod_armor[name.loc] = mod
                    self.has_mod_armor = True

            # Ammunition
            elif (name.typ == 'ammunition'):
                for ammo in self.ammolist.list:
                    if (name.name == ammo.name):
                        ammo.addone()
                        self.a_weight += ammo.get_weight()
                        ident = True
                        # Add explosive ammo to location
                        if ammo.explosive == "X":
                            expl = self.exp_ammo.get(name.loc, 0)
                            expl += 1
                            self.exp_ammo[name.loc] = expl

            # Not found
            if not ident:
                print "Unidentified:", name.name, ":", name.typ
                error_exit("gear")

        # Calculate tarcomp weight
        if self.tarcomp == 1:  #IS
            self.tc_weight = ceil(self.weaponlist.tcw_weight / 4.0)
        if self.tarcomp == 2:  #Clan
            self.tc_weight = ceil(self.weaponlist.tcw_weight / 5.0)

        # Add ammo to weapon
        for ammo in self.ammolist.list:
            if ammo.count > 0:
                ident = False
                for weap in self.weaponlist.list.itervalues():
                    for i in ammo.wname:
                        if weap.name == i:
                            weap.add_ammo(ammo.count * ammo.weight,
                                          ammo.count * ammo.amount)
                            ident = True
                # We need to do defensive equipment also due to AMS
                for equip in self.equiplist.list:
                    for i in ammo.wname:
                        if equip.name == i:
                            equip.add_ammo(ammo.count * ammo.weight,
                                           ammo.count * ammo.amount)
                            ident = True
                if (not ident):
                    print "ERROR: Unknown weapon:", ammo.wname
                    error_exit("weapon")

    def get_rules_level(self):
        """
        Get rules level of all gear

        No checking for ammo, since we can assume that there is ammo
        of the same rules level as the corresponding weapon
        and that more advanced ammo can be switched out
        """
        r_level = 0
        tmp = self.weaponlist.get_rules_level()
        if tmp > r_level:
            r_level = tmp
        tmp = self.physicallist.get_rules_level()
        if tmp > r_level:
            r_level = tmp
        tmp = self.equiplist.get_rules_level()
        if tmp > r_level:
            r_level = tmp
        # Hack: Supercharger is advanced rules
        if self.supercharger and r_level < 2:
            r_level = 2
        # Hack: Targeting computer
        if self.tarcomp > 0 and r_level < 1:
            r_level = 1
        # Hack: CASE
        if self.case_rule > r_level:
            r_level = self.case_rule

        return r_level

    def get_cost(self):
        """
        Get the cost of all equipment

        Ammo cost will not be handled by this fuction, due to the
        difference between dry and loaded costs.
        """
        cost = 0
        # weapons
        cost += self.weaponlist.get_cost()
        # physical
        cost += self.physicallist.get_cost()
        # equipment
        cost += self.equiplist.get_cost()
        # TODO: Supercharger
        # 10000 x Engine rating
        # Hack: Targeting computer
        if self.tarcomp > 0:
            cost += 10000 * self.tc_weight

        # Hack: CASE
        for cas in self.case.itervalues():
            if cas == "CASE":
                cost += 50000
            elif cas == "CASEII":
                cost += 175000
        # Hack: Clan CASE
        if self.c_case == "TRUE":
            case_list = {}
            for i in self.exp_ammo.keys():
                case_list[i] = 1
            for i in self.exp_weapon.get_keys():
                case_list[i] = 1
            cost += len(case_list) * 50000

        return cost


    def get_w_weight(self):
        """
        Get weapons weight
        """
        return self.weaponlist.w_weight

    def get_a_weight(self):
        """
        Get ammo weight
        """
        return self.a_weight

    def get_e_weight(self):
        """
        Get equipment, tarcomp & CASE weight
        """
        return self.e_weight + self.tc_weight

    def get_p_weight(self):
        """
        Get physical weapon weight
        """
        return self.physicallist.p_weight

    def get_speed_adj(self):
        """
        Get speed reduction from certain items, like shields and modular armor.
        """
        red = 0
        red += self.physicallist.get_speed_adj()
        if self.has_mod_armor:
            red -= 1
        return red

    def get_def_bv(self):
        """
        Get defensive gear BV
        """
        batt_val = 0.0
        # From gear
        batt_val += self.equiplist.get_def_bv()
        # Defensive physical weapons
        batt_val += self.physicallist.get_def_bv()
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
            if (i == "HD" or i == "CT"):
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
                elif (self.c_case == "FALSE"):
                    # No CASE
                    if (cas != "CASE" and cas != "CASEII"):
                        neg_bv -= 15.0 * self.exp_ammo[i]
            # Arms are complicated
            elif (i == "LA" or i == "FLL"):
                # we can use torso CASE
                cas2 = self.case.get("LT", "")
                # Inner Sphere XL Engines means that side torsos are vulnerable
                if engine.vulnerable():
                    if (cas != "CASEII" and cas2 != "CASEII"
                        and self.c_case == "FALSE"):
                        neg_bv -= 15.0 * self.exp_ammo[i]
                # Otherwise we check for CASE
                elif (self.c_case == "FALSE"):
                    # No CASE
                    if ((cas != "CASE" and cas != "CASEII") and
                        (cas2 != "CASE" and cas2 != "CASEII")):
                        neg_bv -= 15.0 * self.exp_ammo[i]
            elif (i == "RA" or i == "FRL"):
                # we can use torso CASE
                cas2 = self.case.get("RT", "")
                # Inner Sphere XL Engines means that side torsos are vulnerable
                if engine.vulnerable():
                    if (cas != "CASEII" and cas2 != "CASEII"
                        and self.c_case == "FALSE"):
                        neg_bv -= 15.0 * self.exp_ammo[i]
                # Otherwise we check for CASE
                elif (self.c_case == "FALSE"):
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
        for i in self.exp_weapon.get_keys():
            cas = self.case.get(i, "")
            # Head and center torso always
            if (i == "HD" or i == "CT"):
                neg_bv -= self.exp_weapon.get_slots(i)
            # So are legs
            elif (i == "LL" or i == "RL" or i == "RLL" or i == "RRL"):
                neg_bv -= self.exp_weapon.get_slots(i)
            # Side torsos depends on several factors
            elif (i == "LT" or i == "RT"):
                # Inner Sphere XL Engines means that side torsos are vulnerable
                if engine.vulnerable():
                    if (cas != "CASEII"):
                        neg_bv -= self.exp_weapon.get_slots(i)
                # Otherwise we check for CASE
                elif (self.c_case == "FALSE"):
                    # No CASE
                    if (cas != "CASE" and cas != "CASEII"):
                        neg_bv -= self.exp_weapon.get_slots(i)
            # Arms are complicated
            elif (i == "LA" or i == "FLL"):
                # we can use torso CASE
                cas2 = self.case.get("LT", "")
                # Inner Sphere XL Engines means that side torsos are vulnerable
                if engine.vulnerable():
                    if (cas != "CASEII" and cas2 != "CASEII"
                        and self.c_case == "FALSE"):
                        neg_bv -= self.exp_weapon.get_slots(i)
                # Otherwise we check for CASE
                elif (self.c_case == "FALSE"):
                    # No CASE
                    if ((cas != "CASE" and cas != "CASEII") and
                        (cas2 != "CASE" and cas2 != "CASEII")):
                        neg_bv -= self.exp_weapon.get_slots(i)
            elif (i == "RA" or i == "FRL"):
                # we can use torso CASE
                cas2 = self.case.get("RT", "")
                # Inner Sphere XL Engines means that side torsos are vulnerable
                if engine.vulnerable():
                    if (cas != "CASEII" and cas2 != "CASEII"
                        and self.c_case == "FALSE"):
                        neg_bv -= self.exp_weapon.get_slots(i)
                # Otherwise we check for CASE
                elif (self.c_case == "FALSE"):
                    # No CASE
                    if ((cas != "CASE" and cas != "CASEII") and
                        (cas2 != "CASE" and cas2 != "CASEII")):
                        neg_bv -= self.exp_weapon.get_slots(i)
        return neg_bv

    def check_weapon_bv_flip(self):
        """
        Check if front and rear weapons needs to be flipped for BV calculations
        """
        bv_front = 0.0
        bv_rear = 0.0
        # Weapons
        for weap in self.weaponlist.list.itervalues():
            if (weap.count - weap.count_la - weap.count_ra) > 0:
                bv_front += weap.get_bv(self.tarcomp) * (weap.count -
                                                         weap.count_la -
                                                         weap.count_ra)

            if weap.countrear > 0:
                bv_rear += weap.get_bv(self.tarcomp) * weap.countrear
 
        if (bv_rear > bv_front):
            return True
        else:
            return False
        

