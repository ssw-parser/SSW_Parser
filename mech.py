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
Contains the master class for a mech, and its loadouts
"""

from math import ceil
from operator import itemgetter
from error import *
from defensive import IS, Armor
from movement import Cockpit, JumpJets, JumpBoosters, PartialWing
from movement import Enhancement, Gyro, Engine
from gear import Gear, Heatsinks, Equip
from util import ceil_05, get_child, get_child_data

class Loadout:
    """
    An omni loadout
    """
    def __init__(self, load, weight, name, batt_val, partw, prod_era, equip):
        self.weight = weight # Save weight just in case
        self.artemis4 = load.attributes["fcsa4"].value
        self.artemis5 = load.attributes["fcsa5"].value
        self.apollo = load.attributes["fcsapollo"].value
        self.name = name

        # Get source
        self.source = get_child_data(load, 'source')

        # Get Clan Case
        clanc = get_child_data(load, 'clancase')

        self.batt_val = batt_val
        # Set to zero things that might not get defined otherwise
        self.heatsinks = Heatsinks(None)
        self.jjets = JumpJets(None, weight)
        self.partw = PartialWing(weight, partw)

        # Get jump booster
        jumpb = 0
        for jbo in load.getElementsByTagName('jumpbooster'):
            jumpb = int(jbo.attributes["mp"].value)

        self.jumpb = JumpBoosters(weight, jumpb)

        self.prod_era = prod_era

        self.gear = Gear(weight, self.artemis4, self.artemis5, self.apollo,
                         equip, clanc)



    def get_sink(self):
        """
        Get heatsinking capability
        """
        sink = self.heatsinks.get_sink()
        # coolant pods
        if self.gear.coolant > 0:
            cool = ceil(self.heatsinks.number *
                        (float(self.gear.coolant) / 5.0))
            if cool > (self.heatsinks.number * 2):
                cool = self.heatsinks.number * 2
            sink += cool
        # Partial Wing
        if self.partw.has_wing():
            sink += 3
        return sink

    def get_prod_era(self):
        """
        Get production era
        """
        return self.prod_era


    def get_jump(self):
        """
        Get max jumping range
        """
        # Ordinary jump-jets
        jmp = self.jjets.get_jump()
        # Handle partial wing
        if jmp and self.partw.has_wing():
            if self.weight >= 60:
                jmp += 1
            else:
                jmp += 2
        # Mechanical jump boosters
        jump = max(jmp, self.jumpb.get_jump())
        return jump

    def off_bv(self, mech, printq):
        """
        Get offensive weapon and ammo BV
        """
        obv = 0.0
        bwbr = 0.0
        heat = 0
        ammo_bv = 0.0

        run_heat = 2
        if (mech.engine.etype == "XXL Engine"):
            run_heat = 6

        move_heat = max(run_heat, self.jjets.get_heat(mech))
        heat_eff = 6 + self.get_sink() - move_heat
        if (printq):
            print "Heat Efficiency", heat_eff

        # Check for weapon BV flip
        flip = self.gear.check_weapon_bv_flip()

        w_list = []
        # Weapons
        for weap in self.gear.weaponlist.list:
            if weap.count > 0:
                i = weap.count
                if (flip and (i - weap.countarm > 0)):
                    batt_val = weap.get_bv(self.gear.tarcomp, self.artemis4,
                                     self.artemis5, self.apollo) / 2.0
                else:
                    batt_val = weap.get_bv(self.gear.tarcomp, self.artemis4,
                                     self.artemis5, self.apollo)

                while (i):
                    w_list.append((batt_val, weap.heat, weap.name))
                    i -= 1

            # Rear-facing weapons counts as half
            if weap.countrear > 0:
                i = weap.countrear
                if (flip):
                    batt_val = weap.get_bv(self.gear.tarcomp, self.artemis4,
                                     self.artemis5, self.apollo)
                else:
                    batt_val = weap.get_bv(self.gear.tarcomp, self.artemis4,
                                     self.artemis5, self.apollo) / 2.0
                while (i):
                    w_list.append((batt_val, weap.heat, weap.name))
                    i -= 1

            # Count possible Ammo BV
            ammo_bv += weap.get_ammo_bv()

        # Physical weapons
        for weap in self.gear.physicallist.list:
            if weap.count > 0:
                i = weap.count
                batt_val = weap.get_bv(self.weight)
                while (i):
                    w_list.append((batt_val, 0, weap.name))
                    i -= 1

        # Sort list, from largest BV to smallest,
        # and from lowest heat to highest
        w_list.sort(key=itemgetter(1)) # secondary by heat
        w_list.sort(key=itemgetter(0), reverse=True) # primary by BV

        # Calculate weapon BV
        over = 0
        for i in w_list:
            if (over > 0 and i[1] > 0):
                bwbr += i[0] / 2.0
                heat += i[1]
            else:
                bwbr += i[0]
                heat += i[1]
            # We have to much heat, halve future weapon BV
            if heat >= heat_eff:
                over = 1
            if (printq):
                print i
        if (printq):
            print "BWBR", bwbr
        obv = bwbr

        # Ammo & TODO: other non-heat gear
        obv += ammo_bv
        if (printq):
            print "Ammo BV: ", ammo_bv

        return obv



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

            # Get production era
            self.prod_era = int(get_child_data(mmech, 'productionera'))

            # Get mech type (battle, industrial)
            self.mechtype = get_child_data(mmech, 'mech_type')

            # Get techbase (IS, Clan)
            # get first instance only to avoid problems with Omni-mechs
            self.techbase = get_child_data(mmech, 'techbase')

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
            self.enhancement = Enhancement(None, self.weight)
            for enh in mmech.getElementsByTagName('enhancement'):
                self.enhancement = Enhancement(enh, self.weight)

            # Get armor.
            self.armor = Armor(get_child(mmech, 'armor'),
                               self.weight, self.motive)

            ### Loadout stuff starts here ###

            # Get baseloadout
            for blo in mmech.getElementsByTagName('baseloadout'):
                partw = False

                # Get jumpjets, needs for loop
                jjets = JumpJets(None, self.weight)
                for jets in blo.getElementsByTagName('jumpjets'):
                    jjets = JumpJets(jets, self.weight)

                # Get heat sinks
                heatsinks = Heatsinks(get_child(blo, 'heatsinks'))

                # Get multi-slot stuff
                for mlts in blo.getElementsByTagName('multislot'):
                    slot = mlts.attributes["name"].value
                    self.multi.append(slot)

                # Get partial wing
                for paw in blo.getElementsByTagName('partialwing'):
                    partw = True

                # Get equipment
                equip = []

                for node in blo.getElementsByTagName('equipment'):
                    equip.append(Equip(node))

            # Construct current loadout, empty name for base loadout
            self.load = Loadout(blo, self.weight, "", self.batt_val,
                                partw, self.prod_era, equip)
            self.load.heatsinks = heatsinks
            self.load.jjets = jjets

            # Get omni loadouts
            self.loads = []
            for load in mmech.getElementsByTagName('loadout'):
                name = load.attributes["name"].value

                # Get production era
                prod_era = int(get_child_data(load, 'loadout_productionera'))

                # Get BV.
                batt_val = int(get_child_data(load, 'battle_value'))

                # Get equipment
                equip_l = list(equip)

                for node in load.getElementsByTagName('equipment'):
                    equip_l.append(Equip(node))

                # Construct current loadout
                current = Loadout(load, self.weight, name, batt_val,
                                  partw, prod_era, equip_l)
                # Use base config heatsinks if not overriden
                current.heatsinks = self.load.heatsinks
                # Use base config jump-jets if not overriden
                current.jjets = self.load.jjets

                # Get jumpjets
                for jets in load.getElementsByTagName('jumpjets'):
                    current.jjets = JumpJets(jets, self.weight)

                # Get heat sinks
                for heat in load.getElementsByTagName('heatsinks'):
                    current.heatsinks = Heatsinks(heat)
                    
                self.loads.append(current)
                

    def get_walk(self):
        """
        Get walk speed
        """
        return self.engine.speed

    def get_run(self):
        """
        Get standard running speed, with no modifiers
        """
        spd = self.engine.speed
        factor = 1.5
        rspeed = int(ceil(spd * factor))
        return rspeed

    def get_max_run(self):
        """
        Get maximum running speed
        """
        spd = self.engine.speed
        factor = 1.5
        if self.enhancement.is_tsm():
            spd += 1
        elif self.enhancement.is_masc():
            factor += 0.5
        if self.load.gear.supercharger:
            factor += 0.5
        rspeed = int(ceil(spd * factor))
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
        cur = self.armor.get_armor_bv()
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
        dbv += cur
        if (printq):
            print "Gyro Def BV: ", cur
        # Defensive equipment
        cur = load.gear.get_def_bv()
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
        if (self.enhancement.is_tsm()):
            weight_factor = self.weight * 1.5
        else:
            weight_factor = self.weight
        if (printq):
            print "Weight BV: ", weight_factor
        obv += weight_factor

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
        if self.cockpit.type == "Small Cockpit":
            batt_val = int(round(base_bv * 0.95))
        else:
            batt_val = int(round(base_bv))
        if batt_val != load.batt_val:
            print self.name, self.model, load.name, batt_val, load.batt_val
        assert batt_val == load.batt_val, "Error in BV calculation!"
        return batt_val

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
        if self.load.gear.supercharger:
            motive += ceil_05(self.engine.get_weight() * 0.1)
        mratio = float(motive) / float(self.weight) * 100
        m_diff = mratio - 33.3
        m_str = "   "
        if (m_diff > 0):
            m_str = "M:" + str(int(m_diff))

        # Defensive stuff
        defensive = self.structure.get_weight()
        defensive += self.armor.get_weight()
        defensive += self.load.gear.get_d_weight()
        dratio = float(defensive) / float(self.weight) * 100
        d_diff = dratio - 33.3
        d_str = "   "
        if (d_diff > 0):
            d_str = "D:" + str(int(d_diff))

        # Offensive stuff
        # Heat sinks
        offensive = self.load.heatsinks.get_weight()
        # Weapons
        offensive += self.load.gear.get_w_weight()
        # Ammo
        offensive += self.load.gear.get_a_weight()
        # Offensive gear
        offensive += self.load.gear.get_o_weight()
        # Physical weapons
        offensive += self.load.gear.get_p_weight()
        oratio = float(offensive) / float(self.weight) * 100
        o_diff = oratio - 33.3
        o_str = "   "
        if (o_diff > 0):
            o_str = "O:" + str(int(o_diff))

        # leftover
        left = self.weight - motive - defensive - offensive
        assert left >= 0.0, "Mech is overweight!"
        if (short):
            # Only show leftover if there is something to show
            if (left):
                return ("%2.1f%% %2.1f%% %2.1f%% Left: %3.1ft" %
                        (mratio, dratio, oratio, left))
            else:
#                return ("%2.1f%% %2.1f%% %2.1f%%" % (mratio, dratio, oratio))
                return ("%s %s %s" % (m_str, d_str, o_str))
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
        spd = self.engine.speed
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

    def parse_speed(self, weight):
        """
        Check if a mech is too slow for its weight class
        """
        spd = self.engine.speed
        # Bigger of ground speed and jump range
        speed = max((spd, self.load.get_jump()))
        # Light
        if (speed < 6 and weight < 40):
            msg = ("WARNING: Mech is too slow for its weight class!")
            warnings.add((msg,))
            print_warning((msg,))
        # Medium
        elif (speed < 5 and weight < 60):
            msg = "WARNING: Mech is too slow for its weight class!"
            warnings.add((msg,))
            print_warning((msg,))
        # Heavy
        elif (speed < 4 and weight < 80):
            msg = "WARNING: Mech is too slow for its weight class!"
            warnings.add((msg,))
            print_warning((msg,))
        # Assault
        elif (speed < 3):
            msg = "WARNING: Mech is too slow for its weight class!"
            warnings.add((msg,))
            print_warning((msg,))

    def print_engine_report(self, weight):
        """
        Print out a report about the mech engine
        """
        eweight = self.engine.get_weight()
        eratio = float(eweight) / float(weight)
        print "Engine: ", self.engine.get_type(), self.engine.erating, eweight, "tons", int(eratio * 100), "%"
        if (eratio > 0.4):
            msg = "WARNING: Very heavy engine!"
            msg2 = "  Mounting LFE or XLFE suggested."
            warnings.add((msg, msg2))
            print_warning((msg, msg2))
        print "Speed: " + self.get_move_string()
        self.parse_speed(weight)
        gweight = self.gyro.get_weight()
        print self.gyro.summary_string()
        jweight = self.load.jjets.get_weight()
        if self.load.get_jump() > 0:
            print "Fixed jump: ", self.load.get_jump(), self.load.jjets.summary_string()
        enhweight = self.enhancement.get_weight()
        print "Enhancement: ", self.enhancement.summary_string()
        tweight = eweight + gweight + jweight + enhweight
        tratio = float(tweight) / float(weight)
        print "Total motive weight: ", tweight, "tons", int(tratio * 100), "%"

