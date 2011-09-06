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

# Prints out a one-line summary of a mech

import sys
import string
from xml.dom import minidom
from operator import itemgetter
from mech import *
from defensive import *
from movement import *


#############################
##### Utility functions #####
#############################

# Convert era to string
#
# TODO: Add missing eras: AoW, SL, Rep, DA
#
def conv_era(era):
    conv = {
        2 : "SW-E",
        3 : "SW-L",
        4 : "Clan",
        5 : "CW",
        6 : "Jihad"
        }
    return conv[era]
    

# Load mech from file
#
# Takes a file name as argument, returns a mech object
#
def load_mech(file_name):
    # Read file
    fsock = open(file_name)
    xmldoc = minidom.parse(fsock)
    fsock.close()

    # Get mech
    return Mech(xmldoc)


###############################
##### Mech entry creation #####
###############################

# Create a list of mechs
#
# file_list is the list of files containing mech info
# select is the selection criteria
# creator specifies which items should be included
# Note that item 0 is always supposed to be the name,
# item 1 is supposed to be BV, and item 2 is supposed to be Weight
#
def create_mech_list(file_list, select_l, creator):
    mech_list =[]
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
    mech_list.sort(key=itemgetter(2))

    return mech_list


###################################
##### Output format functions #####
###################################

# BV_list output
#
# In the form of name, BV, weight, BV/weight, Era
# sorted by BV/weight, descending
#
def create_BV_list_item(mech, i):
    name_str = mech.name + " " + mech.model + i.name
    BV = mech.get_BV(i)
    weight = mech.weight
    BV_t = float(BV)/float(weight)
    pe = conv_era(i.get_prod_era())
    return (name_str, BV, weight, BV_t, pe)

def print_BV_list(file_list, select_l, header):
    # Build list
    mech_list = create_mech_list(file_list, select_l, create_BV_list_item)

    # Sort by BV/ton
    mech_list.sort(key=itemgetter(3), reverse=True)

    # Print output
    print header
    print "Name                           BV   Wgt BV/Wt Era"
    for i in mech_list:
        print ("%-30s %4d %3d %.2f %s" % (i[0], i[1], i[2], i[3], i[4]))


# armor_list output
#
# In the form of name, BV, weight, Armor%, Explosive, Stealth
# sorted by armor%, descending
#
def create_armor_list_item(mech, i):
    name_str = mech.name + " " + mech.model + i.name
    BV = mech.get_BV(i)
    weight = mech.weight
    armor = mech.armor.get_armor_percent()
    exp = i.gear.get_ammo_exp_BV(mech.engine) + i.gear.get_weapon_exp_BV(mech.engine)
    if exp < 0:
        e_str = "EXP"
    else:
        e_str = ""
    sth = mech.get_stealth()
    if sth:
        s_str = "STH"
    else:
        s_str = ""
    return (name_str, BV, weight, armor, e_str, s_str)

def print_armor_list(file_list, select_l, header):
    # Build list
    mech_list = create_mech_list(file_list, select_l, create_armor_list_item)

    # Sort by armor%
    mech_list.sort(key=itemgetter(3), reverse=True)

    # Print output
    print header
    print "Name                           BV   Wgt Armr Exp Sth"
    for i in mech_list:
        print ("%-30s %4d %3d %.0f%% %3s %3s" % (i[0], i[1], i[2], i[3], i[4], i[5]))


# speed_list output
#
# In the form of name, BV, weight, speed
# sorted by speed, descending
#
def create_speed_list_item(mech, i):
    name_str = mech.name + " " + mech.model + i.name
    BV = mech.get_BV(i)
    weight = mech.weight
    walk = mech.get_walk()
    run = mech.get_run()
    jump = i.get_jump()
    spd = max(walk, jump)
    return (name_str, BV, weight, spd, walk, run, jump)

def print_speed_list(file_list, select_l, header):
    # Build list
    mech_list = create_mech_list(file_list, select_l, create_speed_list_item)

    # Sort by speed
    mech_list.sort(key=itemgetter(3), reverse=True)

    # Print output
    print header
    print "Name                           BV   Wgt Speed"
    for i in mech_list:
        print ("%-30s %4d %3d %2d/%2d/%2d" % (i[0], i[1], i[2], i[4], i[5], i[6]))


