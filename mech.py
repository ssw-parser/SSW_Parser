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



from xml.dom import minidom
from math import ceil, pow
from operator import itemgetter
from error import *
from defensive import *
from movement import *
from gear import *

# Get a text node data
def gettext(nodes):
    for node in nodes:
        if node.nodeType == node.TEXT_NODE:
            return node.data  

# An omni loadout

class Loadout:
    def __init__(self, weight, a4, a5, ap, name, BV, partw, jumpb, prod_era, source):
        self.weight = weight # Save weight just in case
        self.artemis4 = a4
        self.artemis5 = a5
        self.apollo = ap
        self.name = name
        self.BV = BV
        # Set to zero things that might not get defined otherwise
        self.heatsinks = Heatsinks("Single Heat Sink", "2", 0)
        self.jj = JumpJets(weight, 0, "")
        self.partw = partw
        self.jumpb = jumpb
        self.prod_era = prod_era
        self.source = source

    # Get heatsinking capability
    def get_sink(self):
        sink = self.heatsinks.get_sink()
        # coolant pods
        if self.gear.coolant > 0:
            cool = ceil(self.heatsinks.nr * (float(self.gear.coolant) / 5.0))
            if cool > (self.heatsinks.nr * 2):
                cool = self.heatsinks.nr * 2
            sink += cool
        # Partial Wing
        if self.partw:
            sink += 3
        return sink

    # Get production era
    def get_prod_era(self):
        return self.prod_era


    # Get max jumping range
    def get_jump(self):
        # Ordinary jump-jets
        jmp = self.jj.get_jump()
        # Handle partial wing
        if jmp and self.partw:
            if self.weight >= 60:
                jmp += 1
            else:
                jmp += 2
        # Mechanical jump boosters
        jump = max(jmp, self.jumpb)
        return jump

    # Get offensive weapon and ammo BV
    def off_BV(self, mech, printq):
        oBV = 0.0
        BWBR = 0.0
        heat = 0
        ammo_BV = 0.0

        run_heat = 2
        if (mech.engine.etype == "XXL Engine"):
            run_heat = 6

        move_heat = max(run_heat, self.jj.get_heat(mech))
        heat_eff = 6 + self.get_sink() - move_heat
        if (printq):
            print "Heat Efficiency", heat_eff

        # Check for weapon BV flip
        flip = self.gear.check_weapon_BV_flip()

        w_list = []
        # Weapons
        for w in self.gear.weaponlist.list:
            if w.count > 0:
                i = w.count
                if (flip and (i - w.countarm > 0)):
                    BV = w.get_BV(self.gear.tarcomp, self.artemis4, self.artemis5, self.apollo) / 2.0
                else:
                    BV = w.get_BV(self.gear.tarcomp, self.artemis4, self.artemis5, self.apollo)

                while (i):
                    w_list.append((BV, w.heat, w.name))
                    i -= 1

            # Rear-facing weapons counts as half
            if w.countrear > 0:
                i = w.countrear
                if (flip):
                    BV = w.get_BV(self.gear.tarcomp, self.artemis4, self.artemis5, self.apollo)
                else:
                    BV = w.get_BV(self.gear.tarcomp, self.artemis4, self.artemis5, self.apollo) / 2.0
                while (i):
                    w_list.append((BV, w.heat, w.name))
                    i -= 1

            # Count possible Ammo BV
            ammo_BV += w.get_ammo_BV()

        # Physical weapons
        for w in self.gear.physicallist.list:
            if w.count > 0:
                i = w.count
                BV = w.get_BV(self.weight)
                while (i):
                    w_list.append((BV, 0, w.name))
                    i -= 1

        # Sort list, from largest BV to smallest,
        # and from lowest heat to highest
        w_list.sort(key=itemgetter(1)) # secondary by heat
        w_list.sort(key=itemgetter(0), reverse=True) # primary by BV

        # Calculate weapon BV
        over = 0
        for i in w_list:
            if (over > 0 and i[1] > 0):
                BWBR += i[0] / 2.0
                heat += i[1]
            else:
                BWBR += i[0]
                heat += i[1]
            # We have to much heat, halve future weapon BV
            if heat >= heat_eff:
                over = 1
            if (printq):
                print i
        if (printq):
            print "BWBR", BWBR
        oBV = BWBR

        # Ammo & TODO: other non-heat gear
        oBV += ammo_BV
        if (printq):
            print "Ammo BV: ", ammo_BV

        return oBV



# A mech class with data read from SSW xml data for use in various
# applications.

