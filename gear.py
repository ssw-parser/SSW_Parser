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
from weapons import WEAPONS, LRM_LIST, Weaponlist
from physical import PHYSICAL, Physicallist

# A class to contain data about battlemech gear to allow for clearer code,
# by using named class members.

# Ammo
#
# Name, weapon, amount, weight, explosive?
#
AMMO = {
    "(IS) @ AC/2" : [["(IS) Autocannon/2"], 45, 1, "X"],
    "(IS) @ AC/5" : [["(IS) Autocannon/5"], 20, 1, "X"],
    "(IS) @ AC/10" : [["(IS) Autocannon/10"], 10, 1, "X"],
    "(IS) @ AC/20" : [["(IS) Autocannon/20"], 5, 1, "X"],
    "(IS) @ Light Gauss Rifle" : [["(IS) Light Gauss Rifle"], 16, 1, ""],
    "@ Gauss Rifle" : [["(IS) Gauss Rifle", "(CL) Gauss Rifle"], 8, 1, ""],
    "(IS) @ Heavy Gauss Rifle" : [["(IS) Heavy Gauss Rifle"], 4, 1, ""],
    "(IS) @ LB 2-X AC (Slug)" : [["(IS) LB 2-X AC"], 45, 1, "X"],
    "(IS) @ LB 2-X AC (Cluster)" : [["(IS) LB 2-X AC"], 45, 1, "X"],
    "(IS) @ LB 5-X AC (Slug)" : [["(IS) LB 5-X AC"], 20, 1, "X"],
    "(IS) @ LB 5-X AC (Cluster)" : [["(IS) LB 5-X AC"], 20, 1, "X"],
    "(IS) @ LB 10-X AC (Slug)" : [["(IS) LB 10-X AC"], 10, 1, "X"],
    "(IS) @ LB 10-X AC (Cluster)" : [["(IS) LB 10-X AC"], 10, 1, "X"],
    "(IS) @ LB 20-X AC (Slug)" : [["(IS) LB 20-X AC"], 5, 1, "X"],
    "(IS) @ LB 20-X AC (Cluster)" : [["(IS) LB 20-X AC"], 5, 1, "X"],
    "(IS) @ Light AC/2" : [["(IS) Light AC/2"], 45, 1, "X"],
    "(IS) @ Light AC/5" : [["(IS) Light AC/5"], 20, 1, "X"],
    "@ Light Machine Gun" :
        [["(IS) Light Machine Gun", "(CL) Light Machine Gun",
          "(IS) MG Array (2 Light Machine Gun)",
          "(IS) MG Array (3 Light Machine Gun)",
          "(IS) MG Array (4 Light Machine Gun)",
          "(CL) MG Array (3 Light Machine Gun)",
          "(CL) MG Array (4 Light Machine Gun)"], 200, 1, "X"],
    "@ Light Machine Gun (1/2)" :
        [["(IS) Light Machine Gun", "(CL) Light Machine Gun",
          "(IS) MG Array (2 Light Machine Gun)",
          "(IS) MG Array (3 Light Machine Gun)",
          "(IS) MG Array (4 Light Machine Gun)",
          "(CL) MG Array (3 Light Machine Gun)",
          "(CL) MG Array (4 Light Machine Gun)"], 100, 0.5, "X"],
    "@ Machine Gun" :
        [["(IS) Machine Gun", "(CL) Machine Gun",
          "(IS) MG Array (3 Machine Gun)",
          "(IS) MG Array (4 Machine Gun)",
          "(CL) MG Array (4 Machine Gun)"], 200, 1, "X"],
    "@ Machine Gun (1/2)" :
        [["(IS) Machine Gun", "(CL) Machine Gun",
          "(IS) MG Array (3 Machine Gun)",
          "(IS) MG Array (4 Machine Gun)",
          "(CL) MG Array (4 Machine Gun)"], 100, 0.5, "X"],
    "@ Heavy Machine Gun" :
        [["(CL) Heavy Machine Gun",
          "(IS) MG Array (3 Heavy Machine Gun)",
          "(CL) MG Array (3 Heavy Machine Gun)",
          "(CL) MG Array (4 Heavy Machine Gun)"], 100, 1, "X"],
    "@ Heavy Machine Gun (1/2)" :
        [["(CL) Heavy Machine Gun",
          "(IS) MG Array (3 Heavy Machine Gun)",
          "(CL) MG Array (3 Heavy Machine Gun)",
          "(CL) MG Array (4 Heavy Machine Gun)"], 50, 0.5, "X"],
    "(IS) @ Rotary AC/2" : [["(IS) Rotary AC/2"], 45, 1, "X"],
    "(IS) @ Rotary AC/5" : [["(IS) Rotary AC/5"], 20, 1, "X"],
    "(IS) @ Ultra AC/2" : [["(IS) Ultra AC/2"], 45, 1, "X"],
    "(IS) @ Ultra AC/5" : [["(IS) Ultra AC/5"], 20, 1, "X"],
    "(IS) @ Ultra AC/10" : [["(IS) Ultra AC/10"], 10, 1, "X"],
    "(IS) @ Ultra AC/20" : [["(IS) Ultra AC/20"], 5, 1, "X"],
    "(IS) @ Plasma Rifle" : [["(IS) Plasma Rifle"], 10, 1, ""],
    "(IS) @ LRM-5" : [["(IS) LRM-5"], 24, 1, "X"],
    "(IS) @ LRM-10" : [["(IS) LRM-10"], 12, 1, "X"],
    "(IS) @ LRM-15" : [["(IS) LRM-15"], 8, 1, "X"],
    "(IS) @ LRM-20" : [["(IS) LRM-20"], 6, 1, "X"],
    "(IS) @ LRM-5 (Artemis IV Capable)" : [["(IS) LRM-5"], 24, 1, "X"],
    "(IS) @ LRM-10 (Artemis IV Capable)" : [["(IS) LRM-10"], 12, 1, "X"],
    "(IS) @ LRM-15 (Artemis IV Capable)" : [["(IS) LRM-15"], 8, 1, "X"],
    "(IS) @ LRM-20 (Artemis IV Capable)" : [["(IS) LRM-20"], 6, 1, "X"],
    "(IS) @ LRM-5 (Narc Capable)" : [["(IS) LRM-5"], 24, 1, "X"],
    "(IS) @ LRM-10 (Narc Capable)" : [["(IS) LRM-10"], 12, 1, "X"],
    "(IS) @ LRM-15 (Narc Capable)" : [["(IS) LRM-15"], 8, 1, "X"],
    "(IS) @ LRM-20 (Narc Capable)" : [["(IS) LRM-20"], 6, 1, "X"],
    "(IS) @ LRT-5 (Torpedo)" : [["(IS) LRT-5"], 24, 1, "X"],
    "(IS) @ LRT-10 (Torpedo)" : [["(IS) LRT-10"], 12, 1, "X"],
    "(IS) @ LRT-15 (Torpedo)" : [["(IS) LRT-15"], 8, 1, "X"],
    "(IS) @ MML-3 (LRM)" : [["(IS) MML-3"], 40, 1, "X"],
    "(IS) @ MML-3 (SRM)" : [["(IS) MML-3"], 33, 1, "X"],
    "(IS) @ MML-5 (LRM)" : [["(IS) MML-5"], 24, 1, "X"],
    "(IS) @ MML-5 (SRM)" : [["(IS) MML-5"], 20, 1, "X"],
    "(IS) @ MML-7 (LRM)" : [["(IS) MML-7"], 17, 1, "X"],
    "(IS) @ MML-7 (SRM)" : [["(IS) MML-7"], 14, 1, "X"],
    "(IS) @ MML-9 (LRM)" : [["(IS) MML-9"], 13, 1, "X"],
    "(IS) @ MML-9 (SRM)" : [["(IS) MML-9"], 11, 1, "X"],
    "(IS) @ MML-3 (LRM Artemis IV Capable)" : [["(IS) MML-3"], 40, 1, "X"],
    "(IS) @ MML-3 (SRM Artemis IV Capable)" : [["(IS) MML-3"], 33, 1, "X"],
    "(IS) @ MML-5 (LRM Artemis IV Capable)" : [["(IS) MML-5"], 24, 1, "X"],
    "(IS) @ MML-5 (SRM Artemis IV Capable)" : [["(IS) MML-5"], 20, 1, "X"],
    "(IS) @ MML-7 (LRM Artemis IV Capable)" : [["(IS) MML-7"], 17, 1, "X"],
    "(IS) @ MML-7 (SRM Artemis IV Capable)" : [["(IS) MML-7"], 14, 1, "X"],
    "(IS) @ MML-9 (LRM Artemis IV Capable)" : [["(IS) MML-9"], 13, 1, "X"],
    "(IS) @ MML-9 (SRM Artemis IV Capable)" : [["(IS) MML-9"], 11, 1, "X"],
    "(IS) @ MRM-10" : [["(IS) MRM-10"], 24, 1, "X"],
    "(IS) @ MRM-20" : [["(IS) MRM-20"], 12, 1, "X"],
    "(IS) @ MRM-30" : [["(IS) MRM-30"], 8, 1, "X"],
    "(IS) @ MRM-40" : [["(IS) MRM-40"], 6, 1, "X"],
    "@ SRM-2" : [["(IS) SRM-2", "(CL) SRM-2"], 50, 1, "X"],
    "@ SRM-4" : [["(IS) SRM-4", "(CL) SRM-4"], 25, 1, "X"],
    "@ SRM-6" : [["(IS) SRM-6", "(CL) SRM-6"], 15, 1, "X"],
    "@ SRM-4 (Artemis IV Capable)" :
        [["(IS) SRM-4", "(CL) SRM-4"], 25, 1, "X"],
    "@ SRM-6 (Artemis IV Capable)" :
        [["(IS) SRM-6", "(CL) SRM-6"], 15, 1, "X"],
    "@ SRM-2 (Narc Capable)" : [["(IS) SRM-2", "(CL) SRM-2"], 50, 1, "X"],
    "@ SRM-4 (Narc Capable)" : [["(IS) SRM-4", "(CL) SRM-4"], 25, 1, "X"],
    "@ SRM-6 (Narc Capable)" : [["(IS) SRM-6", "(CL) SRM-6"], 15, 1, "X"],
    "@ SRT-2 (Torpedo)" : [["(CL) SRT-2"], 50, 1, "X"],
    "@ SRT-4 (Torpedo)" : [["(IS) SRT-4", "(CL) SRT-4"], 25, 1, "X"],
    "@ SRT-6 (Torpedo)" : [["(CL) SRT-6"], 15, 1, "X"],
    "(IS) @ Streak SRM-2" : [["(IS) Streak SRM-2"], 50, 1, "X"],
    "(IS) @ Streak SRM-4" : [["(IS) Streak SRM-4"], 25, 1, "X"],
    "(IS) @ Streak SRM-6" : [["(IS) Streak SRM-6"], 15, 1, "X"],
    "(IS) @ Narc (Homing)" : [["(IS) Narc Missile Beacon"], 6, 1, "X"],
    "(IS) @ iNarc (Homing)" : [["(IS) iNarc Launcher"], 4, 1, "X"],
    "(IS) @ Anti-Missile System" :
        [["(IS) Anti-Missile System"], 12, 1, "X"],
    # Advanced
    "(IS) @ Magshot Gauss Rifle" : [["(IS) Magshot Gauss Rifle"], 50, 1, ""],
    "(IS) @ BattleMech Taser" : [["(IS) BattleMech Taser"], 5, 1, "X"],
    "(IS) @ Thunderbolt-5" : [["(IS) Thunderbolt-5"], 12, 1, "X"],
    "(IS) @ Thunderbolt-10" : [["(IS) Thunderbolt-10"], 6, 1, "X"],
    "(IS) @ Thunderbolt-15" : [["(IS) Thunderbolt-15"], 4, 1, "X"],
    "(IS) @ Thunderbolt-20" : [["(IS) Thunderbolt-20"], 3, 1, "X"],
    "(IS) @ NLRM-5" : [["(IS) Enhanced LRM-5"], 24, 1, "X"],
    "(IS) @ ELRM-10" : [["(IS) Extended LRM-10"], 9, 1, "X"],
    "(IS) @ ELRM-20" : [["(IS) Extended LRM-20"], 4, 1, "X"],
    "@ Fluid Gun (Water)" : [["(IS) Fluid Gun"], 20, 1, ""],
    "@ C3 Remote Launcher" : [["C3 Remote Sensor Launcher"], 4, 1, "X"],
    # Clan
    "(CL) @ LB 2-X AC (Slug)" : [["(CL) LB 2-X AC"], 45, 1, "X"],
    "(CL) @ LB 2-X AC (Cluster)" : [["(CL) LB 2-X AC"], 45, 1, "X"],
    "(CL) @ LB 5-X AC (Slug)" : [["(CL) LB 5-X AC"], 20, 1, "X"],
    "(CL) @ LB 5-X AC (Cluster)" : [["(CL) LB 5-X AC"], 20, 1, "X"],
    "(CL) @ LB 10-X AC (Slug)" : [["(CL) LB 10-X AC"], 10, 1, "X"],
    "(CL) @ LB 10-X AC (Cluster)" : [["(CL) LB 10-X AC"], 10, 1, "X"],
    "(CL) @ LB 20-X AC (Slug)" : [["(CL) LB 20-X AC"], 5, 1, "X"],
    "(CL) @ LB 20-X AC (Cluster)" : [["(CL) LB 20-X AC"], 5, 1, "X"],
    "(CL) @ Ultra AC/2" : [["(CL) Ultra AC/2"], 45, 1, "X"],
    "(CL) @ Ultra AC/5" : [["(CL) Ultra AC/5"], 20, 1, "X"],
    "(CL) @ Ultra AC/10" : [["(CL) Ultra AC/10"], 10, 1, "X"],
    "(CL) @ Ultra AC/20" : [["(CL) Ultra AC/20"], 5, 1, "X"],
    "(CL) @ AP Gauss Rifle" : [["(CL) AP Gauss Rifle"], 40, 1, ""],
    "(CL) @ Hyper Assault Gauss 20" :
        [["(CL) Hyper Assault Gauss 20"], 6, 1, ""],
    "(CL) @ Hyper Assault Gauss 30" :
        [["(CL) Hyper Assault Gauss 30"], 4, 1, ""],
    "(CL) @ Hyper Assault Gauss 40" :
        [["(CL) Hyper Assault Gauss 40"], 3, 1, ""],
    "(CL) @ Plasma Cannon" : [["(CL) Plasma Cannon"], 10, 1, ""],
    "(CL) @ ATM-3" : [["(CL) ATM-3"], 20, 1, "X"],
    "(CL) @ ATM-3 (ER)" : [["(CL) ATM-3"], 20, 1, "X"],
    "(CL) @ ATM-3 (HE)" : [["(CL) ATM-3"], 20, 1, "X"],
    "(CL) @ ATM-6" : [["(CL) ATM-6"], 10, 1, "X"],
    "(CL) @ ATM-6 (ER)" : [["(CL) ATM-6"], 10, 1, "X"],
    "(CL) @ ATM-6 (HE)" : [["(CL) ATM-6"], 10, 1, "X"],
    "(CL) @ ATM-9" : [["(CL) ATM-9"], 7, 1, "X"],
    "(CL) @ ATM-9 (ER)" : [["(CL) ATM-9"], 7, 1, "X"],
    "(CL) @ ATM-9 (HE)" : [["(CL) ATM-9"], 7, 1, "X"],
    "(CL) @ ATM-12" : [["(CL) ATM-12"], 5, 1, "X"],
    "(CL) @ ATM-12 (ER)" : [["(CL) ATM-12"], 5, 1, "X"],
    "(CL) @ ATM-12 (HE)" : [["(CL) ATM-12"], 5, 1, "X"],
    "(CL) @ LRM-5" : [["(CL) LRM-5"], 24, 1, "X"],
    "(CL) @ LRM-10" : [["(CL) LRM-10"], 12, 1, "X"],
    "(CL) @ LRM-15" : [["(CL) LRM-15"], 8, 1, "X"],
    "(CL) @ LRM-20" : [["(CL) LRM-20"], 6, 1, "X"],
    "(CL) @ LRM-5 (Artemis IV Capable)" : [["(CL) LRM-5"], 24, 1, "X"],
    "(CL) @ LRM-10 (Artemis IV Capable)" : [["(CL) LRM-10"], 12, 1, "X"],
    "(CL) @ LRM-15 (Artemis IV Capable)" : [["(CL) LRM-15"], 8, 1, "X"],
    "(CL) @ LRM-20 (Artemis IV Capable)" : [["(CL) LRM-20"], 6, 1, "X"],
    "(CL) @ LRM-15 (Artemis V)" : [["(CL) LRM-15"], 8, 1, "X"],        
    "(CL) @ LRM-20 (Artemis V)" : [["(CL) LRM-20"], 6, 1, "X"],        
    "(CL) @ LRM-5 (Narc Capable)" : [["(CL) LRM-5"], 24, 1, "X"],
    "(CL) @ LRM-15 (Narc Capable)" : [["(CL) LRM-15"], 8, 1, "X"],
    "(CL) @ LRM-20 (Narc Capable)" : [["(CL) LRM-20"], 6, 1, "X"],
    "(CL) @ LRT-5 (Torpedo)" : [["(CL) LRT-5"], 24, 1, "X"],
    "(CL) @ LRT-10 (Torpedo)" : [["(CL) LRT-10"], 12, 1, "X"],
    "(CL) @ LRT-15 (Torpedo)" : [["(CL) LRT-15"], 8, 1, "X"],
    "(CL) @ Streak SRM-2" : [["(CL) Streak SRM-2"], 50, 1, "X"],
    "(CL) @ Streak SRM-4" : [["(CL) Streak SRM-4"], 25, 1, "X"],
    "(CL) @ Streak SRM-6" : [["(CL) Streak SRM-6"], 15, 1, "X"],
    "(CL) @ Narc (Homing)" : [["(CL) Narc Missile Beacon"], 6, 1, "X"],
    "(CL) @ Anti-Missile System" :
        [["(CL) Anti-Missile System"], 24, 1, "X"],
    # Advanced
    "(CL) @ Rotary AC/2" : [["(CL) Rotary AC/2"], 45, 1, "X"],
    "(CL) @ Rotary AC/5" : [["(CL) Rotary AC/5"], 20, 1, "X"],
    "(CL) @ Protomech AC/4" : [["(CL) Protomech AC/4"], 20, 1, "X"],
    "(CL) @ Protomech AC/8" : [["(CL) Protomech AC/8"], 10, 1, "X"],
    "(CL) @ Streak LRM-10" : [["(CL) Streak LRM-10"], 12, 1, "X"],
    "(CL) @ Streak LRM-15" : [["(CL) Streak LRM-15"], 8, 1, "X"],
    "(CL) @ 'Mech Mortar 8 (Anti-Personnel)" :
        [["(CL) Mech Mortar 8"], 4, 1, "X"],
    "@ Heavy Flamer" : [["Heavy Flamer"], 10, 1, "X"],
    "(IS) @ HVAC/10" : [["(IS) Hyper-Velocity Autocannon/10"], 8, 1, "X"],
    "(IS) @ Improved Heavy Gauss Rifle" :
        [["(IS) Improved Heavy Gauss Rifle"], 4, 1, ""],
    "(IS) @ Silver Bullet Gauss" :
        [["(IS) Silver Bullet Gauss"], 8, 1, ""],
    "@ Long Tom Cannon" :
        [["Long Tom Artillery Cannon"], 5, 1, "X"],
    # Artillery
    "(IS) @ Arrow IV (Non-Homing)" : [["(IS) Arrow IV Missile"], 5, 1, "X"],
    "(IS) @ Arrow IV (Homing)" : [["(IS) Arrow IV Missile"], 5, 1, "X"],
    "(CL) @ Arrow IV (Non-Homing)" : [["(CL) Arrow IV Missile"], 5, 1, "X"],
    "(CL) @ Arrow IV (Homing)" : [["(CL) Arrow IV Missile"], 5, 1, "X"],
    "@ Sniper" : [["(IS) Sniper"], 10, 1, "X"]
    }

