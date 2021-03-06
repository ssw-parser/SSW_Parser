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
loadout.py
==========
Contains mech loadouts
"""

from math import ceil
from operator import itemgetter
from jump import JumpJets, JumpBoosters, PartialWing
from gear import Equip, Gear, Heatsinks
from util import ceil_05, gettext, get_child, get_child_data, year_era_test
from item import Item
from error import error_exit


class BoobyTrap(Item):
    """
    A class to hold information about booby traps
    """
    def __init__(self, mweight, booby):
        Item.__init__(self)
        self.weight = mweight  # Mech weight, not booby trap weight
        self.booby = booby  # Bool: Do we mount a booby trap

    def get_type(self):
        """
        Return booby trap
        """
        return "Booby Trap"

    def get_rules_level(self):
        """
        Booby traps are advanced rules
        """
        if self.booby:
            return 2
        else:
            return 0

    def get_weight(self):
        """
        Get weight of booby trap
        """
        if self.booby:
            return ceil_05(0.1 * self.weight)
        else:
            return 0

    def get_cost(self):
        """
        Get cost of booby trap
        """
        if self.booby:
            return  100000
        else:
            return 0

#    def has_booby_trap(self):
#        """
#        Return true if we have a booby trap
#        """
#        return self.booby


class AES(Item):
    """
    A class to hold information about actuator enhancement system
    """
    def __init__(self, mweight, motive, typ):
        Item.__init__(self)
        self.weight = mweight  # Mech weight, not booby trap weight
        self.motive = motive
        self.type = typ

    def get_type(self):
        """
        Return AES
        """
        return "AES"

    def get_rules_level(self):
        """
        AES is experimental rules
        """
        if self.type == "None":
            return 0
        else:
            return 3

    def get_weight(self):
        """
        Get weight of AES
        """
        if self.type == "None":
            return 0.0

        if self.motive == "Quad":
            return ceil_05(self.weight / 50.0)
        elif self.motive == "Biped":
            return ceil_05(self.weight / 35.0)
        else:
            error_exit(self.motive)

    def get_cost(self):
        """
        Get cost of AES
        """
        if self.type == "Arm":
            return self.weight * 500
        elif self.type == "Leg":
            return self.weight * 700
        else:
            return 0


class PowerAmp(Item):
    """
    Power Amplifiers

    Check if needed at creation, and if not set en_weight to zero.
    """
    def __init__(self, load, ene_weight):
        Item.__init__(self)
        self.load = load  # Reference to parent
        self.ene_weight = ene_weight

    def get_type(self):
        """
        Return Power Amplifiers
        """
        if self.ene_weight > 0.0:
            return "Power Amplifiers"
        else:
            return ""

    def get_rules_level(self):
        """
        Return power amplifier rules level
        0 = intro, 1 = tournament legal, 2 = advanced, 3 = experimental
        """
        if self.ene_weight > 0.0:
            return 1
        else:
            return 0

    def get_weight(self):
        """
        Return power amplifier weight
        """
        if self.ene_weight > 0.0:
            return ceil_05(self.ene_weight * 0.1)
        else:
            return 0.0

    def get_cost(self):
        """
        Return power amplifier cost
        """
        return self.get_weight() * 20000