class Mech:
    def __init__(self, xmldoc):

        # Set some data to zero that sometimes will not get set otherwise
        jump = 0
        jjtype = ""
        enhancement = "---"
        etb = 2
        self.multi = []
 
        # Get top-level stucture data
        for mmech in xmldoc.getElementsByTagName('mech'):
            self.model = mmech.attributes["model"].value
            self.name = mmech.attributes["name"].value
            self.omni = mmech.attributes["omnimech"].value
            self.weight = int(mmech.attributes["tons"].value)

            # Get BV. Should give prime variant BV for Omni-mechs
            # get first instance only to avoid problems with Omni-mechs
            battv = mmech.getElementsByTagName('battle_value')[0]
            self.BV = int(gettext(battv.childNodes))

            # Get production era
            pe = mmech.getElementsByTagName('productionera')[0]
            self.prod_era = int(gettext(pe.childNodes))

            # Get mech type (battle, industrial)
            for mt in mmech.getElementsByTagName('mech_type'):
                self.mechtype = gettext(mt.childNodes)

            # Get techbase (IS, Clan)
            # get first instance only to avoid problems with Omni-mechs
            tb = mmech.getElementsByTagName('techbase')[0]
            self.techbase = gettext(tb.childNodes)

            # Get motive type (biped, quad)
            for mt in mmech.getElementsByTagName('motive_type'):
                self.motive = gettext(mt.childNodes)

            # Get internal structure type
            for stru in mmech.getElementsByTagName('structure'):
                sbase = int(stru.attributes["techbase"].value)
                snode = stru.getElementsByTagName("type")[0]
                stype = gettext(snode.childNodes)
                self.structure = IS(stype, sbase, self.weight, self.motive)
           
            # Get engine data
            for eng in mmech.getElementsByTagName('engine'):
                erating = int(eng.attributes["rating"].value)
                ebase = int(eng.attributes["techbase"].value)
                etype = gettext(eng.childNodes)

            # Get gyro
            for gy in mmech.getElementsByTagName('gyro'):
                gtype = gettext(gy.childNodes)
                gbase = int(gy.attributes["techbase"].value)

            # Get cockpit
            for cpt in mmech.getElementsByTagName('cockpit'):
                cnode = cpt.getElementsByTagName("type")[0]
                console = cnode.attributes["commandconsole"].value
                cockpit = gettext(cnode.childNodes)
                self.cockpit = Cockpit(cockpit, console)

            # Get enhancement
            for enh in mmech.getElementsByTagName('enhancement'):
                enode = enh.getElementsByTagName("type")[0]
                enhancement = gettext(enode.childNodes)
                etb = int(enh.attributes["techbase"].value)

            # Get armor.
            for arm in mmech.getElementsByTagName('armor'):
                atbase = arm.attributes["techbase"].value
                anode = arm.getElementsByTagName("type")[0]
                armortype = gettext(anode.childNodes)
                anode = arm.getElementsByTagName("hd")[0]
                hd = int(gettext(anode.childNodes))
                anode = arm.getElementsByTagName("ct")[0]
                ct = int(gettext(anode.childNodes))
                anode = arm.getElementsByTagName("ctr")[0]
                ctr = int(gettext(anode.childNodes))
                anode = arm.getElementsByTagName("lt")[0]
                lt = int(gettext(anode.childNodes))
                anode = arm.getElementsByTagName("ltr")[0]
                ltr = int(gettext(anode.childNodes))
                anode = arm.getElementsByTagName("rt")[0]
                rt = int(gettext(anode.childNodes))
                anode = arm.getElementsByTagName("rtr")[0]
                rtr = int(gettext(anode.childNodes))
                anode = arm.getElementsByTagName("la")[0]
                la = int(gettext(anode.childNodes))
                anode = arm.getElementsByTagName("ra")[0]
                ra = int(gettext(anode.childNodes))
                anode = arm.getElementsByTagName("ll")[0]
                ll = int(gettext(anode.childNodes))
                anode = arm.getElementsByTagName("rl")[0]
                rl = int(gettext(anode.childNodes))
                self.armor = Armor(self.weight, self.motive, armortype, atbase,
                                   hd, ct, ctr, lt, ltr, rt, rtr, la, ra, ll, rl)

            # Get baseloadout
            for blo in mmech.getElementsByTagName('baseloadout'):
                a4 = blo.attributes["fcsa4"].value
                a5 = blo.attributes["fcsa5"].value
                ap = blo.attributes["fcsapollo"].value
                partw = False
                jumpb = 0

                # Get source
                sr = blo.getElementsByTagName('source')[0]
                source = gettext(sr.childNodes)

                # Get Clan Case
                for cc in blo.getElementsByTagName('clancase'):
                    cc = gettext(cc.childNodes)

                # Get jumpjets
                for jj in blo.getElementsByTagName('jumpjets'):
                    jump = int(jj.attributes["number"].value)
                    jnode = jj.getElementsByTagName("type")[0]
                    jjtype = gettext(jnode.childNodes)

                # Get heat sinks
                for hs in blo.getElementsByTagName('heatsinks'):
                    heatsinks = int(hs.attributes["number"].value)
                    hsbase = hs.attributes["techbase"].value
                    hnode = hs.getElementsByTagName("type")[0]
                    hstype = gettext(hnode.childNodes)

                # Get multi-slot stuff
                for mlts in blo.getElementsByTagName('multislot'):
                    slot = mlts.attributes["name"].value
                    self.multi.append(slot)

                # Get partial wing
                for pw in blo.getElementsByTagName('partialwing'):
                    partw = True

                # Get jump booster
                for jb in blo.getElementsByTagName('jumpbooster'):
                    jumpb = int(jb.attributes["mp"].value)
                    
                # Get equipment
                equip = []
                equiprear = []

                for node in blo.getElementsByTagName('equipment'):
                    nnode = node.getElementsByTagName("name")[0]
                    name = gettext(nnode.childNodes)
                    tnode = node.getElementsByTagName("type")[0]
                    typ = gettext(tnode.childNodes)
                    l = node.getElementsByTagName("location")
                    # Normal case, no split
                    if (l):
                        lnode = l[0]
                        loc = gettext(lnode.childNodes)
                    # Split location
                    else:
                        loc = []
                        l = node.getElementsByTagName("splitlocation")
                        for lnode in l:
                            lnr = int(lnode.attributes["number"].value)
                            loc_temp = gettext(lnode.childNodes)
                            loc.append((loc_temp, lnr))
                    # Check for rear-mounted stuff
                    if name[0:4] == "(R) ":
                        equiprear.append((name[4:],typ,loc))
                   # Hack -- also check for turreted
                    elif name[0:4] == "(T) ":
                         equip.append((name[4:],typ,loc))
                    else:
                        # Save in a tuple with name and type
                        equip.append((name,typ,loc))

            self.engine = Motive(self.weight, etype, erating, ebase, gtype, gbase, enhancement, etb)

            # Construct current loadout, empty name for base loadout
            self.load = Loadout(self.weight, a4, a5, ap, "", self.BV, partw, jumpb, self.prod_era, source)
            self.load.gear = Gear(self.weight, a4, a5, ap, equip, equiprear, cc)
            self.load.heatsinks = Heatsinks(hstype, hsbase, heatsinks)
            self.load.jj = JumpJets(self.weight, jump, jjtype)

            # Get omni loadouts
            self.loads = []
            for lo in mmech.getElementsByTagName('loadout'):
                a4 = lo.attributes["fcsa4"].value
                a5 = lo.attributes["fcsa5"].value
                ap = lo.attributes["fcsapollo"].value
                name = lo.attributes["name"].value

                # Get source
                sr = lo.getElementsByTagName('source')[0]
                source = gettext(sr.childNodes)

                # Get production era
                pe = lo.getElementsByTagName('loadout_productionera')[0]
                prod_era = int(gettext(pe.childNodes))

                # Get BV.
                for battv in lo.getElementsByTagName('battle_value'):
                    BV = int(gettext(battv.childNodes))

                # Get jump booster
                for jb in blo.getElementsByTagName('jumpbooster'):
                    jumpb = int(hs.attributes["mp"].value)
                    
                # Construct current loadout
                current = Loadout(self.weight, a4, a5, ap, name, BV, partw, jumpb, prod_era, source)
                # Use base config heatsinks if not overriden
                current.heatsinks = self.load.heatsinks
                # Use base config jump-jets if not overriden
                current.jj = self.load.jj

                # Get Clan Case
                for cc in blo.getElementsByTagName('clancase'):
                    cc = gettext(cc.childNodes)

                # Get jumpjets
                for jj in lo.getElementsByTagName('jumpjets'):
                    jump = int(jj.attributes["number"].value)
                    jnode = jj.getElementsByTagName("type")[0]
                    jjtype = gettext(jnode.childNodes)
                    current.jj = JumpJets(self.weight, jump, jjtype)

                # Get heat sinks
                for hs in lo.getElementsByTagName('heatsinks'):
                    heatsinks = int(hs.attributes["number"].value)
                    hsbase = hs.attributes["techbase"].value
                    hnode = hs.getElementsByTagName("type")[0]
                    hstype = gettext(hnode.childNodes)
                    current.heatsinks = Heatsinks(hstype, hsbase, heatsinks)
                    
                # Get equipment
                equip_l = list(equip)
                equiprear_l = list(equiprear)

                for node in lo.getElementsByTagName('equipment'):
                    nnode = node.getElementsByTagName("name")[0]
                    name = gettext(nnode.childNodes)
                    tnode = node.getElementsByTagName("type")[0]
                    typ = gettext(tnode.childNodes)
                    l = node.getElementsByTagName("location")
                    # Normal case, no split
                    if (l):
                        lnode = l[0]
                        loc = gettext(lnode.childNodes)
                    # Split location
                    else:
                        loc = []
                        l = node.getElementsByTagName("splitlocation")
                        for lnode in l:
                            lnr = int(lnode.attributes["number"].value)
                            loc_temp = gettext(lnode.childNodes)
                            loc.append((loc_temp, lnr))
                    # Check for rear-mounted stuff
                    if name[0:4] == "(R) ":
                        equiprear_l.append((name[4:],typ,loc))
                    # Hack -- also check for turreted
                    elif name[0:4] == "(T) ":
                         equip_l.append((name[4:],typ,loc))
                    else:
                        # Save in a tuple with name and type
                        equip_l.append((name,typ,loc))

                current.gear = Gear(self.weight, a4, a5, ap, equip_l, equiprear_l, cc)

                self.loads.append(current)
                

    # Get walk speed
    def get_walk(self):
        return self.engine.speed

    # Get standard running speed, with no modifiers
    def get_run(self):
        spd = self.engine.speed
        factor = 1.5
        rspeed = int(ceil(spd * factor))
        return rspeed

    # Get maximum running speed
    def get_max_run(self):
        spd = self.engine.speed
        factor = 1.5
        if self.engine.enhancement == "TSM":
            spd += 1
        elif self.engine.enhancement == "MASC":
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



    # Get target modifier from movement, see Total Warfare for details
    def get_move_target_modifier(self, load):
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

    # Get defensive BV
    def def_BV(self, load, printq):
        dBV = 0.0
        # Armor
        cur = self.armor.get_armor_BV()
        dBV += cur
        if (printq):
            print "Armor Def BV: ", cur
        # Internal
        cur = self.structure.get_BV_factor() * self.engine.get_engine_BVmod()
        dBV += cur
        if (printq):
            print "Internal Def BV: ", cur
        # Gyro
        cur = self.weight * self.engine.get_gyro_BVmod()
        dBV += cur
        if (printq):
            print "Gyro Def BV: ", cur
        # Defensive equipment
        cur = load.gear.get_def_BV()
        dBV += cur
        if (printq):
            print "Equipment Def BV: ", cur
        # Explosive
        cur = load.gear.get_ammo_exp_BV(self.engine)
        dBV += cur
        if (printq):
            print "Explosive Ammo BV: ", cur
        cur = load.gear.get_weapon_exp_BV(self.engine)
        dBV += cur
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
        df = 1.0 + (mtm / 10.0)
        if (printq):
            print "Target modifier: ", mtm
            print "Defensive Faction: ", df

        # Final result
        dBV *= df
        if (printq):
            print "Defensive BV: ", dBV
        return dBV


    # Get offensive BV
    def off_BV(self, load, printq):
        oBV = load.off_BV(self, printq)

        # Tonnage (physical)
        if (self.engine.enhancement == "TSM"):
            wf = self.weight * 1.5
        else:
            wf = self.weight
        if (printq):
            print "Weight BV: ", wf
        oBV += wf

        # total
        if (printq):
            print "Total Base Offensive: ", oBV

        # speed factor
        sf = self.get_max_run() + ceil(load.get_jump() / 2.0)
        if (printq):
            print "Speed Factor: ", sf
        asf = ((sf - 5.0) / 10.0) + 1.0 
        osf = round(pow(asf, 1.2), 2)
        if (printq):
            print "Offensive Speed Factor: ", osf

        # Final result
        oBV *= osf
        if (printq):
            print "Offensive BV: ", oBV
        return oBV

    def get_BV(self, load):
        Base_BV = self.off_BV(load, False) + self.def_BV(load, False)
        if self.cockpit.type == "Small Cockpit":
            BV = int(round(Base_BV * 0.95))
        else:
            BV = int(round(Base_BV))
        if BV != load.BV:
            print self.name, self.model, load.name, BV, load.BV
        assert BV == load.BV, "Error in BV calculation!"
        return BV

    def weight_summary(self, short):
        # Motive stuff
        motive = self.engine.get_engine_weight()
        motive += self.engine.get_gyro_weight()
        motive += self.load.jj.get_weight()
        motive += self.engine.get_enh_weight()
        motive += self.cockpit.get_weight()
        if self.load.gear.supercharger:
            motive += ceil_05(self.engine.get_engine_weight() * 0.1)
        mratio = float(motive) / float(self.weight) * 100
        m2 = mratio - 33.3
        m3 = "   "
        if (m2 > 0):
            m3 = "M:" + str(int(m2))

        # Defensive stuff
        defensive = self.structure.get_weight()
        defensive += self.armor.get_weight()
        defensive += self.load.gear.get_d_weight()
        dratio = float(defensive) / float(self.weight) * 100
        d2 = dratio - 33.3
        d3 = "   "
        if (d2 > 0):
            d3 = "D:" + str(int(d2))

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
        # Command console
        offensive += self.cockpit.get_c_weight()
        oratio = float(offensive) / float(self.weight) * 100
        o2 = oratio - 33.3
        o3 = "   "
        if (o2 > 0):
            o3 = "O:" + str(int(o2))

        # leftover
        left = self.weight - motive - defensive - offensive
        assert left >= 0.0, "Mech is overweight!"
        if (short):
            # Only show leftover if there is something to show
            if (left):
                return ("%2.1f%% %2.1f%% %2.1f%% Left: %3.1ft" % (mratio, dratio, oratio, left))
            else:
