#!/usr/bin/python
# coding: utf-8

# Prints out a one-line summary of a mech
# Should later be made able to handle multiple files

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

import sys
import string
from xml.dom import minidom
from operator import itemgetter
from mech import *
from defensive import *
from movement import *

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

# BV_list output
#
# In the form of name, BV, weight, BV/weight
# sorted by BV/weight, descending
#
def print_BV_list(file_list, select, header):
    mech_list =[]
    # Loop over input
    for i in file_list:
        # Load mech from file
        mech = load_mech(i)

        # Construct data
        if mech.omni == "TRUE":
            for i in mech.loads:
                name_str = mech.name + " " + mech.model + i.name
                BV = mech.get_BV(i)
                weight = mech.weight
                BV_t = float(BV)/float(weight)
                pe = mech.get_prod_era()
                if select(mech, i):
                    mech_list.append((name_str, BV, weight, BV_t, pe))
        else:
            name_str = mech.name + " " + mech.model
            BV = mech.get_BV(mech.load)
            weight = mech.weight
            BV_t = float(BV)/float(weight)
            pe = mech.get_prod_era()
	    if select(mech, mech.load):
		    mech_list.append((name_str, BV, weight, BV_t, pe))

    # Sort by BV/ton
    mech_list.sort(key=itemgetter(3), reverse=True)

    # Print output
    print header
    print "Name                           BV   Wgt BV/Wt Era"
    for i in mech_list:
        print ("%-30s %4d %3d %.2f %s" % (i[0], i[1], i[2], i[3], i[4]))


# armor_list output
#
# In the form of name, BV, weight, BV/weight
# sorted by BV/weight, descending
#
def print_armor_list(file_list, select, header):
    mech_list =[]
    # Loop over input
    for i in file_list:
        # Load mech from file
        mech = load_mech(i)

        # Construct data
        if mech.omni == "TRUE":
            for i in mech.loads:
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
                if select(mech, i):
                    mech_list.append((name_str, BV, weight, armor, e_str, s_str))
        else:
            name_str = mech.name + " " + mech.model
            BV = mech.get_BV(mech.load)
            weight = mech.weight
            BV_t = float(BV)/float(weight)
            armor = mech.armor.get_armor_percent()
            exp = mech.load.gear.get_ammo_exp_BV(mech.engine) + mech.load.gear.get_weapon_exp_BV(mech.engine)
            if exp < 0:
                e_str = "EXP"
            else:
                e_str = ""
            sth = mech.get_stealth()
            if sth:
                s_str = "STH"
            else:
                s_str = ""
            if select(mech, mech.load):
                mech_list.append((name_str, BV, weight, armor, e_str, s_str))

    # Sort by armor%
    mech_list.sort(key=itemgetter(3), reverse=True)

    # Print output
    print header
    print "Name                           BV   Wgt Armr Exp Sth"
    for i in mech_list:
        print ("%-30s %4d %3d %.0f%% %3s %3s" % (i[0], i[1], i[2], i[3], i[4], i[5]))


# Default output format, in flux
def print_default(file_list, select, header):
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
output_type = 's'
select = lambda x, y: True
header = ""

for arg in sys.argv[1:]:
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
    # If first argument is -f, read input list from file,
    elif arg == "-f":
        file_arg = True
        continue
    # BV summary output
    elif arg == '-b':
        output_type = 'b'
        continue
    # Armor summary output
    elif arg == '-a':
        output_type = 'a'
        continue
    # TAG summary output
    elif arg == '-t':
        select = lambda x, y: y.gear.has_tag
        header = "Mechs with TAG:"
        continue
    # C3 slave summary output
    elif arg == '-c':
        select = lambda x, y: y.gear.has_c3
        header = "Mechs with C3 Slave:"
        continue
    # C3 master summary output
    elif arg == '-cm':
        select = lambda x, y: y.gear.has_c3m
        header = "Mechs with C3 Master:"
        continue
    # C3i summary output
    elif arg == '-ci':
        select = lambda x, y: y.gear.has_c3i
        header = "Mechs with C3i:"
        continue
    # Narc summary output
    elif arg == '-n':
        select = lambda x, y: y.gear.has_narc
        header = "Mechs with Narc:"
        continue
    # IS summary output
    elif arg == '-i':
        select = lambda x, y: x.techbase == "Inner Sphere"
        header = "Inner Sphere-tech Mechs:"
        continue
    # Clan summary output
    elif arg == '-cl':
        select = lambda x, y: x.techbase == "Clan"
        header = "Clan-tech Mechs:"
        continue
    # Command console summary output
    elif arg == '-cc':
        select = lambda x, y: x.cockpit.console == "TRUE"
        header = "Mechs with Command Console:"
        continue
    # otherwise read in each argument as a mech file
    else:
        file_list.append(''.join(arg))
        print file_list

### Process output ###

if output_type == 'b':
    print_BV_list(file_list, select, header)
elif output_type == 'a':
    print_armor_list(file_list, select, header)
else:
    print_default(file_list, select, header)

