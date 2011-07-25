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

# Name, year, BV multiplier
#
# Missing: Industrial, Heavy Industrial, Commericial, TO armor
armor = [["Standard Armor", 2470, 1.0],
         ["Ferro-Fibrous", 2571, 1.0],
         ["Light Ferro-Fibrous", 3067, 1.0],
         ["Heavy Ferro-Fibrous", 3069, 1.0],
         ["Stealth Armor", 3063, 1.0]]



# A class to hold armor info for a mech
class Armor:
    def __init__(self, atype, hd, ct, ctr, lt, ltr, rt, rtr, la, ra, ll, rl):
        self.atype = atype
        self.hd = hd
        self.ct = ct
        self.ctr = ctr
        self.lt = lt
        self.ltr = ltr
        self.rt = rt
        self.rtr = rtr
        self.la = la
        self.ra = ra
        self.ll = ll
        self.rl = rl
        self.armortotal = self.hd + self.ct + self.ctr + self.lt + self.ltr + self.rt + self.rtr + self.la + self.ra + self.ll + self.rl

    # Return armor BV
    def get_armor_BV(self):
        id = 0
        arBV = 0
        for i in armor:
            if self.atype == i[0]:
                arBV = i[2]
                id = 1
        if id == 0:
            error_exit(clist.name)
        return (arBV * 2.5 * self.armortotal)
       

    # Return earliest year armor is available
    def get_armor_year(self):
        id = 0
        for i in armor:
            if i[0] == self.atype:
                id = 1
                return i[1]
        if id == 0:
            error_exit(self.atype)

    # Print a report of the armor in a cetain location in the form:
    # Location: armor/max xx%
    def print_report(self, loc, armor, maxa):
        ratio = float(armor) / float(maxa)
        msg = loc + ": " + str(armor) + "/" + str(maxa) + " " + str(int(ratio * 100)) + " %"
        print msg

    def head_report(self):
        self.print_report("Head", self.hd, 9)
        if (self.hd < 8):
            st1 = "WARNING: 10-points hits will head-cap!"
            st2 = "  Head armor: " + str(self.hd)
            warnings.add((st1, st2))
            print_warning((st1, st2))

    def center_torso_report(self, weight):
        maxa = ctIS[weight] * 2
        self.print_report("Center Torso front", self.ct, maxa)
        if (self.ct < ctIS[weight]):
            st1 = "WARNING: Weak center torso armor!"
            st2 = "  Center torso armor: " + str(self.ct)
            warnings.add((st1, st2))
            print_warning((st1, st2))
        self.print_report("Center Torso rear", self.ctr, maxa)
         # Falling damage
        fall_dam = ceil(weight / 10.0)
        if (self.ctr < fall_dam):
            st1 = "WARNING: Falling damage might go internal on center torso rear armor!"
            st2 = "  Damage: " + str(fall_dam) + ", armor: " + str(self.ctr)
            warnings.add((st1, st2))
            print_warning((st1, st2))
        self.print_report("Center Torso total", (self.ct + self.ctr), maxa)

    def left_torso_report(self, weight):
        maxa = stIS[weight] * 2
        self.print_report("Left Torso front", self.lt, maxa)
        if (self.lt < stIS[weight]):
            st1 = "WARNING: Weak left torso armor!"
            st2 = "  Left torso armor: " + str(self.lt)
            warnings.add((st1, st2))
            print_warning((st1, st2))
        self.print_report("Left Torso rear", self.ltr, maxa)
        # Falling damage
        fall_dam = ceil(weight / 10.0)
        if (self.ltr < fall_dam):
            st1 = "WARNING: Falling damage might go internal on left torso rear armor!"
            st2 = "  Damage: " + str(fall_dam) + ", armor: " + str(self.ltr)
            warnings.add((st1, st2))
            print_warning((st1, st2))
        self.print_report("Left Torso total", (self.lt + self.ltr), maxa)

    def right_torso_report(self, weight):
        maxa = stIS[weight] * 2
        self.print_report("Right Torso front", self.rt, maxa)
        if (self.rt < stIS[weight]):
            st1 = "WARNING: Weak right torso armor!"
            st2 = "  Right torso armor: " + str(self.rt)
            warnings.add((st1, st2))
            print_warning((st1, st2))
        self.print_report("Right Torso rear", self.rtr, maxa)
        # Falling damage
        fall_dam = ceil(weight / 10.0)
        if (self.rtr < fall_dam):
            st1 = "WARNING: Falling damage might go internal on right torso rear armor!"
            st2 = "  Damage: " + str(fall_dam) + ", armor: " + str(self.rtr)
            warnings.add((st1, st2))
            print_warning((st1, st2))
        self.print_report("Right Torso total", (self.rt + self.rtr), maxa)

    def left_leg_report(self, weight, motive):
        maxa = legIS[weight] * 2
        if motive == "Quad":
            self.print_report("Rear Left Leg", self.ll, maxa)
        elif motive == "Biped":
            self.print_report("Left Leg", self.ll, maxa)
        else:
            error_exit(mech.motive)
        if ((self.ll < legIS[weight])):
            st1 = "WARNING: Weak left leg armor!"
            st2 =  "  Left leg armor: " + str(self.ll)
            warnings.add((st1, st2))
            print_warning((st1, st2))

    def right_leg_report(self, weight, motive):
        maxa = legIS[weight] * 2
        if motive == "Quad":
            self.print_report("Rear Right Leg", self.rl, maxa)
        elif motive == "Biped":
            self.print_report("Right Leg", self.rl, maxa)
        else:
            error_exit(mech.motive)
        if (self.rl < legIS[weight]):
            st1 = "WARNING: Weak right leg armor!"
            st2 =  "  Right leg armor: " + str(self.rl)
            warnings.add((st1, st2))
            print_warning((st1, st2))

    def left_arm_report(self, weight, motive):
        if motive == "Quad":
            maxa = legIS[weight] * 2
            self.print_report("Front Left Leg", self.la, maxa)
            if (self.la < legIS[weight]):
                st1 =  "WARNING: Weak left front leg armor!"
                st2 =  "  Left front leg armor: " + str(self.la)
                warnings.add((st1, st2))
                print_warning((st1, st2))
        elif motive == "Biped":
            maxa = armIS[weight] * 2
            self.print_report("Left Arm", self.la, maxa)
            if (self.la < armIS[weight]):
                st1 = "WARNING: Weak left arm armor!"
                st2 = "  Left arm armor: " +  str(self.la)
                warnings.add((st1, st2))
                print_warning((st1, st2))
        else:
            error_exit(mech.motive)

    def right_arm_report(self, weight, motive):
        if motive == "Quad":
            maxa = legIS[weight] * 2
            self.print_report("Front Right Leg", self.ra, maxa)
            if (self.ra < legIS[weight]):
                st1 =  "WARNING: Weak right front leg armor!"
                st2 =  "  Right front leg armor: " + str(self.ra)
                warnings.add((st1, st2))
                print_warning((st1, st2))
        elif motive == "Biped":
            maxa = armIS[weight] * 2
            self.print_report("Right Arm", self.ra, maxa)
            if (self.ra < armIS[weight]):
                st1 = "WARNING: Weak right arm armor!"
                st2 = "  Right arm armor: " +  str(self.ra)
                warnings.add((st1, st2))
                print_warning((st1, st2))
        else:
            error_exit(mech.motive)

    def armor_total_report(self, w, motive):
        # Commented out calculates tonnage with standard armor
        #    print atype, armor, "pts", int(round(float(armor)/30))
        if motive == "Quad":
            maxa = 2*ctIS[w] + 4*stIS[w] + 8*legIS[w] + 9
        elif motive == "Biped":
            maxa = 2*ctIS[w] + 4*stIS[w] + 4*legIS[w] + 4*armIS[w] + 9
        else:
            error_exit(mech.motive)
        self.print_report(self.atype, self.armortotal, maxa)

    def parse_armor(self, weight, motive):
        self.armor_total_report(weight, motive)
        self.head_report()
        self.center_torso_report(weight)
        self.left_torso_report(weight)
        self.right_torso_report(weight)
        self.left_leg_report(weight, motive)
        self.right_leg_report(weight, motive)
        self.left_arm_report(weight, motive)
        self.right_arm_report(weight, motive)





