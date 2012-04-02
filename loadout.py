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
Contains mech loadouts
"""

from math import ceil
from operator import itemgetter
from movement import JumpJets, JumpBoosters, PartialWing
from gear import Equip, Gear, Heatsinks
from util import gettext, get_child, get_child_data

class Load:
    """
    Parent class for omni loadouts
    """
    def __init__(self, load, weight, batt_val, partw, prod_era, equip):
        self.weight = weight # Save weight just in case
        self.artemis4 = load.attributes["fcsa4"].value
        self.artemis5 = load.attributes["fcsa5"].value
        self.apollo = load.attributes["fcsapollo"].value

        # Get source
        self.source = get_child_data(load, 'source')

        # Get Clan Case
        clanc = get_child_data(load, 'clancase')

        self.batt_val = batt_val
        # Set to zero things that might not get defined otherwise
        self.heatsinks = Heatsinks(None)
        self.jjets = JumpJets(None, weight)
        self.partw = PartialWing(weight, partw)

        # Get Actuator Enhancement System
        self.aes_ra = False
        self.aes_la = False
        for aes in load.getElementsByTagName('arm_aes'):
            if aes.attributes["location"].value == "LA":
                self.aes_la = True
            elif aes.attributes["location"].value == "RA":
                self.aes_ra = True

        # Get jump booster
        jumpb = 0
        for jbo in load.getElementsByTagName('jumpbooster'):
            jumpb = int(jbo.attributes["mp"].value)

        self.jumpb = JumpBoosters(weight, jumpb)

        # Get Armored locations
        arm_loc = []
        for arm in load.getElementsByTagName('armored_locations'):
            for loc in arm.getElementsByTagName('location'):
                index = int(loc.attributes["index"].value)
                location = gettext(loc.childNodes)
                print "Armored: ", location, index
                arm_loc += [location, index]

        self.prod_era = prod_era

        self.gear = Gear(weight, self.artemis4, self.artemis5, self.apollo,
                         equip, clanc)


    def get_name(self):
        """
        Return the name of the Loadout, if any
        """
        raise NotImplementedError

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
        return int(sink)

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

    def get_move_heat(self, mech):
        """
        Get maximum heat produced by movement.
        """
        run_heat = 2
        if (mech.engine.etype == "XXL Engine"):
            run_heat = 6

        move_heat = max(run_heat, self.jjets.get_heat(mech))
        return move_heat

    def off_bv(self, mech, printq):
        """
        Get offensive weapon and ammo BV
        """
        obv = 0.0
        bwbr = 0.0
        heat = 0
        ammo_bv = 0.0

        heat_eff = 6 + self.get_sink() - self.get_move_heat(mech)
        if (printq):
            print "Heat Efficiency", heat_eff

        # Check for weapon BV flip
        flip = self.gear.check_weapon_bv_flip()

        w_list = []
        # Weapons
        for weap in self.gear.weaponlist.list:
            if weap.count > 0:
                i = weap.count
                la = weap.count_la
                ra = weap.count_ra
                if (flip and (i - weap.count_la - weap.count_ra > 0)):
                    batt_val = weap.get_bv(self.gear.tarcomp) / 2.0
                else:
                    batt_val = weap.get_bv(self.gear.tarcomp)
                # Handle AES
                if (la > 0 and self.aes_la):
                    batt_val *= 1.5
                    la -= 1
                elif (ra > 0 and self.aes_ra):
                    batt_val *= 1.5
                    ra -= 1
                while (i):
                    w_list.append((batt_val, weap.get_heat(), weap.name))
                    i -= 1

            # Rear-facing weapons counts as half
            if weap.countrear > 0:
                i = weap.countrear
                if (flip):
                    batt_val = weap.get_bv(self.gear.tarcomp)
                else:
                    batt_val = weap.get_bv(self.gear.tarcomp) / 2.0
                while (i):
                    w_list.append((batt_val, weap.get_heat(), weap.name))
                    i -= 1

            # Count possible Ammo BV
            ammo_bv += weap.get_ammo_bv()

        # Physical weapons
        for weap in self.gear.physicallist.list:
            if weap.count > 0:
                i = weap.count
                la = weap.count_la
                ra = weap.count_ra
                batt_val = weap.get_bv()
                # Handle AES
                if (la > 0 and self.aes_la):
                    batt_val *= 1.5
                    la -= 1
                elif (ra > 0 and self.aes_ra):
                    batt_val *= 1.5
                    ra -= 1
                while (i):
                    w_list.append((batt_val, weap.heat, weap.name))
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
                if (printq):
                    print "Over-heat"
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

class Baseloadout(Load):
    """
    An base omni loadout
    """
    def __init__(self, load, weight, batt_val, partw, prod_era):

        # Get equipment
        self.equip = []

        for node in load.getElementsByTagName('equipment'):
            self.equip.append(Equip(node))

        Load.__init__(self, load, weight, batt_val, partw, prod_era,
                      self.equip)

        # Get jumpjets, needs for loop
        self.jjets = JumpJets(None, self.weight)
        for jets in load.getElementsByTagName('jumpjets'):
            self.jjets = JumpJets(jets, self.weight)

        # Get heat sinks
        self.heatsinks = Heatsinks(get_child(load, 'heatsinks'))

    def get_name(self):
        """
        Return empty string for name
        """
        return ""

class Loadout(Load):
    """
    An omni loadout
    """
    def __init__(self, load, base, weight, partw):
        self.name = load.attributes["name"].value

        # Get production era
        prod_era = int(get_child_data(load, 'loadout_productionera'))

        # Get BV.
        batt_val = int(get_child_data(load, 'battle_value'))

        # Get equipment
        self.equip = list(base.equip)

        for node in load.getElementsByTagName('equipment'):
            self.equip.append(Equip(node))

        Load.__init__(self, load, weight, batt_val, partw, prod_era,
                      self.equip)
        # These needs to be set after call to Load

        # Use base config heatsinks if not overriden
        self.heatsinks = base.heatsinks
        # Use base config jump-jets if not overriden
        self.jjets = base.jjets

        # Get jumpjets
        for jets in load.getElementsByTagName('jumpjets'):
            self.jjets = JumpJets(jets, self.weight)

        # Get heat sinks
        for heat in load.getElementsByTagName('heatsinks'):
            self.heatsinks = Heatsinks(heat)

    def get_name(self):
        """
        Return configuration name
        """
        return self.name

