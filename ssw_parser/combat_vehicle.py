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
Contains the master class for a combat vehicle
"""

import sys
from util import get_child_data, year_era_test
from loadout import Baseloadout

class CombatVehicle:
    """
    A master class holding info about a combat vehicle.
    """
    def __init__(self, xmldoc):

        # This is a combat vehicle
        self.type = "CV"

        # Get top-level structure data
        for cveh in xmldoc.getElementsByTagName('combatvehicle'):
            self.model = cveh.attributes["model"].value
            self.name = cveh.attributes["name"].value
            self.motive = cveh.attributes["motive"].value
            self.omni = cveh.attributes["omni"].value
            self.weight = int(cveh.attributes["tons"].value)

            # Get BV. Should give prime variant BV for Omni-vehicles
            # get first instance only to avoid problems with Omni-vehicles
            self.batt_val = int(get_child_data(cveh, 'battle_value'))

            # Motive

            # Get Cost.
            cost = float(get_child_data(cveh, 'cost'))

            # Get production era
            self.prod_era = int(get_child_data(cveh, 'productionera'))

            # Get techbase (IS, Clan)
            # get first instance only to avoid problems with Omni-vehicles
            self.techbase = get_child_data(cveh, 'techbase')

            # Get year
            self.year = int(get_child_data(cveh, 'year'))

            # Sanity check for year
            year_era_test(self.year, self.prod_era,
                          self.name + " " + self.model)

            if (self.year < 2470):
                print self.name, self.model
                print "Combat Vehicles not available before 2470!"
                sys.exit(1)

            if (self.year < 2854 and self.omni == "TRUE"):
                print self.name, self.model
                print "OmniVehicles not available before 2854!"
                sys.exit(1)

            ### Components starts here ###

            # Structure

            # Engine

            # Armor

            ### Loadout stuff starts here ###

            # Get baseloadout
            blo = cveh.getElementsByTagName('baseloadout')[0]

            # Costruct current loadout, empty name for base loadout
            self.load = Baseloadout(blo, self, self.batt_val,
                                    False, self.prod_era, cost)