class Load:
    """
    Parent class for omni loadouts
    """
    def __init__(self, load, mech, batt_val, prod_era, equip, cost):
        self.weight = mech.weight  # Save weight just in case
        self.artemis4 = load.attributes["fcsa4"].value
        self.artemis5 = load.attributes["fcsa5"].value
        self.apollo = load.attributes["fcsapollo"].value
        self.cost = cost
        self.unit = mech  # Reference to parent

        # Create a container for special abilities
        # ES, SEAL, SOA, SRCH is always available for mechs
        # Combat Vehicles gets SRCH
        if mech.type == "BM":
            self.specials = {"ES": 1, "SEAL": 1, "SOA": 1, "SRCH": 1}
        elif mech.type == "CV":
            self.specials = {"SRCH": 1}

        # Get source
        self.source = get_child_data(load, 'source')

        # Get Clan CASE
        # Note that there is currently a bug in combat vehicles regarding
        # Clan CASE.
        if mech.type == "BM":
            clanc = get_child_data(load, 'clancase')
        else:
            clanc = "FALSE"

        # Get actuator status
        for act in load.getElementsByTagName('actuators'):
            self.left_hand = act.attributes["lh"].value
            self.left_arm = act.attributes["lla"].value
            self.right_hand = act.attributes["rh"].value
            self.right_arm = act.attributes["rla"].value

        self.batt_val = batt_val
        # Set to zero things that might not get defined otherwise
        self.heatsinks = Heatsinks(None, self)
        self.jjets = JumpJets(None, mech.weight)
        self.partw = PartialWing(mech.weight, False, 2)

        # Assume not mixed tech
        self.mixed = False
        for rll in load.getElementsByTagName('techbase'):
            if gettext(rll.childNodes) == "Mixed":
                self.mixed = True

        # Get Actuator Enhancement System
        self.aes_ra = AES(mech.weight, mech.motive, "None")
        self.aes_la = AES(mech.weight, mech.motive, "None")
        for aes in load.getElementsByTagName('arm_aes'):
            if aes.attributes["location"].value == "LA":
                self.aes_la = AES(mech.weight, mech.motive, "Arm")
            elif aes.attributes["location"].value == "RA":
                self.aes_ra = AES(mech.weight, mech.motive, "Arm")

        # Get jump booster
        jumpb = 0
        for jbo in load.getElementsByTagName('jumpbooster'):
            jumpb = int(jbo.attributes["mp"].value)

        self.jumpb = JumpBoosters(mech.weight, jumpb)

        # Get Armored locations
        self.arm_loc = []
        self.arm_gyro = False
        self.armored = False
        for arm in load.getElementsByTagName('armored_locations'):
            for loc in arm.getElementsByTagName('location'):
                index = int(loc.attributes["index"].value)
                location = gettext(loc.childNodes)
                self.arm_loc.append((location, index))
                self.armored = True
                # Armored Gyro
                if location == "CT" and index == 3:
                    self.arm_gyro = True

        self.prod_era = prod_era

        # Get booby trap
        booby = False
        for bob in load.getElementsByTagName('boobytrap'):
            booby = True
        self.btrap = BoobyTrap(mech.weight, booby)

        # Hack: Get turret
        self.turret = False
        for tur in load.getElementsByTagName('turret'):
            self.turret = True

        self.gear = Gear(mech, self.artemis4, self.artemis5, self.apollo,
                         equip, clanc)

        # Add Power Amplifiers
        if (self.unit.engine.etype == "I.C.E. Engine" or
            self.unit.engine.etype == "No Engine"):
            self.power_amp = PowerAmp(self, self.gear.weaponlist.ene_weight)
        else:
            self.power_amp = PowerAmp(self, 0.0)

        self.build_special()

    def build_special(self):
        """
        Add special abilities to list
        """
        # Scan equipment
        for equip in self.gear.equiplist.list:
            if (equip.count > 0 and equip.name == "C3 Computer (Master)"):
                self.specials["C3M"] = equip.count
                self.specials["TAG"] = 1
            if (equip.count > 0 and
                equip.name == "C3 Boosted Computer (Master)"):
                self.specials["C3BSM"] = equip.count
                self.specials["TAG"] = 1
            if (equip.count > 0 and equip.name == "Improved C3 Computer"):
                self.specials["C3I"] = 1
            if (equip.count > 0 and equip.name == "C3 Computer (Slave)"):
                self.specials["C3S"] = 1
            if (equip.count > 0 and
                equip.name == "C3 Boosted Computer (Slave)"):
                self.specials["C3BSS"] = 1
            if (equip.count > 0 and equip.name == "TAG"):
                self.specials["TAG"] = 1
            if (equip.count > 0 and equip.name == "Light TAG"):
                self.specials["LTAG"] = 1
            if (equip.count > 0 and equip.name == "Watchdog CEWS"):
                self.specials["WAT"] = 1
            if (equip.count > 0 and
                (equip.name == "Guardian ECM Suite" or
                 equip.name == "ECM Suite" or
                 equip.name == "Electronic Warfare Equipment")):
                self.specials["ECM"] = 1
            if (equip.count > 0 and equip.name == "Angel ECM"):
                self.specials["AECM"] = 1
            if (equip.count > 0 and equip.name == "Bloodhound Active Probe"):
                self.specials["BH"] = 1
                self.specials["RCN"] = 1
            if (equip.count > 0 and (equip.name == "Beagle Active Probe" or
                                     equip.name == "Active Probe")):
                self.specials["PRB"] = 1
                self.specials["RCN"] = 1
            if (equip.count > 0 and equip.name == "Light Active Probe"):
                self.specials["LPRB"] = 1
                self.specials["RCN"] = 1
            if (equip.count > 0 and equip.name == "Remote Sensor Dispenser"):
                self.specials["RSD"] = equip.count
                self.specials["RCN"] = 1
            if (equip.count > 0 and equip.name == "C3 Remote Sensor Launcher"):
                self.specials["C3RS"] = 1
            if (equip.count > 0 and
                (equip.name == "(IS) Anti-Missile System" or
                 equip.name == "(CL) Anti-Missile System" or
                 equip.name == "(IS) Laser Anti-Missile System" or
                 equip.name == "(CL) Laser Anti-Missile System")):
                self.specials["AMS"] = 1

        # Scan weapons
        for weap in self.gear.weaponlist.list.itervalues():
            if (weap.count > 0 and (weap.name == "(IS) Narc Missile Beacon" or
                                    weap.name == "(CL) Narc Missile Beacon")):
                self.specials["SNARC"] = weap.count
            if (weap.count > 0 and (weap.name == "(IS) iNarc Launcher")):
                self.specials["INARC"] = weap.count
            if (weap.count > 0 and weap.name == "(IS) BattleMech Taser"):
                self.specials["MTAS"] = weap.count
            if (weap.count > 0 and weap.name == "(IS) Arrow IV Missile"):
                self.specials["ARTAIS"] = weap.count
            if (weap.count > 0 and weap.name == "(CL) Arrow IV Missile"):
                self.specials["ARTAC"] = weap.count
            if (weap.count > 0 and weap.name == "(IS) Sniper"):
                self.specials["ARTS"] = weap.count
            # Is this one really correct? Does Artillery Cannons count?
            if (weap.count > 0 and weap.name == "Long Tom Artillery Cannon"):
                self.specials["ARTLTC"] = weap.count

    def get_name(self):
        """
        Return the name of the Loadout, if any
        """
        raise NotImplementedError

    def get_rules_level(self):
        """
        Return rules level of loadout
        """
        r_level = 0
        # Mixed Tech is advanced rules
        if self.mixed:
            r_level = 2
        r_level = max(r_level, self.gear.get_rules_level())
        r_level = max(r_level, self.heatsinks.get_rules_level())
        r_level = max(r_level, self.jjets.get_rules_level())
        r_level = max(r_level, self.partw.get_rules_level())
        r_level = max(r_level, self.jumpb.get_rules_level())
        r_level = max(r_level, self.btrap.get_rules_level())
        r_level = max(r_level, self.aes_ra.get_rules_level())
        r_level = max(r_level, self.aes_la.get_rules_level())
        r_level = max(r_level, self.power_amp.get_rules_level())

        # Hack: Armored location
        if self.armored == True and r_level < 2:
            r_level = 2

        return r_level

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

    def get_def_bv(self, mech):
        """
        Get defensive equipment BV
        """
        dbv = self.gear.get_def_bv()
        # Track things left
        arm_loc = self.arm_loc[:]
        # Deal with armored components
        for i in self.arm_loc:
            # Gyros, BV calculated elsewhere
            for j in mech.gyro.get_slots():
                if not cmp(i, j):
                    arm_loc.remove(i)
            # Engines
            for j in mech.engine.get_slots():
                if not cmp(i, j):
                    dbv += 5
                    arm_loc.remove(i)
            # Cockpits
            for j in mech.cockpit.get_slots():
                if not cmp(i, j):
                    dbv += 5
                    arm_loc.remove(i)
            # Actuators
            act_locations = [("LA", 0), ("LA", 1), ("RA", 0), ("RA", 1),
                             ("LL", 0), ("LL", 1), ("LL", 2), ("LL", 3),
                             ("RL", 0), ("RL", 1), ("RL", 2), ("RL", 3)]
            if self.left_arm == "TRUE":
                act_locations.append(("LA", 2))
            if self.left_hand == "TRUE":
                act_locations.append(("LA", 3))
            if self.right_arm == "TRUE":
                act_locations.append(("RA", 2))
            if self.right_hand == "TRUE":
                act_locations.append(("RA", 3))
            for j in act_locations:
                if not cmp(i, j):
                    dbv += 5
                    arm_loc.remove(i)
        if arm_loc:
            print "Unknown armored items left: ", arm_loc
            raise NotImplementedError
        return dbv

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
        for weap in self.gear.weaponlist.list.itervalues():
            if weap.count > 0:
                i = weap.count
                left_arm = weap.count_la
                right_arm = weap.count_ra
                if (flip and (i - weap.count_la - weap.count_ra -
                              weap.count_tur > 0)):
                    batt_val = weap.get_bv(self.gear.tarcomp) / 2.0
                else:
                    batt_val = weap.get_bv(self.gear.tarcomp)
                # Handle AES
                if (left_arm > 0 and self.aes_la.type == "Arm"):
                    batt_val *= 1.5
                    left_arm -= 1
                elif (right_arm > 0 and self.aes_ra.type == "Arm"):
                    batt_val *= 1.5
                    right_arm -= 1
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
            # Only offensive physical gear
            if (weap.count > 0 and weap.get_bv() > 0):
                i = weap.count
                left_arm = weap.count_la
                right_arm = weap.count_ra
                batt_val = weap.get_bv()
                # Handle AES
                if (left_arm > 0 and self.aes_la.type == "Arm"):
                    batt_val *= 1.5
                    left_arm -= 1
                elif (right_arm > 0 and self.aes_ra.type == "Arm"):
                    batt_val *= 1.5
                    right_arm -= 1
                while (i):
                    w_list.append((batt_val, weap.heat, weap.name))
                    i -= 1

        # Sort list, from largest BV to smallest,
        # and from lowest heat to highest
        w_list.sort(key=itemgetter(1))  # secondary by heat
        w_list.sort(key=itemgetter(0), reverse=True)  # primary by BV

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
            if heat >= heat_eff and mech.type != "CV":
                over = 1
            if (printq):
                print i
        if (printq):
            print "BWBR", bwbr
        obv = bwbr

        # Ammo
        obv += ammo_bv
        if (printq):
            print "Ammo BV: ", ammo_bv

        # Non-heat gear
        equip_bv = 0
        for equip in self.gear.equiplist.list:
            # Only offensive physical gear
            if (equip.count > 0 and equip.off_bv[0] > 0):
                bv_gear = equip.off_bv[0] * equip.count
                equip_bv += bv_gear
                # Handle C3 ammo (and possible other ammo)
                if (equip.off_bv[1] > 0 and equip.ammocount > 0):
                    bv_ammo = equip.off_bv[1] * equip.ammo_ton
                    # Disallow ammo BV to be greater than that of
                    # the system itself
                    if bv_ammo > bv_gear:
                        bv_ammo = bv_gear
                    equip_bv += bv_ammo

        obv += equip_bv
        if (printq):
            print "Equipment BV: ", equip_bv

        return obv


