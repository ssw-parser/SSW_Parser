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
from weapons import LRM_LIST, SRM_LIST, AC_LIST

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
    if weap.enhance == "A4":
        enh = "a4"
    elif weap.enhance == "A5":
        enh = "a5"
    elif weap.enhance == "AP":
        enh = "ap"
    elif mech.gear.tarcomp > 0 and weap.enhance == "TC":
        enh = "tc"
    print ("%-7s %-27s %3d %1d/%1d/%2d/%2d %-2s" % 
           (report, weap.name, weap.count * weap.get_heat(),
            weap.get_min_range(), weap.get_short_range(), weap.get_med_range(),
            weap.get_range(), enh))


def print_lrm(i):
    """
    Print a report on LRMs
    """
    print
    print "----------------------------------------"
    print "LRM status:"
    print "Nr Name                        Heat Dam Ammo"
    t_dam = 0
    t_heat = 0
    for weap in i.gear.weaponlist.list:
        for launcher in LRM_LIST:
            if (weap.name == launcher[0] and weap.count > 0):
                cnt = weap.count
                heat = cnt * weap.get_heat()
                dam = cnt * weap.get_damage(18)
                t_heat += heat
                t_dam += dam
                print ("%2d %-27s %3d %3d %3d" %
                       (cnt, weap.name, heat, dam,
                        weap.get_ammo_per_weapon()))
    print ("Total Damage: %5.2f Heat: %d/%d" %
           (t_dam, t_heat, i.get_sink()))
    print "----------------------------------------"


def print_srm(i):
    """
    Print a report on SRMs
    """
    print
    print "----------------------------------------"
    print "SRM status:"
    print "Nr Name                        Heat Dam Ammo"
    t_dam = 0
    t_heat = 0
    for weap in i.gear.weaponlist.list:
        for launcher in SRM_LIST:
            if (weap.name == launcher[0] and weap.count > 0):
                cnt = weap.count
                heat = cnt * weap.get_heat()
                dam = cnt * weap.get_damage(6)
                t_heat += heat
                t_dam += dam
                print ("%2d %-27s %3d %3d %3d" %
                       (cnt, weap.name, heat, dam,
                        weap.get_ammo_per_weapon()))
    print ("Total Damage: %5.2f Heat: %d/%d" %
           (t_dam, t_heat, i.get_sink()))
    print "----------------------------------------"


def print_ac(i):
    """
    Print a report on Autocannons
    """
    print
    print "----------------------------------------"
    print "AC status:"
    print "Nr Name                        Heat Dam Ammo"
    t_dam = 0
    t_heat = 0
    for weap in i.gear.weaponlist.list:
        for launcher in AC_LIST:
            if (weap.name == launcher[0] and weap.count > 0):
                cnt = weap.count
                heat = cnt * weap.get_heat()
                dam = cnt * weap.get_damage(9)
                t_heat += heat
                t_dam += dam
                print ("%2d %-27s %3d %3d %3d" %
                       (cnt, weap.name, heat, dam,
                        weap.get_ammo_per_weapon()))
    print ("Total Damage: %5.2f Heat: %d/%d" %
           (t_dam, t_heat, i.get_sink()))
    print "----------------------------------------"


def parse_gear(mech):
    """
    Parse an equipment node
    """
    ldam = 0
    mdam = 0
    sdam = 0
    lheat = 0
    mheat = 0
    sheat = 0

    # Print used weapons
    print "Nr      Name                       Heat Range     Enh"
    for weap in mech.gear.weaponlist.list:
        if (weap.count > 0 or weap.countrear > 0):
            print_weapon(mech, weap)
            # Get BV balance, also count heat
            if weap.get_range() >= 18:
                ldam += weap.count * weap.get_damage(18)
                lheat += weap.count * weap.get_heat()
            if weap.get_range() >= 9:
                mdam += weap.count * weap.get_damage(9)
                mheat += weap.count * weap.get_heat()
            if weap.get_range() >= 3:
                sdam += weap.count * weap.get_damage(3)
                sheat += weap.count * weap.get_heat()

    # Print used equipment
    for equip in mech.gear.equiplist.list:
        if equip.count > 0:
            report = str(equip.count) + " " + equip.name
            print report

    # Print used physicals
    for phys in mech.gear.physicallist.list:
        if phys.count > 0:
            dam = phys.get_damage()
            print ("%1d %-20s Dam: %4.1f Wgt: %4.1f" %
                   (phys.count, phys.name, dam, phys.get_weight()))

    # Explosive ammo
    for i in mech.gear.exp_ammo.keys():
        print "Explosive: ", i, mech.gear.exp_ammo[i]

    # Print damage Summary
    print
    print ("Long Range (18)  Damage: %5.2f Heat: %d/%d" %
           (ldam, lheat, mech.get_sink()))
    print ("Medium Range (9) Damage: %5.2f Heat: %d/%d" %
           (mdam, mheat, mech.get_sink()))
    print ("Short Range (3)  Damage: %5.2f Heat: %d/%d" %
           (sdam, sheat, mech.get_sink()))

    # Print LRM status is appliable
    if mech.gear.lrms > 0:
        print_lrm(mech)

    # Print SRM status is appliable
    if mech.gear.srms > 0:
        print_srm(mech)

    # Print Autocannon status is appliable
    if mech.gear.has_ac:
        print_ac(mech)

def parse_omni(mech, battv):
    """
    Handle omni-mechs
    """
    if mech.omni == "TRUE":
        print "-------------------------------"
        print "Omni Loadouts"
        for i in mech.loads:
            print "-------------------------------"
            print "Config: ", i.get_name()
            if battv:
                print "==============================="
                mech.def_bv(i, True)
                print "-------------------------------"
                mech.off_bv(i, True)
                print "==============================="
            print "BV: ", mech.get_bv(i)
            if (i.get_jump()):
                print "Jump: ", i.get_jump(), i.jjets.jjtype
            if (i.heatsinks.number):
                print i.heatsinks.number, i.heatsinks.type
            parse_gear(i)
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

    print "================================="
    print "Name: ", mech.name, mech.model
#    mech.weight_summary(False)

    print "-Basic---------------------------"
    print "Tech:      ", mech.techbase
    print "Weight:    ", mech.weight
    if (mech.omni == "TRUE"):
        print "Motive:    ", mech.motive, mech.mechtype, "(Omni mech)"
    else:
        print "Motive:    ", mech.motive, mech.mechtype
    print "Structure: ", mech.structure.summary_string()
    print "-Movement------------------------"
    mech.print_engine_report(mech.weight)
    print "-Fixed Heatsinks-----------------"
    print mech.load.heatsinks.summary_string()
    print "-Armor---------------------------"
    mech.parse_armor()
    print "-5-------------------------------"
    if (mech.omni == "TRUE"):
        print "WARNING: Omni mech, results might be garbage."

    if args.b:
        print_bv(mech)

    # Gear
    parse_gear(mech.load)

    # Omni configs
    parse_omni(mech, args.b)

if __name__ == "__main__":
    main()
