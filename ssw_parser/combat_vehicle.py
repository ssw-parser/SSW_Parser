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
Contains the master class for a combat vehicle
"""

import sys
from math import ceil
from defensive import VehicleStructure, VehicleArmor
from movement import Engine
from util import ceil_05, get_child, get_child_data, year_era_test
from loadout import Baseloadout, Loadout
from item import Item


class LiftEquipment(Item):
    """
    A class to hold information about lift/dive equipment or rotors
    """
    def __init__(self, mweight, mot_type):
        Item.__init__(self)
        self.weight = mweight  # Mech weight
        self.mot_type = mot_type

    def get_type(self):
        """
        Return type of equipment
        """
        if self.mot_type == "VTOL":
            return "Rotors"
        elif self.mot_type == "Hovercraft":
            return "Lift Equipment"
        else:
            return ""

    def get_rules_level(self):
        """
        Standard rules
        """
        return 1

    def get_weight(self):
        """
        Get weight
        """
        if self.mot_type == "VTOL" or self.mot_type == "Hovercraft":
            return ceil_05(0.1 * self.weight)
        else:
            return 0

    def get_cost(self):
        """
        Get cost
        """
        if self.mot_type == "Hovercraft":
            return  20000 * self.get_weight()
        elif self.mot_type == "VTOL":
            return 40000 * self.get_weight()
        else:
            return 0


class ControlSystems(Item):
    """
    A class to hold control systems
    """
    def __init__(self, mweight):
        Item.__init__(self)
        self.weight = mweight  # Mech weight

    def get_type(self):
        """
        Return type of equipment
        """
        return "Control Systems"

    def get_rules_level(self):
        """
        Standard rules
        """
        return 1

    def get_weight(self):
        """
        Get weight
        """
        return ceil_05(0.05 * self.weight)

    def get_cost(self):
        """
        Get cost
        """
        return 10000 * self.get_weight()


class CombatVehicle:
    """
    A master class holding info about a combat vehicle.
    """
    def __init__(self, xmldoc):

        # This is a combat vehicle
        self.type = "CV"

        # Get top-level structure data
        for cveh in xmldoc.getElementsByTagName('combatvehicle'):
            self.model = cveh.attributes["model"].value
            self.name = cveh.attributes["name"].value
            self.motive = cveh.attributes["motive"].value
            self.omni = cveh.attributes["omni"].value
            self.weight = int(cveh.attributes["tons"].value)

            # Get BV. Should give prime variant BV for Omni-vehicles
            # get first instance only to avoid problems with Omni-vehicles
            self.batt_val = int(get_child_data(cveh, 'battle_value'))

            # Motive
            for mot in cveh.getElementsByTagName('motive'):
                self.mot_type = mot.attributes["type"].value
                self.cruise = int(mot.attributes["cruise"].value)
                self.turret = mot.attributes["turret"].value

            # Get Cost.
            cost = float(get_child_data(cveh, 'cost'))

            # Get production era
            self.prod_era = int(get_child_data(cveh, 'productionera'))

            # Get techbase (IS, Clan)
            # get first instance only to avoid problems with Omni-vehicles
            self.techbase = get_child_data(cveh, 'techbase')

            # Get year
            self.year = int(get_child_data(cveh, 'year'))

            # Sanity check for year
            year_era_test(self.year, self.prod_era,
                          self.name + " " + self.model)

            if (self.year < 2470):
                print self.name, self.model
                print "Combat Vehicles not available before 2470!"
                sys.exit(1)

            if (self.year < 2854 and self.omni == "TRUE"):
                print self.name, self.model
                print "OmniVehicles not available before 2854!"
                sys.exit(1)

            ### Components starts here ###

            self.structure = VehicleStructure(get_child(cveh, 'structure'),
                                              self.weight,
                                              self.mot_type, self.turret)

            self.engine = Engine(get_child(cveh, 'engine'), self)

            self.lift = LiftEquipment(self.weight, self.mot_type)

            if self.engine.etype == "No Engine":
                self.control = ControlSystems(0.0)
            else:
                self.control = ControlSystems(self.weight)

            self.armor = VehicleArmor(get_child(cveh, 'armor'),
                                      self.weight)

            ### Loadout stuff starts here ###

            # Get baseloadout
            blo = cveh.getElementsByTagName('baseloadout')[0]

            # Construct current loadout, empty name for base loadout
            self.load = Baseloadout(blo, self, self.batt_val,
                                    self.prod_era, cost)

            # Get omni loadouts
            self.loads = []
            for load in cveh.getElementsByTagName('loadout'):

                # Construct current loadout
                current = Loadout(load, self.load, self)

                self.loads.append(current)

    def get_walk(self):
        """
        Get walk speed
        """
        return self.cruise + self.load.gear.get_speed_adj()

    def get_run(self):
        """
        Get standard running speed, with no modifiers
        """
        spd = self.cruise + self.load.gear.get_speed_adj()
        factor = 1.5
        rspeed = int(ceil(spd * factor))
        # Hardened Armor
        if self.armor.atype == "Hardened Armor":
            rspeed -= 1
        return rspeed

    def get_max_run(self):
        """
        Get maximum running speed
        """
        spd = self.cruise + self.load.gear.get_speed_adj()
        factor = 1.5
        if self.load.gear.supercharger.has_sc():
            factor += 0.5
        rspeed = int(ceil(spd * factor))
        # Hardened Armor
        if self.armor.atype == "Hardened Armor":
            rspeed -= 1
        return rspeed

    def get_move_target_modifier(self, load):
        """
        Get target modifier from movement, see Total Warfare for details
        """
        run_speed = self.get_max_run()
        jump_speed = load.get_jump()

        if (run_speed < 3):
            r_mod = 0
        elif (run_speed < 5):
            r_mod = 1
        elif (run_speed < 7):
            r_mod = 2
        elif (run_speed < 10):
            r_mod = 3
        elif (run_speed < 18):
            r_mod = 4
        elif (run_speed < 25):
            r_mod = 5
        else:
            r_mod = 6

        # VTOLs gets +1 for being airborne
        if self.mot_type == "VTOL":
            r_mod += 1

        if (jump_speed < 3):
            j_mod = 0
        elif (jump_speed < 5):
            j_mod = 1
        elif (jump_speed < 7):
            j_mod = 2
        elif (jump_speed < 10):
            j_mod = 3
        elif (jump_speed < 18):
            j_mod = 4
        elif (jump_speed < 25):
            j_mod = 5
        else:
            j_mod = 6

        # Do not give jump mods if no jumpjets
        if (jump_speed > 0):
            j_mod += 1

        return max(j_mod, r_mod)

    def get_stealth(self):
        """
        Returns true if the mech mounts a stealth system
        """
        stlth = False
        if self.armor.atype == "Stealth Armor":
            stlth = True
        return stlth

    def def_bv(self, load, printq):
        """
        Get defensive BV
        """
        dbv = 0.0
        # Armor
        cur = self.armor.get_armor_bv()
        dbv += cur
        if (printq):
            print "Armor Def BV: ", cur

        # Internal Structure
        cur = self.structure.points * 1.5
        dbv += cur
        if (printq):
            print "Structure Def BV: ", cur

        # Defensive equipment
        cur = load.get_def_bv(self)
        dbv += cur
        if (printq):
            print "Equipment Def BV: ", cur

        # Multiply with vehicle type modifier
        # Missing: Naval, WiGE
        if self.mot_type == "VTOL":
            cur = 0.7
        elif self.mot_type == "Hovercraft":
            cur = 0.7
        elif self.mot_type == "Tracked":
            cur = 0.9
        elif self.mot_type == "Wheeled":
            cur = 0.8
        dbv *= cur
        if (printq):
            print "Vehicle Type Modifier: ", cur

        # Defensive factor
        mtm = self.get_move_target_modifier(load)
        # Stealth armor adds to to-hit
        if self.armor.atype == "Stealth Armor":
            mtm += 2
        assert mtm >= 0, "Negative defensive modifier!"
        def_factor = 1.0 + (mtm / 10.0)
        if (printq):
            print "Target modifier: ", mtm
            print "Defensive Faction: ", def_factor

        # Final result
        dbv *= def_factor
        if (printq):
            print "Defensive BV: ", dbv
        return dbv

    def off_bv(self, load, printq):
        """
        Get offensive BV
        """
        obv = load.off_bv(self, printq)

        # Tonnage
        if (printq):
            print "Weight BV: ", 0.5 * self.weight
        obv += 0.5 * self.weight

        # total
        if (printq):
            print "Total Base Offensive: ", obv

        # speed factor
        speed_factor = self.get_max_run() + ceil(load.get_jump() / 2.0)
        if (printq):
            print "Speed Factor: ", speed_factor
        adj_sf = ((speed_factor - 5.0) / 10.0) + 1.0
        off_speed_factor = round(pow(adj_sf, 1.2), 2)
        if (printq):
            print "Offensive Speed Factor: ", off_speed_factor

        # Final result
        obv *= off_speed_factor
        if (printq):
            print "Offensive BV: ", obv
        return obv

    def get_bv(self, load):
        """
        Get the BV of a specific loadout. Use vehicle.load if not an omni.
        """
        batt_val = int(round(self.off_bv(load, False) +
                             self.def_bv(load, False)))

        if batt_val != load.batt_val:
            print ("%s %s%s: %d %d" % (self.name, self.model, load.get_name(),
                                       batt_val, load.batt_val))

        assert batt_val == load.batt_val, "Error in BV calculation!"
        return batt_val

    def get_year(self, load):
        """
        Get year
        """
        if self.omni == "TRUE":
            return load.year
        else:
            return self.year

    def get_rules_level(self, load):
        """
        Return rules level of mech
        """
        r_level = 0
        # Mixed tech is advanced rules
        if self.techbase == "Mixed":
            r_level = 2
        r_level = max(r_level, self.structure.get_rules_level())
        r_level = max(r_level, self.engine.get_rules_level())
        r_level = max(r_level, self.armor.get_rules_level())
        # Hack -- turrets are advanced rules
        if load.turret and r_level < 2:
            r_level = 2

        r_level = max(r_level, load.get_rules_level())

        return r_level

    def calculate_cost(self, i):
        """
        Calculate the cost of a combat vehicle
        """

        # Structural costs
        cost = 0

        # Internal structure
        cost += self.structure.get_cost()

        # Control Components
        cost += self.control.get_cost()

        # Lift/Dive Equipment & Rotors
        cost += self.lift.get_cost()

        # Engine
        cost += self.engine.get_cost()
        # Jump Jets
        cost += i.jjets.get_cost()
        # Heat Sinks
        cost += i.heatsinks.get_cost()

        # Armor
        cost += self.armor.get_cost()

        # HACK: Turrets
        cost += i.gear.tur_weight * 5000

        # Power Amplifiers
        cost += i.power_amp.get_cost()

        # Partial Wing, jump boosters
        cost += i.partw.get_cost()
        cost += i.jumpb.get_cost()

        # Booby trap
        cost += i.btrap.get_cost()

        # Hack: Armored components
        cost += len(i.arm_loc) * 150000

        # Gear
        cost += i.gear.get_cost()

        # Final calculation
        if self.mot_type == "VTOL":
            divisor = 30.0
        elif self.mot_type == "Hovercraft":
            divisor = 50.0
        elif self.mot_type == "Tracked":
            divisor = 100.0
        elif self.mot_type == "Wheeled":
            divisor = 200.0

        cost *= (1.0 + (self.weight / divisor))
        if self.omni == "TRUE":
            cost *= 1.25

        return round(cost)
