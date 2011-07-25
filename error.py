#!/usr/bin/python

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
