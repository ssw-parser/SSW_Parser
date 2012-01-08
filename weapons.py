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

# Weapons in the order of name, BV[main, ammo], range,
# enhancement(A=artemis, T=tarcomp P=apollo),
# year, uses ammo rate?, weight, heat(as used for BV calcs), explosive slots
#
# To be loaded into the gear class
#
# TODO1: IS: Flamer (Vehicle), HMG,  Clan: Flamer (Vehicle)
# TODO2: IS: MG Arrays: 2 HMG, 4 HMG, 2 MG
# Clan: 2 HMG, 2 LMG, 4 LMG, 2 MG, 3 MG
WEAPONS = {
    "(IS) Autocannon/2" : [[37, 5], "L", "T", 2300, 1, 6, 1, 0],
    "(IS) Autocannon/5" : [[70, 9], "L", "T", 2250, 1, 8, 1, 0],
    "(IS) Autocannon/10" : [[123, 15], "M", "T", 2460, 1, 12, 3, 0],
    "(IS) Autocannon/20" : [[178, 22], "M", "T", 2500, 1, 14, 7, 0],
    "(IS) Light Gauss Rifle" : [[159, 20], "L", "T", 3056, 1, 12, 1, 5],
    "(IS) Gauss Rifle" : [[320, 40], "L", "T", 2590, 1, 15, 1, 7],
    "(IS) Heavy Gauss Rifle" : [[346, 43], "L", "T", 3061, 1, 18, 2, 11],
    "(IS) LB 2-X AC" : [[42, 5], "L", "T", 3058, 1, 6, 1, 0],
    "(IS) LB 5-X AC" : [[83, 10], "L", "T", 3058, 1, 8, 1, 0],
    "(IS) LB 10-X AC" : [[148, 19], "L", "T", 2595, 1, 11, 2, 0],
    "(IS) LB 20-X AC" : [[237, 30], "M", "T", 3058, 1, 14, 6, 0],
    "(IS) Light AC/2" : [[30, 4], "L", "T", 3068, 1, 4, 1, 0],
    "(IS) Light AC/5" : [[62, 8], "M", "T", 3068, 1, 5, 1, 0],
    "(IS) Light Machine Gun" : [[5, 1], "M", "", 3068, 1, 0.5, 0, 0],
    "(IS) MG Array (2 Light Machine Gun)" : [[16.7, 1], "M", "", 3068,
                                             2, 1.5, 0, 0],
    "(IS) MG Array (3 Light Machine Gun)" : [[25.05, 1], "M", "", 3068,
                                             3, 2, 0, 0],
    "(IS) MG Array (4 Light Machine Gun)" : [[33.4, 1], "M", "", 3068,
                                             4, 2.5, 0, 0],
    "(IS) Machine Gun" : [[5, 1], "S", "", 1900, 1, 0.5, 0, 0],
    # MG 2
    "(IS) MG Array (3 Machine Gun)" : [[25.05, 1], "S", "", 3068,
                                       3, 2, 0, 0],
    "(IS) MG Array (4 Machine Gun)" : [[33.4, 1], "S", "", 3068,
                                       4, 2.5, 0, 0],
    # HMG
    # HMG 2
    "(IS) MG Array (3 Heavy Machine Gun)" : [[30.06, 1], "S", "", 3068,
                                             3, 3.5, 0, 0],
    # HMG 4
    # Nail/rivet
    "(IS) Rotary AC/2" : [[118, 15], "L", "T", 3062, 6, 8, 6, 0],
    "(IS) Rotary AC/5" : [[247, 31], "M", "T", 3062, 6, 10, 6, 0],
    "(IS) Ultra AC/2" : [[56, 7], "L", "T", 3057, 2, 7, 2, 0],
    "(IS) Ultra AC/5" : [[112, 14], "L", "T", 2640, 2, 9, 2, 0],
    "(IS) Ultra AC/10" : [[210, 26], "L", "T", 3057, 2, 13, 8, 0],
    "(IS) Ultra AC/20" : [[281, 35], "M", "T", 3060, 2, 15, 16, 0],
    "(IS) ER Large Laser" : [[163, 0], "L", "T", 2620, 0, 5, 12, 0],
    "(IS) ER Medium Laser" : [[62, 0], "M", "T", 3058, 0, 1, 5, 0],
    "(IS) ER Small Laser" : [[17, 0], "M", "T", 3058, 0, 0.5, 2, 0],
    "(IS) Flamer" : [[6, 0], "S", "", 2025, 0, 1, 3, 0],
    # Flamer (Vehicle)
    "(IS) Large Laser" : [[123, 0], "M", "T", 2316, 0, 5, 8, 0],
    "(IS) Medium Laser" : [[46, 0], "M", "T", 2300, 0, 1, 3, 0],
    "(IS) Small Laser" : [[9, 0], "S", "T", 2300, 0, 0.5, 1, 0],
    "(IS) Plasma Rifle" : [[210, 26], "M", "T", 3068, 1, 6, 10, 0],
    "(IS) Light PPC" : [[88, 0], "L", "T", 3067, 0, 3, 5, 0],
    "(IS) Light PPC + PPC Capacitor" : [[132, 0], "L", "T", 3067,
                                        0, 4, 10, 3],
    "(IS) PPC" : [[176, 0], "L", "T", 2460, 0, 7, 10, 0],
    "(IS) Heavy PPC" : [[317, 0], "L", "T", 3067, 0, 10, 15, 0],
    "(IS) ER PPC" : [[229, 0], "L", "T", 2760, 0, 7, 15, 0],
    "(IS) Snub-Nose PPC" : [[165, 0], "M", "T", 3067, 0, 6, 10, 0],
    "(IS) Snub-Nose PPC + PPC Capacitor" : [[252, 0], "M", "T", 3067,
                                            0, 7, 15, 3],
    "(IS) Large Pulse Laser" : [[119, 0], "M", "T", 2609, 0, 7, 10, 0],
    "(IS) Medium Pulse Laser" : [[48, 0], "M", "T", 2609, 0, 2, 4, 0],
    "(IS) Small Pulse Laser" : [[12, 0], "S", "T", 2609, 0, 1, 2, 0],
    "(IS) LRM-5" : [[45, 6], "L", "A", 2300, 1, 2, 2, 0],
    "(IS) LRM-10" : [[90, 11], "L", "A", 2305, 1, 5, 4, 0],
    "(IS) LRM-15" : [[136, 17], "L", "A", 2315, 1, 7, 5, 0],
    "(IS) LRM-20" : [[181, 23], "L", "A", 2322, 1, 10, 6, 0],
    "(IS) MML-3" : [[29, 4], "L", "A", 3068, 1, 1.5, 2, 0],
    "(IS) MML-5" : [[45, 6], "L", "A", 3068, 1, 3, 3, 0],
    "(IS) MML-7" : [[67, 8], "L", "A", 3068, 1, 4.5, 4, 0],
    "(IS) MML-9" : [[86, 11], "L", "A", 3068, 1, 6, 5, 0],
    "(IS) MRM-10" : [[56, 7], "M", "P", 3058, 1, 3, 4, 0],
    "(IS) MRM-20" : [[112, 14], "M", "P", 3058, 1, 7, 6, 0],
    "(IS) MRM-30" : [[168, 21], "M", "P", 3058, 1, 10, 10, 0],
    "(IS) MRM-40" : [[224, 28], "M", "P", 3058, 1, 12, 12, 0],
    "(IS) Rocket Launcher 10" : [[18, 0], "L", "", 3064, 0, 0.5, 0.75, 0],
    "(IS) Rocket Launcher 15" : [[23, 0], "M", "", 3064, 0, 1, 1, 0],
    "(IS) Rocket Launcher 20" : [[24, 0], "M", "", 3064, 0, 1.5, 1.25, 0],
    "(IS) SRM-2" : [[21, 3], "M", "A", 2370, 1, 1, 2, 0],
    "(IS) SRM-4" : [[39, 5], "M", "A", 2370, 1, 2, 3, 0],
    "(IS) SRM-6" : [[59, 7], "M", "A", 2370, 1, 3, 4, 0],
    "(IS) SRM-4 (OS)" : [[8, 0], "M", "A", 2676, 0, 2.5, 0.75, 0],
    "(IS) Streak SRM-2" : [[30, 4], "M", "", 2647, 1, 1.5, 1, 0],
    "(IS) Streak SRM-4" : [[59, 7], "M", "", 3058, 1, 3, 1.5, 0],
    "(IS) Streak SRM-6" : [[89, 11], "M", "", 3058, 1, 4.5, 2, 0],
    "(IS) Streak SRM-2 (OS)" : [[6, 0], "M", "", 2676, 0, 2, 0.5, 0],
    "(IS) Narc Missile Beacon" : [[30, 0], "M", "", 2587, 1, 3, 0, 0],
    "(IS) iNarc Launcher" : [[75, 0], "M", "", 3062, 1, 5, 0, 0],
    # Advanced Weapons
    "(IS) Magshot Gauss Rifle" : [[15, 2], "M", "T", 3072, 1, 0.5, 1, 2],
    "(IS) BattleMech Taser" : [[40, 5], "M", "", 3067, 1, 4, 6, 3],
    "(IS) Small Variable Speed Pulse Laser" : [[22, 0], "M", "T", 3070,
                                               0, 2, 3, 0],
    "(IS) Medium Variable Speed Pulse Laser" : [[56, 0], "M", "T", 3070,
                                                0, 4, 7, 0],
    "(IS) Large Variable Speed Pulse Laser" : [[123, 0], "M", "T", 3070,
                                               0, 9, 10, 0],
    "(IS) Small X-Pulse Laser" : [[21, 0], "M", "T", 3057, 0, 1, 3, 0],
    "(IS) Medium X-Pulse Laser" : [[71, 0], "M", "T", 3057, 0, 2, 6, 0],
    "(IS) Large X-Pulse Laser" : [[178, 0], "M", "T", 3057, 0, 7, 14, 0],
    "(IS) Binary Laser Cannon" : [[222, 0], "M", "T", 2812, 0, 9, 16, 0],
    "(IS) Bombast Laser" : [[137, 0], "M", "T", 3064, 0, 7, 12, 0],
    "(IS) Thunderbolt-5" : [[64, 8], "L", "", 3072, 1, 3, 3, 0],
    "(IS) Thunderbolt-10" : [[127, 16], "L", "", 3072, 1, 7, 5, 0],
    "(IS) Thunderbolt-15" : [[229, 29], "L", "", 3072, 1, 11, 7, 0],
    "(IS) Thunderbolt-20" : [[305, 38], "L", "", 3072, 1, 15, 8, 0],
    "(IS) Enhanced LRM-5" : [[52, 7], "L", "A", 3058, 1, 3, 2, 0],
    "ER Flamer" : [[16, 0], "M", "", 3067, 0, 1, 4, 0],
    # Clan
    "(CL) LB 2-X AC" : [[47, 6], "L", "T", 2826, 1, 5, 1, 0],
    "(CL) LB 5-X AC" : [[93, 12], "L", "T", 2825, 1, 7, 1, 0],
    "(CL) LB 10-X AC" : [[148, 19], "L", "T", 2595, 1, 10, 2, 0],
    "(CL) LB 20-X AC" : [[237, 30], "M", "T", 2826, 1, 12, 6, 0],
    "(CL) Ultra AC/2" : [[62, 8], "L", "T", 2827, 2, 5, 2, 0],
    "(CL) Ultra AC/5" : [[122, 15], "L", "T", 2640, 2, 7, 2, 0],
    "(CL) Ultra AC/10" : [[210, 26], "L", "T", 2825, 2, 10, 6, 0],
    "(CL) Ultra AC/20" : [[335, 42], "M", "T", 2825, 2, 12, 14, 0],
    "(CL) AP Gauss Rifle" : [[21, 3], "M", "T", 3069, 1, 0.5, 1, 1],
    "(CL) Gauss Rifle" : [[320, 40], "L", "T", 2590, 1, 12, 1, 6],
    "(CL) Hyper Assault Gauss 20" : [[267, 33], "L", "T", 3068,
                                     1, 10, 4, 6],
    "(CL) Hyper Assault Gauss 30" : [[401, 50], "L", "T", 3068,
                                     1, 13, 6, 8],
    "(CL) Hyper Assault Gauss 40" : [[535, 67], "L", "T", 3069,
                                     1, 16, 8, 10],
    "(CL) Light Machine Gun" : [[5, 1], "M", "", 3060, 1, 0.25, 0, 0],
    # LMG 2
    "(CL) MG Array (3 Light Machine Gun)" : [[25.05, 1], "M", "", 3069,
                                             3, 1, 0, 0],
    # LMG 4
    "(CL) Machine Gun" : [[5, 1], "S", "", 1900, 1, 0.25, 0, 0],
    # MG 2
    # MG 3
    "(CL) MG Array (4 Machine Gun)" : [[33.4, 1], "S", "", 3069,
                                       4, 1.25, 0, 0],
    "(CL) Heavy Machine Gun" : [[6, 1], "S", "", 3059, 1, 0.5, 0, 0],
    # HMG 2
    "(CL) MG Array (3 Heavy Machine Gun)" : [[30.06, 1], "S", "", 3069,
                                             3, 1.75, 0, 0],
    "(CL) MG Array (4 Heavy Machine Gun)" : [[40.08, 1], "S", "", 3069,
                                             4, 2.25, 0, 0],
    "(CL) Flamer" : [[6, 0], "S", "", 2025, 0, 0.5, 3, 0],
    # Flamer (Vehicle)
    "(CL) ER Micro Laser" : [[7, 0], "M", "T", 3060, 0, 0.25, 1, 0],
    "(CL) ER Small Laser" : [[31, 0], "M", "T", 2825, 0, 0.5, 2, 0],
    "(CL) ER Medium Laser" : [[108, 0], "M", "T", 2824, 0, 1, 5, 0],
    "(CL) ER Large Laser" : [[248, 0], "L", "T", 2620, 0, 4, 12, 0],
    "(CL) Micro Pulse Laser" : [[12, 0], "S", "T", 3060, 0, 0.5, 1, 0],
    "(CL) Small Pulse Laser" : [[24, 0], "M", "T", 2609, 0, 1, 2, 0],
    "(CL) Medium Pulse Laser" : [[111, 0], "M", "T", 2609, 0, 2, 4, 0],
    "(CL) Large Pulse Laser" : [[265, 0], "L", "T", 2609, 0, 6, 10, 0],
    "(CL) Heavy Small Laser" : [[15, 0], "S", "T", 3059, 0, 0.5, 3, 0],
    "(CL) Heavy Medium Laser" : [[76, 0], "M", "T", 3059, 0, 1, 7, 0],
    "(CL) Heavy Large Laser" : [[244, 0], "M", "T", 3059, 0, 4, 18, 0],
    "(CL) Plasma Cannon" : [[170, 21], "L", "T", 3069, 1, 3, 7, 0],
    "(CL) ER PPC" : [[412, 0], "L", "T", 2760, 0, 6, 15, 0],
    "(CL) ATM-3" : [[53, 14], "M", "", 3054, 1, 1.5, 2, 0],
    "(CL) ATM-6" : [[105, 26], "M", "", 3054, 1, 3.5, 4, 0],
    "(CL) ATM-9" : [[147, 36], "M", "", 3054, 1, 5, 6, 0],
    "(CL) ATM-12" : [[212, 52], "M", "", 3055, 1, 7, 8, 0],
    "(CL) LRM-5" : [[55, 7], "L", "A", 2400, 1, 1, 2, 0],
    "(CL) LRM-10" : [[109, 14], "L", "A", 2400, 1, 2.5, 4, 0],
    "(CL) LRM-15" : [[164, 21], "L", "A", 2400, 1, 3.5, 5, 0],
    "(CL) LRM-20" : [[220, 27], "L", "A", 2400, 1, 5, 6, 0],
    "(CL) SRM-2" : [[21, 3], "M", "A", 2370, 1, 0.5, 2, 0],
    "(CL) SRM-4" : [[39, 5], "M", "A", 2370, 1, 1, 3, 0],
    "(CL) SRM-6" : [[59, 7], "M", "A", 2370, 1, 1.5, 4, 0],
    "(CL) Streak SRM-2" : [[40, 5], "M", "", 2647, 1, 1, 1, 0],
    "(CL) Streak SRM-4" : [[79, 10], "M", "", 2826, 1, 2, 1.5, 0],
    "(CL) Streak SRM-6" : [[118, 15], "M", "", 2826, 1, 3, 2, 0],
    "(CL) Streak SRM-4 (OS)" : [[16, 0], "M", "", 2826, 0, 2.5, 0.75, 0],
    "(CL) Narc Missile Beacon" : [[30, 0], "M", "", 2587, 1, 2, 0, 0],
    # Advanced Weapons
    "(CL) Rotary AC/2" : [[161, 20], "L", "T", 3073, 6, 8, 6, 0],
    "(CL) Rotary AC/5" : [[345, 43], "L", "T", 3073, 6, 10, 6, 0],
    "(CL) Protomech AC/4" : [[49, 6], "M", "T", 3073, 1, 4.5, 1, 0],
    "(CL) Improved Heavy Medium Laser" : [[93, 0], "M", "T", 3069,
                                          0, 1, 7, 2],
    "(CL) ER Medium Pulse Laser" : [[117, 0], "M", "T", 3057, 0, 2, 6, 0],
    "(CL) ER Small Pulse Laser" : [[36, 0], "M", "T", 3057, 0, 1.5, 3, 0],
    "(CL) Streak LRM-10" : [[173, 22], "L", "", 3057, 1, 5, 2, 0],
    "(CL) Mech Mortar 8" : [[50, 6], "L", "", 2840, 1, 5, 10, 0],
    # Artillery
    "(IS) Arrow IV Missile" : [[240, 30], "L", "", 2600, 1, 15, 10, 0],
    "(CL) Arrow IV Missile" : [[240, 30], "L", "", 2600, 1, 12, 10, 0],
    "(IS) Sniper" : [[85, 11], "L", "", 1900, 1, 20, 10, 0]
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
    def __init__(self):
        self.list = []
        for weap in WEAPONS.keys():
            self.list.append(Weapon(weap))

class Weapon:
    """
    An individual weapon type
    """
    def __init__(self, key):
        self.name = key
        self.batt_val = WEAPONS[key][0]
        self.range = WEAPONS[key][1]
        self.enhance = WEAPONS[key][2]
        self.useammo = WEAPONS[key][4]
        self.explosive = WEAPONS[key][7]
        self.count = 0
        self.countrear = 0
        self.countarm = 0 # We count arm weapons also, to help with BV calcs
        self.ammocount = 0
        self.ammo_ton = 0

    def get_weight(self):
        """
        Return weight
        """
        return WEAPONS[self.name][5]

    def get_heat(self):
        """
        Return heat
        """
        return WEAPONS[self.name][6]

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

    def get_ammo_per_weapon(self):
        """
        Get amount of ammo for each forward-facing weapon
        """
        if self.count > 0:
            return int(float(self.ammocount) / float(self.count))
        # For no weapons, ammo matters not
        else:
            return 0



