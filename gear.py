#!/usr/bin/python

from math import ceil
from error import *

# A class to contain data about battlemech gear to allow for clearer code,
# by using named class members.

# Weapons in the order of name, BV, range, enhancement(A=artemis, T=tarcomp),
# year, uses ammo rate?, weight, BF info[heat, short, medium, long, extreme]
#
# To be loaded into the gear class
#
# TODO1: IS: Flamer (Vehicle), HMG
# Clan: LB2, LB20, UAC20, HMG, Flamer, Flamer (Vehicle), SRM2, SRM4
# TODO2: IS: MG Arrays: 2 HMG, 4 HMG, 2 MG, 3 MG
# TODO3: Artemis IV versions
weapons = [["(IS) Autocannon/2", 37, "L", "T", 2300, 1, 6, [1, 1.32, 2, 2, 2]],
           ["(IS) Autocannon/5", 70, "L", "T", 2250, 1, 8, [1, 3.75, 5, 5, 0]],
           ["(IS) Autocannon/10", 123, "M", "T", 2460, 1, 12, [3, 10, 10, 0, 0]],
           ["(IS) Autocannon/20", 178, "M", "T", 2500, 1, 14, [7, 20, 20, 0, 0]],
           ["(IS) Light Gauss Rifle", 159, "L", "T", 3056, 1, 12, [1, 6, 8, 8, 8]],
           ["(IS) Gauss Rifle", 320, "L", "T", 2590, 1, 15, [1, 12.45, 15, 15, 0]],
           ["(IS) Heavy Gauss Rifle", 346, "L", "T", 3061, 1, 18, [2, 16.5, 20, 10, 0]],
           ["(IS) LB 2-X AC", 42, "L", "T", 3058, 1, 6, [1, 0.69, 1.05, 1.05, 1.05]],
           ["(IS) LB 5-X AC", 83, "L", "T", 3058, 1, 8, [1, 2.36, 3.15, 3.15, 0]],
           ["(IS) LB 10-X AC", 148, "L", "T", 2595, 1, 11, [2, 6.3, 6.3, 6.3, 0]],
           ["(IS) LB 20-X AC", 237, "M", "T", 3058, 1, 14, [6, 12.6, 12.6, 0, 0]],
           ["(IS) Light AC/2", 30, "L", "T", 3068, 1, 4, [1, 2, 2, 2, 0]],
           ["(IS) Light AC/5", 62, "M", "T", 3068, 1, 5, [1, 5, 5, 0, 0]],
           ["(IS) Light Machine Gun", 5, "M", "", 3068, 1, 0.5, [0, 1, 1, 0, 0]],
           ["(IS) MG Array (2 Light Machine Gun)", 6.7, "M", "", 3068, 2, 1.5, [0, 1, 1, 0, 0]],
           ["(IS) MG Array (3 Light Machine Gun)", 10.05, "M", "", 3068, 3, 2, [0, 2, 2, 0, 0]],
           ["(IS) MG Array (4 Light Machine Gun)", 13.4, "M", "", 3068, 4, 2.5, [0, 3, 3, 0, 0]],
           ["(IS) Machine Gun", 5, "S", "", 1900, 1, 0.5, [0, 2, 0, 0, 0]],
           # MG 2
           # MG 3
           ["(IS) MG Array (4 Machine Gun)", 13.4, "S", "", 3068, 4, 2.5, [0, 6, 0, 0, 0]],
           # HMG
           # HMG 2
           ["(IS) MG Array (3 Heavy Machine Gun)", 12.06, "S", "", 3068, 3, 3.5, [0, 6, 0, 0, 0]],
           # HMG 4
           # Nail/rivet
           ["(IS) Rotary AC/2", 118, "L", "T", 3062, 6, 8, [6, 8, 8, 8, 0]],
           ["(IS) Rotary AC/5", 247, "M", "T", 3062, 6, 10, [6, 20, 20, 0, 0]],
           ["(IS) Ultra AC/2", 56, "L", "T", 3057, 2, 7, [2, 2.25, 3, 3, 3]],
           ["(IS) Ultra AC/5", 112, "L", "T", 2640, 2, 9, [2, 6.23, 7.5, 7.5, 0]],
           ["(IS) Ultra AC/10", 210, "L", "T", 3057, 2, 13, [8, 15, 15, 15, 0]],
           ["(IS) Ultra AC/20", 281, "M", "T", 3060, 2, 15, [16, 30, 30, 0, 0]],
           ["(IS) ER Large Laser", 163, "L", "T", 2620, 0, 5, [12, 8, 8, 8, 0]],
           ["(IS) ER Medium Laser", 62, "M", "T", 3058, 0, 1, [5, 5, 5, 0, 0]],
           ["(IS) ER Small Laser", 17, "M", "T", 3058, 0, 0.5, [2, 3, 3, 0, 0]],
           ["(IS) Flamer", 6, "S", "", 2025, 0, 1, [3, 2, 0, 0, 0]],
           # Flamer (Vehicle)
           ["(IS) Large Laser", 123, "M", "T", 2316, 0, 5, [8, 8, 8, 0, 0]],
           ["(IS) Medium Laser", 46, "M", "T", 2300, 0, 1, [3, 5, 5, 0, 0]],
           ["(IS) Small Laser", 9, "S", "T", 2300, 0, 0.5, [1, 3, 0, 0, 0]],
           ["(IS) Plasma Rifle", 210, "M", "T", 3068, 1, 6, [10, 10, 10, 0, 0]],
           ["(IS) Light PPC", 88, "L", "T", 3067, 0, 3, [5, 3.75, 5, 5, 0]],
           ["(IS) PPC", 176, "L", "T", 2460, 0, 7, [10, 7.5, 10, 10, 0]],
           ["(IS) Heavy PPC", 317, "L", "T", 3067, 0, 10, [15, 11.25, 15, 15, 0]],
           ["(IS) ER PPC", 229, "L", "T", 2760, 0, 7, [15, 10, 10, 10, 0]],
           ["(IS) Snub-Nose PPC", 165, "M", "T", 3067, 0, 6, [10, 10, 6.5, 0, 0]],
           ["(IS) Large Pulse Laser", 119, "M", "T", 2609, 0, 7, [10, 9.9, 9.9, 0, 0]],
           ["(IS) Medium Pulse Laser", 48, "M", "T", 2609, 0, 2, [4, 6.6, 6.6, 0, 0]],
           ["(IS) Small Pulse Laser", 12, "S", "T", 2609, 0, 1, [2, 3.3, 0, 0, 0]],
           ["(IS) LRM-5", 45, "L", "A", 2300, 1, 2, [2, 1.5, 3, 3, 0]],
           ["(IS) LRM-10", 90, "L", "A", 2305, 1, 5, [4, 3, 6, 6, 0]],
           ["(IS) LRM-15", 136, "L", "A", 2315, 1, 7, [5, 4.5, 9, 9, 0]],
           ["(IS) LRM-20", 181, "L", "A", 2322, 1, 10, [6, 6, 12, 12, 0]],
           ["(IS) MML-3", 29, "L", "A", 3068, 1, 1.5, [2, 4, 3, 2, 0]],
           ["(IS) MML-5", 45, "L", "A", 3068, 1, 3, [3, 6, 4.5, 3, 0]],
           ["(IS) MML-7", 67, "L", "A", 3068, 1, 4.5, [4, 8, 6, 4, 0]],
           ["(IS) MML-9", 86, "L", "A", 3068, 1, 6, [5, 10, 7.5, 5, 0]],
           ["(IS) MRM-10", 56, "M", "", 3058, 1, 3, [5, 5.7, 5.7, 0, 0]],
           ["(IS) MRM-20", 112, "M", "", 3058, 1, 7, [6, 11.4, 11.4, 0, 0]],
           ["(IS) MRM-30", 168, "M", "", 3058, 1, 10, [10, 17.1, 17.1, 0, 0]],
           ["(IS) MRM-40", 224, "M", "", 3058, 1, 12, [12, 22.8, 22.8, 0, 0]],
           ["(IS) Rocket Launcher 10", 18, "L", "", 3064, 0, 0.5, [3, 0.6, 0.6, 0.6, 0]],
           ["(IS) Rocket Launcher 15", 23, "M", "", 3064, 0, 1, [4, 0.9, 0.9, 0, 0]],
           ["(IS) Rocket Launcher 20", 24, "M", "", 3064, 0, 1.5, [5, 1.2, 1.2, 0, 0]],
           ["(IS) SRM-2", 21, "M", "A", 2370, 1, 1, [2, 2, 2, 0, 0]],
           ["(IS) SRM-4", 39, "M", "A", 2370, 1, 2, [3, 6, 6, 0, 0]],
           ["(IS) SRM-6", 59, "M", "A", 2370, 1, 3, [4, 8, 8, 0, 0]],
           ["(IS) Streak SRM-2", 30, "M", "", 2647, 1, 1.5, [2, 4, 4, 0, 0]],
           ["(IS) Streak SRM-4", 59, "M", "", 3058, 1, 3, [3, 8, 8, 0, 0]],
           ["(IS) Streak SRM-6", 89, "M", "", 3058, 1, 4.5, [4, 12, 12, 0, 0]],
           ["(IS) Narc Missile Beacon", 30, "M", "", 2587, 1, 3, [0, 0, 0, 0, 0]],
           ["(IS) iNarc Launcher", 75, "M", "", 3062, 1, 5, [0, 0, 0, 0, 0]],
           # Advanced Weapons
           ["(IS) Medium Variable Speed Pulse Laser", 56, "M", "T", 3072, 1, 4, [6, 10.35, 5.25, 0, 0]],
           # Clan
           # LB 2
           ["(CL) LB 5-X AC", 93, "L", "T", 2825, 1, 7, [1, 2.36, 3.15, 3.15, 0]],
           ["(CL) LB 10-X AC", 148, "L", "T", 2595, 1, 10, [2, 6.3, 6.3, 6.3, 0]],
           # LB 20
           ["(CL) Ultra AC/2", 62, "L", "T", 2827, 2, 5, [0, 0, 0, 0, 0]],
           ["(CL) Ultra AC/5", 122, "L", "T", 2640, 2, 8, [0, 0, 0, 0, 0]],
           ["(CL) Ultra AC/10", 210, "L", "T", 2825, 2, 10, [0, 0, 0, 0, 0]],
           # UAC 20
           ["(CL) AP Gauss Rifle", 21, "M", "T", 3069, 1, 0.5, [1, 3, 3, 0, 0]],
           ["(CL) Gauss Rifle", 320, "L", "T", 2590, 1, 12, [1, 12.45, 15, 15, 0]],
           ["(CL) Hyper Assault Gauss 20", 267, "L", "T", 3068, 1, 10, [4, 13.28, 12, 12, 0]],
           ["(CL) Hyper Assault Gauss 30", 401, "L", "T", 3068, 1, 13, [6, 19.92, 18, 18, 0]],
           ["(CL) Hyper Assault Gauss 40", 535, "L", "T", 3069, 1, 16, [8, 26.56, 24, 24, 0]],
           ["(CL) Light Machine Gun", 5, "M", "", 3060, 1, 0.25, [0, 1, 0, 0, 0]],
           ["(CL) Machine Gun", 5, "S", "", 1900, 1, 0.25, [0, 2, 0, 0, 0]],
           # HMG
           ["(CL) MG Array (3 Heavy Machine Gun)", 12.06, "S", "", 3069, 3, 1.75, [0, 0, 0, 0, 0]],
           # Flamer
           # Flamer (Vehicle)
           ["(CL) ER Micro Laser", 7, "M", "T", 3060, 0, 0.25, [1, 2, 0, 0, 0]],
           ["(CL) ER Small Laser", 31, "M", "T", 2825, 0, 0.5, [2, 5, 5, 0, 0]],
           ["(CL) ER Medium Laser", 108, "M", "T", 2824, 0, 1, [5, 7, 7, 0, 0]],
           ["(CL) ER Large Laser", 248, "L", "T", 2620, 0, 4, [12, 10, 10, 10, 10]],
           ["(CL) Micro Pulse Laser", 12, "S", "T", 3060, 0, 0.5, [1, 3.3, 0, 0, 0]],
           ["(CL) Small Pulse Laser", 24, "M", "T", 2609, 0, 1, [2, 3.3, 3.3, 0, 0]],
           ["(CL) Medium Pulse Laser", 111, "M", "T", 2609, 0, 2, [4, 7.7, 7.7, 0, 0]],
           ["(CL) Large Pulse Laser", 265, "L", "T", 2609, 0, 6, [10, 11, 11, 11, 0]],
           ["(CL) Heavy Small Laser", 15, "S", "T", 3059, 0, 0.5, [3, 5.7, 0, 0, 0]],
           ["(CL) Heavy Medium Laser", 76, "M", "T", 3059, 0, 1, [7, 9.5, 9.5, 0, 0]],
           ["(CL) Heavy Large Laser", 244, "M", "T", 3059, 0, 4, [18, 15.2, 15.2, 0, 0]],
           ["(CL) Plasma Cannon", 170, "L", "T", 3069, 1, 3, [7, 10, 10, 10, 0]],
           ["(CL) ER PPC", 412, "L", "T", 2760, 0, 6, [15, 15, 15, 15, 0]],
           ["(CL) ATM-3", 53, "M", "", 3054, 1, 1.5, [2, 6, 4, 2, 2]],
           ["(CL) ATM-6", 105, "M", "", 3054, 1, 3.5, [4, 15, 10, 5, 5]],
           ["(CL) ATM-9", 147, "M", "", 3054, 1, 5, [6, 21, 14, 7, 7]],
           ["(CL) ATM-12", 212, "M", "", 3055, 1, 7, [8, 30, 20, 10, 10]],
           ["(CL) LRM-5", 55, "L", "A", 2400, 1, 1, [2, 3, 3, 3, 0]],
           ["(CL) LRM-10", 109, "L", "A", 2400, 1, 2.5, [4, 6, 6, 6, 0]],
           ["(CL) LRM-15", 164, "L", "A", 2400, 1, 3.5, [5, 9, 9, 9, 0]],
           ["(CL) LRM-20", 220, "L", "A", 2400, 1, 5, [6, 12, 12, 12, 0]],
           # SRM2
           # SRM4
           ["(CL) SRM-6", 59, "M", "A", 2370, 1, 1.5, [4, 8, 8, 0, 0]],
           ["(CL) Streak SRM-2", 40, "M", "", 2647, 1, 1, [2, 4, 4, 0, 0]],
           ["(CL) Streak SRM-4", 79, "M", "", 2826, 1, 2, [3, 8, 8, 0, 0]],
           ["(CL) Streak SRM-6", 118, "M", "", 2826, 1, 3, [4, 12, 12, 0, 0]]]