class Baseloadout(Load):
    """
    An base omni loadout
    """
    def __init__(self, load, mech, batt_val, prod_era, cost):

        # Save year
        self.year = mech.year

        # Get equipment
        self.equip = []

        for node in load.getElementsByTagName('equipment'):
            self.equip.append(Equip(node))

        Load.__init__(self, load, mech, batt_val, prod_era,
                      self.equip, cost)

        # Get jumpjets, needs for loop
        self.jjets = JumpJets(None, self.weight)
        for jets in load.getElementsByTagName('jumpjets'):
            self.jjets = JumpJets(jets, self.weight)

        # Get heat sinks
        self.heatsinks = Heatsinks(get_child(load, 'heatsinks'), self)

        # Get partial wing
        partw = False
        tech = 2
        for paw in load.getElementsByTagName('partialwing'):
            partw = True
            tech = int(paw.attributes["tech"].value)

        self.partw = PartialWing(mech.weight, partw, tech)

    def get_name(self):
        """
        Return empty string for name
        """
        return ""


class Loadout(Load):
    """
    An omni loadout
    """
    def __init__(self, load, base, mech):
        self.name = load.attributes["name"].value

        # Get production era
        prod_era = int(get_child_data(load, 'loadout_productionera'))

        # Get year
        self.year = int(get_child_data(load, 'loadout_year'))

        # Get BV.
        batt_val = int(get_child_data(load, 'battle_value'))

        # Get cost
        cost = float(get_child_data(load, 'cost'))

        # Sanity check for year
        year_era_test(self.year, prod_era,
                      mech.name + " " + mech.model + self.name)

        # Get equipment
        self.equip = list(base.equip)

        for node in load.getElementsByTagName('equipment'):
            self.equip.append(Equip(node))

        Load.__init__(self, load, mech, batt_val, prod_era,
                      self.equip, cost)
        # These needs to be set after call to Load

        # Use base config heatsinks if not overriden
        self.heatsinks = base.heatsinks
        # Use base config jump-jets if not overriden
        self.jjets = base.jjets
        # Use base config partial wing (no over-ride cannot be pod-mounted)
        self.partw = base.partw

        # Get jumpjets
        for jets in load.getElementsByTagName('jumpjets'):
            self.jjets = JumpJets(jets, self.weight)

        # Get heat sinks
        for heat in load.getElementsByTagName('heatsinks'):
            self.heatsinks = Heatsinks(heat, self)

    def get_name(self):
        """
        Return configuration name
        """
        return self.name
