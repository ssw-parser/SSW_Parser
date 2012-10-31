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
mech.py
=======
Contains the master class for a mech

Also contains the Multi class.
"""

import sys
from math import ceil
from defensive import MechStructure, MechArmor
from movement import Cockpit, Enhancement, Gyro, Engine
from util import get_child, get_child_data, year_era_test
from util import get_move_target_modifier
from loadout import Baseloadout, Loadout
from battle_force import BattleForce
from item import Item
from unit import Unit

# A mech class with data read from SSW xml data for use in various
# applications.


class Multi(Item):
    """
    Multi-slot items (chameleon, void, null)
    """
    def __init__(self):
        Item.__init__(self)
        self.multi = []

    def add(self, string):
        """
        Add an item
        """
        self.multi.append(string)

    def get_type(self):
        """
        Return all strings
        """
        desc = ""
        for string in self.multi:
            desc += " " + string
        return desc

    def get_rules_level(self):
        """
        Return heat-sink rules level
        0 = intro, 1 = tournament legal, 2 = advanced, 3 = experimental
        """
        r_level = 0
        for i in self.multi:
            if i == "Chameleon LPS":
                tmp = 3
            elif i == "Null Signature System":
                tmp = 3
            elif i == "Void Signature System":
                tmp = 2
            if tmp > r_level:
                r_level = tmp

        return r_level

    def get_stealth(self):
        """
        Check for stealth items.
        """
        stlth = False
        for i in self.multi:
            if i == "Chameleon LPS":
                stlth = True
            elif i == "Null Signature System":
                stlth = True
            elif i == "Void Signature System":
                stlth = True

        return stlth

    def get_def_mod(self):
        """
        Get defensive move target modifier
        """
        mtm = 0
        # Chameleon LPS & Null-sig system
        for i in self.multi:
            if i == "Chameleon LPS":
                mtm += 2
            elif i == "Null Signature System":
                mtm += 2
            elif i == "Void Signature System":
                mtm += 3

        return mtm

    def get_weight(self):
        """
        All these items are weighless
        """
        return 0.0

    def get_cost(self):
        """
        Return costs
        """
        cost = 0
        for mult in self.multi:
            if mult == "Chameleon LPS":
                cost += 600000
            elif mult == "Null Signature System":
                cost += 1400000
            elif mult == "Void Signature System":
                cost += 2000000

        return cost


class Mech(Unit):
    """
    A master class holding info about a mech.
    """
    def __init__(self, xmldoc):
        Unit.__init__(self)

        # This is a mech
        self.type = "BM"

        # Set some data to zero that sometimes will not get set otherwise
        self.multi = Multi()

        # Get top-level structure data
        for mmech in xmldoc.getElementsByTagName('mech'):
            self.model = mmech.attributes["model"].value
            self.name = mmech.attributes["name"].value
            self.omni = mmech.attributes["omnimech"].value
            self.weight = int(mmech.attributes["tons"].value)

            # Get BV. Should give prime variant BV for Omni-mechs
            # get first instance only to avoid problems with Omni-mechs
            self.batt_val = int(get_child_data(mmech, 'battle_value'))

            # Get Cost.
            cost = float(get_child_data(mmech, 'cost'))

            # Get production era
            self.prod_era = int(get_child_data(mmech, 'productionera'))

            # Get mech type (battle, industrial)
            self.mechtype = get_child_data(mmech, 'mech_type')

            # Only support battlemechs
            if (self.mechtype != "BattleMech" and
                self.mechtype != "PrimitiveBattleMech"):
                print self.name, self.model
                print "Industrial Mechs not supported!"
                sys.exit(1)

            # Get techbase (IS, Clan)
            # get first instance only to avoid problems with Omni-mechs
            self.techbase = get_child_data(mmech, 'techbase')

            # Get year
            self.year = int(get_child_data(mmech, 'year'))

            # Sanity check for year
            year_era_test(self.year, self.prod_era,
                          self.name + " " + self.model)

            if (self.year < 2439):
                print self.name, self.model
                print "Battlemech older than Mackie!"
                sys.exit(1)

            if (self.year < 2470 and self.mechtype == "BattleMech"):
                print self.name, self.model
                print "Non-primitive BattleMechs not available before 2470!"
                sys.exit(1)

            if (self.year < 2854 and self.omni == "TRUE"):
                print self.name, self.model
                print "OmniMechs not available before 2854!"
                sys.exit(1)

            # Get motive type (biped, quad)
            self.motive = get_child_data(mmech, 'motive_type')

            ### Components starts here ###

            # Get internal structure type
            self.structure = MechStructure(get_child(mmech, 'structure'),
                                           self.weight, self.motive)

            # Get engine data
            self.engine = Engine(get_child(mmech, 'engine'), self)

            # Get gyro
            self.gyro = Gyro(get_child(mmech, 'gyro'),
                             self.engine.etype, self.engine.erating)

            # Get cockpit
            self.cockpit = Cockpit(get_child(mmech, 'cockpit'), self)

            # Get enhancement, needs for loop
            self.enhancement = Enhancement(None, self.weight,
                                           self.engine.erating)
            for enh in mmech.getElementsByTagName('enhancement'):
                self.enhancement = Enhancement(enh, self.weight,
                                               self.engine.erating)

            # Get armor.
            self.armor = MechArmor(get_child(mmech, 'armor'),
                                   self.weight, self.motive)

            ### Loadout stuff starts here ###

            # Get baseloadout
            blo = mmech.getElementsByTagName('baseloadout')[0]

            # Get multi-slot stuff
            for mlts in blo.getElementsByTagName('multislot'):
                slot = mlts.attributes["name"].value
                self.multi.add(slot)

            # Construct current loadout, empty name for base loadout
            self.load = Baseloadout(blo, self, self.batt_val,
                                    self.prod_era, cost)

            # HACK -- Apply modular armor
            if self.load.gear.has_mod_armor:
                self.armor.apply_modular(self.load.gear.mod_armor)

            # Get omni loadouts
            self.loads = []
            for load in mmech.getElementsByTagName('loadout'):

                # Construct current loadout
                current = Loadout(load, self.load, self)

                self.loads.append(current)

    def get_walk(self):
        """
        Get walk speed
        """
        return self.engine.speed + self.load.gear.get_speed_adj()

    def get_run(self):
        """
        Get standard running speed, with no modifiers
        """
        spd = self.engine.speed + self.load.gear.get_speed_adj()
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
        spd = self.engine.speed + self.load.gear.get_speed_adj()
        factor = 1.5
        if self.enhancement.is_tsm():
            spd += 1
        elif self.enhancement.is_masc():
            factor += 0.5
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

        r_mod = get_move_target_modifier(run_speed)
        j_mod = get_move_target_modifier(jump_speed)

        # Do not give jump mods if no jumpjets
        if (jump_speed > 0):
            j_mod += 1

        return max(j_mod, r_mod)

    def get_stealth(self):
        """
        Returns true if the mech mounts a stealth system
        """
        stlth = False
        if self.multi.get_stealth():
            stlth = True
        if self.armor.atype == "Stealth Armor":
            stlth = True
        return stlth

    def def_bv(self, load, printq):
        """
        Get defensive BV
        """
        dbv = 0.0
        # Armor
        torso_cockpit = False
        if self.cockpit.type == "Torso-Mounted Cockpit":
            torso_cockpit = True
        cur = self.armor.get_armor_bv(torso_cockpit)
        dbv += cur
        if (printq):
            print "Armor Def BV: ", cur
        # Internal
        cur = self.structure.get_bv_factor() * self.engine.get_bv_mod()
        dbv += cur
        if (printq):
            print "Internal Def BV: ", cur
        # Gyro
        cur = self.weight * self.gyro.get_bv_mod()
        if (load.arm_gyro and (self.gyro.gtype == "Standard Gyro" or
                               self.gyro.gtype == "Heavy-Duty Gyro")):
            cur *= 1.20
        elif (load.arm_gyro and self.gyro.gtype == "Compact Gyro"):
            cur *= 1.10
        elif (load.arm_gyro and self.gyro.gtype == "Extra-Light Gyro"):
            cur *= 1.30
        dbv += cur
        if (printq):
            print "Gyro Def BV: ", cur
        # Defensive equipment
        cur = load.get_def_bv(self)
        dbv += cur
        if (printq):
            print "Equipment Def BV: ", cur
        # Explosive
        cur = load.gear.get_ammo_exp_bv(self.engine)
        dbv += cur
        if (printq):
            print "Explosive Ammo BV: ", cur
        cur = load.gear.get_weapon_exp_bv(self.engine)
        dbv += cur
        if (printq):
            print "Explosive Weapon BV: ", cur
        # Defensive factor
        mtm = self.get_move_target_modifier(load)
        # Stealth armor adds to to-hit
        if self.armor.atype == "Stealth Armor":
            mtm += 2
        # Chameleon LPS & Null-sig system
        mtm += self.multi.get_def_mod()
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

        # Tonnage (physical)
        weight_factor = 1.0
        if (self.load.aes_ra.type == "Arm"):
            weight_factor += 0.1
        if (self.load.aes_la.type == "Arm"):
            weight_factor += 0.1
        if (self.enhancement.is_tsm()):
            weight_factor *= 1.5
        if (printq):
            print "Weight BV: ", weight_factor * self.weight
        obv += weight_factor * self.weight

        # total
        if (printq):
            print "Total Base Offensive: ", obv

        # speed factor
        off_speed_factor = self.get_off_speed_factor(load, printq)

        # Final result
        obv *= off_speed_factor
        if (printq):
            print "Offensive BV: ", obv
        return obv

    def get_bv(self, load):
        """
        Get the BV of a specific loadout. Use mech.load if not an omni.
        """
        base_bv = self.off_bv(load, False) + self.def_bv(load, False)
        if (self.cockpit.type == "Small Cockpit" or
            self.cockpit.type == "Torso-Mounted Cockpit"):
            batt_val = int(round(base_bv * 0.95))
        else:
            batt_val = int(round(base_bv))
        if batt_val != load.batt_val:
            print ("%s %s%s: %d %d" % (self.name, self.model, load.get_name(),
                                       batt_val, load.batt_val))

        assert batt_val == load.batt_val, "Error in BV calculation!"
        return batt_val

    def get_move_string(self):
        """
        Create a full movement string with TSM and MASC effects
        """
        spd = self.engine.speed + self.load.gear.get_speed_adj()
        if self.enhancement.is_tsm():
            wstr = str(spd) + "[" + str(spd + 1) + "]"
        else:
            wstr = str(spd)
        rspeed = int(ceil(spd * 1.5))
        if self.enhancement.is_tsm():
            rspeed2 = int(ceil((spd + 1) * 1.5))
            rstr = str(rspeed) + "[" + str(rspeed2) + "]"
        elif self.enhancement.is_masc():
            rspeed2 = int(ceil(spd * 2.0))
            rstr = str(rspeed) + "[" + str(rspeed2) + "]"
        else:
            rstr = str(rspeed)
        string = ("%s/%s/%d" % (wstr, rstr, self.load.get_jump()))
        return string

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
        r_level = max(r_level, self.gyro.get_rules_level())
        r_level = max(r_level, self.cockpit.get_rules_level())
        r_level = max(r_level, self.enhancement.get_rules_level())
        r_level = max(r_level, self.armor.get_rules_level())
        r_level = max(r_level, self.multi.get_rules_level())
        # Hack -- turrets are advanced rules
        if load.turret and r_level < 2:
            r_level = 2

        r_level = max(r_level, load.get_rules_level())

        return r_level

    ### Mech type tests ###

    # These functions should probably be removed?

    def is_juggernaut(self, i):
        """
        Check if a mech is a juggernaut

        Definition:
        - Walking and jump speed no more than 4
        - BF armor at least 5
        - Able to do 30 damage at range 6
        - Do less than 20 damage at range 18
        """
        if self.get_walk() > 4 or i.get_jump() > 4:
            return False

        batt_f = BattleForce(self, i)
        if batt_f.get_armor() < 5:
            return False

        if i.gear.weaponlist.count_damage(6) < 30:
            return False

        if i.gear.weaponlist.count_damage(18) >= 20:
            return False

        return True

    def is_sniper(self, i):
        """
        Check if a mech is a sniper

        Definition:
        - Able to do 10 damage at range 18
        - Do same (or less) damage at range 15 than range 18
          or is slower than walk or jump 4
        """
        dam18 = i.gear.weaponlist.count_damage(18)
        if dam18 < 10:
            return False

        if (i.gear.weaponlist.count_damage(15) > dam18 and
            (self.get_walk() > 3 or i.get_jump() > 4)):
            return False

        return True

    def is_missile_boat(self, i):
        """
        Check if a mech is a missile boat

        Definition:
        - Has at least 20 LRM tubes
        """
        if i.gear.weaponlist.lrms < 20:
            return False

        return True

    def is_striker(self, i):
        """
        Check if a mech is a striker

        Definition:
        - Speed at least walk 5 or jump 5
        - Able to do 15 damage at range 3
        """
        if self.get_walk() < 5 and i.get_jump() < 5:
            return False

        if i.gear.weaponlist.count_damage(3) < 15:
            return False

        return True

    def is_skirmisher(self, i):
        """
        Check if a mech is a skirmisher

        Definition:
        - Speed at least walk 5 or jump 5
        - BF armor at least 3
        - Able to do 5 damage at range 15
        """
        if self.get_walk() < 5 and i.get_jump() < 5:
            return False

        batt_f = BattleForce(self, i)
        if batt_f.get_armor() < 3:
            return False

        if i.gear.weaponlist.count_damage(15) < 5:
            return False

        return True

    def is_scout(self, i):
        """
        Check if a mech is a scout

        Definition:
        - Speed at least walk 6 or jump 6
        """
        if self.get_walk() < 6 and i.get_jump() < 6:
            return False

        return True

    def is_brawler(self, i):
        """
        Check if a mech is a brawler

        Definition:
        - Speed at least walk 4 or jump 4
        - BF armor at least 4
        - Able to do 10 damage at range 15
        - Do more damage at range 15 than range 18
        """
        if self.get_walk() < 4 and i.get_jump() < 4:
            return False

        batt_f = BattleForce(self, i)
        if batt_f.get_armor() < 4:
            return False

        dam15 = i.gear.weaponlist.count_damage(15)
        if dam15 < 10:
            return False

        if i.gear.weaponlist.count_damage(18) >= dam15:
            return False

        return True

    def calculate_cost(self, i):
        """
        Calculate the cost of a mech
        """

        # Structural costs
        cost = 0
        # Cockpit
        cost += self.cockpit.get_cost()
        # Life support
        cost += 50000
        # Sensors
        cost += 2000 * self.weight
        # Musculature. Handle TSM cost here instead of in enhancement
        if self.enhancement.is_tsm():
            cost += 16000 * self.weight
        # Primitive mech
        elif self.engine.etype == "Primitive Fusion Engine":
            cost += 1000 * self.weight
        else:
            cost += 2000 * self.weight
        # Internal structure
        cost += self.structure.get_cost()

        # Acutuators
        if self.motive == "Biped":  # Arms
            cost += 2 * 100 * self.weight  # Upper arms
            if i.left_arm == "TRUE":
                cost += 50 * self.weight
            if i.right_arm == "TRUE":
                cost += 50 * self.weight
            if i.left_hand == "TRUE":
                cost += 80 * self.weight
            if i.right_hand == "TRUE":
                cost += 80 * self.weight
        elif self.motive == "Quad":  # Front legs
            cost += 2 * 150 * self.weight  # Upper legs
            cost += 2 * 80 * self.weight  # Lower legs
            cost += 2 * 120 * self.weight  # Feet

        # Legs/Rear legs
        cost += 2 * 150 * self.weight  # Upper legs
        cost += 2 * 80 * self.weight  # Lower legs
        cost += 2 * 120 * self.weight  # Feet

        # Engine
        cost += self.engine.get_cost()
        # Gyro
        cost += self.gyro.get_cost()
        # Jump Jets
        cost += i.jjets.get_cost()
        # MASC
        cost += self.enhancement.get_cost()
        # Heat Sinks
        cost += i.heatsinks.get_cost()
        # Power Amplifiers
        cost += i.power_amp.get_cost()

        # Add Tracks here if/when implemented

        # Armor
        cost += self.armor.get_cost()

        # Partial Wing, jump boosters
        cost += i.partw.get_cost()
        cost += i.jumpb.get_cost()

        # Booby trap
        cost += i.btrap.get_cost()

        # Multi-slot stuff
        cost += self.multi.get_cost()

        # AES
        cost += i.aes_ra.get_cost()
        cost += i.aes_la.get_cost()

        # Hack: Armored components
        cost += len(i.arm_loc) * 150000

        # Hack: Turrets
        cost += i.gear.tur_weight * 10000

        # Gear
        cost += i.gear.get_cost()

        # Final calculation
        cost *= (1.0 + (self.weight / 100.0))
        if self.omni == "TRUE":
            cost *= 1.25

        return round(cost)
