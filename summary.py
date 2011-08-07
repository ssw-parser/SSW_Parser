#!/usr/bin/python

# Prints out a one-line summary of a mech
# Should later be made able to handle multiple files

import sys
import string
from xml.dom import minidom
from mech import *
from defensive import *
from movement import *

# If first argument is -f, read input list from file,
if sys.argv[1] == "-f":
    in_file = sys.argv[2]
    f = open(in_file)
    file_list_raw = f.readlines()
    f.close()
    # Strip out trailing newlines
    file_list = map(string.strip, file_list_raw)
# otherwise read in each argument as a mech file
else:
    file_list = sys.argv[1:]

print "Name                       Wgt Movement    Armor  BV Mot   Def   Off"
# Loop over input
for i in file_list:
    # Read file
    fsock = open(i)
    xmldoc = minidom.parse(fsock)
    fsock.close()

    # Get mech
    mech = Mech(xmldoc)

    name_str = mech.name + " " + mech.model
    move = mech.engine.get_move_string()
    armor = mech.armor.get_armor_percent()
    BV = mech.BV
    percent = mech.weight_summary(True)
#    print ("%-26s %3s %-11s %4s %4s" % (name_str, mech.weight, move, armor, BV))
    print ("%-26s %3s %-11s %4s %4s %s" % (name_str, mech.weight, move, armor, BV, percent))
