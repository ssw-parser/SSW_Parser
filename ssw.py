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

# Parse a component list
def parse_comp(mechitem, clist, date):
    id = 0
    for i in clist.list:
        if mechitem == i.name:
            if date < i.year:
                date = i.year
            id = 1
    if id == 0:
        error_exit(clist.name)
    return date

# Check for earliest year
def get_comp_year(call, date):
    year = call();
    if date < year:
        date = year
    return date

# Parse a component list
#def parse_gyroBV(gyro, clist):
#    id = 0
#    gyBV = 0
#    for i in clist.list:
#        if gyro == i.name:
#            gyBV = i.BVmult
#            id = 1
#    if id == 0:
#        error_exit(clist.name)
#    return gyBV

# Parse a component list
def parse_structBV(struct, clist):
    id = 0
    stBV = 0
    for i in clist.list:
        if struct == i.name:
            stBV = i.BVmult
            id = 1
    if id == 0:
        error_exit(clist.name)
    return stBV

# Parse a component list
#def parse_engBV(engine, clist):
#    id = 0
#    enBV = 0
#    for i in clist.list:
#        if engine == i.name:
#            enBV = i.BVmult
#            id = 1
#    if id == 0:
#        error_exit(clist.name)
#    return enBV

# Parse an equipment node
def parse_gear(mech, date):
    lbv = 0
    mbv = 0
    sbv = 0
    lbf = 0
    mbf = 0
    sbf = 0
    lheat = 0
    mheat = 0
    # We need to create local lists for avoid trouble with Omni-mechs
    weaponlist = Weaponlist()
    equiplist = Equiplist()
    physicallist = Physicallist()
    ammolist = Ammolist()
    # Keep track of tarcomp
    tarcomp = 0
    # Mech has a physical weapon?
    phys = 0

    # Count gear
    for name in mech.equip:
        # Go through weapon list
        id = 0
        for w in weaponlist.list:
            if name[0] == w.name:
                w.addone()
                id = 1
        # Handle non-weapon equipment
        # HACK: Handle CASE, Tarcomp
        for e in equiplist.list:
            if (name[0] == e.name and 
                (name[1] == 'equipment' or name[1] == 'CASE' or
                 name[1] == 'TargetingComputer')):
                e.addone()
                id = 1
                # TODO: Clan tarcomp
                if (name[0] == "(IS) Targeting Computer" and name[1] =='TargetingComputer'):
                    tarcomp = 1
        for p in physicallist.list:
            if (name[0] == p.name and name[1] == 'physical'):
                p.addone()
                id = 1
                phys = 1
        for a in ammolist.list:
            if (name[0] == a.name and name[1] == 'ammunition'):
                a.addone()
                id = 1
        # Not found
        if id == 0:
            print "Unidentified:", name
            error_exit("gear")

    for name in mech.equiprear:
        # Go through weapon list
        id = 0
        for w in weaponlist.list:
            if name[0] == w.name:
                w.addone_rear()
                id = 1
        # Not found
        if (id == 0):
            print "Unidentified:", name
            error_exit("gear")

    # Add ammo to weapon
    for a in ammolist.list:
        if a.count > 0:
            id = 0
            for w in weaponlist.list:
                if w.name == a.wname:
                    w.add_ammo(a.count * a.amount)
                    id = 1
            # We need to do equipment also due to AMS
            for e in equiplist.list:
                if e.name == a.wname:
                    e.add_ammo(a.count * a.amount)
                    id = 1
            if (id == 0):
                print "ERROR: Unknown weapon:", a.wname
                error_exit("weapon")

    # Deal with ammo issues
    for w in weaponlist.list:
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
    for e in equiplist.list:
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
    for w in weaponlist.list:
        if (w.count > 0 or w.countrear > 0):
            # Check for inefficient weapons
            if ((w.BV/w.weight) < 10.0):
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
            # Get BV balance, Artemis first, then tarcomp, no enhancement last
            # Also count heat
            if (mech.artemis4 == "TRUE" and w.enhance == "A"):
                if w.range == "L":
                    lbv = lbv + w.count * w.BV * 1.2
                    lheat = lheat + w.count * w.BF[0]
                elif w.range == "M":
                    mbv = mbv + w.count * w.BV * 1.2
                    mheat = mheat + w.count * w.BF[0]
                elif w.range == "S":
                    sbv = sbv + w.count * w.BV * 1.2
            elif (tarcomp == 1 and w.enhance =="T"):
                if w.range == "L":
                    lbv = lbv + w.count * w.BV * 1.25
                    lheat = lheat + w.count * w.BF[0]
                elif w.range == "M":
                    mbv = mbv + w.count * w.BV * 1.25
                    mheat = mheat + w.count * w.BF[0]
                elif w.range == "S":
                    sbv = sbv + w.count * w.BV * 1.25
            else:
                if w.range == "L":
                    lbv = lbv + w.count * w.BV
                    lheat = lheat + w.count * w.BF[0]
                elif w.range == "M":
                    mbv = mbv + w.count * w.BV
                    mheat = mheat + w.count * w.BF[0]
                elif w.range == "S":
                    sbv = sbv + w.count * w.BV
            sbf = sbf + w.BF[1] * w.count
            mbf = mbf + w.BF[2] * w.count
            lbf = lbf + w.BF[3] * w.count

    # Print used equipment
    for e in equiplist.list:
        if e.count > 0:
            # calculate earliest date
            if date < e.year:
                date = e.year

            report = str(e.count)
            report = report + " " + e.name
            print report


    # Print used physicals
    for p in physicallist.list:
        if p.count > 0:
            # calculate earliest date
            if date < p.year:
                date = p.year

            report = str(p.count)
            report = report + " " + p.name
            dam = p.dam(mech.weight)
            print report
            print p.name, "Damage", dam
            sbv = sbv + p.count * dam * p.BVmult

    # Check TSM & physical combo
    if (phys == 1 and mech.engine.enhancement != "TSM"):
        st1 = "WARNING: Physical weapon mounted without TSM!"
        warnings.add((st1,))
        print_warning((st1,))
    elif (phys == 0 and mech.engine.enhancement == "TSM"):
        st1 = "WARNING: TSM mounted without Physical weapon!"
        warnings.add((st1,))
        print_warning((st1,))


    # Check heat
    if mech.hstype == "Single Heat Sink":
        hbal = lheat - mech.heatsinks
        if (hbal > 4):
            st1 = "WARNING: Long range weapons overheats a lot!"
            st2 = "  Overheat: " + str(hbal)
            warnings.add((st1, st2))
            print_warning((st1, st2))
        hbal = mheat - mech.heatsinks
        if (hbal > 4):
            st1 = "WARNING: Medium range weapons overheats a lot!"
            st2 = "  Overheat: " + str(hbal)
            warnings.add((st1, st2))
            print_warning((st1, st2))
    elif mech.hstype == "Double Heat Sink":
        hbal = lheat - 2 * mech.heatsinks
        if (hbal > 4):
            st1 = "WARNING: Long range weapons overheats a lot!"
            st2 = "  Overheat: " + str(hbal)
            warnings.add((st1, st2))
            print_warning((st1, st2))
        hbal = mheat - 2 * mech.heatsinks
        if (hbal > 4):
            st1 = "WARNING: Medium range weapons overheats a lot!"
            st2 = "  Overheat: " + str(hbal)
            warnings.add((st1, st2))
            print_warning((st1, st2))
    else:
        error_exit(mech.hstype)
        

    print "LR BV: ", lbv
    print "MR BV: ", mbv
    print "SR BV: ", sbv
    print "BF balance: ", sbf, mbf, lbf

    if lbv >= (mbv + sbv):
        return ("Long-Range", date)
    else:
        return ("Short-Range", date)


