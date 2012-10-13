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


def print_bvt_list(header_l, unit_list):
    """
    BV_list output

    In the form of name, weight, BV, BV/weight, def BV, off BV, small cockpit?
    """
    # Construct header
    header = create_header(header_l)

    # Print output
    print "=== Battle Value List by BV/weight ==="
    print header
    header2 = "Name                            "
    header2 += "Tons BV    BV/Wt | defBV   offBV   cpit"
    print header2
    for i in unit_list:
        print ("%-32.32s %3d %4d  %5.2f | %7.2f %7.2f %s" %
               (i[0], i[1], i[2], i[3], i[4], i[5], i[6]))


def print_bv_list(header_l, unit_list):
    """
    BV_list output

    In the form of name, weight, BV, BV/weight, def BV, off BV, small cockpit?
    """

    # Construct header
    header = create_header(header_l)

    # Print output
    print "=== Battle Value List by BV ==="
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



