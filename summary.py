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
# Should later be made able to handle multiple files



import sys
import string
from xml.dom import minidom
from operator import itemgetter
from mech import *
from defensive import *
from movement import *


# Convert era to string
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

# BV_list output
#
# In the form of name, BV, weight, BV/weight, Era
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
                pe = conv_era(i.get_prod_era())
                if select(mech, i):
                    mech_list.append((name_str, BV, weight, BV_t, pe))
        else:
            name_str = mech.name + " " + mech.model
            BV = mech.get_BV(mech.load)
            weight = mech.weight
            BV_t = float(BV)/float(weight)
            pe = conv_era(mech.load.get_prod_era())
            if select(mech, mech.load):
                mech_list.append((name_str, BV, weight, BV_t, pe))

    # Default: Sort by weight, name
    mech_list.sort(key=itemgetter(0))
    mech_list.sort(key=itemgetter(2))

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

    # Default: Sort by weight, name
    mech_list.sort(key=itemgetter(0))
    mech_list.sort(key=itemgetter(2))

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
def print_speed_list(file_list, select, header):
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
                walk = mech.get_walk()
                run = mech.get_run()
                jump = i.get_jump()
                spd = max(walk, jump)
                if select(mech, i):
                    mech_list.append((name_str, BV, weight, spd, walk, run, jump))
        else:
            name_str = mech.name + " " + mech.model
            BV = mech.get_BV(mech.load)
            weight = mech.weight
            walk = mech.get_walk()
            run = mech.get_run()
            jump = mech.load.get_jump()
            spd = max(walk, jump)
            if select(mech, mech.load):
                mech_list.append((name_str, BV, weight, spd, walk, run, jump))

    # Default: Sort by weight, name
    mech_list.sort(key=itemgetter(0))
    mech_list.sort(key=itemgetter(2))

    # Sort by speed
    mech_list.sort(key=itemgetter(3), reverse=True)

    # Print output
    print header
    print "Name                           BV   Wgt Speed"
    for i in mech_list:
        print ("%-30s %4d %3d %2d/%2d/%2d" % (i[0], i[1], i[2], i[4], i[5], i[6]))


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
era_arg = False
speed_arg = False
output_type = ''
select = lambda x, y: True
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
        select = lambda x, y: (y.get_prod_era() <= era)
        header = ("Mechs available at era %s:" % conv_era(era))
        era_arg = False
        continue

    # The upcoming argument is a speed
    elif (speed_arg):
        spd = int(arg)
        select = lambda x, y: (max(x.get_walk(), y.get_jump()) >= spd)
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
        select = lambda x, y: y.gear.has_tag
        header = "Mechs with TAG:"
        continue
    # C3 slave filter
    elif arg == '-c':
        select = lambda x, y: y.gear.has_c3
        header = "Mechs with C3 Slave:"
        continue
    # C3 master filter
    elif arg == '-cm':
        select = lambda x, y: y.gear.has_c3m
        header = "Mechs with C3 Master:"
        continue
    # C3i filter
    elif arg == '-ci':
        select = lambda x, y: y.gear.has_c3i
        header = "Mechs with C3i:"
        continue
    # Narc filter
    elif arg == '-n':
        select = lambda x, y: y.gear.has_narc
        header = "Mechs with Narc:"
        continue
    # IS filter
    elif arg == '-i':
        select = lambda x, y: x.techbase == "Inner Sphere"
        header = "Inner Sphere-tech Mechs:"
        continue
    # Clan filter
    elif arg == '-cl':
        select = lambda x, y: x.techbase == "Clan"
        header = "Clan-tech Mechs:"
        continue
    # Command console filter
    elif arg == '-cc':
        select = lambda x, y: x.cockpit.console == "TRUE"
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
    print_BV_list(file_list, select, header)
elif output_type == 'a':
    print_armor_list(file_list, select, header)
elif output_type == 's':
    print_speed_list(file_list, select, header)
else:
    print_default(file_list, select, header)

