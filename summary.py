#!/usr/bin/python

# Prints out a one-line summary of a mech
# Should later be made able to handle multiple files

import sys
from xml.dom import minidom
from mech import *
from armor import *
from engine import *

# Loop over input
for i in sys.argv[1:]:
    # Read file
    fsock = open(i)
    xmldoc = minidom.parse(fsock)
    fsock.close()

    # Get mech
    mech = Mech(xmldoc)

    name_str = mech.name + " " + mech.model
    move = mech.engine.get_move_string()
    print ("%-22s %3s %s" % (name_str, mech.weight, move))