# Ammo
#
# Name, weapon, ammount, weight
#
# TODO: Vehicle flamer
# TODO: Advanced weapons
ammo = [["(IS) @ AC/2", "(IS) Autocannon/2", 45, 1],
        ["(IS) @ AC/5", "(IS) Autocannon/5", 20, 1],
        ["(IS) @ AC/10", "(IS) Autocannon/10", 10, 1],
        ["(IS) @ AC/20", "(IS) Autocannon/20", 5, 1],
        ["@ Gauss Rifle", "(IS) Gauss Rifle", 8, 1],
        ["(IS) @ LB 5-X AC (Slug)", "(IS) LB 5-X AC", 20, 1],
        ["(IS) @ LB 5-X AC (Cluster)", "(IS) LB 5-X AC", 20, 1],
        ["(IS) @ LB 10-X AC (Slug)", "(IS) LB 10-X AC", 10, 1],
        ["(IS) @ LB 10-X AC (Cluster)", "(IS) LB 10-X AC", 10, 1],
        ["@ Machine Gun", "(IS) Machine Gun", 200, 1],
        ["@ Machine Gun (1/2)", "(IS) Machine Gun", 100, 0.5],
        ["(IS) @ Ultra AC/5", "(IS) Ultra AC/5", 20, 1],
        ["(IS) @ Plasma Rifle", "(IS) Plasma Rifle", 10, 1],
        ["(IS) @ LRM-5", "(IS) LRM-5", 24, 1],
        ["(IS) @ LRM-10", "(IS) LRM-10", 12, 1],
        ["(IS) @ LRM-15", "(IS) LRM-15", 8, 1],
        ["(IS) @ LRM-20", "(IS) LRM-20", 6, 1],
        ["(IS) @ LRM-5 (Artemis IV Capable)", "(IS) LRM-5", 24, 1],
        ["(IS) @ LRM-10 (Artemis IV Capable)", "(IS) LRM-10", 12, 1],
        ["(IS) @ LRM-15 (Artemis IV Capable)", "(IS) LRM-15", 8, 1],
        ["@ SRM-2", "(IS) SRM-2", 50, 1],
        ["@ SRM-4", "(IS) SRM-4", 25, 1],
        ["@ SRM-6", "(IS) SRM-6", 15, 1],
        ["@ SRM-6 (Artemis IV Capable)", "(IS) SRM-6", 15, 1],
        ["(IS) @ MRM-20", "(IS) MRM-20", 12, 1],
        ["(IS) @ Streak SRM-2", "(IS) Streak SRM-2", 50, 1],
        ["(IS) @ Anti-Missile System", "(IS) Anti-Missile System", 12, 1]]

