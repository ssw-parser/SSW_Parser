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
summary_view.py
==========
View module for summary.py

Handles representation of output for summary.py, in the form of
printing out one-line summaries of units.
"""


def create_header(header_l):
    """
    Construct filter header

    :param header_l: List of header segments
    :type header_l: list of strings
    :return: merged header
    :rtype: string
    """
    # Start with Units
    header = "Units "
    count = 5

    # Add specific filter description(s)
    for h_item in header_l:
        header += h_item
        count += len(h_item)
        # Need new-line?
        if count > 60:
            header += ",\n"
            count = 0
        else:
            header += ", "
            count += 2

    # Clean up end
    header = header[:-2] + ":"

    return header


def print_bv_list(title, header_l, unit_list):
    """
    BV_list output

    In the form of name, weight, BV, BV/weight, def BV, off BV, small cockpit?
    """

    # Construct header
    header = create_header(header_l)

    # Print output
    print "=== " + title + " ==="
    print header
    header2 = "Name                            "
    header2 += "Tons BV    BV/Wt | defBV   offBV   cpit"
    print header2
    for i in unit_list:
        print ("%-32.32s %3d %4d  %5.2f | %7.2f %7.2f %s" %
               (i[0], i[1], i[2], i[3], i[4], i[5], i[6]))


def print_armor_list(header_l, unit_list):
    """
    armor_list output

    In the form of name, weight, BV, points/max, Armor%, armor tonnage,
    armor type, battleforce armor value, Explosive, Stealth,
    sorted by armor points, descending
    """
    # Construct header
    header = create_header(header_l)

    # Print output
    print "=== Armor List ==="
    print header
    header2 = "Name                            "
    header2 += "Tons BV   Points  Armr Tons  Type  | BF Exp Sth"
    print header2
    for i in unit_list:
        print ("%-32.32s %3d %4d %3d/%3d %3.0f%% %4.1ft %-5s | %2d %3s %3s" %
               (i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9],
                i[10]))


def print_speed_list(header_l, unit_list):
    """
    speed_list output

    In the form of name, weight, BV, speed, myomer enhancement, target mod,
    battleforce string
    sorted by speed, descending
    """
    # Construct header
    header = create_header(header_l)

    # Print output
    print "=== Speed List ==="
    print header
    header2 = "Name                            "
    header2 += "Tons BV    Speed   Enh  Eng Mod BF    OSF  Super"
    print header2
    for i in unit_list:
        print ("%-32.32s %3d %4d %2d/%2d/%2d %-4s %-3s %d   %-5s %4.2f %s" %
               (i[0], i[1], i[2], i[4], i[5], i[6], i[7], i[8], i[9], i[10],
                i[11], i[12]))


def print_electronics_list(header_l, unit_list):
    """
    electronics_list output

    In the form of name, weight, BV, speed, myomer enhancement, target mod,
    battleforce string
    sorted by speed, descending
    """
    # Construct header
    header = create_header(header_l)

    # Print output
    print "=== Electronics List ==="
    print header
    header2 = "Name                            "
    header2 += "Tons BV    Speed   ECM BAP TAG NARC C3S C3M C3I"
    print header2
    for i in unit_list:
        print ("%-32.32s %3d %4d %2d/%2d/%2d %3s %3s %3s %4s %3s %3s %3s" %
               (i[0], i[1], i[2], i[4], i[5], i[6], i[7], i[8], i[9], i[10],
                i[11], i[12], i[13]))


def print_weapon_list(title, header_l, unit_list):
    """
    weapon_list output

    In the form of name, weight, BV, Movement, weapon details
    sorted by BV, descending
    """
    # Construct header
    header = create_header(header_l)

    # Print output
    print "=== " + title + " ==="
    print header
    header2 = "Name                            "
    header2 += "Tons BV   Mov Weapons/turns of fire"
    print header2
    for i in unit_list:
        print ("%-32.32s %3d %4d %-3s %s" %
               (i[0], i[1], i[2], i[3], i[4]))


def print_timeline_list(header_l, unit_list):
    """
    timeline_list output

    In the form of year, name, weight, BV, Movement, structure, armor,
    weapon details
    sorted by BV, descending
    """
    # Construct header
    header = create_header(header_l)

    # Print output
    print "=== List of mechs sorted by year ==="
    print header
    header2 = "Year Name                            "
    header2 += "Tons Mov Eng Str Armr Weapons/turns of fire"
    print header2
    for i in unit_list:
        print ("%4d %-32.32s %3d %-3s %-3s %-3s %-4s %s" %
               (i[3], i[0], i[1], i[4], i[2], i[5], i[6], i[7]))


def print_missile_list(header_l, unit_list):
    """
    missile_list output

    In the form of name, weight, BV, LRM tubes, Artemis, Heat, Movement,
    launcher details
    sorted by LRM tubes, descending
    """
    # Construct header
    header = create_header(header_l)

    # Print output
    print "=== List of LRM Tubes ==="
    print header
    header2 = "Name                            "
    header2 += "Tons BV   LRM Art Heat  Mov Lnchrs/turns of fire"
    print header2
    for i in unit_list:
        print ("%-32.32s %3d %4d %3d %-3s %-5s %-3s %s" %
               (i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7]))


def print_srm_list(header_l, unit_list):
    """
    srm_list output

    In the form of name, weight, BV, SRM tubes, Artemis, Heat, Movement,
    launcher details
    sorted by SRM tubes, descending
    """
    # Construct header
    header = create_header(header_l)

    # Print output
    print "=== List of SRM Tubes ==="
    print header
    header2 = "Name                            "
    header2 += "Tons BV   SRM Art Heat  Mov Lnchrs/turns of fire"
    print header2
    for i in unit_list:
        print ("%-32.32s %3d %4d %3d %-3s %-5s %-3s %s" %
               (i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7]))


def print_autocannon_list(header_l, unit_list):
    """
    autocannon_list output

    In the form of name, weight, BV, damage, tarcomp, Heat, Movement,
    weapon details
    sorted by damage, descending
    """
    # Construct header
    header = create_header(header_l)

    # Print output
    print "=== List of Special Ammo Capable Autocannons ==="
    print header
    header2 = "Name                            "
    header2 += "Tons BV   Dam TC  Heat  Mov Guns/turns of fire"
    print header2
    for i in unit_list:
        print ("%-32.32s %3d %4d %3d %-3s %-5s %-3s %s" %
               (i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7]))


def print_std_list(title, header_l, unit_list):
    """
    print out lists created by create_std_list_item

    In the form of name, weight, BV, damage, heat, movement, weapon details
    sorted by damage, descending
    """
    # Construct header
    header = create_header(header_l)

    # Print output
    print "=== " + title + " ==="
    print header
    header2 = "Name                            "
    header2 += "Tons BV   Dam Heat  Mov Arm Wpns/turns of fire"
    print header2
    for i in unit_list:
        print ("%-32.32s %3d %4d %3d %-5s %-3s %3d %s" %
               (i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7]))


def print_headcap_list(header_l, unit_list):
    """
    headcap_list output

    In the form of name, weight, BV, Headcappers, Movement, Armor, Tarcomp
    weapon details
    sorted by number of headcappers, descending
    """
    # Construct header
    header = create_header(header_l)

    # Print output
    print "=== List of Headcappers ==="
    print header
    header2 = "Name                            "
    header2 += "Tons BV   Cap Mov Armr TC Weapons/turns of fire"
    print header2
    for i in unit_list:
        if i[3] > 0:
            print ("%-32.32s %3d %4d %3d %-3s %3.0f%% %-2s %s" %
                   (i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7]))


def print_battle_force_list(header_l, unit_list):
    """
    battle_force_list output

    In the form of name, weight, BV, Headcappers, Movement, Armor, Tarcomp
    weapon details
    sorted by number of headcappers, descending
    """
    # Construct header
    header = create_header(header_l)

    # Print output
    print "=== BattleForce Data List (Alpha) ==="
    print header
    header2 = "Name                            "
    header2 += "Wg Pt Mov  Arm"
    print header2
    for i in unit_list:
        if i[3] > 0:
            print ("%-32.32s %1d %2d %-5s %2d" %
                   (i[0], i[1], i[2], i[3], i[4]))


def print_damage_range_list(header_l, unit_list):
    """
    range_list output

    In the form of name, weight, BV, damage
    sorted by damage, descending
    """
    # Construct header
    header = create_header(header_l)

    # Print output
    print "=== Damage by Range List ==="
    print header
    header2 = "Name                            "
    header2 += "Tons BV    D3  D6  D9 D12 D15 D18 D21 D24"
    print header2
    for i in unit_list:
        print ("%-32.32s %3d %4d %3d %3d %3d %3d %3d %3d %3d %3d" %
               (i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9],
                i[10]))


def print_type_list(header_l, unit_list):
    """
    type_list output

    In the form of name, weight, BV, damage
    sorted by damage, descending
    """
    # Construct header
    header = create_header(header_l)

    # Print output
    print "=== List of Units by Type (Alpha) ==="
    print header
    header2 = "Name                          "
    header2 += "Tons BV    SCT STR SKR BRW MIS SNP JUG WARN"
    print header2
    for i in unit_list:
        print ("%-30s %3d %4d  %c   %c   %c   %c   %c   %c   %c  %s" %
               (i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9],
                i[10]))


def print_cost_list(header_l, unit_list):
    """
    cost_list output

    In the form of name, weight, BV, cost
    sorted by cost, descending
    """

    # Construct header
    header = create_header(header_l)

    # Print output
    print "=== List of Unit Costs (Alpha) ==="
    print header
    header2 = "Name                            "
    header2 += "Tons BV      cost       cost(SSW)     difference"
    print header2
    for i in unit_list:
        print ("%-32.32s %3d %4d  %11d %11d %11d" %
               (i[0], i[1], i[2], i[3], i[4], i[5]))


def print_weight_list(header_l, unit_list):
    """
    weight_list output

    In the form of name, weight, BV, cost
    sorted by cost, descending
    """
    # Construct header
    header = create_header(header_l)

    # Print output
    print "=== List of Unit Weight Distributions ==="
    print header
    header2 = "Name                            "
    header2 += "Tons | Stru Eng  Arm  Ctrl Jmp  Heat Tur  Gear Rest"
    print header2
    for i in unit_list:
        print ("%-32.32s %3d | %4.1f %4.1f %4.1f %4.1f %4.1f %4.1f %4.1f %4.1f %s" %
               (i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9],
                i[10]))


def print_default(header_l, unit_list):
    """
    Default output format

    In the form of name, weight, BV, source, era
    Intended to conform to the MUL format
    """
    # Construct header
    header = create_header(header_l)

    # Print output
    print "=== MUL-Type Listing of Units ==="
    print header
    print "Name                            Tons BV   Source   Rul Era   Year"
    for i in unit_list:
        print ("%-32.32s %3d %4d %-8s %-3s %-5s %4d" %
               (i[0], i[1], i[2], i[3], i[4], i[5], i[6]))
