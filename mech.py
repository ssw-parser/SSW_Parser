#!/usr/bin/python

from xml.dom import minidom
from defensive import *
from movement import *

# Get a text node data
def gettext(nodes):
    for node in nodes:
        if node.nodeType == node.TEXT_NODE:
            return node.data  

# An omni loadout

class Loadout:
    def __init__(self, a4, a5, ap, name):
        self.artemis4 = a4
        self.artemis5 = a5
        self.apollo = ap
        self.name = name
        # Set to zero things that might not get defined otherwise
        self.heatsinks = 0
        self.jump = 0


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
                self.structure = IS(stype, sbase, self.weight)
           
            # Get engine data
            for eng in mmech.getElementsByTagName('engine'):
                erating = int(eng.attributes["rating"].value)
                ebase = int(eng.attributes["techbase"].value)
                etype = gettext(eng.childNodes)

            # Get gyro
            for gy in mmech.getElementsByTagName('gyro'):
                gtype = gettext(gy.childNodes)
                gbase = int(gy.attributes["techbase"].value)

            # Get cockpit, TODO: base
            for cpt in mmech.getElementsByTagName('cockpit'):
                cnode = cpt.getElementsByTagName("type")[0]
                self.console = cnode.attributes["commandconsole"].value
                self.cockpit = gettext(cnode.childNodes)

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
                self.artemis4 = blo.attributes["fcsa4"].value
                self.artemis5 = blo.attributes["fcsa5"].value
                self.apollo = blo.attributes["fcsapollo"].value

                # Get jumpjets
                for jj in blo.getElementsByTagName('jumpjets'):
                    jump = int(jj.attributes["number"].value)
                    jnode = jj.getElementsByTagName("type")[0]
                    jjtype = gettext(jnode.childNodes)

                # Get heat sinks
                for hs in blo.getElementsByTagName('heatsinks'):
                    self.heatsinks = int(hs.attributes["number"].value)
                    hnode = hs.getElementsByTagName("type")[0]
                    self.hstype = gettext(hnode.childNodes)
                    
                # Get equipment
                self.equip = []
                self.equiprear = []

                for node in blo.getElementsByTagName('equipment'):
                    nnode = node.getElementsByTagName("name")[0]
                    name = gettext(nnode.childNodes)
                    tnode = node.getElementsByTagName("type")[0]
                    typ = gettext(tnode.childNodes)
                    # Check for rear-mounted stuff
                    if name[0:4] == "(R) ":
                        self.equiprear.append((name[4:],typ))
                    else:
                        # Save in a tuple with name and type
                        self.equip.append((name,typ))

            self.engine = Motive(self.weight, etype, erating, ebase, gtype, gbase, jump, jjtype, enhancement, etb)

            # Get omni loadouts
            self.loads = []
            for lo in mmech.getElementsByTagName('loadout'):
                a4 = lo.attributes["fcsa4"].value
                a5 = lo.attributes["fcsa5"].value
                ap = lo.attributes["fcsapollo"].value
                name = lo.attributes["name"].value

                # Construct current loadout
                current = Loadout(a4, a5, ap, name)

                # Get BV.
                for battv in lo.getElementsByTagName('battle_value'):
                    current.BV = int(gettext(battv.childNodes))

                # Get jumpjets
                for jj in lo.getElementsByTagName('jumpjets'):
                    current.jump = int(jj.attributes["number"].value)
                    jnode = jj.getElementsByTagName("type")[0]
                    current.jjtype = gettext(jnode.childNodes)

                # Get heat sinks
                for hs in lo.getElementsByTagName('heatsinks'):
                    current.heatsinks = int(hs.attributes["number"].value)
                    hnode = hs.getElementsByTagName("type")[0]
                    current.hstype = gettext(hnode.childNodes)
                    
                # Get equipment
                current.equip = []
                current.equiprear = []

                for node in lo.getElementsByTagName('equipment'):
                    nnode = node.getElementsByTagName("name")[0]
                    name = gettext(nnode.childNodes)
                    tnode = node.getElementsByTagName("type")[0]
                    typ = gettext(tnode.childNodes)
                    # Check for rear-mounted stuff
                    if name[0:4] == "(R) ":
                        current.equiprear.append((name[4:],typ))
                    else:
                        # Save in a tuple with name and type
                        current.equip.append((name,typ))


                self.loads.append(current)


