#!/usr/bin/python

from xml.dom import minidom
from math import ceil, pow
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
    def __init__(self, weight, a4, a5, ap, name):
        self.weight = weight # Save weight just in case
        self.artemis4 = a4
        self.artemis5 = a5
        self.apollo = ap
        self.name = name
        # Set to zero things that might not get defined otherwise
        self.heatsinks = Heatsinks("Single Heat Sink", "2", 0)
        self.jj = JumpJets(weight, 0, "")


# A mech class with data read from SSW xml data for use in various
# applications.

class Mech:

    def __init__(self, xmldoc):

        # Set some data to zero that sometimes will not get set otherwise
        jump = 0
        jjtype = ""
        enhancement = "---"
        etb = 2
 
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

                # Get equipment
                equip = []
                equiprear = []

                for node in blo.getElementsByTagName('equipment'):
                    nnode = node.getElementsByTagName("name")[0]
                    name = gettext(nnode.childNodes)
                    tnode = node.getElementsByTagName("type")[0]
                    typ = gettext(tnode.childNodes)
                    # Check for rear-mounted stuff
                    if name[0:4] == "(R) ":
                        equiprear.append((name[4:],typ))
                    else:
                        # Save in a tuple with name and type
                        equip.append((name,typ))

            self.engine = Motive(self.weight, etype, erating, ebase, gtype, gbase, enhancement, etb)

            # Construct current loadout
            self.load = Loadout(self.weight, a4, a5, ap, "BASE")
            self.load.gear = Gear(self.weight, a4, equip, equiprear)
            self.load.heatsinks = Heatsinks(hstype, hsbase, heatsinks)
            self.load.jj = JumpJets(self.weight, jump, jjtype)

            # Get omni loadouts
            self.loads = []
            for lo in mmech.getElementsByTagName('loadout'):
                a4 = lo.attributes["fcsa4"].value
                a5 = lo.attributes["fcsa5"].value
                ap = lo.attributes["fcsapollo"].value
                name = lo.attributes["name"].value

                # Construct current loadout
                current = Loadout(self.weight, a4, a5, ap, name)
                # Use base config heatsinks if not overriden
                current.heatsinks = self.load.heatsinks
                # Use base config jump-jets if not overriden
                current.jj = self.load.jj

                # Get BV.
                for battv in lo.getElementsByTagName('battle_value'):
                    current.BV = int(gettext(battv.childNodes))

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
                equip = []
                equiprear = []

                for node in lo.getElementsByTagName('equipment'):
                    nnode = node.getElementsByTagName("name")[0]
                    name = gettext(nnode.childNodes)
                    tnode = node.getElementsByTagName("type")[0]
                    typ = gettext(tnode.childNodes)
                    lnode = node.getElementsByTagName("location")[0]
                    loc = gettext(lnode.childNodes)
                    # Check for rear-mounted stuff
                    if name[0:4] == "(R) ":
                        equiprear.append((name[4:],typ,loc))
                    else:
                        # Save in a tuple with name and type
                        equip.append((name,typ,loc))

                current.gear = Gear(self.weight, a4, equip, equiprear)


                self.loads.append(current)

    def get_move_target_modifier(self, load):
        run_speed = self.engine.get_max_run()
        jump_speed = load.jj.get_jump()

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
        # Explosive: TODO, requires location tracking

        # Defensive factor: TODO
        mtm = self.get_move_target_modifier(load)
        # Stealth armor adds to to-hit
        if self.armor.atype == "Stealth Armor":
            mtm += 2
        assert mtm >= 0, "Negative defensive modifier!"
        df = 1.0 + (mtm / 10.0)
        if (printq):
            print "Target modifier: ", mtm
            print "Defensive Faction: ", df

    def off_BV(self, load, printq):
        oBV = 0.0
        BWBR = 0.0
        heat = 0
        ammo_BV = 0.0

        move_heat = max(2, load.jj.get_heat())
        heat_eff = 6 + load.heatsinks.get_sink() - move_heat
        if (printq):
            print "Heat Efficiency", heat_eff

        w_list = []
        # Weapons
        for w in load.gear.weaponlist.list:
            if w.count > 0:
                i = w.count
                BV = w.get_BV(load.gear.tarcomp, load.artemis4)
                while (i):
                    w_list.append((BV, w.heat, w.name))
                    i -= 1

            if w.countrear > 0:
                i = w.count
                BV = w.get_BV(load.gear.tarcomp, load.artemis4) / 2.0
                while (i):
                    w_list.append((BV, w.heat, w.name))
                    i -= 1

            # Count possible Ammo BV
            ammo_BV += w.get_ammo_BV()

        # Physical weapons
        for w in load.gear.physicallist.list:
            if w.count > 0:
                i = w.count
                BV = w.get_BV(self.weight)
                while (i):
                    w_list.append((BV, 0, w.name))
                    i -= 1

        # Sort list, from largest BV to smallest
        w_list.sort()
        w_list.reverse()

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
        sf = self.engine.get_max_run() + ceil(load.jj.get_jump() / 2.0)
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

    def weight_summary(self, short):
        # Motive stuff
        motive = self.engine.get_engine_weight()
        motive += self.engine.get_gyro_weight()
        motive += self.load.jj.get_weight()
        motive += self.engine.get_enh_weight()
        motive += self.cockpit.get_weight()
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
        string = ("%s/%s/%d" % (wstr, rstr, self.load.jj.get_jump()))
        return string

    def parse_speed(self, weight):
        spd = self.engine.speed
        # Bigger of ground speed and jump range
        speed = max((spd, self.load.jj.get_jump()))
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
        if self.load.jj.get_jump() > 0:
            print "Fixed jump: ", self.load.jj.get_jump(), self.load.jj.jjtype, jweight, "tons"
        enhweight = self.engine.get_enh_weight()
        print "Enhancement: ", self.engine.enhancement, enhweight, "tons"
        tweight = eweight + gweight + jweight + enhweight
        tratio = float(tweight) / float(weight)
        print "Total motive weight: ", tweight, "tons", int(tratio * 100), "%"

