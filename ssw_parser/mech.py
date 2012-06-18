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
Contains the master class for a mech
"""

import sys
from math import ceil
from defensive import IS, Armor
from movement import Cockpit, Enhancement, Gyro, Engine
from util import ceil_05, get_child, get_child_data
from loadout import Baseloadout, Loadout
from battle_force import BattleForce

# A mech class with data read from SSW xml data for use in various
# applications.

class Mech:
    """
    A master class holding info about a mech.
    """
    def __init__(self, xmldoc):

        # Set some data to zero that sometimes will not get set otherwise
        self.multi = []
 
        # Get top-level stucture data
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
            self.structure = IS(get_child(mmech, 'structure'),
                                self.weight, self.motive)
           
            # Get engine data
            self.engine = Engine(get_child(mmech, 'engine'), self.weight)

            # Get gyro
            self.gyro = Gyro(get_child(mmech, 'gyro'),
                             self.engine.etype, self.engine.erating)

            # Get cockpit
            self.cockpit = Cockpit(get_child(mmech, 'cockpit'))

            # Get enhancement, needs for loop
            self.enhancement = Enhancement(None, self.weight,
                                           self.engine.erating)
            for enh in mmech.getElementsByTagName('enhancement'):
                self.enhancement = Enhancement(enh, self.weight,
                                               self.engine.erating)

            # Get armor.
            self.armor = Armor(get_child(mmech, 'armor'),
                               self.weight, self.motive)

            ### Loadout stuff starts here ###

            # Get baseloadout
            blo = mmech.getElementsByTagName('baseloadout')[0]
            partw = False

            # Get multi-slot stuff
            for mlts in blo.getElementsByTagName('multislot'):
                slot = mlts.attributes["name"].value
                self.multi.append(slot)

            # Get partial wing
            for paw in blo.getElementsByTagName('partialwing'):
                partw = True

            # Construct current loadout, empty name for base loadout
            self.load = Baseloadout(blo, self, self.batt_val,
                                    partw, self.prod_era, cost)

            # HACK -- Apply modular armor
            if self.load.gear.has_mod_armor:
                self.armor.apply_modular(self.load.gear.mod_armor)

            # Get omni loadouts
            self.loads = []
            for load in mmech.getElementsByTagName('loadout'):
 
                # Construct current loadout
                current = Loadout(load, self.load, self, partw)

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
#        rspeed = int(ceil(spd * 1.5))
#        if self.engine.enhancement == "TSM":
#            rspeed = int(ceil((spd + 1) * 1.5))
#        elif self.engine.enhancement == "MASC":
#            rspeed = int(ceil(spd * 2.0))
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

        j_mod += 1

        return max(j_mod, r_mod)

    def get_stealth(self):
        """
        Returns true if the mech mounts a stealth system
        """
        stlth = False
        for i in self.multi:
            if i == "Chameleon LPS":
                stlth = True
            elif i == "Null Signature System":
                stlth = True
            elif i == "Void Signature System":
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
        for i in self.multi:
            if i == "Chameleon LPS":
                mtm += 2
            elif i == "Null Signature System":
                mtm += 2
            elif i == "Void Signature System":
                mtm += 3
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
        if (self.load.aes_ra):
            weight_factor += 0.1
        if (self.load.aes_la):
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
        Get the BV a specific loadout. Use mech.load if not an omni.
        """
        base_bv = self.off_bv(load, False) + self.def_bv(load, False)
        if (self.cockpit.type == "Small Cockpit" or
            self.cockpit.type == "Torso-Mounted Cockpit"):
            batt_val = int(round(base_bv * 0.95))
        else:
            batt_val = int(round(base_bv))
        if batt_val != load.batt_val:
            print self.name, self.model, load.get_name(), batt_val, load.batt_val
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


    def weight_summary(self, short):
        """
        Create a report on what the mech spends its tonnage on
        """
        # Motive stuff
        motive = self.engine.get_weight()
        motive += self.gyro.get_weight()
        motive += self.load.jjets.get_weight()
        motive += self.enhancement.get_weight()
        motive += self.cockpit.get_weight()
        if self.load.gear.supercharger.has_sc():
            motive += ceil_05(self.engine.get_weight() * 0.1)
        mratio = float(motive) / float(self.weight) * 100

        # Defensive stuff
        defensive = self.structure.get_weight()
        defensive += self.armor.get_weight()
        dratio = float(defensive) / float(self.weight) * 100

        # Offensive stuff
        # Heat sinks
        offensive = self.load.heatsinks.get_weight()
        # Weapons
        offensive += self.load.gear.get_w_weight()
        # Ammo
        offensive += self.load.gear.get_a_weight()
        # Offensive gear
        offensive += self.load.gear.get_e_weight()
        # Physical weapons
        offensive += self.load.gear.get_p_weight()
        oratio = float(offensive) / float(self.weight) * 100

        # leftover
        left = self.weight - motive - defensive - offensive
        assert left >= 0.0, "Mech is overweight!"
        if (short):
            # Only show leftover if there is something to show
            if (left):
                return ("%2.1f%% %2.1f%% %2.1f%% Left: %3.1ft" %
                        (mratio, dratio, oratio, left))
            else:
                return ("%2.1f%% %2.1f%% %2.1f%%" % (mratio, dratio, oratio))
        else:
            print ("Total weight    : %3.1ft" % (self.weight))
            print ("Motive weight   : %3.1ft %2.1f%%" % (motive, mratio))
            print ("Defensive weight: %3.1ft %2.1f%%" % (defensive, dratio))
            print ("Offensive weight: %3.1ft %2.1f%%" % (offensive, oratio))
            print ("Other           : %3.1ft" % (left))
            return


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

    def print_engine_report(self):
        """
        Print out a report about the mech engine
        """
        eweight = self.engine.get_weight()
        print "Engine:     ", self.engine.summary_string()
        print "Speed:      ", self.get_move_string()
        gweight = self.gyro.get_weight()
        print "Gyro:       ", self.gyro.summary_string()
        jweight = self.load.jjets.get_weight()
        if self.load.get_jump() > 0:
            print "Fixed jump: ", self.load.jjets.summary_string()
        enhweight = self.enhancement.get_weight()
        if enhweight > 0:
            print "Enhancement:", self.enhancement.summary_string()
        tweight = eweight + gweight + jweight + enhweight
        print "Total motive weight: ", tweight, "tons"
        print "Cockpit:    ", self.cockpit.summary_string()

    def parse_armor(self):
        """
        Parse the armor of a mech.
        """
        # Standard armor report
        self.armor.parse_armor()
        # Battle force armor
        batt_f = BattleForce(self, self.load)
        print "BF Armor: ", batt_f.get_armor()


    def get_rules_level(self, load):
        """
        Return rules level of mech
        """
        r_level = 0
        # Mixed tech is advanced rules
        if self.techbase == "Mixed":
            r_level = 2
        tmp = self.structure.get_rules_level()
        if tmp > r_level:
            r_level = tmp
        tmp = self.engine.get_rules_level()
        if tmp > r_level:
            r_level = tmp
        tmp = self.gyro.get_rules_level()
        if tmp > r_level:
            r_level = tmp
        tmp = self.cockpit.get_rules_level()
        if tmp > r_level:
            r_level = tmp
        tmp = self.enhancement.get_rules_level()
        if tmp > r_level:
            r_level = tmp
        tmp = self.armor.get_rules_level()
        if tmp > r_level:
            r_level = tmp
        # Hack -- multi-slot
        for i in self.multi:
            if i == "Chameleon LPS":
                tmp = 3
            elif i == "Null Signature System":
                tmp = 3
            elif i == "Void Signature System":
                tmp = 2
            if tmp > r_level:
                r_level = tmp

        tmp = load.get_rules_level()
        if tmp > r_level:
            r_level = tmp

        return r_level

    ### Mech type tests ###

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
        if self.motive == "Biped": # Arms
            cost += 2 * 100 * self.weight # Upper arms
            if i.left_arm == "TRUE":
                cost += 50 * self.weight
            if i.right_arm == "TRUE":
                cost += 50 * self.weight
            if i.left_hand == "TRUE":
                cost += 80 * self.weight
            if i.right_hand == "TRUE":
                cost += 80 * self.weight
        elif self.motive == "Quad": # Front legs
            cost += 2 * 150 * self.weight # Upper legs
            cost += 2 * 80 * self.weight # Lower legs
            cost += 2 * 120 * self.weight # Feet

        # Legs/Rear legs
        cost += 2 * 150 * self.weight # Upper legs
        cost += 2 * 80 * self.weight # Lower legs
        cost += 2 * 120 * self.weight # Feet

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
        # Add Power Amplifiers here if/when implemented

        # Add Tracks here if/when implemented

        # Armor
        cost += self.armor.get_cost()

        # Partial Wing, jump boosters
        cost += i.partw.get_cost()
        cost += i.jumpb.get_cost()

        # Booby trap
        cost += i.btrap.get_cost()

        # Multi-slot stuff
        for m in self.multi:
            if m == "Chameleon LPS":
                cost += 600000
            elif m == "Null Signature System":
                cost += 1400000
            elif m == "Void Signature System":
                cost += 2000000

        # Hack: AES
        if i.aes_ra:
            cost += self.weight * 500
        if i.aes_la:
            cost += self.weight * 500

        # Hack: Armored components
        cost += len(i.arm_loc) * 150000

        # Gear
        cost += i.gear.get_cost()

        # Final calculation
        cost *= (1.0 + (self.weight / 100.0))
        if self.omni == "TRUE":
            cost *= 1.25

        return round(cost)