# Equipment
#
# Name, BV, year, uses ammo rate
#
# TODO: lTAG
equipment = [["A-Pod", 1, 3055, 0],
             ["B-Pod", 2, 3069, 0],
             ["(IS) Anti-Missile System", 32, 2617, 1],
             ["Guardian ECM Suite", 61, 2597, 0],
             ["Beagle Active Probe", 10, 2576, 0],
             ["C3 Computer (Slave)", 0, 3050, 0],
             ["C3 Computer (Master)", 0, 3050, 0],
             ["Improved C3 Computer", 0, 3062, 0],
             ["TAG", 0, 2600, 0],
             ["ECM Suite", 61, 2597, 0], # Clan
             ["Active Probe", 12, 2576, 0], # Clan
             ["(CL) Anti-Missile System", 32, 2617, 1],
             ["CASE", 0, 2476, 0], # HACK: CASE
             ["(IS) Targeting Computer", 0, 3062, 0],
             ["(CL) Targeting Computer", 0, 2860, 0], # HACK: Tarcomp
             # Experimental
             ["Electronic Warfare Equipment", 39, 3025, 0]]

# Info on heatsink types
#
# Name, techbase, year
#
# Where techbase 0 = IS, 1 = Clan, 2 = Both, 10 = unknown
#
heatsink = [["Single Heat Sink", 2, 2022],
            ["Double Heat Sink", 0, 2567],
            ["Double Heat Sink", 1, 2567]]

