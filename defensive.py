#!/usr/bin/python

from math import ceil
from error import *

# Armor related stuff

# These four tables lists internal structure for each weight class in
# 1st: center torso, 2nd: side torsos, 3rd: arms, and 4th: legs
ctIS = {
    20 : 6,
    25 : 8,
    30 : 10,
    35 : 11,
    40 : 12,
    45 : 14,
    50 : 16,
    55 : 18,
    60 : 20,
    65 : 21,
    70 : 22,
    75 : 23,
    80 : 25,
    85 : 27,
    90 : 29,
    95 : 30,
    100 : 31
    }

stIS = {
    20 : 5,
    25 : 6,
    30 : 7,
    35 : 8,
    40 : 10,
    45 : 11,
    50 : 12,
    55 : 13,
    60 : 14,
    65 : 15,
    70 : 15,
    75 : 16,
    80 : 17,
    85 : 18,
    90 : 19,
    95 : 20,
    100 : 21
    }

armIS = {
    20 : 3,
    25 : 4,
    30 : 5,
    35 : 6,
    40 : 6,
    45 : 7,
    50 : 8,
    55 : 9,
    60 : 10,
    65 : 10,
    70 : 11,
    75 : 12,
    80 : 13,
    85 : 14,
    90 : 15,
    95 : 16,
    100 : 17
    }

legIS = {
    20 : 4,
    25 : 6,
    30 : 7,
    35 : 8,
    40 : 10,
    45 : 11,
    50 : 12,
    55 : 13,
    60 : 14,
    65 : 15,
    70 : 15,
    75 : 16,
    80 : 17,
    85 : 18,
    90 : 19,
    95 : 20,
    100 : 21
    }

# Info on internal structure types
#
# Name, techbase, year, BV multiplier, weight factor
#
# Where techbase 0 = IS, 1 = Clan, 2 = Both, 10 = unknown
#
# Missing: Industrial
structure = [["Standard Structure", 2, 2439, 1.0, 0.1],
             ["Endo-Steel", 0, 2487, 1.0, 0.05],
             ["Endo-Steel", 1, 2487, 1.0, 0.05],
             # No year given for primitive structure,
             # assume it becomes available the same year as the Mackie
             ["Primitive Structure", 0, 2439, 1.0, 0.1]]


# Info on armor types
#
# Name, techbase, year, BV multiplier, armor multiplier
#
# Where techbase 0 = IS, 1 = Clan, 2 = Both, 10 = unknown
#
# Missing: Industrial, Heavy Industrial, Commericial, TO armor
armor = [["Standard Armor", 2, 2470, 1.0, 1.0],
         ["Ferro-Fibrous", 0, 2571, 1.0, 1.12],
         ["Ferro-Fibrous", 1, 2571, 1.0, 1.2],
         ["Light Ferro-Fibrous", 0, 3067, 1.0, 1.06],
         ["Heavy Ferro-Fibrous", 0, 3069, 1.0, 1.24],
         ["Stealth Armor", 0, 3063, 1.0, 1.0],
         # No year given for primitive armor, assume it becomes available
         # the same year as the Mackie
         ["Primitive Armor", 0, 2439, 1.0, 0.67]]


# A class to hold info about the internal stucture
class IS:
    def __init__(self, istype, tb, weight, motive):
        self.type = istype
        self.tb = int(tb)
        wgt = weight

        # Check for legal structure type, save data
        id = 0
        for i in structure:
            if (i[0] == self.type and i[1] == self.tb):
                id = 1
                self.year = i[2]
                self.isBV = i[3]
                wgtf = i[4]
        if id == 0:
            error_exit((self.type, self.tb))

        # Calculate IS weight
        wgt *= wgtf
        # hack to get half-ton rounding up
        wgt *= 2
        wgt = ceil(wgt)
        wgt /= 2
        self.wgt = wgt

        # Calculate IS points
        self.points = 0

        # Head always have 3 IS
        self.points += 3

        # Otherwise get from table
        self.points += ctIS[weight];
        self.points += stIS[weight] * 2;
        self.points += legIS[weight] * 2;

        # The arms/front legs need to check if mech is Biped or Quad
        if motive == "Quad":
            self.points += legIS[weight] * 2;
        elif motive == "Biped":
            self.points += armIS[weight] * 2;
        else:
            error_exit(mech.motive)


    # Return earliest year structure is available
    def get_year(self):
        return self.year

    # Return structure weight
    def get_weight(self):
        return self.wgt

    # Return IS BV factor
    def get_BV_factor(self):
        return self.points * 1.5 * self.isBV

