#!/usr/bin/python

# Analyze and print out some data about a mech.
# Takes a SSW file as argument.
# Uses external file mech.py to read in data.

import sys
from xml.dom import minidom
from math import ceil
from mech import *
from gear import *
from defensive import *
from error import *
from movement import *

# Check for earliest year
def get_comp_year(call, date):
    year = call();
    if date < year:
        date = year
    return date

# Parse an equipment node
def parse_gear(mech, date):
    lbv = 0
    mbv = 0
    sbv = 0
    lheat = 0
    mheat = 0

    # Deal with ammo issues
    for w in mech.gear.weaponlist.list:
        if ((w.count > 0 or w.countrear > 0) and w.useammo > 0):
            # Sum up weapons
            total = w.count + w.countrear
            ammo = w.ammocount
            ApW = float(ammo) / float(total * w.useammo)
            if (ApW < 15.0):
                st1 = "WARNING: Ammo supply low!"
                st2 = "  Weapon: " + str(w.name)
                st3 = "  Ammo Supply: " + str(ApW)
                warnings.add((st1, st2, st3))
                print_warning((st1, st2, st3))
            elif (ApW > 50.0):
                st1 = "WARNING: Ammo supply high!"
                st2 = "  Weapon: " + str(w.name)
                st3 = "  Ammo Supply: " + str(ApW)
                warnings.add((st1, st2, st3))
                print_warning((st1, st2, st3))
    for e in mech.gear.d_equiplist.list:
        if (e.count > 0 and e.useammo > 0):
            # Sum up weapons
            total = e.count
            ammo = e.ammocount
            ApW = float(ammo) / float(total * e.useammo)
            if (ApW < 15.0):
                st1 = "WARNING: Ammo supply low!"
                st2 = "  Weapon: " + str(e.name)
                st3 = "  Ammo Supply: " + str(ApW)
                warnings.add((st1, st2, st3))
                print_warning((st1, st2, st3))
            elif (ApW > 50.0):
                st1 = "WARNING: Ammo supply high!"
                st2 = "  Weapon: " + str(e.name)
                st3 = "  Ammo Supply: " + str(ApW)
                warnings.add((st1, st2, st3))
                print_warning((st1, st2, st3))

    # Print used weapons
    for w in mech.gear.weaponlist.list:
        if (w.count > 0 or w.countrear > 0):
            # Check for inefficient weapons
            if ((w.BV[0]/w.weight) < 10.0):
                st1 = "WARNING: Ineffient weapon mounted!"
                st2 = "  Weapon: " + w.name
                warnings.add((st1, st2))
                print_warning((st1, st2))

            # calculate earliest date
            if date < w.year:
                date = w.year

            report = str(w.count)
            # If there is rear-mounted stuff, only list them, do not count for
            # evaluation
            if w.countrear > 0:
                report = report + ", " + str(w.countrear) + "(R) "
            report = report + " " + w.name
            print report
            # Get BV balance, also count heat
            if w.range == "L":
                lbv = lbv + w.count * w.get_BV(mech.gear.tarcomp, mech.artemis4, mech.artemis5, mech.apollo)
                lheat = lheat + w.count * w.heat
            elif w.range == "M":
                mbv = mbv + w.count * w.get_BV(mech.gear.tarcomp, mech.artemis4, mech.artemis5, mech.apollo)
                mheat = mheat + w.count * w.heat
            elif w.range == "S":
                sbv = sbv + w.count * w.get_BV(mech.gear.tarcomp, mech.artemis4, mech.artemis5, mech.apollo)

    # Print used equipment
    for e in mech.gear.o_equiplist.list:
        if e.count > 0:
            # calculate earliest date
            if date < e.year:
                date = e.year

            report = str(e.count)
            report = report + " " + e.name
            print report

    for e in mech.gear.d_equiplist.list:
        if e.count > 0:
            # calculate earliest date
            if date < e.year:
                date = e.year

            report = str(e.count)
            report = report + " " + e.name
            print report


    # Print used physicals
    for p in mech.gear.physicallist.list:
        if p.count > 0:
            # calculate earliest date
            if date < p.year:
                date = p.year

            report = str(p.count)
            report = report + " " + p.name
            dam = p.dam(mech.weight)
            print report
            print p.name, "Damage", dam, "Weight", mech.gear.get_p_weight()
            sbv = sbv + p.count * dam * p.BVmult

    # Check TSM & physical combo
