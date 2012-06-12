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
from weapon_list import LRM_LIST, SRM_LIST, AC_LIST

def print_weapon(mech, weap):
    """
    Print out info about a weapon
    """
    enh = ""
    report = weap.count_string()
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
    if i.artemis4 == "TRUE":
        print "ArtemisIV"
    elif i.artemis5 == "TRUE":
        print "ArtemisV"
    print "Nr Name                        Heat Dam Ammo"
    t_dam = 0
    t_heat = 0
    for weap in i.gear.weaponlist.list.itervalues():
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
    if i.artemis4 == "TRUE":
        print "ArtemisIV"
    elif i.artemis5 == "TRUE":
        print "ArtemisV"
    print "Nr Name                        Heat Dam Ammo"
    t_dam = 0
    t_heat = 0
    for weap in i.gear.weaponlist.list.itervalues():
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
    for weap in i.gear.weaponlist.list.itervalues():
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
    for weap in mech.gear.weaponlist.list.itervalues():
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
    if mech.gear.weaponlist.lrms > 0:
        print_lrm(mech)

    # Print SRM status is appliable
    if mech.gear.weaponlist.count_srms() > 0:
        print_srm(mech)

    # Print Autocannon status is appliable
    if mech.gear.weaponlist.has_ac():
        print_ac(mech)

def print_upgrade(wlist, upgr, orig, uclass):
    """
    Print out a suggested upgrade
    """
    heat = wlist[upgr].get_heat() - wlist[orig].get_heat()
    dam = (wlist[upgr].get_damage(wlist[upgr].get_range()) -
           wlist[orig].get_damage(wlist[orig].get_range()))
    rng = wlist[upgr].get_range() - wlist[orig].get_range()
    wgt = wlist[upgr].get_weight() - wlist[orig].get_weight()
    if (wgt > 0):
        return
    battv = wlist[upgr].get_bv(0) - wlist[orig].get_bv(0) # No tarcomp
    if (battv < 0):
        print "  WARNING: POSSIBLE DOWNGRADE SUGGESTED!:"
    print ("  %-6s (Class %c) | %d heat, %.1f dam, %d range, %.1f ton, %d BV" %
           (wlist[upgr].get_short(), uclass, heat, dam, rng, wgt, battv))

def evaluate_upgrades(mech):
    """
    Suggest upgrades
    """
    print "================================="
    print "=== Upgrade evaluation        ==="
    print "================================="
    wlist = mech.gear.weaponlist.list
    for weap in wlist.itervalues():
        if (weap.name == "(IS) Autocannon/2" and weap.count > 0):
            print weap.count, weap.get_short(), "Suggested upgrades:"
            weap2 = "(IS) Medium Laser"
            print_upgrade(wlist, weap2, weap.name, "B")
            weap2 = "(IS) Medium Pulse Laser"
            print_upgrade(wlist, weap2, weap.name, "B")
            weap2 = "(IS) LRM-5"
            print_upgrade(wlist, weap2, weap.name, "B")
            weap2 = "(IS) SRM-4"
            print_upgrade(wlist, weap2, weap.name, "B")

        if (weap.name == "(IS) Autocannon/5" and weap.count > 0):
            print weap.count, weap.get_short(), "Suggested upgrades:"
#            weap2 = "(IS) Rotary AC/2"
#            print_upgrade(wlist, weap2, weap.name, "A")
#            weap2 = "(IS) Light PPC"
#            print_upgrade(wlist, weap2, weap.name, "B")
            weap2 = "(IS) PPC"
            print_upgrade(wlist, weap2, weap.name, "B")
            weap2 = "(IS) ER PPC"
            print_upgrade(wlist, weap2, weap.name, "B")
            weap2 = "(IS) Large Laser"
            print_upgrade(wlist, weap2, weap.name, "B")
            weap2 = "(IS) ER Large Laser"
            print_upgrade(wlist, weap2, weap.name, "B")
            weap2 = "(IS) Large Pulse Laser"
            print_upgrade(wlist, weap2, weap.name, "B")
            weap2 = "(IS) LRM-10"
            print_upgrade(wlist, weap2, weap.name, "B")
            weap2 = "(IS) LRM-15"
            print_upgrade(wlist, weap2, weap.name, "B")

        if (weap.name == "(IS) Autocannon/10" and weap.count > 0):
            print weap.count, weap.get_short(), "Suggested upgrades:"
            weap2 = "(IS) LB 10-X AC"
            print_upgrade(wlist, weap2, weap.name, "A")