# A class to hold info about the armor in one location
class Armor_loc:
    def __init__(self, loc_name, armor, maximum):
        self.l_name = loc_name
        self.a = armor
        self.m = maximum
        assert self.a <= self.m, "More than maximum armor!"

    # Check if armor is at least value
    def check_value(self, value):
        return self.a >= value

    # Check if armor is at least percent of max
    def check_percent(self, percent):
        return (self.a >= self.m * percent)

    # Used if an report of armor value should be added to warnings
    def get_warning_string(self):
        st = "  " + self.l_name + " armor: " + str(self.a)
        return st

# A class to hold armor info for a mech
class Armor:
    def __init__(self, weight, motive, atype, tb,
                 hd, ct, ctr, lt, ltr, rt, rtr, la, ra, ll, rl):
        # Save type of armor
        self.atype = atype
        # and its techbase
        self.tb = int(tb)

        # Check for legal armor type, save data
        id = 0
        for i in armor:
            if (i[0] == self.atype and i[1] == self.tb):
                id = 1
                self.year = i[2]
                self.arBV = i[3]
                self.arMult = i[4]
        if id == 0:
            error_exit((self.atype, self.tb))


        # Head always have max 9 armor
        self.hd = Armor_loc("Head", hd, 9)

        # Otherwise 2 times Internal Structure
        # We store three different values for each torso part
        # to simplify the interface. Front, rear and total
        self.ctf = Armor_loc("Center Torso front", ct, ctIS[weight] * 2);
        self.ctr = Armor_loc("Center Torso rear", ctr, ctIS[weight] * 2);
        self.ct = Armor_loc("Center Torso total", ct + ctr, ctIS[weight] * 2);
        self.ltf = Armor_loc("Left Torso front", lt, stIS[weight] * 2);
        self.ltr = Armor_loc("Left Torso rear", ltr, stIS[weight] * 2);
        self.lt = Armor_loc("Left Torso total", lt + ltr, stIS[weight] * 2);
        self.rtf = Armor_loc("Right Torso front", rt, stIS[weight] * 2);
        self.rtr = Armor_loc("Right Torso rear", rtr, stIS[weight] * 2);
        self.rt = Armor_loc("Right Torso total", rt + rtr, stIS[weight] * 2);

        # The arms/front legs need to check if mech is Biped or Quad
        if motive == "Quad":
            self.la = Armor_loc("Front Left Leg", la, legIS[weight] * 2);
        elif motive == "Biped":
            self.la = Armor_loc("Left Arm", la, armIS[weight] * 2);
        else:
            error_exit(mech.motive)

        if motive == "Quad":
            self.ra = Armor_loc("Front Right Leg", ra, legIS[weight] * 2);
        elif motive == "Biped":
            self.ra = Armor_loc("Right Arm", ra, armIS[weight] * 2);
        else:
            error_exit(mech.motive)

        if motive == "Quad":
            self.ll = Armor_loc("Rear Left Leg", ll, legIS[weight] * 2);
        elif motive == "Biped":
            self.ll = Armor_loc("Left Leg", ll, legIS[weight] * 2);
        else:
            error_exit(mech.motive)

        if motive == "Quad":
            self.rl = Armor_loc("Rear Right Leg", rl, legIS[weight] * 2);
        elif motive == "Biped":
            self.rl = Armor_loc("Right Leg", rl, legIS[weight] * 2);
        else:
            error_exit(mech.motive)

        # Last sum up total
        armortotal = self.hd.a + self.ct.a + self.lt.a + self.rt.a + self.la.a + self.ra.a + self.ll.a + self.rl.a
        maxtotal = self.hd.m + self.ct.m + self.lt.m + self.rt.m + self.la.m + self.ra.m + self.ll.m + self.rl.m
        self.total = Armor_loc("Total", armortotal, maxtotal);

        # Store potential falling damage
        self.fall_dam = ceil(weight / 10.0)


    # Return armor BV
    def get_armor_BV(self):
        return (self.arBV * 2.5 * self.total.a)
       

    # Return earliest year armor is available
    def get_year(self):
        return self.year

    # Return armor weight
    def get_weight(self):
        wgt = self.total.a / (16 * self.arMult)
        # hack to get half-ton rounding up
        wgt *= 2
        wgt = ceil(wgt)
        wgt /= 2
        return wgt

    # Return armor percent
    def get_armor_percent(self):
        ratio = float(self.total.a) / float(self.total.m)
        msg = str(int(ratio * 100)) + "%"
        return msg

    # Print a report of the armor in a cetain location in the form:
    # Location: armor/max xx%
    def print_report(self, armor):
        ratio = float(armor.a) / float(armor.m)
        msg = ("%-18s: %3d/%3d %3d %%" % (armor.l_name, armor.a, armor.m, int(ratio * 100)))
        print msg

    def head_report(self):
        self.print_report(self.hd)
        if (not self.hd.check_value(8)):
            st1 = "WARNING: 10-points hits will head-cap!"
            st2 = self.hd.get_warning_string()
            warnings.add((st1, st2))
            print_warning((st1, st2))

    # Falling damage armor report
    def report_fall(self, a_loc):
        if (a_loc.a < self.fall_dam):
            st1 = "WARNING: Falling damage might go internal on " + a_loc.l_name + " armor!"
            st2 = "  Damage: " + str(self.fall_dam) + ", armor: " + str(a_loc.a)
            warnings.add((st1, st2))
            print_warning((st1, st2))

    # Standard armor location report, should be used in most cases
    # Considers an armor value of less than 50% of max to be too weak
    def report_standard(self, a_loc):
        self.print_report(a_loc)
        if (not a_loc.check_percent(0.5)):
            st1 = "WARNING: Weak " + a_loc.l_name + " armor!"
            st2 = a_loc.get_warning_string()
            warnings.add((st1, st2))
            print_warning((st1, st2))
        # Also check for falling damage, just in case
        self.report_fall(a_loc)

    def center_torso_report(self):
        # Standard for front armor
        self.report_standard(self.ctf)
        # Only falling damage check for rear
        self.print_report(self.ctr)
        self.report_fall(self.ctr)
        # No checks for total armor
        self.print_report(self.ct)

    def left_torso_report(self):
        # Standard for front armor
        self.report_standard(self.ltf)
        # Only falling damage check for rear
        self.print_report(self.ltr)
        self.report_fall(self.ltr)
        # No checks for total armor
        self.print_report(self.lt)

    def right_torso_report(self):
        # Standard for front armor
        self.report_standard(self.rtf)
        # Only falling damage check for rear
        self.print_report(self.rtr)
        self.report_fall(self.rtr)
        # No checks for total armor
        self.print_report(self.rt)

    def armor_total_report(self):
        # Commented out calculates tonnage with standard armor
        #    print atype, armor, "pts", int(round(float(armor)/30))
        if self.tb == 0:
            base = "(Inner Sphere)"
        elif self.tb == 1:
            base = "(Clan)"
        elif self.tb == 2:
            base = ""
        print str(self.get_weight()) + " tons " + self.atype + " " + base
        self.print_report(self.total)

    def parse_armor(self):
        self.armor_total_report()
        self.head_report()
        self.center_torso_report()
        self.left_torso_report()
        self.right_torso_report()
        self.report_standard(self.ll)
        self.report_standard(self.rl)
        self.report_standard(self.la)
        self.report_standard(self.ra)

# TODO: Tactical operations armor
# TODO: track crit slots used?
# - Move warnings.add & print_warning stuff outside