# Equipment
#
# Name : off BV, def BV, rules level, weight, uses ammo rate, explosive slots
#
# Where rules level is: 0 = intro, 1 = tournament legal, 2 = advanced,
# 3 = experimental, 4 = primitive
#

EQUIPMENT = {
    "C3 Computer (Slave)" : [[0, 0], [0, 0], 1, 1, 0, 0],
    "C3 Computer (Master)" : [[0, 0], [0, 0], 1, 5, 0, 0],
    "Improved C3 Computer" : [[0, 0], [0, 0], 1, 2.5, 0, 0],
    "TAG" : [[0, 0], [0, 0], 1, 1, 0, 0],
    "Light TAG" : [[0, 0], [0, 0], 1, 0.5, 0, 0],
    "Cargo, Liquid" : [[0, 0], [0, 0], 1, 1, 0, 0],
    "Communications Equipment" : [[0, 0], [0, 0], 1, 1, 0, 0],
    "Remote Sensor Dispenser" : [[0, 0], [0, 0], 1, 0.5, 1, 0],
    "Lift Hoist" : [[0, 0], [0, 0], 1, 3, 0, 0],
    # Experimental
    "Chaff Pod" : [[0, 0], [19, 0], 2, 1, 0, 1],
    "Collapsible Command Module (CCM)" : [[0, 0], [0, 0], 3, 16, 0, 0],
    "Coolant Pod" : [[0, 0], [0, 0], 2, 1, 0, 1],
    "C3 Boosted Computer (Slave)" : [[0, 0], [0, 0], 3, 3, 0, 0],
    "C3 Boosted Computer (Master)" : [[0, 0], [0, 0], 3, 6, 0, 0], 

    "A-Pod" : [[0, 0], [1, 0], 1, 0.5, 0, 0],
    "B-Pod" : [[0, 0], [2, 0], 1, 1, 0, 0],
    "(IS) Anti-Missile System" : [[0, 0], [32, 11], 1, 0.5, 1, 0],
    "Guardian ECM Suite" : [[0, 0], [61, 0], 1, 1.5, 0, 0],
    "Beagle Active Probe" : [[0, 0], [10, 0], 1, 1.5, 0, 0],
    "ECM Suite" : [[0, 0], [61, 0], 1, 1, 0, 0], # Clan
    "Active Probe" : [[0, 0], [12, 0], 1, 1, 0, 0], # Clan
    "Light Active Probe" : [[0, 0], [7, 0], 1, 0.5, 0, 0],
    "(CL) Anti-Missile System" : [[0, 0], [32, 22], 1, 0.5, 1, 0],
    # Experimental
    "Angel ECM" : [[0, 0], [100, 0], 2, 2, 0, 0],
    "Bloodhound Active Probe" : [[0, 0], [25, 0], 2, 2, 0, 0],
    "Electronic Warfare Equipment" : [[0, 0], [39, 0], 3, 7.5, 0, 0],
    "(CL) Laser Anti-Missile System" : [[0, 0], [45, 0], 2, 1, 0, 0],
    "Watchdog CEWS" : [[0, 0], [68, 0], 1, 1.5, 0, 0],
    "MW Aquatic Survival System" : [[0, 0], [9, 0], 2, 1.5, 0, 0],
    "HarJel" : [[0, 0], [0, 0], 3, 1, 0, 0],
    "(IS) Laser Anti-Missile System" : [[0, 0], [45, 0], 2, 1.5, 0, 0],
    "M-Pod" : [[5, 0], [0, 0], 2, 1, 0, 1],
    "C3 Remote Sensor Launcher" : [[30, 6], [0, 0], 3, 4, 1, 0],
    }