#            weap2 = "(IS) Light Gauss Rifle"
#            print_upgrade(wlist, weap2, weap.name, "A")
#            weap2 = "(IS) Rotary AC/5"
#            print_upgrade(wlist, weap2, weap.name, "A")
            weap2 = "(IS) Gauss Rifle"
            print_upgrade(wlist, weap2, weap.name, "A")
            weap2 = "(IS) PPC"
            print_upgrade(wlist, weap2, weap.name, "B")
            weap2 = "(IS) Large Laser"
            print_upgrade(wlist, weap2, weap.name, "B")
            weap2 = "(IS) ER Large Laser"
            print_upgrade(wlist, weap2, weap.name, "B")
            weap2 = "(IS) ER PPC"
            print_upgrade(wlist, weap2, weap.name, "B")
#            weap2 = "(IS) Plasma Rifle"
#            print_upgrade(wlist, weap2, weap.name, "B")
            weap2 = "(IS) LRM-15"
            print_upgrade(wlist, weap2, weap.name, "B")
            weap2 = "(IS) LRM-20"
            print_upgrade(wlist, weap2, weap.name, "B")

        if (weap.name == "(IS) Autocannon/20" and weap.count > 0):
            print weap.count, weap.get_short(), "Suggested upgrades:"
            weap2 = "(IS) Gauss Rifle"
            print_upgrade(wlist, weap2, weap.name, "A")
            weap2 = "(IS) ER PPC"
            print_upgrade(wlist, weap2, weap.name, "B")
            weap2 = "(IS) LRM-20"
            print_upgrade(wlist, weap2, weap.name, "B")

        if (weap.name == "(IS) Machine Gun" and weap.count > 0):
            print weap.count, weap.get_short(), "Suggested upgrades:"
            weap2 = "(IS) Autocannon/2"
            print_upgrade(wlist, weap2, weap.name, "A")
            weap2 = "(IS) Small Laser"
            print_upgrade(wlist, weap2, weap.name, "B")
            weap2 = "(IS) Small Pulse Laser"
            print_upgrade(wlist, weap2, weap.name, "B")
            weap2 = "(IS) Medium Laser"
            print_upgrade(wlist, weap2, weap.name, "B")
            weap2 = "(IS) Medium Pulse Laser"
            print_upgrade(wlist, weap2, weap.name, "B")
            weap2 = "(IS) Flamer"
            print_upgrade(wlist, weap2, weap.name, "B")
            weap2 = "(IS) LRM-5"
            print_upgrade(wlist, weap2, weap.name, "B")
            weap2 = "(IS) SRM-2"
            print_upgrade(wlist, weap2, weap.name, "B")
            weap2 = "(IS) SRM-4"
            print_upgrade(wlist, weap2, weap.name, "B")
            weap2 = "(IS) Streak SRM-2"
            print_upgrade(wlist, weap2, weap.name, "B")

        if (weap.name == "(IS) Small Laser" and weap.count > 0):
            print weap.count, weap.get_short(), "Suggested upgrades:"
