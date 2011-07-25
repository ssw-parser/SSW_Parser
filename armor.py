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

# A class to hold info about the armor in one location
class Armor_loc:
    def __init__(self, armor, maximum):
        self.a = armor
        self.m = maximum
        assert self.a <= self.m, "More than maximum armor!"

# A class to hold armor info for a mech
class Armor:
    def __init__(self, weight, motive, atype,
                 hd, ct, ctr, lt, ltr, rt, rtr, la, ra, ll, rl):
        # Save type of armor
        self.atype = atype

        # Head always have max 9 armor
        self.hd = Armor_loc(hd, 9)

        # Otherwise 2 times Internal Structure
        self.ct = Armor_loc(ct, ctIS[weight] * 2);
        self.ctr = Armor_loc(ctr, ctIS[weight] * 2);
        self.lt = Armor_loc(lt, stIS[weight] * 2);
        self.ltr = Armor_loc(ltr, stIS[weight] * 2);
        self.rt = Armor_loc(rt, stIS[weight] * 2);
        self.rtr = Armor_loc(rtr, stIS[weight] * 2);

        # The arms/front legs need to check if mech is Biped or Quad
        if motive == "Quad":
            self.la = Armor_loc(la, legIS[weight] * 2);
        elif motive == "Biped":
            self.la = Armor_loc(la, armIS[weight] * 2);
        if motive == "Quad":
            self.ra = Armor_loc(ra, legIS[weight] * 2);
        elif motive == "Biped":
            self.ra = Armor_loc(ra, armIS[weight] * 2);

        # Legs are normal
        self.ll = Armor_loc(ll, legIS[weight] * 2);
        self.rl = Armor_loc(rl, legIS[weight] * 2);

        # Last sum up total
        self.armortotal = self.hd.a + self.ct.a + self.ctr.a + self.lt.a + self.ltr.a + self.rt.a + self.rtr.a + self.la.a + self.ra.a + self.ll.a + self.rl.a


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
        self.print_report("Head", self.hd.a, 9)
        if (self.hd.a < 8):
            st1 = "WARNING: 10-points hits will head-cap!"
            st2 = "  Head armor: " + str(self.hd.a)
            warnings.add((st1, st2))
            print_warning((st1, st2))

    def center_torso_report(self, weight):
        maxa = ctIS[weight] * 2
        self.print_report("Center Torso front", self.ct.a, maxa)
        if (self.ct.a < ctIS[weight]):
            st1 = "WARNING: Weak center torso armor!"
            st2 = "  Center torso armor: " + str(self.ct.a)
            warnings.add((st1, st2))
            print_warning((st1, st2))
        self.print_report("Center Torso rear", self.ctr.a, maxa)
         # Falling damage
        fall_dam = ceil(weight / 10.0)
        if (self.ctr.a < fall_dam):
            st1 = "WARNING: Falling damage might go internal on center torso rear armor!"
            st2 = "  Damage: " + str(fall_dam) + ", armor: " + str(self.ctr.a)
            warnings.add((st1, st2))
            print_warning((st1, st2))
        self.print_report("Center Torso total", (self.ct.a + self.ctr.a), maxa)

    def left_torso_report(self, weight):
        maxa = stIS[weight] * 2
        self.print_report("Left Torso front", self.lt.a, maxa)
        if (self.lt.a < stIS[weight]):
            st1 = "WARNING: Weak left torso armor!"
            st2 = "  Left torso armor: " + str(self.lt.a)
            warnings.add((st1, st2))
            print_warning((st1, st2))
        self.print_report("Left Torso rear", self.ltr.a, maxa)
        # Falling damage
        fall_dam = ceil(weight / 10.0)
        if (self.ltr.a < fall_dam):
            st1 = "WARNING: Falling damage might go internal on left torso rear armor!"
            st2 = "  Damage: " + str(fall_dam) + ", armor: " + str(self.ltr.a)
            warnings.add((st1, st2))
            print_warning((st1, st2))
        self.print_report("Left Torso total", (self.lt.a + self.ltr.a), maxa)

    def right_torso_report(self, weight):
        maxa = stIS[weight] * 2
        self.print_report("Right Torso front", self.rt.a, maxa)
        if (self.rt.a < stIS[weight]):
            st1 = "WARNING: Weak right torso armor!"
            st2 = "  Right torso armor: " + str(self.rt.a)
            warnings.add((st1, st2))
            print_warning((st1, st2))
        self.print_report("Right Torso rear", self.rtr.a, maxa)
        # Falling damage
        fall_dam = ceil(weight / 10.0)
        if (self.rtr.a < fall_dam):
            st1 = "WARNING: Falling damage might go internal on right torso rear armor!"
            st2 = "  Damage: " + str(fall_dam) + ", armor: " + str(self.rtr.a)
            warnings.add((st1, st2))
            print_warning((st1, st2))
        self.print_report("Right Torso total", (self.rt.a + self.rtr.a), maxa)

    def left_leg_report(self, weight, motive):
        maxa = legIS[weight] * 2
        if motive == "Quad":
            self.print_report("Rear Left Leg", self.ll.a, maxa)
        elif motive == "Biped":
            self.print_report("Left Leg", self.ll.a, maxa)
        else:
            error_exit(mech.motive)
        if ((self.ll.a < legIS[weight])):
            st1 = "WARNING: Weak left leg armor!"
            st2 =  "  Left leg armor: " + str(self.ll.a)
            warnings.add((st1, st2))
            print_warning((st1, st2))

    def right_leg_report(self, weight, motive):
        maxa = legIS[weight] * 2
        if motive == "Quad":
            self.print_report("Rear Right Leg", self.rl.a, maxa)
        elif motive == "Biped":
            self.print_report("Right Leg", self.rl.a, maxa)
        else:
            error_exit(mech.motive)
        if (self.rl.a < legIS[weight]):
            st1 = "WARNING: Weak right leg armor!"
            st2 =  "  Right leg armor: " + str(self.rl.a)
            warnings.add((st1, st2))
            print_warning((st1, st2))

    def left_arm_report(self, weight, motive):
        if motive == "Quad":
            maxa = legIS[weight] * 2
            self.print_report("Front Left Leg", self.la.a, maxa)
            if (self.la.a < legIS[weight]):
                st1 =  "WARNING: Weak left front leg armor!"
                st2 =  "  Left front leg armor: " + str(self.la.a)
                warnings.add((st1, st2))
                print_warning((st1, st2))
        elif motive == "Biped":
            maxa = armIS[weight] * 2
            self.print_report("Left Arm", self.la.a, maxa)
            if (self.la.a < armIS[weight]):
                st1 = "WARNING: Weak left arm armor!"
                st2 = "  Left arm armor: " +  str(self.la.a)
                warnings.add((st1, st2))
                print_warning((st1, st2))
        else:
            error_exit(mech.motive)

    def right_arm_report(self, weight, motive):
        if motive == "Quad":
            maxa = legIS[weight] * 2
            self.print_report("Front Right Leg", self.ra.a, maxa)
            if (self.ra.a < legIS[weight]):
                st1 =  "WARNING: Weak right front leg armor!"
                st2 =  "  Right front leg armor: " + str(self.ra.a)
                warnings.add((st1, st2))
                print_warning((st1, st2))
        elif motive == "Biped":
            maxa = armIS[weight] * 2
            self.print_report("Right Arm", self.ra.a, maxa)
            if (self.ra.a < armIS[weight]):
                st1 = "WARNING: Weak right arm armor!"
                st2 = "  Right arm armor: " +  str(self.ra.a)
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





