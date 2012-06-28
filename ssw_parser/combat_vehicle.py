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

from util import get_child_data

class CombatVehicle:
    """
    A master class holding info about a combat vehicle.
    """
    def __init__(self, xmldoc):

        # Get top-level structure data
        for cveh in xmldoc.getElementsByTagName('combatvehicle'):
            self.model = cveh.attributes.["model"].value
            self.name = cveh.attributes.["name"].value
            self.motive = cveh.attributes.["motive"].value
            self.omni = cveh.attributes.["omni"].value
            self.weight = int(cveh.attributes.["tons"].value)

            # Get BV. Should give prime variant BV for Omni-vehicles
            # get first instance only to avoid problems with Omni-vehicles
            self.batt_val = int(get_child_data(cveh, 'battle_value'))

            # Get Cost.
            cost = float(get_child_data(cveh, 'cost'))

            # Get production era
            self.prod_era = int(get_child_data(cveh, 'productionera'))

            # Get techbase (IS, Clan)
            # get first instance only to avoid problems with Omni-vehicles
            self.techbase = get_child_data(cveh, 'techbase')
