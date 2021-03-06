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
gear.py
=======
Contains master gear class and misc other related classes.
"""

from math import ceil
from error import error_exit
from util import ceil_05, gettext, get_child_data
from item import Item
from weapon_list import Weaponlist
from physical import Physicallist
from ammo import Ammolist

# A class to contain data about battlemech gear to allow for clearer code,
# by using named class members.

# Equipment
#
# Name: off BV, def BV, rules level, weight, uses ammo rate, explosive slots,
# cost
#
# Where rules level is: 0 = intro, 1 = tournament legal, 2 = advanced,
# 3 = experimental, 4 = primitive
#

EQUIPMENT = {
    # Tournament legal, TM
    "C3 Computer (Slave)": [[0, 0], [0, 0], 1, 1, 0, 0, 250000],
    "C3 Computer (Master)": [[0, 0], [0, 0], 1, 5, 0, 0, 1500000],
    "Improved C3 Computer": [[0, 0], [0, 0], 1, 2.5, 0, 0, 750000],
    "TAG": [[0, 0], [0, 0], 1, 1, 0, 0, 50000],
    "Light TAG": [[0, 0], [0, 0], 1, 0.5, 0, 0, 40000],
    "A-Pod": [[0, 0], [1, 0], 1, 0.5, 0, 0, 1500],
    "B-Pod": [[0, 0], [2, 0], 1, 1, 0, 0, 2500],
    "(IS) Anti-Missile System": [[0, 0], [32, 11], 1, 0.5, 1, 0, 100000],
    "Guardian ECM Suite": [[0, 0], [61, 0], 1, 1.5, 0, 0, 200000],
    "Beagle Active Probe": [[0, 0], [10, 0], 1, 1.5, 0, 0, 200000],
    "ECM Suite": [[0, 0], [61, 0], 1, 1, 0, 0, 200000],  # Clan
    "Active Probe": [[0, 0], [12, 0], 1, 1, 0, 0, 200000],  # Clan
    "Light Active Probe": [[0, 0], [7, 0], 1, 0.5, 0, 0, 50000],
    "(CL) Anti-Missile System": [[0, 0], [32, 22], 1, 0.5, 1, 0, 100000],
    # Industrial gear, TM
    "Cargo, Liquid": [[0, 0], [0, 0], 1, 1, 0, 0, 100],
    "Cargo, Insulated, Vehicular": [[0, 0], [0, 0], 1, 1, 0, 0, 250],
    "Cargo, Standard, Vehicular": [[0, 0], [0, 0], 1, 1, 0, 0, 0],
    "Communications Equipment": [[0, 0], [0, 0], 1, 1, 0, 0, 10000],
    "Infantry Compartment": [[0, 0], [0, 0], 1, 1, 0, 0, 0],
    "MASH": [[0, 0], [0, 0], 1, 3.5, 0, 0, 35000],
    "Paramadic Equipment": [[0, 0], [0, 0], 1, 0.25, 0, 0, 7500],
    "Remote Sensor Dispenser": [[0, 0], [0, 0], 1, 0.5, 1, 0, 30000],
    "Lift Hoist": [[0, 0], [0, 0], 1, 3, 0, 0, 50000],
    # New TL
    "Watchdog CEWS": [[0, 0], [68, 0], 1, 1.5, 0, 0, 600000],

    # Advanced
    "Angel ECM": [[0, 0], [100, 0], 2, 2, 0, 0, 750000],
    "Bloodhound Active Probe": [[0, 0], [25, 0], 2, 2, 0, 0, 500000],
    "Chaff Pod": [[0, 0], [19, 0], 2, 1, 0, 1, 2000],
    "Coolant Pod": [[0, 0], [0, 0], 2, 1, 0, 1, 50000],
    "(IS) Laser Anti-Missile System": [[0, 0], [45, 0], 2, 1.5, 0, 0, 225000],
    "(CL) Laser Anti-Missile System": [[0, 0], [45, 0], 2, 1, 0, 0, 225000],
    "M-Pod": [[5, 0], [0, 0], 2, 1, 0, 1, 6000],
    "MW Aquatic Survival System": [[0, 0], [9, 0], 2, 1.5, 0, 0, 4000],
    "Drone Carrier Control System": [[0, 0], [0, 0], 2, 2.5, 0, 0, 25000],
    "Ground Mobile HPG": [[0, 0], [0, 0], 2, 12, 0, 0, 4000000000],
    # Experimental
    "Collapsible Command Module (CCM)": [[0, 0], [0, 0], 3, 16, 0, 0, 500000],
    "C3 Boosted Computer (Slave)": [[0, 0], [0, 0], 3, 3, 0, 0, 500000],
    "C3 Boosted Computer (Master)": [[0, 0], [0, 0], 3, 6, 0, 0, 3000000],
    "Electronic Warfare Equipment": [[0, 0], [39, 0], 3, 7.5, 0, 0, 500000],
    "HarJel": [[0, 0], [0, 0], 3, 1, 0, 0, 120000],
    "C3 Remote Sensor Launcher": [[30, 6], [0, 0], 3, 4, 1, 0, 400000],
    "Nova CEWS" : [[0, 0], [68, 0], 3, 1.5, 0, 0, 11100000],
    }

# CASE
#
# Name: rules level, weight
#
# Where rules level is: 0 = intro, 1 = tournament legal, 2 = advanced,
# 3 = experimental, 4 = primitive
#

CASE = {
    "CASE": [1, 0.5],
    "(IS) CASE II": [2, 1],
    "(CL) CASE II": [2, 0.5]
    }

# Targeting computers
#
# rules level
#
TARCOMPS = {
    "(IS) Targeting Computer": [1],
    "(CL) Targeting Computer": [1]
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
    Heatsinks for an unit
    """
    def __init__(self, heat, load):
        Item.__init__(self)
        self.load = load  # Reference to parent
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
        1 ton/sink, 10 free for fusion types
        """
        if (self.load.unit.engine.etype == "I.C.E. Engine" or
            self.load.unit.engine.etype == "No Engine"):
            return self.number
        else:
            return self.number - 10

    def get_cost(self):
        """
        Return heatsink cost
        10 single heat sinks in fusion engine costs nothing
        """
        if (self.type == "Single Heat Sink" and
            self.load.unit.engine.etype != "I.C.E. Engine"):
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

        # Extract tonnage for variable weight gear
        tons = node.getElementsByTagName("tons")
        if (tons):
            self.wgt = float(gettext(tons[0].childNodes))
        # Handle no info, we use 0.0 to indicate we get the weight from tables
        else:
            self.wgt = 0.0

        # Handle location info
        lnd = node.getElementsByTagName("location")
        # Normal case, no split
        if (lnd):
            lnode = lnd[0]
            self.loc = gettext(lnode.childNodes)
            if self.loc == "Turret":
                self.turret = True
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
        # Also check if turret-mounted
        elif self.name[0:4] == "(T) ":
            self.turret = True
            self.name = self.name[4:]


class Equiplist:
    """
    Store the list with equipment
    """
    def __init__(self):
        self.list = []
        for equip in EQUIPMENT.keys():
            self.list.append(Equipment(equip))

    def get_turret_weight(self):
        """
        Get weight of turret mounted gear
        """
        tur_weight = 0.0
        for equip in self.list:
            if equip.tur_count > 0:
                tur_weight += equip.tur_count * equip.get_weight()

        return tur_weight

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
        self.tur_count = 0
        self.ammocount = 0
        self.ammo_ton = 0
        self.weight = 0.0

    def get_rules_level(self):
        """
        Get rules level of equipment
        """
        return EQUIPMENT[self.name][2]

    def get_weight(self):
        """
        Get weight of equipment
        """
        return (self.weight / float(self.count))

    def get_cost(self):
        """
        Get cost of one piece of equipment
        """
        return EQUIPMENT[self.name][6]

    def addone(self, tons, turret):
        """
        Add one piece of equipment
        """
        self.count = self.count + 1
        if turret:
            self.tur_count += 1
        if tons > 0.0:
            self.weight += tons
        else:
            self.weight += EQUIPMENT[self.name][3]

    # We need to track tonnage and rounds separately due to BV
    # calculations and how MML ammo works
    def add_ammo(self, count, amount):
        """
        Add ammo to equipment
        """
        self.ammocount = self.ammocount + amount
        self.ammo_ton += count


class Supercharger:
    """
    A supercharger
    """
    def __init__(self, rating, eweight):
        self.supercharger = False
        self.eng_rating = rating
        self.eng_weight = eweight

    def get_rules_level(self):
        """
        Get rules level of supercharger
        """
        if self.supercharger:
            return 2
        else:
            return 0

    def get_weight(self):
        """
        Get weight of supercharger
        """
        if self.supercharger:
            return ceil_05(self.eng_weight / 10.0)
        else:
            return 0

    def get_cost(self):
        """
        Get cost of supercharger
        """
        if self.supercharger:
            return 10000 * self.eng_rating
        else:
            return 0

    def add(self):
        """
        Add supercharger
        """
        self.supercharger = True

    def has_sc(self):
        """
        Is supercharger installed?
        """
        return self.supercharger


class Gear:
    """
    Store Gear

    Take in lists of front and rear facing gears
    """
    def __init__(self, mech, art4, art5, apollo, equip, clan_case):
        self.equip = equip
        self.c_case = clan_case  # Clan CASE

        # We need to create local lists for avoid trouble with Omni-mechs
        self.weaponlist = Weaponlist(art4, art5, apollo)
        self.equiplist = Equiplist()
        self.physicallist = Physicallist(mech.weight)
        self.ammolist = Ammolist()
        self.supercharger = Supercharger(mech.engine.erating,
                                         mech.engine.get_weight())
        # Keep track of tarcomp
        self.tarcomp = 0
        # Gear weight
        self.a_weight = 0.0
        self.e_weight = 0.0
        self.tc_weight = 0.0
        self.mod_weight = 0.0
        self.tur_weight = 0.0
        # Track explosive ammo by locations
        self.exp_ammo = {}
        # Save reference to explosive weapon count
        self.exp_weapon = self.weaponlist.exp_weapon
        self.case = {}
        # Track coolant pods
        self.coolant = 0
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
                found = self.weaponlist.add(name.name, name.loc, name.rear,
                                            name.turret)
                if found:
                    ident = True

            # Handle non-weapon equipment
            elif (name.typ == 'equipment'):
                for equip in self.equiplist.list:
                    if (name.name == equip.name):
                        equip.addone(name.wgt, name.turret)
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
                        # Hack SSW store fixed CASE on omnis twice
                        if not name.loc in self.case:
                            self.e_weight += CASE[cas][1]
                        ident = True
                        # Save CASE status
                        self.case[name.loc] = name.typ
                        # Hack CASE rules level
                        if self.case_rule < CASE[cas][0]:
                            self.case_rule = CASE[cas][0]

            # Hack, handle targeting computer
            elif (name.name == "(IS) Targeting Computer" and
                name.typ == 'TargetingComputer'):
                self.tarcomp = 1
                ident = True
            elif (name.name == "(CL) Targeting Computer" and
                name.typ == 'TargetingComputer'):
                self.tarcomp = 2
                ident = True

            # Hack, supercharger
            elif (name.name == "Supercharger" and name.typ == "Supercharger"):
                self.supercharger.add()
                ident = True

            # A possible physical weapon
            elif (name.typ == 'physical'):
                found = self.physicallist.add(name.name, name.loc, name.turret)
                if found:
                    ident = True

            # Modular armor
            elif (name.typ == 'miscellaneous'):
                if name.name == "Modular Armor":
                    ident = True
                    mod = self.mod_armor.get(name.loc, 0)
                    mod += 10
                    self.mod_armor[name.loc] = mod
                    self.mod_weight = 1.0
                    self.has_mod_armor = True
                # Ignore Hitches for now
                if name.name == "Hitch":
                    ident = True

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
        if self.tarcomp == 1:  # IS
            self.tc_weight = ceil(self.weaponlist.tcw_weight / 4.0)
        if self.tarcomp == 2:  # Clan
            self.tc_weight = ceil(self.weaponlist.tcw_weight / 5.0)

        # Calculate turret weight
        self.tur_weight = ceil_05((self.weaponlist.tur_weight +
                                   self.equiplist.get_turret_weight() +
                                   self.physicallist.get_turret_weight()) /
                                  10.0)

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
        r_level = max(r_level, self.weaponlist.get_rules_level())
        r_level = max(r_level, self.physicallist.get_rules_level())
        r_level = max(r_level, self.equiplist.get_rules_level())
        r_level = max(r_level, self.supercharger.get_rules_level())
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
        # Supercharger
        cost += self.supercharger.get_cost()
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
        Get equipment, tarcomp, supercharger, modular armor & CASE weight
        """
        wgt = self.e_weight + self.tc_weight + self.supercharger.get_weight()
        wgt += self.mod_weight
        return wgt

    def get_p_weight(self):
        """
        Get physical weapon weight
        """
        return self.physicallist.p_weight

    def get_weight(self):
        """
        Get weight of all gear
        """
        wgt = (self.get_w_weight() + self.get_a_weight() +
               self.get_e_weight() + self.get_p_weight())
        return wgt

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
            fr_count = (weap.count - weap.count_la - weap.count_ra -
                        weap.count_tur)
            if (fr_count) > 0:
                bv_front += weap.get_bv(self.tarcomp) * (fr_count)

            if weap.countrear > 0:
                bv_rear += weap.get_bv(self.tarcomp) * weap.countrear

        if (bv_rear > bv_front):
            return True
        else:
            return False