# Not used.
missile_ench = [["Artemis IV", 2598],
                ["Apollo", 3071]]

# Name, year, BV multiplier, damage formula
physical = [["Hatchet", 3022, 1.5, (lambda x : x / 5)],
            ["Sword", 3058, 1.725, (lambda x : x / 10 + 1)],
            ["Claws", 3060, 1.275, (lambda x : ceil(x / 7))],
            ["Mace", 3061, 1.0, (lambda x : ceil(x / 4))]]

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
        if id == 0:
            error_exit((self.type, self.tb))

    # Return earliest year heatsink is available
    def get_year(self):
        return self.year

    # Return heatsink weight
    # 1 ton/sink, 10 free
    def get_weight(self):
        return self.nr - 10

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
        self.BF = ginfo[7]
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

class Equiplist:
    def __init__(self):
        self.list = []
        for e in equipment:
            self.list.append(Equipment(e))

class Equipment:
    def __init__(self, ginfo):
        self.name = ginfo[0]
        self.BV = ginfo[1]
        self.year = ginfo[2]
        self.useammo = ginfo[3]
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
        self.count = 0

    def addone(self):
        self.count = self.count + 1

# Store Gear
#
# Take in lists of front and rear facing gears
class Gear:
    def __init__(self, equip, equiprear):
        self.equip = equip
        self.equiprear = equiprear

        # We need to create local lists for avoid trouble with Omni-mechs
        self.weaponlist = Weaponlist()
        self.equiplist = Equiplist()
        self.physicallist = Physicallist()
        self.ammolist = Ammolist()
        # Keep track of tarcomp
        self.tarcomp = 0
        # Mech has a physical weapon?
        self.phys = 0
        # Gear weight
        self.w_weight = 0.0
        self.a_weight = 0.0

        # Count gear
        for name in self.equip:
            # Go through weapon list
            id = 0
            for w in self.weaponlist.list:
                if name[0] == w.name:
                    w.addone()
                    self.w_weight += w.weight
                    id = 1
            # Handle non-weapon equipment
            # HACK: Handle CASE, Tarcomp
            for e in self.equiplist.list:
                if (name[0] == e.name and 
                    (name[1] == 'equipment' or name[1] == 'CASE' or
                     name[1] == 'TargetingComputer')):
                    e.addone()
                    id = 1
                    # TODO: Clan tarcomp
                    if (name[0] == "(IS) Targeting Computer" and name[1] =='TargetingComputer'):
                        self.tarcomp = 1
            for p in self.physicallist.list:
                if (name[0] == p.name and name[1] == 'physical'):
                    p.addone()
                    id = 1
                    self.phys = 1
            for a in self.ammolist.list:
                if (name[0] == a.name and name[1] == 'ammunition'):
                    a.addone()
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
                    id = 1
            # Not found
            if (id == 0):
                print "Unidentified:", name
                error_exit("gear")

    # Get weapons weight
    def get_w_weight(self):
        return self.w_weight

    # Get ammo weight
    def get_a_weight(self):
        return self.a_weight

# TODO:
# - Equipment, physical weight
# - rest of ammo
# - handle shared IS & Clan ammo
# - defensive equipment