# CASE
#
# Name : rules level, weight, uses ammo rate, explosive slots
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
# Name, techbase, sinking capability, rules level
#
# Where techbase 0 = IS, 1 = Clan, 2 = Both, 10 = unknown
# Where rules level is 0 = intro, 1 = TL, 2 = advanced, 3 = experimental
#
HEATSINK = [["Single Heat Sink", 2, 1, 0],
            ["Double Heat Sink", 0, 2, 1],
            ["Double Heat Sink", 1, 2, 1],
            ["Laser Heat Sink", 1, 2, 2]]

class Heatsinks(Item):
    """
    Heatsinks for a mech
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

    def get_sink(self):
        """
        Return sinking capability
        """
        return self.number * self.cap


class Equip(Item):
    """
    The new equipment class being tested out
    """
    # TODO: Make a real item
    # TODO: Make this a parent class, and split according to type?
    def __init__(self, node):
        Item.__init__(self)
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


    def get_type(self):
        """
        Return equipment name
        """
        return self.name

    def get_rules_level(self):
        """
        Return rules level of equipment piece
        0 = intro, 1 = tournament legal, 2 = advanced, 3 = experimental
        """
        if (self.typ == "equipment" or self.typ == "CASE" or
            self.typ == "CASEII"):
            rule = EQUIPMENT[self.name][2]
        elif self.typ == "TargetingComputer":
            rule = TARCOMPS[self.name][0]
        elif (self.typ == "ballistic" or self.typ == "energy" or
              self.typ == "missile" or self.typ == "artillery" or
              self.typ == "mgarray"):
            rule = WEAPONS[self.name][2]
        elif self.typ == "physical":
            rule = PHYSICAL[self.name][5]
        # Hack -- assume that ammunition is of same rules level as weapon
        elif self.typ == "ammunition":
            rule = 0
        # Supercharger are advanced rules
        elif self.typ == "Supercharger":
            rule = 2
        # Tarcomps are tournament legal are advanced rules
        elif self.typ == "TargetingComputer":
            rule = 1
        else:
            print "Unknown tech level:", self.name, ":", self.typ
            error_exit("gear")

        return rule

    def get_weight(self):
        # TODO: Artemis & friends weight
        # Tarcomp
        # Physical parameter
        if (self.typ == "equipment" or self.typ == "CASE" or
            self.typ == "CASEII"):
            return EQUIPMENT[self.name][3]
        elif self.typ == "ammunition":
            return AMMO[self.name][2]
        elif self.typ == "physical":
            return PHYSICAL[self.name][2](mech.weight)
        elif (self.typ == "missile" or self.typ == "ballistic" or
              self.typ == "energy"):
            return WEAPONS[self.name][8]
        else:
            print "Unknown item", self.name, self.typ
            raise NotImplementedError
            

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

class Equiplist:
    """
    Store the list with equipment
    """
    def __init__(self):
        self.list = []
        for equip in EQUIPMENT.keys():
            self.list.append(Equipment(equip))

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
        self.weight = EQUIPMENT[key][3]
        self.useammo = EQUIPMENT[key][4]
        self.explosive = EQUIPMENT[key][5]
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

class ExplosiveWeapons:
    """
    Store Where explosive weapon slots are located.
    """
    def __init__(self):
        self.exp_weapon = {}

    def add_weapon(self, location, slots):
        """
        Store where weapon explosive slots are located
        """
        # Split weapons, assign to innermost
        if type(location).__name__ == 'list':
            j = ""
            loc = ""
            for i in location:
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
            expl += slots
            self.exp_weapon[loc] = expl
        # No split, easy to handle
        else:
            expl = self.exp_weapon.get(location, 0)
            expl += slots
            self.exp_weapon[location] = expl

    def get_keys(self):
        """
        Returns all the locations that contains explosive stuff
        """
        return self.exp_weapon.keys()

    def get_slots(self, i):
        """
        Returns how many explosive slots in a given location
        """
        return self.exp_weapon[i]

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
        self.w_weight = 0.0
        self.a_weight = 0.0
        self.e_weight = 0.0
        # Weight of targeting computer weapons
        self.tcw_weight = 0.0
        # Track explosive ammo by locations
        self.exp_ammo = {}
        self.exp_weapon = ExplosiveWeapons()
        self.case = {}
        # Track coolant pods
        self.coolant = 0
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
            # A weapon
            if (name.typ == 'ballistic' or name.typ == 'energy' or
                name.typ == 'missile' or name.typ == 'artillery' or
                name.typ == 'mgarray'):
                for weap in self.weaponlist.list.itervalues():
                    # Weapon identified
                    if (name.name == weap.name):
                        # Add weapon
                        if name.rear:
                            weap.addone_rear()
                        else:
                            weap.addone(name.loc)

                        # track weapons weight
                        self.w_weight += weap.get_weight()
                        # track weight for targeting computer
                        if weap.enhance == "T":
                            self.tcw_weight += weap.get_weight()

                        # We have found a valid weapon
                        ident = True

                        # Count LRM tubes that can fire special ammo
                        # Missing: NLRM-10, NLRM-15, NLRM-20
                        for launcher in LRM_LIST:
                            if (name.name == launcher[0]):
                                self.lrms += launcher[2]

                        # Add explosive weapon to location
                        if weap.explosive > 0:
                            self.exp_weapon.add_weapon(name.loc, weap.explosive)

            # Handle non-weapon equipment
            elif (name.typ == 'equipment'):
                for equip in self.equiplist.list:
                    if (name.name == equip.name):
                        equip.addone()
                        self.e_weight += name.get_weight()
                        ident = True
                        # Hack, coolant pods
                        if name.name == "Coolant Pod":
                            self.coolant += 1
                        # Add explosive weapon to location
                        if equip.explosive > 0:
                            self.exp_weapon.add_weapon(name.loc, equip.explosive)
            # Hack, CASE
            elif (name.typ == 'CASE' or name.typ == 'CASEII'):
                for cas in CASE.keys():
                    if (name.name == cas):
                        self.e_weight += CASE[cas][1]
                        ident = True
                        # Save CASE status
                        self.case[name.loc] = name.typ

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

            # Ammunition
            elif (name.typ == 'ammunition'):
                for ammo in self.ammolist.list:
                    if (name.name == ammo.name):
                        ammo.addone()
                        self.a_weight += name.get_weight()
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
            self.e_weight += ceil(self.tcw_weight / 4.0)
        if self.tarcomp == 2:  #Clan
            self.e_weight += ceil(self.tcw_weight / 5.0)

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

    def get_e_weight(self):
        """
        Get equipment weight
        """
        return self.e_weight

    def get_p_weight(self):
        """
        Get physical weapon weight
        """
        return self.physicallist.p_weight

    def get_speed_adj(self):
        """
        Get speed reduction from certain items, like shields.
        Also add modular armor here.
        """
        red = 0
        red += self.physicallist.get_speed_adj()
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
        