# Default output format, in flux
#
# TODO: outdated code, rewrite
def print_default(file_list, select_l, header):
    print header
    print "Name                       Wgt Movement    Armor  BV Mot   Def   Off"
    # Loop over input
    for i in file_list:
        # Load mech from file
        mech = load_mech(i)

        name_str = mech.name + " " + mech.model
        move = mech.get_move_string()
        armor = mech.armor.get_armor_percent()
        #    percent = mech.weight_summary(True)
        if mech.omni == "TRUE":
            for i in mech.loads:
                BV = mech.get_BV(i)
                name_str2 = name_str + i.name
                if select(mech, i):
                    print ("%-28s %3s %-11s %.2f%% %4s" % (name_str2, mech.weight, move, armor, BV))
        else:
            BV = mech.get_BV(mech.load)
            if select(mech, mech.load):
                print ("%-28s %3s %-11s %.2f%% %4s" % (name_str, mech.weight, move, armor, BV))
#        print ("%-28s %3s %-11s %4s %4s %s" % (name_str, mech.weight, move, armor, BV, percent))


####################################
##### Main program starts here #####
####################################

### Handle arguments ###
file_list = []
file_arg = False
era_arg = False
speed_arg = False
output_type = ''
select = lambda x, y: True
select_l = []
select_l.append(select)
header = ""

for arg in sys.argv[1:]:

    ### Handle multi-arg switches ###
    # The upcoming argument is a file list, read it in
    if (file_arg):
        in_file = arg
        f = open(in_file)
        file_list_raw = f.readlines()
        f.close()
        # Strip out trailing newlines
        file_list += map(string.strip, file_list_raw)
        file_arg = False
        continue

    # The upcoming argument is an era
    elif (era_arg):
        era = int(arg)
        select_l.append(lambda x, y: (y.get_prod_era() <= era))
        header = ("Mechs available at era %s:" % conv_era(era))
        era_arg = False
        continue

    # The upcoming argument is a speed
    elif (speed_arg):
        spd = int(arg)
        select_l.append(lambda x, y: (max(x.get_walk(), y.get_jump()) >= spd))
        header = ("Mechs with at least speed %d:" % spd)
        speed_arg = False
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

    ### Selectors ###
    # TAG filter
    elif arg == '-t':
        select_l.append(lambda x, y: y.gear.has_tag)
        header = "Mechs with TAG:"
        continue
    # C3 slave filter
    elif arg == '-c':
        select_l.append(lambda x, y: y.gear.has_c3)
        header = "Mechs with C3 Slave:"
        continue
    # C3 master filter
    elif arg == '-cm':
        select_l.append(lambda x, y: y.gear.has_c3m)
        header = "Mechs with C3 Master:"
        continue
    # C3i filter
    elif arg == '-ci':
        select_l.append(lambda x, y: y.gear.has_c3i)
        header = "Mechs with C3i:"
        continue
    # Narc filter
    elif arg == '-n':
        select_l.append(lambda x, y: y.gear.has_narc)
        header = "Mechs with Narc:"
        continue
    # IS filter
    elif arg == '-i':
        select_l.append(lambda x, y: x.techbase == "Inner Sphere")
        header = "Inner Sphere-tech Mechs:"
        continue
    # Clan filter
    elif arg == '-cl':
        select_l.append(lambda x, y: x.techbase == "Clan")
        header = "Clan-tech Mechs:"
        continue
    # Command console filter
    elif arg == '-cc':
        select_l.append(lambda x, y: x.cockpit.console == "TRUE")
        header = "Mechs with Command Console:"
        continue
    # Era filter
    elif arg == '-e':
        era_arg = True
        continue
    # Speed filter
    elif arg == '-sf':
        speed_arg = True
        continue
    # otherwise read in each argument as a mech file
    else:
        file_list.append(''.join(arg))
        print file_list

### Process output ###

if output_type == 'b':
    print_BV_list(file_list, select_l, header)
elif output_type == 'a':
    print_armor_list(file_list, select_l, header)
elif output_type == 's':
    print_speed_list(file_list, select_l, header)
else:
    print_default(file_list, select_l, header)

