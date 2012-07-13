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
Contains code for ammo.
"""
# Ammo
#
# Name, weapon, amount, weight, explosive?, cost
#
AMMO = {
    "(IS) @ AC/2": [["(IS) Autocannon/2"], 45, 1, "X", 1000],
    "(IS) @ AC/5": [["(IS) Autocannon/5"], 20, 1, "X", 4500],
    "(IS) @ AC/10": [["(IS) Autocannon/10"], 10, 1, "X", 6000],
    "(IS) @ AC/20": [["(IS) Autocannon/20"], 5, 1, "X", 10000],
    "(IS) @ Light Gauss Rifle":
        [["(IS) Light Gauss Rifle"], 16, 1, "", 20000],
    "@ Gauss Rifle":
        [["(IS) Gauss Rifle", "(CL) Gauss Rifle"], 8, 1, "", 20000],
    "(IS) @ Heavy Gauss Rifle": [["(IS) Heavy Gauss Rifle"], 4, 1, "", 20000],
    "(IS) @ LB 2-X AC (Slug)": [["(IS) LB 2-X AC"], 45, 1, "X", 2000],
    "(IS) @ LB 2-X AC (Cluster)": [["(IS) LB 2-X AC"], 45, 1, "X", 3300],
    "(IS) @ LB 5-X AC (Slug)": [["(IS) LB 5-X AC"], 20, 1, "X", 9000],
    "(IS) @ LB 5-X AC (Cluster)": [["(IS) LB 5-X AC"], 20, 1, "X", 15000],
    "(IS) @ LB 10-X AC (Slug)": [["(IS) LB 10-X AC"], 10, 1, "X", 12000],
    "(IS) @ LB 10-X AC (Cluster)": [["(IS) LB 10-X AC"], 10, 1, "X", 20000],
    "(IS) @ LB 20-X AC (Slug)": [["(IS) LB 20-X AC"], 5, 1, "X", 20000],
    "(IS) @ LB 20-X AC (Cluster)": [["(IS) LB 20-X AC"], 5, 1, "X", 34000],
    "(IS) @ Light AC/2": [["(IS) Light AC/2"], 45, 1, "X", 1000],
    "(IS) @ Light AC/5": [["(IS) Light AC/5"], 20, 1, "X", 4500],
    "@ Light Machine Gun":
        [["(IS) Light Machine Gun", "(CL) Light Machine Gun",
          "(IS) MG Array (2 Light Machine Gun)",
          "(IS) MG Array (3 Light Machine Gun)",
          "(IS) MG Array (4 Light Machine Gun)",
          "(CL) MG Array (3 Light Machine Gun)",
          "(CL) MG Array (4 Light Machine Gun)"], 200, 1, "X", 500],
    "@ Light Machine Gun (1/2)":
        [["(IS) Light Machine Gun", "(CL) Light Machine Gun",
          "(IS) MG Array (2 Light Machine Gun)",
          "(IS) MG Array (3 Light Machine Gun)",
          "(IS) MG Array (4 Light Machine Gun)",
          "(CL) MG Array (3 Light Machine Gun)",
          "(CL) MG Array (4 Light Machine Gun)"], 100, 0.5, "X", 250],
    "@ Machine Gun":
        [["(IS) Machine Gun", "(CL) Machine Gun",
          "(IS) MG Array (3 Machine Gun)",
          "(IS) MG Array (4 Machine Gun)",
          "(CL) MG Array (4 Machine Gun)"], 200, 1, "X", 1000],
    "@ Machine Gun (1/2)":
        [["(IS) Machine Gun", "(CL) Machine Gun",
          "(IS) MG Array (3 Machine Gun)",
          "(IS) MG Array (4 Machine Gun)",
          "(CL) MG Array (4 Machine Gun)"], 100, 0.5, "X", 500],
    "@ Heavy Machine Gun":
        [["(IS) Heavy Machine Gun", "(CL) Heavy Machine Gun",
          "(IS) MG Array (3 Heavy Machine Gun)",
          "(CL) MG Array (3 Heavy Machine Gun)",
          "(CL) MG Array (4 Heavy Machine Gun)"], 100, 1, "X", 1000],
    "@ Heavy Machine Gun (1/2)":
        [["(CL) Heavy Machine Gun",
          "(IS) MG Array (3 Heavy Machine Gun)",
          "(CL) MG Array (3 Heavy Machine Gun)",
          "(CL) MG Array (4 Heavy Machine Gun)"], 50, 0.5, "X", 500],
    "(IS) @ Rotary AC/2": [["(IS) Rotary AC/2"], 45, 1, "X", 3000],
    "(IS) @ Rotary AC/5": [["(IS) Rotary AC/5"], 20, 1, "X", 12000],
    "(IS) @ Ultra AC/2": [["(IS) Ultra AC/2"], 45, 1, "X", 1000],
    "(IS) @ Ultra AC/5": [["(IS) Ultra AC/5"], 20, 1, "X", 9000],
    "(IS) @ Ultra AC/10": [["(IS) Ultra AC/10"], 10, 1, "X", 12000],
    "(IS) @ Ultra AC/20": [["(IS) Ultra AC/20"], 5, 1, "X", 20000],
    "(IS) @ Vehicle Flamer": [["Vehicle Flamer"], 20, 1, "X", 1000],
    "(IS) @ Plasma Rifle": [["(IS) Plasma Rifle"], 10, 1, "", 10000],
    "(IS) @ LRM-5": [["(IS) LRM-5"], 24, 1, "X", 30000],
    "(IS) @ LRM-10": [["(IS) LRM-10"], 12, 1, "X", 30000],
    "(IS) @ LRM-15": [["(IS) LRM-15"], 8, 1, "X", 30000],
    "(IS) @ LRM-20": [["(IS) LRM-20"], 6, 1, "X", 30000],
    "(IS) @ LRM-5 (Artemis IV Capable)": [["(IS) LRM-5"], 24, 1, "X", 60000],
    "(IS) @ LRM-10 (Artemis IV Capable)":
        [["(IS) LRM-10"], 12, 1, "X", 60000],
    "(IS) @ LRM-15 (Artemis IV Capable)": [["(IS) LRM-15"], 8, 1, "X", 60000],
    "(IS) @ LRM-20 (Artemis IV Capable)": [["(IS) LRM-20"], 6, 1, "X", 60000],
    "(IS) @ LRM-5 (Narc Capable)": [["(IS) LRM-5"], 24, 1, "X", 60000],
    "(IS) @ LRM-10 (Narc Capable)": [["(IS) LRM-10"], 12, 1, "X", 60000],
    "(IS) @ LRM-15 (Narc Capable)": [["(IS) LRM-15"], 8, 1, "X", 60000],
    "(IS) @ LRM-20 (Narc Capable)": [["(IS) LRM-20"], 6, 1, "X", 60000],
    "(IS) @ LRT-5 (Torpedo)": [["(IS) LRT-5"], 24, 1, "X", 30000],
    "(IS) @ LRT-10 (Torpedo)": [["(IS) LRT-10"], 12, 1, "X", 30000],
    "(IS) @ LRT-15 (Torpedo)": [["(IS) LRT-15"], 8, 1, "X", 30000],
    "(IS) @ MML-3 (LRM)": [["(IS) MML-3"], 40, 1, "X", 30000],
    "(IS) @ MML-3 (SRM)": [["(IS) MML-3"], 33, 1, "X", 27000],
    "(IS) @ MML-5 (LRM)": [["(IS) MML-5"], 24, 1, "X", 30000],
    "(IS) @ MML-5 (SRM)": [["(IS) MML-5"], 20, 1, "X", 27000],
    "(IS) @ MML-7 (LRM)": [["(IS) MML-7"], 17, 1, "X", 30000],
    "(IS) @ MML-7 (SRM)": [["(IS) MML-7"], 14, 1, "X", 27000],
    "(IS) @ MML-9 (LRM)": [["(IS) MML-9"], 13, 1, "X", 30000],
    "(IS) @ MML-9 (SRM)": [["(IS) MML-9"], 11, 1, "X", 27000],
    "(IS) @ MML-3 (LRM Artemis IV Capable)":
        [["(IS) MML-3"], 40, 1, "X", 60000],
    "(IS) @ MML-3 (SRM Artemis IV Capable)":
        [["(IS) MML-3"], 33, 1, "X", 54000],
    "(IS) @ MML-5 (LRM Artemis IV Capable)":
        [["(IS) MML-5"], 24, 1, "X", 60000],
    "(IS) @ MML-5 (SRM Artemis IV Capable)":
        [["(IS) MML-5"], 20, 1, "X", 54000],
    "(IS) @ MML-7 (LRM Artemis IV Capable)":
        [["(IS) MML-7"], 17, 1, "X", 60000],
    "(IS) @ MML-7 (SRM Artemis IV Capable)":
        [["(IS) MML-7"], 14, 1, "X", 54000],
    "(IS) @ MML-9 (LRM Artemis IV Capable)":
        [["(IS) MML-9"], 13, 1, "X", 60000],
    "(IS) @ MML-9 (SRM Artemis IV Capable)":
        [["(IS) MML-9"], 11, 1, "X", 54000],
    "(IS) @ MRM-10": [["(IS) MRM-10"], 24, 1, "X", 5000],
    "(IS) @ MRM-20": [["(IS) MRM-20"], 12, 1, "X", 5000],
    "(IS) @ MRM-30": [["(IS) MRM-30"], 8, 1, "X", 5000],
    "(IS) @ MRM-40": [["(IS) MRM-40"], 6, 1, "X", 5000],
    "@ SRM-2": [["(IS) SRM-2", "(CL) SRM-2"], 50, 1, "X", 27000],
    "@ SRM-4": [["(IS) SRM-4", "(CL) SRM-4"], 25, 1, "X", 27000],
    "@ SRM-6": [["(IS) SRM-6", "(CL) SRM-6"], 15, 1, "X", 27000],
    "@ SRM-4 (Artemis IV Capable)":
        [["(IS) SRM-4", "(CL) SRM-4"], 25, 1, "X", 54000],
    "@ SRM-6 (Artemis IV Capable)":
        [["(IS) SRM-6", "(CL) SRM-6"], 15, 1, "X", 54000],
    "@ SRM-2 (Narc Capable)":
        [["(IS) SRM-2", "(CL) SRM-2"], 50, 1, "X", 54000],
    "@ SRM-4 (Narc Capable)":
        [["(IS) SRM-4", "(CL) SRM-4"], 25, 1, "X", 54000],
    "@ SRM-6 (Narc Capable)":
        [["(IS) SRM-6", "(CL) SRM-6"], 15, 1, "X", 54000],
    "@ SRT-2 (Torpedo)": [["(CL) SRT-2"], 50, 1, "X", 27000],
    "@ SRT-4 (Torpedo)": [["(IS) SRT-4", "(CL) SRT-4"], 25, 1, "X", 27000],
    "@ SRT-6 (Torpedo)": [["(CL) SRT-6"], 15, 1, "X", 27000],
    "(IS) @ Streak SRM-2": [["(IS) Streak SRM-2"], 50, 1, "X", 54000],
    "(IS) @ Streak SRM-4": [["(IS) Streak SRM-4"], 25, 1, "X", 54000],
    "(IS) @ Streak SRM-6": [["(IS) Streak SRM-6"], 15, 1, "X", 54000],
    "(IS) @ Narc (Homing)": [["(IS) Narc Missile Beacon"], 6, 1, "X", 6000],
    "(IS) @ iNarc (Homing)": [["(IS) iNarc Launcher"], 4, 1, "X", 7500],
    "(IS) @ Anti-Missile System":
        [["(IS) Anti-Missile System"], 12, 1, "X", 2000],
    "@ Remote Sensors (1/2)":
        [["Remote Sensor Dispenser"], 30, 0.5, "", 10500],
    # Clan
    "(CL) @ LB 2-X AC (Slug)": [["(CL) LB 2-X AC"], 45, 1, "X", 2000],
    "(CL) @ LB 2-X AC (Cluster)": [["(CL) LB 2-X AC"], 45, 1, "X", 3300],
    "(CL) @ LB 5-X AC (Slug)": [["(CL) LB 5-X AC"], 20, 1, "X", 9000],
    "(CL) @ LB 5-X AC (Cluster)": [["(CL) LB 5-X AC"], 20, 1, "X", 15000],
    "(CL) @ LB 10-X AC (Slug)": [["(CL) LB 10-X AC"], 10, 1, "X", 12000],
    "(CL) @ LB 10-X AC (Cluster)": [["(CL) LB 10-X AC"], 10, 1, "X", 20000],
    "(CL) @ LB 20-X AC (Slug)": [["(CL) LB 20-X AC"], 5, 1, "X", 20000],
    "(CL) @ LB 20-X AC (Cluster)": [["(CL) LB 20-X AC"], 5, 1, "X", 34000],
    "(CL) @ Ultra AC/2": [["(CL) Ultra AC/2"], 45, 1, "X", 1000],
    "(CL) @ Ultra AC/5": [["(CL) Ultra AC/5"], 20, 1, "X", 9000],
    "(CL) @ Ultra AC/10": [["(CL) Ultra AC/10"], 10, 1, "X", 12000],
    "(CL) @ Ultra AC/20": [["(CL) Ultra AC/20"], 5, 1, "X", 20000],
    "(CL) @ AP Gauss Rifle": [["(CL) AP Gauss Rifle"], 40, 1, "", 3000],
    "(CL) @ Hyper Assault Gauss 20":
        [["(CL) Hyper Assault Gauss 20"], 6, 1, "", 30000],
    "(CL) @ Hyper Assault Gauss 30":
        [["(CL) Hyper Assault Gauss 30"], 4, 1, "", 30000],
    "(CL) @ Hyper Assault Gauss 40":
        [["(CL) Hyper Assault Gauss 40"], 3, 1, "", 30000],
    "(CL) @ Plasma Cannon": [["(CL) Plasma Cannon"], 10, 1, "", 12000],
    "(CL) @ ATM-3": [["(CL) ATM-3"], 20, 1, "X", 75000],
    "(CL) @ ATM-3 (ER)": [["(CL) ATM-3"], 20, 1, "X", 75000],
    "(CL) @ ATM-3 (HE)": [["(CL) ATM-3"], 20, 1, "X", 75000],
    "(CL) @ ATM-6": [["(CL) ATM-6"], 10, 1, "X", 75000],
    "(CL) @ ATM-6 (ER)": [["(CL) ATM-6"], 10, 1, "X", 75000],
    "(CL) @ ATM-6 (HE)": [["(CL) ATM-6"], 10, 1, "X", 75000],
    "(CL) @ ATM-9": [["(CL) ATM-9"], 7, 1, "X", 75000],
    "(CL) @ ATM-9 (ER)": [["(CL) ATM-9"], 7, 1, "X", 75000],
    "(CL) @ ATM-9 (HE)": [["(CL) ATM-9"], 7, 1, "X", 75000],
    "(CL) @ ATM-12": [["(CL) ATM-12"], 5, 1, "X", 75000],
    "(CL) @ ATM-12 (ER)": [["(CL) ATM-12"], 5, 1, "X", 75000],
    "(CL) @ ATM-12 (HE)": [["(CL) ATM-12"], 5, 1, "X", 75000],
    "(CL) @ LRM-5": [["(CL) LRM-5"], 24, 1, "X", 30000],
    "(CL) @ LRM-10": [["(CL) LRM-10"], 12, 1, "X", 30000],
    "(CL) @ LRM-15": [["(CL) LRM-15"], 8, 1, "X", 30000],
    "(CL) @ LRM-20": [["(CL) LRM-20"], 6, 1, "X", 30000],
    "(CL) @ LRM-5 (Artemis IV Capable)": [["(CL) LRM-5"], 24, 1, "X", 60000],
    "(CL) @ LRM-10 (Artemis IV Capable)":
        [["(CL) LRM-10"], 12, 1, "X", 60000],
    "(CL) @ LRM-15 (Artemis IV Capable)": [["(CL) LRM-15"], 8, 1, "X", 60000],
    "(CL) @ LRM-20 (Artemis IV Capable)": [["(CL) LRM-20"], 6, 1, "X", 60000],
    "(CL) @ LRM-15 (Artemis V)": [["(CL) LRM-15"], 8, 1, "X", 150000],
    "(CL) @ LRM-20 (Artemis V)": [["(CL) LRM-20"], 6, 1, "X", 150000],
    "(CL) @ LRM-5 (Narc Capable)": [["(CL) LRM-5"], 24, 1, "X", 60000],
    "(CL) @ LRM-15 (Narc Capable)": [["(CL) LRM-15"], 8, 1, "X", 60000],
    "(CL) @ LRM-20 (Narc Capable)": [["(CL) LRM-20"], 6, 1, "X", 60000],
    "(CL) @ LRT-5 (Torpedo)": [["(CL) LRT-5"], 24, 1, "X", 30000],
    "(CL) @ LRT-10 (Torpedo)": [["(CL) LRT-10"], 12, 1, "X", 30000],
    "(CL) @ LRT-15 (Torpedo)": [["(CL) LRT-15"], 8, 1, "X", 30000],
    "(CL) @ Streak SRM-2": [["(CL) Streak SRM-2"], 50, 1, "X", 54000],
    "(CL) @ Streak SRM-4": [["(CL) Streak SRM-4"], 25, 1, "X", 54000],
    "(CL) @ Streak SRM-6": [["(CL) Streak SRM-6"], 15, 1, "X", 54000],
    "(CL) @ Narc (Homing)": [["(CL) Narc Missile Beacon"], 6, 1, "X", 6000],
    "(CL) @ Anti-Missile System":
        [["(CL) Anti-Missile System"], 24, 1, "X", 2000],
    # Advanced
    "(IS) @ Magshot Gauss Rifle":
        [["(IS) Magshot Gauss Rifle"], 50, 1, "", 1000],
    "(IS) @ BattleMech Taser": [["(IS) BattleMech Taser"], 5, 1, "X", 2000],
    "(IS) @ Thunderbolt-5": [["(IS) Thunderbolt-5"], 12, 1, "X", 50000],
    "(IS) @ Thunderbolt-10": [["(IS) Thunderbolt-10"], 6, 1, "X", 50000],
    "(IS) @ Thunderbolt-15": [["(IS) Thunderbolt-15"], 4, 1, "X", 50000],
    "(IS) @ Thunderbolt-20": [["(IS) Thunderbolt-20"], 3, 1, "X", 50000],
    "(IS) @ NLRM-5": [["(IS) Enhanced LRM-5"], 24, 1, "X", 31000],
    "(IS) @ ELRM-10": [["(IS) Extended LRM-10"], 9, 1, "X", 35000],
    "(IS) @ ELRM-20": [["(IS) Extended LRM-20"], 4, 1, "X", 35000],
    "@ Fluid Gun (Water)": [["(IS) Fluid Gun"], 20, 1, "", 500],
    "@ C3 Remote Launcher":
        [["C3 Remote Sensor Launcher"], 4, 1, "X", 100000],
    "(CL) @ Rotary AC/2": [["(CL) Rotary AC/2"], 45, 1, "X", 3000],
    "(CL) @ Rotary AC/5": [["(CL) Rotary AC/5"], 20, 1, "X", 12000],
    "(CL) @ Protomech AC/4": [["(CL) Protomech AC/4"], 20, 1, "X", 4800],
    "(CL) @ Protomech AC/8": [["(CL) Protomech AC/8"], 10, 1, "X", 6300],
    "(CL) @ Streak LRM-10": [["(CL) Streak LRM-10"], 12, 1, "X", 60000],
    "(CL) @ Streak LRM-15": [["(CL) Streak LRM-15"], 8, 1, "X", 60000],
    "(CL) @ 'Mech Mortar 8 (Anti-Personnel)":
        [["(CL) Mech Mortar 8"], 4, 1, "X", 24000],
    "@ Heavy Flamer": [["Heavy Flamer"], 10, 1, "X", 2000],
    "(IS) @ HVAC/10":
        [["(IS) Hyper-Velocity Autocannon/10"], 8, 1, "X", 20000],
    "(IS) @ Improved Heavy Gauss Rifle":
        [["(IS) Improved Heavy Gauss Rifle"], 4, 1, "", 20000],
    "(IS) @ Silver Bullet Gauss":
        [["(IS) Silver Bullet Gauss"], 8, 1, "", 25000],
    "@ Long Tom Cannon":
        [["Long Tom Artillery Cannon"], 5, 1, "X", 20000],
    # Artillery
    "(IS) @ Arrow IV (Non-Homing)":
        [["(IS) Arrow IV Missile"], 5, 1, "X", 10000],
    "(IS) @ Arrow IV (Homing)": [["(IS) Arrow IV Missile"], 5, 1, "X", 15000],
    "(CL) @ Arrow IV (Non-Homing)":
        [["(CL) Arrow IV Missile"], 5, 1, "X", 10000],
    "(CL) @ Arrow IV (Homing)": [["(CL) Arrow IV Missile"], 5, 1, "X", 15000],
    "@ Thumper": [["(IS) Thumper"], 20, 1, "X", 4500],
    "@ Sniper": [["(IS) Sniper"], 10, 1, "X", 6000],
    "@ Long Tom": [["(IS) Long Tom"], 5, 1, "X", 10000]
    }


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
