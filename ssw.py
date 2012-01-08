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
Analyze and print out some data about a mech.
Takes a SSW file as argument.
Uses external file mech.py to read in data.
"""

import argparse
from xml.dom import minidom
from mech import Mech

def print_weapon(mech, weap):
    """
    Print out info about a weapon
    """
    enh = ""
    report = str(weap.count)
    if weap.useammo > 0:
        report += "/" + str(weap.get_ammo_per_weapon())
    # If there is rear-mounted stuff, only list them, do not count for
    # evaluation
    if weap.countrear > 0:
        report += ", " + str(weap.countrear) + "(R)"
    if mech.artemis4 == "TRUE" and weap.enhance == "A":
        enh = "a4"
    elif mech.artemis5 == "TRUE" and weap.enhance == "A":
        enh = "a5"
    elif mech.apollo == "TRUE" and weap.enhance == "P":
        enh = "ap"
    elif mech.gear.tarcomp > 0 and weap.enhance == "T":
        enh = "tc"
    print ("%-7s %-27s %3d %-2s" % 
           (report, weap.name, weap.count * weap.heat, enh))


def parse_gear(mech):
    """
    Parse an equipment node
    """
    lbv = 0
    mbv = 0
    sbv = 0
    lheat = 0
    mheat = 0

    # Print used weapons
    print "Nr      Name                       Heat Enh"
    for weap in mech.gear.weaponlist.list:
        if (weap.count > 0 or weap.countrear > 0):
            print_weapon(mech, weap)
            # Get BV balance, also count heat
            if weap.range == "L":
                lbv = lbv + weap.count * weap.get_bv(mech.gear.tarcomp,
                                               mech.artemis4, mech.artemis5,
                                               mech.apollo)
                lheat = lheat + weap.count * weap.heat
            elif weap.range == "M":
                mbv = mbv + weap.count * weap.get_bv(mech.gear.tarcomp,
                                               mech.artemis4, mech.artemis5,
                                               mech.apollo)
                mheat = mheat + weap.count * weap.heat
            elif weap.range == "S":
                sbv = sbv + weap.count * weap.get_bv(mech.gear.tarcomp,
                                               mech.artemis4, mech.artemis5,
                                               mech.apollo)

    # Print used equipment
    for equip in mech.gear.o_equiplist.list:
        if equip.count > 0:
            report = str(equip.count) + " " + equip.name
            print report

    for equip in mech.gear.d_equiplist.list:
        if equip.count > 0:
            report = str(equip.count) + " " + equip.name
            print report


    # Print used physicals
    for phys in mech.gear.physicallist.list:
        if phys.count > 0:
            report = str(phys.count) + " " + phys.name
            dam = phys.dam(mech.weight)
            print report
            print phys.name, "Damage", dam, "Weight", mech.gear.get_p_weight()
            sbv = sbv + phys.count * phys.get_bv(mech.weight)

    # Explosive ammo
    for i in mech.gear.exp_ammo.keys():
        print "Explosive: ", i, mech.gear.exp_ammo[i]

    # Check heat
    print "Long range heat: ", lheat, "/", mech.get_sink()
    print "Medium range heat: ", mheat, "/", mech.get_sink()

    print "LR BV: ", lbv
    print "MR BV: ", mbv
    print "SR BV: ", sbv

    if lbv >= (mbv + sbv):
        return "Long-Range"
    else:
        return "Short-Range"


def parse_omni(mech, mspd):
    """
    Handle omni-mechs
    """
    if mech.omni == "TRUE":
        print "-------------------------------"
        print "Omni Loadouts"
        for i in mech.loads:
            print "-------------------------------"
            print "Config: ", i.get_name()
            print "BV: ", mech.get_bv(i)
            if (i.get_jump()):
                print "Jump: ", i.get_jump(), i.jjets.jjtype
            if (i.heatsinks.number):
                print i.heatsinks.number, i.heatsinks.type
            rnge = parse_gear(i)
            print mspd, rnge
        print "-------------------------------"


def print_bv(mech):
    """
    Print out battle value details if requested.
    """
    print "==============================="
    mech.def_bv(mech.load, True)
    print "-------------------------------"
    mech.off_bv(mech.load, True)
    print "-------------------------------"
    if not mech.omni == "TRUE":
        print "BV: ", mech.get_bv(mech.load)
        print ("BV/ton: %.2f" % (float(mech.batt_val)/float(mech.weight)))
    print "==============================="


def main():
    """
    main() function for ssw.py. Prints out a detailed overview of a mech.
    """

    ### Handle arguments ###

    # Create parser
    parser = argparse.ArgumentParser(description='Print mech details.')
    parser.add_argument('-b', action='store_true',
                        help='Show BV calculations')
    parser.add_argument('-r', action='store_true',
                        help='Show raw xml data')
    # Default: one filename
    parser.add_argument('file', nargs=1)    

    args = parser.parse_args()

    # Read file
    fsock = open(args.file[0])
    xmldoc = minidom.parse(fsock)
    fsock.close()

    # Print raw info for debugging
    if args.r:
        print xmldoc.toxml() 
        print "===BREAK==="

    # Get mech
    mech = Mech(xmldoc)

    print "Name: ", mech.model, mech.name
    mech.weight_summary(False)

    print "-1-----------------------------"
    print "Tech:      ", mech.techbase
    print "Weight:    ", mech.weight
    print "Motive:    ", mech.motive, mech.mechtype
    if (mech.omni == "TRUE"):
        print "Omni mech"
    print "Structure: ", mech.structure.summary_string()
    print "-2-----------------------------"
    mech.print_engine_report(mech.weight)
    print mech.cockpit.summary_string()
    print "-3-----------------------------"
    print mech.load.heatsinks.summary_string()
    print "-4-----------------------------"
    mech.parse_armor()
    print "-5-----------------------------"
    if (mech.omni == "TRUE"):
        print "WARNING: Omni mech, results might be garbage."

    if args.b:
        print_bv(mech)

    # Gear
    rnge = parse_gear(mech.load)

    # Figure out best speed
    speed = mech.engine.erating/mech.weight
    if mech.load.get_jump() > speed:
        mspd = mech.load.get_jump()
    else:
        mspd = speed

    # Print classification
    print mspd, rnge

    parse_omni(mech, mspd)

if __name__ == "__main__":
    main()
