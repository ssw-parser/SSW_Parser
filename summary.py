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
Prints out a one-line summary of a mech
"""

import sys
from xml.dom import minidom
from operator import itemgetter
from mech import Mech


#############################
##### Utility functions #####
#############################

#
# TODO: Add missing eras: SL, Rep, DA
#
def conv_era(era):
    """
    Convert era to string
    """
    conv = {
        0 : "AoW",
        2 : "SW-E",
        3 : "SW-L",
        4 : "Clan",
        5 : "CW",
        6 : "Jihad"
        }
    return conv[era]
    

def load_mech(file_name):
    """
    Load mech from file

    Takes a file name as argument, returns a mech object
    """
    # Read file
    fsock = open(file_name)
    xmldoc = minidom.parse(fsock)
    fsock.close()

    # Get mech
    return Mech(xmldoc)


def create_header(header_l):
    """
    Construct filter header
    """
    # Start with Mechs
    header = "Mechs "

    # Add specific filter description(s)
    for h_item in header_l:
        header += h_item
        header += ", "

    # Clean up end
    header = header[:-2] + ":"

    return header


###############################
##### Mech entry creation #####
###############################

def create_mech_list(file_list, select_l, creator):
    """
    Create a list of mechs

    file_list is the list of files containing mech info
    select is the selection criteria
    creator specifies which items should be included
    Note that item 0 is always supposed to be the name,
    item 1 is supposed to be Weight, and item 2 is supposed to be BV
    """
    mech_list = []
    # Loop over input
    for i in file_list:
        # Load mech from file
        mech = load_mech(i)

        # Construct data
        if mech.omni == "TRUE":
            for i in mech.loads:
                sel = True
                # Go through the list of selections
                for select in select_l:
                    if select(mech, i) and sel:
                        sel = True
                    else:
                        sel = False
                if sel:
                    item = creator(mech, i)
                    mech_list.append(item)
        else:
            sel = True
            # Go through the list of selections
            for select in select_l:
                if select(mech, mech.load) and sel:
                    sel = True
                else:
                    sel = False
            if sel:
                item = creator(mech, mech.load)
                mech_list.append(item)

    # Default: Sort by weight, name
    mech_list.sort(key=itemgetter(0))
    mech_list.sort(key=itemgetter(1))

    return mech_list


###################################
##### Output format functions #####
###################################

# When constructing a list function, always set
# first item as name
# second item as weight
# third item as BV

def create_bv_list_item(mech, i):
    """
    Compile info used by print_BV_list()
    """
    name_str = mech.name + " " + mech.model + i.name
    BV = mech.get_BV(i)
    weight = mech.weight
    bv_ton = float(BV)/float(weight)
    bv_def = mech.def_BV(i, False)
    bv_off = mech.off_BV(i, False)
    cockp = ""
    if mech.cockpit.type == "Small Cockpit":
        cockp = "SML"
    return (name_str, weight, BV, bv_ton, bv_def, bv_off, cockp)

def print_bv_list(file_list, select_l, header):
    """
    BV_list output

    In the form of name, weight, BV, BV/weight, def BV, off BV, small cockpit?
    sorted by BV/weight, descending
    """

    # Build list
    mech_list = create_mech_list(file_list, select_l, create_bv_list_item)

    # Sort by BV/ton
    mech_list.sort(key=itemgetter(3), reverse=True)

    # Print output
    print header
    print "Name                          Tons BV    BV/Wt | defBV   offBV   cpit"
    for i in mech_list:
        print ("%-30s %3d %4d  %5.2f | %7.2f %7.2f %s" %
               (i[0], i[1], i[2], i[3], i[4], i[5], i[6]))


def create_armor_list_item(mech, i):
    """
    Compile info used by print_armor_list()
    """
    name_str = mech.name + " " + mech.model + i.name
    BV = mech.get_BV(i)
    weight = mech.weight
    # Armor coverage relative to maximum
    armor = mech.armor.get_armor_percent()
    # Check for explosive stuff that can disable the mech
    exp = i.gear.get_ammo_exp_BV(mech.engine) + i.gear.get_weapon_exp_BV(mech.engine)
    if exp < 0:
        e_str = "EXP"
    else:
        e_str = ""
    # Check for a stealth system
    sth = mech.get_stealth()
    if sth:
        s_str = "STH"
    else:
        s_str = ""
    # Armor points
    arm_p = mech.armor.total.arm
    max_p = mech.armor.total.max
    # Armor weight
    wgt = mech.armor.get_weight()

    return (name_str, weight, BV, armor, e_str, s_str, arm_p, max_p, wgt)

def print_armor_list(file_list, select_l, header):
    """
    armor_list output

    In the form of name, weight, BV, Armor%, Explosive, Stealth, points/max,
    armor tonnage
    sorted by armor%, descending
    """
    # Build list
    mech_list = create_mech_list(file_list, select_l, create_armor_list_item)

    # Sort by armor%
    mech_list.sort(key=itemgetter(3), reverse=True)

    # Print output
    print header
    print "Name                          Tons BV   Armr Exp Sth | Points  Tons"
    for i in mech_list:
        print ("%-30s %3d %4d %3.0f%% %3s %3s | %3d/%3d %4.1ft" % 
               (i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8]))


def create_speed_list_item(mech, i):
    """
    Compile info used by print_speed_list()
    """
    name_str = mech.name + " " + mech.model + i.name
    BV = mech.get_BV(i)
    weight = mech.weight
    walk = mech.get_walk()
    run = mech.get_run()
    jump = i.get_jump()
    spd = max(walk, jump)
    enh = mech.engine.enhancement
    if enh == "---":
        enh = ""
    return (name_str, weight, BV, spd, walk, run, jump, enh)

def print_speed_list(file_list, select_l, header):
    """
    speed_list output

    In the form of name, weight, BV, speed, myomer enhancement
    sorted by speed, descending
    """
    # Build list
    mech_list = create_mech_list(file_list, select_l, create_speed_list_item)

    # Sort by speed
    mech_list.sort(key=itemgetter(3), reverse=True)

    # Print output
    print header
    print "Name                          Tons BV    Speed   Enh"
    for i in mech_list:
        print ("%-30s %3d %4d %2d/%2d/%2d %-4s" % 
               (i[0], i[1], i[2], i[4], i[5], i[6], i[7]))


def create_missile_list_item(mech, i):
    """
    Compile info used by print_missile_list()
    """
    name_str = mech.name + " " + mech.model + i.name
    BV = mech.get_BV(i)
    weight = mech.weight
    lrm = i.gear.LRMs
    if i.gear.a4 == "TRUE":
        art = "AIV"
    elif i.gear.a5 == "TRUE":
        art = "AV"
    else:
        art = ""
    return (name_str, weight, BV, lrm, art)

def print_missile_list(file_list, select_l, header):
    """
    missile_list output

    In the form of name, weight, BV, LRM tubes, Artemis
    sorted by LRM tubes, descending
    """
    # Build list
    mech_list = create_mech_list(file_list, select_l, create_missile_list_item)

    # Sort by speed
    mech_list.sort(key=itemgetter(3), reverse=True)

    # Print output
    print header
    print "Name                          Tons BV   LRM Artemis"
    for i in mech_list:
        print ("%-30s %3d %4d %3d %3s" % (i[0], i[1], i[2], i[3], i[4]))


def create_def_list_item(mech, i):
    """
    Compile info used by print_default()
    """
    name_str = mech.name + " " + mech.model + i.name
    BV = mech.get_BV(i)
    weight = mech.weight
    source = i.source
    prod_era = conv_era(i.get_prod_era())
    return (name_str, weight, BV, source, prod_era)


def print_default(file_list, select_l, header):
    """
    Default output format

    In the form of name, weight, BV, source, era
    Intended to conform to the MUL format
    """
    # Build list
    mech_list = create_mech_list(file_list, select_l, create_def_list_item)

    # Print output
    print header
    print "Name                          Tons BV   Source   Era"
    for i in mech_list:
        print ("%-30s %3d %4d %-8s %s" % (i[0], i[1], i[2], i[3], i[4]))


####################################
##### Main program starts here #####
####################################

def main():
### Handle arguments ###
    file_list = []
    file_arg = False
    era_arg = False
    speed_arg = False
    lrm_arg = False
    output_type = ''
    select = lambda x, y: True
    select_l = []
    select_l.append(select)
    header_l = []

    for arg in sys.argv[1:]:

    ### Handle multi-arg switches ###

        # The upcoming argument is a file list, read it in
        if (file_arg):
            in_file = arg
            f = open(in_file)
            file_list_raw = f.readlines()
            f.close()
            # Strip out trailing newlines
            for file_name in file_list_raw:
                file_list.append(file_name.strip())
            file_arg = False
            continue

        # The upcoming argument is an era
        elif (era_arg):
            era = int(arg)
            select_l.append(lambda x, y: (y.get_prod_era() <= era))
            header_l.append(("available at era %s" % conv_era(era)))
            era_arg = False
            continue

        # The upcoming argument is a speed
        elif (speed_arg):
            spd = int(arg)
            select_l.append(lambda x, y: (max(x.get_walk(), y.get_jump()) >= spd))
            header_l.append(("with at least speed %d" % spd))
            speed_arg = False
            continue

        # The upcoming argument is a lrm tube count
        elif (lrm_arg):
            lrm = int(arg)
            select_l.append(lambda x, y: (y.gear.LRMs >= lrm))
            header_l.append(("with at least %d lrm tubes" % lrm))
            lrm_arg = False
            continue

    ### Input switches ###

        # If first argument is -f, read input list from file,
        elif arg == "-f":
            file_arg = True
            continue

    ### Output types ###

        # BV summary output
        elif arg == '-b':
            output_type = 'b'
            continue

        # Armor summary output
        elif arg == '-a':
            output_type = 'a'
            continue

        # Speed summary output
        elif arg == '-s':
            output_type = 's'
            continue

        # LRM summary output
        elif arg == '-l':
            output_type = 'l'
            continue

    ### Selectors ###

        # TAG filter
        elif arg == '-t':
            select_l.append(lambda x, y: y.gear.has_tag)
            header_l.append("with TAG")
            continue
        # C3 slave filter
        elif arg == '-c':
            select_l.append(lambda x, y: y.gear.has_c3)
            header_l.append("with C3 Slave")
            continue
        # C3 master filter
        elif arg == '-cm':
            select_l.append(lambda x, y: y.gear.has_c3m)
            header_l.append("with C3 Master")
            continue
        # C3i filter
        elif arg == '-ci':
            select_l.append(lambda x, y: y.gear.has_c3i)
            header_l.append("with C3i")
            continue
        # Narc filter
        elif arg == '-n':
            select_l.append(lambda x, y: y.gear.has_narc)
            header_l.append("with Narc")
            continue
        # IS filter
        elif arg == '-i':
            select_l.append(lambda x, y: x.techbase == "Inner Sphere")
            header_l.append("Inner Sphere-tech")
            continue
        # Clan filter
        elif arg == '-cl':
            select_l.append(lambda x, y: x.techbase == "Clan")
            header_l.append("Clan-tech")
            continue
        # Command console filter
        elif arg == '-cc':
            select_l.append(lambda x, y: x.cockpit.console == "TRUE")
            header_l.append("with Command Console")
            continue
        # Era filter
        elif arg == '-e':
            era_arg = True
            continue
        # Speed filter
        elif arg == '-sf':
            speed_arg = True
            continue
        # Speed filter
        elif arg == '-lrm':
            lrm_arg = True
            continue
        # otherwise read in each argument as a mech file
        else:
            file_list.append(''.join(arg))
            print file_list

### Process output ###

    # Construct header
    header = create_header(header_l)

    if output_type == 'b':
        print_bv_list(file_list, select_l, header)
    elif output_type == 'a':
        print_armor_list(file_list, select_l, header)
    elif output_type == 's':
        print_speed_list(file_list, select_l, header)
    elif output_type == 'l':
        print_missile_list(file_list, select_l, header)
    else:
        print_default(file_list, select_l, header)

if __name__ == "__main__":
    main()