#    if (mech.gear.phys == 1 and mech.engine.enhancement != "TSM"):
#        st1 = "WARNING: Physical weapon mounted without TSM!"
#        warnings.add((st1,))
#        print_warning((st1,))
#    elif (mech.gear.phys == 0 and mech.engine.enhancement == "TSM"):
#        st1 = "WARNING: TSM mounted without Physical weapon!"
#        warnings.add((st1,))
#        print_warning((st1,))


    # Explosive ammo
    for i in mech.gear.exp_ammo.keys():
        print "Explosive: ", i, mech.gear.exp_ammo[i]

    # Check heat
    hbal = lheat - mech.heatsinks.get_sink()
    if (hbal > 4):
        st1 = "WARNING: Long range weapons overheats a lot!"
        st2 = "  Overheat: " + str(hbal)
        warnings.add((st1, st2))
        print_warning((st1, st2))
    hbal = mheat - mech.heatsinks.get_sink()
    if (hbal > 4):
        st1 = "WARNING: Medium range weapons overheats a lot!"
        st2 = "  Overheat: " + str(hbal)
        warnings.add((st1, st2))
        print_warning((st1, st2))
        

    print "LR BV: ", lbv
    print "MR BV: ", mbv
    print "SR BV: ", sbv

    if lbv >= (mbv + sbv):
        return ("Long-Range", date)
    else:
        return ("Short-Range", date)


# HACK: Handle this better
def parse_artemis(mech, date):
    if mech.load.artemis4 == "TRUE":
        if date < 2598:
            date = 2598
    # HACK: We class artemis V as unknown for now
    if mech.load.artemis5 == "TRUE":
        error_exit("fire_control")
    if mech.load.apollo == "TRUE":
        if date < 3071:
            date = 3071
    return date

# Handle omni-mechs
def parse_omni(mech, date):
    if mech.omni == "TRUE":
        print "-----------------"
        print "Omni Loadouts"
        for i in mech.loads:
            d = date
            print "-----------------"
            print "Config: ", i.name
            print "BV: ", i.BV
            if (i.jj.get_jump()):
                d = get_comp_year(i.jj.get_year, d)
                print "Jump: ", i.jj.get_jump(), i.jj.jjtype
            if (i.heatsinks.nr):
                d = get_comp_year(mech.heatsinks.get_year, d)
                print i.heatsinks.nr, i.heatsinks.type
            d = parse_artemis(mech, d)
            if i.artemis4 == "TRUE":
                print "Artemis IV"
            if i.apollo == "TRUE":
                print "Apollo"
            (rnge, d) = parse_gear(i, d)
            print "Earliest Year: ", d
        print "-----------------"


# Read file
fsock = open(sys.argv[1])
xmldoc = minidom.parse(fsock)
fsock.close()

# Print raw info for debugging 
print xmldoc.toxml() 
print "===BREAK==="

# Get mech
mech = Mech(xmldoc)
# Count earliest year here
date = 0

print "Name: ", mech.model, mech.name
mech.weight_summary(False)

print "-1-----------------------------"
print "Tech: ", mech.techbase
print "Weight: ", mech.weight
print "Motive: ", mech.motive, mech.mechtype
if (mech.omni == "TRUE"):
    print "Omni mech"
date = get_comp_year(mech.structure.get_year, date)
print "Structure: ", mech.structure.type, mech.structure.get_weight(), "tons"
print "-2-----------------------------"
mech.print_engine_report(mech.weight)
date = get_comp_year(mech.engine.get_engine_year, date)
date = get_comp_year(mech.engine.get_gyro_year, date)
if mech.load.jj.get_jump() > 0:
    date = get_comp_year(mech.load.jj.get_year, date)
date = get_comp_year(mech.cockpit.get_year, date)
print mech.cockpit.type, mech.cockpit.get_weight()
if mech.cockpit.console == "TRUE":
    print "Command Console"
date = get_comp_year(mech.engine.get_enh_year, date)
print "-3-----------------------------"
date = get_comp_year(mech.load.heatsinks.get_year, date)
print mech.load.heatsinks.type, mech.load.heatsinks.nr
print "-4-----------------------------"
date = get_comp_year(mech.armor.get_year, date)
#speed = mech.engine.erating/mech.weight
#if (speed == 3 and mech.weight < 80):
#    wgt = 80
#    print "Entering pocket assault mode!"
#elif (speed == 4 and mech.weight < 60):
#    wgt = 60
#    print "Entering pocket heavy mode!"
#elif (speed == 5 and mech.weight < 40):
#    wgt = 40
#    print "Entering pocket medium mode!"
#else:
#    wgt = mech.weight
wgt = mech.weight
mech.armor.parse_armor()
print "-5-----------------------------"
if (mech.omni == "TRUE"):
    print "WARNING: Omni mech, results might be garbage."
#    sys.exit(1)

# Check for Artemis IV, Apollo
# TODO: Move to parse_gear
date = parse_artemis(mech, date)
if mech.load.artemis4 == "TRUE":
    print "Artemis IV"
if mech.load.apollo == "TRUE":
    print "Apollo"
print "==============================="
mech.def_BV(mech.load, True)
print "-------------------------------"
mech.off_BV(mech.load, True)
print "-------------------------------"
print "BV: ", mech.BV
print ("BV/ton: %.2f" % (float(mech.BV)/float(mech.weight)))
print "==============================="

# Gear
(rnge, date) = parse_gear(mech.load, date)

# Figure out best speed
speed = mech.engine.erating/mech.weight
if mech.load.jj.get_jump() > speed:
    mspd = mech.load.jj.get_jump()
else:
    mspd = speed

# Print classification
print mspd, rnge

# Print time-period
print "Earliest Year: ", date

parse_omni(mech, date)
warnings.print_warnings()