#                return ("%2.1f%% %2.1f%% %2.1f%%" % (mratio, dratio, oratio))
                return ("%s %s %s" % (m3, d3, o3))
        else:
            print ("Total weight    : %3.1ft" % (self.weight))
            print ("Motive weight   : %3.1ft %2.1f%%" % (motive, mratio))
            print ("Defensive weight: %3.1ft %2.1f%%" % (defensive, dratio))
            print ("Offensive weight: %3.1ft %2.1f%%" % (offensive, oratio))
            print ("Other           : %3.1ft" % (left))
            return


    def get_move_string(self):
        spd = self.engine.speed
        if self.engine.enhancement == "TSM":
            wstr = str(spd) + "[" + str(spd + 1) + "]"
        else:
            wstr = str(spd)
        rspeed = int(ceil(spd * 1.5))
        if self.engine.enhancement == "TSM":
            rspeed2 = int(ceil((spd + 1) * 1.5))
            rstr = str(rspeed) + "[" + str(rspeed2) + "]"
        elif self.engine.enhancement == "MASC":
            rspeed2 = int(ceil(spd * 2.0))
            rstr = str(rspeed) + "[" + str(rspeed2) + "]"
        else:
            rstr = str(rspeed)
        string = ("%s/%s/%d" % (wstr, rstr, self.load.get_jump()))
        return string

    def parse_speed(self, weight):
        spd = self.engine.speed
        # Bigger of ground speed and jump range
        speed = max((spd, self.load.get_jump()))
        # Light
        if (speed < 6 and weight < 40):
            st = ("WARNING: Mech is too slow for its weight class!")
            warnings.add((st,))
            print_warning((st,))
        # Medium
        elif (speed < 5 and weight < 60):
            st = "WARNING: Mech is too slow for its weight class!"
            warnings.add((st,))
            print_warning((st,))
        # Heavy
        elif (speed < 4 and weight < 80):
            st = "WARNING: Mech is too slow for its weight class!"
            warnings.add((st,))
            print_warning((st,))
        # Assault
        elif (speed < 3):
            st = "WARNING: Mech is too slow for its weight class!"
            warnings.add((st,))
            print_warning((st,))

    def print_engine_report(self, weight):
        eweight = self.engine.get_engine_weight()
        eratio = float(eweight) / float(weight)
        print "Engine: ", self.engine.etype, self.engine.erating, eweight, "tons", int(eratio * 100), "%"
        if (eratio > 0.4):
            st = "WARNING: Very heavy engine!"
            st2 = "  Mounting LFE or XLFE suggested."
            warnings.add((st, st2))
            print_warning((st, st2))
        print "Speed: " + self.get_move_string()
        self.parse_speed(weight)
        gweight = self.engine.get_gyro_weight()
        print self.engine.gtype, gweight, "tons"
        jweight = self.load.jj.get_weight()
        if self.load.get_jump() > 0:
            print "Fixed jump: ", self.load.get_jump(), self.load.jj.jjtype, jweight, "tons"
        enhweight = self.engine.get_enh_weight()
        print "Enhancement: ", self.engine.enhancement, enhweight, "tons"
        tweight = eweight + gweight + jweight + enhweight
        tratio = float(tweight) / float(weight)
        print "Total motive weight: ", tweight, "tons", int(tratio * 100), "%"