#            weap2 = "(IS) ER Small Laser"
#            print_upgrade(wlist, weap2, weap.name, "A")
            weap2 = "(IS) Small Pulse Laser"
            print_upgrade(wlist, weap2, weap.name, "A")
            weap2 = "(IS) Medium Laser"
            print_upgrade(wlist, weap2, weap.name, "A")
            weap2 = "(IS) Medium Pulse Laser"
            print_upgrade(wlist, weap2, weap.name, "A")
            weap2 = "(IS) Autocannon/2"
            print_upgrade(wlist, weap2, weap.name, "B")
            weap2 = "(IS) LRM-5"
            print_upgrade(wlist, weap2, weap.name, "B")
            weap2 = "(IS) SRM-2"
            print_upgrade(wlist, weap2, weap.name, "B")
            weap2 = "(IS) SRM-4"
            print_upgrade(wlist, weap2, weap.name, "B")
            weap2 = "(IS) Streak SRM-2"
            print_upgrade(wlist, weap2, weap.name, "B")

        if (weap.name == "(IS) Medium Laser" and weap.count > 0):
            print weap.count, weap.get_short(), "Suggested upgrades:"
            weap2 = "(IS) Medium Pulse Laser"
            print_upgrade(wlist, weap2, weap.name, "A")

        if (weap.name == "(IS) Large Laser" and weap.count > 0):
            print weap.count, weap.get_short(), "Suggested upgrades:"
            weap2 = "(IS) ER Large Laser"
            print_upgrade(wlist, weap2, weap.name, "A")

        if (weap.name == "(IS) PPC" and weap.count > 0):
            print weap.count, weap.get_short(), "Suggested upgrades:"
            weap2 = "(IS) ER PPC"
            print_upgrade(wlist, weap2, weap.name, "A")

        if (weap.name == "(IS) LRM-5" and weap.count > 0):
            print weap.count, weap.get_short(), "Suggested upgrades:"
            weap2 = "(IS) Medium Laser"
            print_upgrade(wlist, weap2, weap.name, "B")
            weap2 = "(IS) Medium Pulse Laser"
            print_upgrade(wlist, weap2, weap.name, "B")

        if (weap.name == "(IS) LRM-10" and weap.count > 0):
            print weap.count, weap.get_short(), "Suggested upgrades:"
            weap2 = "(IS) Large Laser"
            print_upgrade(wlist, weap2, weap.name, "B")
            weap2 = "(IS) ER Large Laser"
            print_upgrade(wlist, weap2, weap.name, "B")
            weap2 = "(IS) Large Pulse Laser"
            print_upgrade(wlist, weap2, weap.name, "B")

        if (weap.name == "(IS) LRM-15" and weap.count > 0):
            print weap.count, weap.get_short(), "Suggested upgrades:"
            weap2 = "(IS) PPC"
            print_upgrade(wlist, weap2, weap.name, "B")
            weap2 = "(IS) ER Large Laser"
            print_upgrade(wlist, weap2, weap.name, "B")
            weap2 = "(IS) ER PPC"
            print_upgrade(wlist, weap2, weap.name, "B")

        if (weap.name == "(IS) LRM-20" and weap.count > 0):
            print weap.count, weap.get_short(), "Suggested upgrades:"
            weap2 = "(IS) ER PPC"
            print_upgrade(wlist, weap2, weap.name, "B")

        if (weap.name == "(IS) SRM-2" and weap.count > 0):
            print weap.count, weap.get_short(), "Suggested upgrades:"
            weap2 = "(IS) LRM-5"
            print_upgrade(wlist, weap2, weap.name, "A")
            weap2 = "(IS) SRM-4"
            print_upgrade(wlist, weap2, weap.name, "A")
            weap2 = "(IS) Streak SRM-2"
            print_upgrade(wlist, weap2, weap.name, "A")
            weap2 = "(IS) Autocannon/2"
            print_upgrade(wlist, weap2, weap.name, "B")
            weap2 = "(IS) Medium Laser"
            print_upgrade(wlist, weap2, weap.name, "B")
            weap2 = "(IS) Medium Pulse Laser"
            print_upgrade(wlist, weap2, weap.name, "B")

        if (weap.name == "(IS) SRM-4" and weap.count > 0):
            print weap.count, weap.get_short(), "Suggested upgrades:"
            weap2 = "(IS) LRM-5"
            print_upgrade(wlist, weap2, weap.name, "A")
            weap2 = "(IS) Medium Laser"
            print_upgrade(wlist, weap2, weap.name, "B")
            weap2 = "(IS) Medium Pulse Laser"
            print_upgrade(wlist, weap2, weap.name, "B")

        if (weap.name == "(IS) SRM-6" and weap.count > 0):
            print weap.count, weap.get_short(), "Suggested upgrades:"
            weap2 = "(IS) LRM-10"
            print_upgrade(wlist, weap2, weap.name, "A")
            weap2 = "(IS) Large Laser"
            print_upgrade(wlist, weap2, weap.name, "B")
            weap2 = "(IS) ER Large Laser"
            print_upgrade(wlist, weap2, weap.name, "B")
            weap2 = "(IS) Large Pulse Laser"
            print_upgrade(wlist, weap2, weap.name, "B")

#        if (weap.name == "(CL) Heavy Machine Gun" and weap.count > 0):
#            print weap.count, weap.get_short(), "suggested upgrades:"
#            weap2 = "(CL) AP Gauss Rifle"
#            print_upgrade(wlist, weap2, weap.name, "A")

#        if (weap.name == "(CL) Heavy Small Laser" and weap.count > 0):
#            print weap.count, weap.get_short(), "suggested upgrades:"
#            weap2 = "(CL) ER Small Laser"
#            print_upgrade(wlist, weap2, weap.name, "A")



def parse_omni(mech, args):
    """
    Handle omni-mechs
    """
    if mech.omni == "TRUE":
        print "-------------------------------"
        print "Omni Loadouts"
        for i in mech.loads:
            print "-------------------------------"
            print "Config: ", i.get_name()
            if args.b:
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
            if args.u:
                evaluate_upgrades(i)
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
    parser.add_argument('-u', action='store_true',
                        help='Suggest weapon upgrades')
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
    mech.print_engine_report()
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
    if args.u:
        evaluate_upgrades(mech.load)

    # Omni configs
    parse_omni(mech, args)

if __name__ == "__main__":
    main()