# HACK: Handle this better
def parse_artemis(mech, date):
    if mech.artemis4 == "TRUE":
        if date < 2598:
            date = 2598
    # HACK: We class artemis V as unknown for now
    if mech.artemis5 == "TRUE":
        error_exit("fire_control")
    if mech.apollo == "TRUE":
        if date < 3071:
            date = 3071
    return date

# Handle commando console
def parse_console(mech, date):
    if mech.console == "TRUE":
        if date < 2631:
            date = 2631
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
            if (i.jump):
                d = parse_comp(i.jjtype, jumpjetlist, d)
                print "Jump: ", i.jump, i.jjtype
            if (i.heatsinks):
                d = parse_comp(mech.hstype, heatsinklist, d)
                print i.heatsinks, i.hstype
            d = parse_artemis(mech, d)
            if i.artemis4 == "TRUE":
                print "Artemis IV"
            if i.apollo == "TRUE":
                print "Apollo"
            (rnge, d) = parse_gear(i, d)
            print "Earliest Year: ", d
        print "-----------------"


# initialize gearlist
heatsinklist = Heatsinklist()

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
mech.weight_summary()

print "-1-----------------------------"
print "Tech: ", mech.techbase
print "Weight: ", mech.weight
print "Motive: ", mech.motive, mech.mechtype
if (mech.omni == "TRUE"):
    print "Omni mech"
date = get_comp_year(mech.structure.get_structure_year, date)
print "Structure: ", mech.structure.type, mech.structure.wgt, "tons"
print "-2-----------------------------"
mech.engine.print_report(mech.weight)
#print "Gyro Def BV: ", mech.weight * parse_gyroBV(mech.engine.gyro, gyrolist)
date = get_comp_year(mech.engine.get_engine_year, date)
date = get_comp_year(mech.engine.get_gyro_year, date)
if mech.engine.jump > 0:
    date = get_comp_year(mech.engine.get_jj_year, date)
date = get_comp_year(mech.cockpit.get_cockpit_year, date)
date = parse_console(mech, date)
print mech.cockpit.type, mech.cockpit.get_cockpit_weight()
if mech.console == "TRUE":
    print "Command Console"
date = get_comp_year(mech.engine.get_enh_year, date)
print "-3-----------------------------"
date = parse_comp(mech.hstype, heatsinklist, date)
print mech.heatsinks, mech.hstype
print "-4-----------------------------"
date = get_comp_year(mech.armor.get_armor_year, date)
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
print "Armor Def BV: ", mech.armor.get_armor_BV()
print "-5-----------------------------"
if (mech.omni == "TRUE"):
    print "WARNING: Omni mech, results might be garbage."
#    sys.exit(1)

# Check for Artemis IV, Apollo
# TODO: Move to parse_gear
date = parse_artemis(mech, date)
if mech.artemis4 == "TRUE":
    print "Artemis IV"
if mech.apollo == "TRUE":
    print "Apollo"

print "BV: ", mech.BV
 
print "BV/ton: ", float(mech.BV)/float(mech.weight)

# Gear
(rnge, date) = parse_gear(mech, date)

# Figure out best speed
speed = mech.engine.erating/mech.weight
if mech.engine.jump > speed:
    mspd = mech.engine.jump
else:
    mspd = speed

# Print classification
print mspd, rnge

# Print time-period
print "Earliest Year: ", date

parse_omni(mech, date)
warnings.print_warnings()
