#!/usr/bin/python

# Prints out a one-line summary of a mech
# Should later be made able to handle multiple files

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
def print_BV_list(file_list):
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
                mech_list.append((name_str, BV, weight, BV_t))
        else:
            name_str = mech.name + " " + mech.model
            BV = mech.get_BV(mech.load)
            weight = mech.weight
            BV_t = float(BV)/float(weight)
            mech_list.append((name_str, BV, weight, BV_t))

    # Sort by BV/ton
    mech_list.sort(key=itemgetter(3), reverse=True)

    # Print output
    print "Name                       BV   Wgt BV/Wgt"
    for i in mech_list:
        print ("%-26s %4d %3d %.2f" % (i[0], i[1], i[2], i[3]))


# TAG_list output
#
# In the form of name, BV, weight, BV/weight
# sorted by BV/weight, descending
#
def print_TAG_list(file_list):
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
                if i.gear.has_tag:
                    mech_list.append((name_str, BV, weight, BV_t))
        else:
            name_str = mech.name + " " + mech.model
            BV = mech.get_BV(mech.load)
            weight = mech.weight
            BV_t = float(BV)/float(weight)
            if mech.load.gear.has_tag:
                mech_list.append((name_str, BV, weight, BV_t))

    # Sort by BV/ton
    mech_list.sort(key=itemgetter(3), reverse=True)

    # Print output
    print "Mechs with TAG:"
    print "Name                       BV   Wgt BV/Wgt"
    for i in mech_list:
        print ("%-26s %4d %3d %.2f" % (i[0], i[1], i[2], i[3]))


# C3_list output
#
# In the form of name, BV, weight, BV/weight
# sorted by BV/weight, descending
#
def print_C3_list(file_list):
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
                if i.gear.has_c3:
                    mech_list.append((name_str, BV, weight, BV_t))
        else:
            name_str = mech.name + " " + mech.model
            BV = mech.get_BV(mech.load)
            weight = mech.weight
            BV_t = float(BV)/float(weight)
            if mech.load.gear.has_c3:
                mech_list.append((name_str, BV, weight, BV_t))

    # Sort by BV/ton
    mech_list.sort(key=itemgetter(3), reverse=True)

    # Print output
    print "Mechs with C3 Slave:"
    print "Name                       BV   Wgt BV/Wgt"
    for i in mech_list:
        print ("%-26s %4d %3d %.2f" % (i[0], i[1], i[2], i[3]))


# C3 Master list output
#
# In the form of name, BV, weight, BV/weight
# sorted by BV/weight, descending
#
def print_C3M_list(file_list):
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
                if i.gear.has_c3m:
                    mech_list.append((name_str, BV, weight, BV_t))
        else:
            name_str = mech.name + " " + mech.model
            BV = mech.get_BV(mech.load)
            weight = mech.weight
            BV_t = float(BV)/float(weight)
            if mech.load.gear.has_c3m:
                mech_list.append((name_str, BV, weight, BV_t))

    # Sort by BV/ton
    mech_list.sort(key=itemgetter(3), reverse=True)

    # Print output
    print "Mechs with C3 Master:"
    print "Name                       BV   Wgt BV/Wgt"
    for i in mech_list:
        print ("%-26s %4d %3d %.2f" % (i[0], i[1], i[2], i[3]))


# C3i_list output
#
# In the form of name, BV, weight, BV/weight
# sorted by BV/weight, descending
#
def print_C3i_list(file_list):
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
                if i.gear.has_c3i:
                    mech_list.append((name_str, BV, weight, BV_t))
        else:
            name_str = mech.name + " " + mech.model
            BV = mech.get_BV(mech.load)
            weight = mech.weight
            BV_t = float(BV)/float(weight)
            if mech.load.gear.has_c3i:
                mech_list.append((name_str, BV, weight, BV_t))

    # Sort by BV/ton
    mech_list.sort(key=itemgetter(3), reverse=True)

    # Print output
    print "Mechs with C3i:"
    print "Name                       BV   Wgt BV/Wgt"
    for i in mech_list:
        print ("%-26s %4d %3d %.2f" % (i[0], i[1], i[2], i[3]))


# Narc_list output
#
# In the form of name, BV, weight, BV/weight
# sorted by BV/weight, descending
#
def print_Narc_list(file_list):
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
                if i.gear.has_narc:
                    mech_list.append((name_str, BV, weight, BV_t))
        else:
            name_str = mech.name + " " + mech.model
            BV = mech.get_BV(mech.load)
            weight = mech.weight
            BV_t = float(BV)/float(weight)
            if mech.load.gear.has_narc:
                mech_list.append((name_str, BV, weight, BV_t))

    # Sort by BV/ton
    mech_list.sort(key=itemgetter(3), reverse=True)

    # Print output
    print "Mechs with Narc:"
    print "Name                       BV   Wgt BV/Wgt"
    for i in mech_list:
        print ("%-26s %4d %3d %.2f" % (i[0], i[1], i[2], i[3]))


# Default output format, in flux
def print_default(file_list):
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
                print ("%-26s %3s %-11s %4s %4s" % (name_str2, mech.weight, move, armor, BV))
        else:
            BV = mech.get_BV(mech.load)
            print ("%-26s %3s %-11s %4s %4s" % (name_str, mech.weight, move, armor, BV))
#        print ("%-26s %3s %-11s %4s %4s %s" % (name_str, mech.weight, move, armor, BV, percent))


####################################
##### Main program starts here #####
####################################

### Handle arguments ###
file_list = []
file_arg = False
output_type = 's'

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
    # TAG summary output
    elif arg == '-t':
        output_type = 't'
        continue
    # C3 slave summary output
    elif arg == '-c':
        output_type = 'c'
        continue
    # C3 master summary output
    elif arg == '-cm':
        output_type = 'cm'
        continue
    # C3i summary output
    elif arg == '-ci':
        output_type = 'ci'
        continue
    # Narc summary output
    elif arg == '-n':
        output_type = 'n'
        continue
    # otherwise read in each argument as a mech file
    else:
        file_list.append(''.join(arg))
        print file_list

### Process output ###

if output_type == 'b':
    print_BV_list(file_list)
elif output_type == 't':
    print_TAG_list(file_list)
elif output_type == 'c':
    print_C3_list(file_list)
elif output_type == 'cm':
    print_C3M_list(file_list)
elif output_type == 'ci':
    print_C3i_list(file_list)
elif output_type == 'n':
    print_Narc_list(file_list)
else:
    print_default(file_list)

