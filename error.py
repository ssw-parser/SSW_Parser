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



# Handle error and warning messages

import sys

# Exit because of unknown component
def error_exit(msg):
    print "WARNING: Unknown", msg, "!"
    sys.exit(1)

# Print warnings directly
def print_warning(strings):
    for i in strings:
        if i != "":
            print i

# A class to store warning messages
class Warnings:
    def __init__(self):
        self.list = []

    def add(self, strings):
        self.list.append(strings)

    def print_warnings(self):
        if self.list != []:
            for i in self.list:
                for j in i:
                    if j != "":
                        print j

# Create global warnings storage
warnings = Warnings()
