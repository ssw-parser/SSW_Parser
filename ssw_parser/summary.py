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
summary.py
==========
Prints out one-line summaries of units.

Note that this is one of the top-level modules that contains a main() function.
"""

import argparse
#import os
import sys
from xml.dom import minidom
from operator import itemgetter
from mech import Mech
from combat_vehicle import CombatVehicle
from weapon_list import LRM_LIST, SRM_LIST, AC_LIST
from battle_force import BattleForce
from util import conv_era
from summary_view import print_default, print_bv_list
from summary_view import print_armor_list, print_speed_list
from summary_view import print_electronics_list, print_weapon_list
from summary_view import print_timeline_list
from summary_view import print_missile_list, print_srm_list
from summary_view import print_autocannon_list, print_std_list
from summary_view import print_headcap_list, print_battle_force_list
from summary_view import print_damage_range_list, print_type_list
from summary_view import print_cost_list, print_weight_list
from type import Type


#############################
##### Utility functions #####
#############################


def conv_rules(rule, form):
    """
    Convert rules level to string.

    :param rule: rules level
    :type rule: int
    :param form: formating type
    :type form: int
    :return: rules level as 3-character string, or longer string
    :rtype: string

    Return is three character if form is 0, else it is a longer string.
    """
    conv_s = {
        0: "Int",
        1: "T-L",
        2: "Adv",
        3: "Exp",
        4: "Pri"
        }

    conv_l = {
        0: "Intro-Tech",
        1: "Tournament-Legal",
        2: "Advanced Rules",
        3: "Experimental Rules",
        4: "Primitive"
        }

    if form == 0:
        return conv_s[rule]
    else:
        return conv_l[rule]


def load_unit(file_name):
    """
    Load unit from file

    :param file_name: file name
    :type file_name: string
    :return: Loaded and constructed unit
    :rtype: Unit object

    Takes a file name as argument, returns a mech or combat vehicle object.
    """
    # Read file
    fsock = open(file_name)
    xmldoc = minidom.parse(fsock)
    fsock.close()

    # Get mech
    if file_name[-4:] == ".ssw":
        return Mech(xmldoc)
    # Get Combat Vehicle
    elif file_name[-4:] == ".saw":
        return CombatVehicle(xmldoc)
    else:
        print "Unknown file extension: ", file_name
        sys.exit(1)


###############################
##### Unit entry creation #####
###############################

def create_unit_list(file_list, select_l, creator, var):
    """
    Create a list of units

    file_list is the list of files containing mech info
    select is the selection criteria
    creator specifies which items should be included
    Note that item 0 is always supposed to be the name,
    item 1 is supposed to be Weight, and item 2 is supposed to be BV
    """
    unit_list = []
    # Loop over input
    for i in file_list:
        # Load unit from file
        unit = load_unit(i)

        # Construct data
        if unit.omni == "TRUE":
            for i in unit.loads:
                sel = True
                # Go through the list of selections
                for select in select_l:
                    if select(unit, i) and sel:
                        sel = True
                    else:
                        sel = False
                if sel:
                    item = creator(unit, i, var)
                    if item:
                        unit_list.append(item)
        else:
            sel = True
            # Go through the list of selections
            for select in select_l:
                if select(unit, unit.load) and sel:
                    sel = True
                else:
                    sel = False
            if sel:
                # Creator returns false if the entry is rejected
                item = creator(unit, unit.load, var)
                if item:
                    unit_list.append(item)

    # Default: Sort by weight, name
    unit_list.sort(key=itemgetter(0))
    unit_list.sort(key=itemgetter(1))

    return unit_list


###################################
##### Output format functions #####
###################################

# When constructing a list function, always set
# first item as name
# second item as weight
# third item as BV

## BV listings, two different sorting methods

def create_bv_list_item(mech, i, var):
    """
    Compile info used by print_BV_list()
    """
    name_str = mech.name + " " + mech.model + i.get_name()
    batt_val = mech.get_bv(i)
    weight = mech.weight
    bv_ton = float(batt_val) / float(weight)
    bv_def = mech.def_bv(i, False)
    bv_off = mech.off_bv(i, False)
    cockp = ""
    if mech.type == "BM" and mech.cockpit.type == "Small Cockpit":
        cockp = "SML"
    return (name_str, weight, batt_val, bv_ton, bv_def, bv_off, cockp)


def handle_bvt_list(file_list, select_l, header_l):
    """
    BV_list output

    In the form of name, weight, BV, BV/weight, def BV, off BV, small cockpit?
    sorted by BV/weight, descending
    """

    # Build list
    unit_list = create_unit_list(file_list, select_l, create_bv_list_item, 0)

    # Sort by BV/ton
    unit_list.sort(key=itemgetter(3), reverse=True)

    # Print output
    print_bv_list("Battle Value List by BV/weight", header_l, unit_list)


def handle_bv_list(file_list, select_l, header_l):
    """
    BV_list output

    In the form of name, weight, BV, BV/weight, def BV, off BV, small cockpit?
    sorted by BV/weight, descending
    """

    # Build list
    unit_list = create_unit_list(file_list, select_l, create_bv_list_item, 0)

    # Sort by BV
    unit_list.sort(key=itemgetter(2), reverse=True)

    # Print output
    print_bv_list("Battle Value List by BV", header_l, unit_list)


## Armor listing

def create_armor_list_item(mech, i, var):
    """
    Compile info used by print_armor_list()
    """
    name_str = mech.name + " " + mech.model + i.get_name()
    batt_val = mech.get_bv(i)
    weight = mech.weight
    # Armor coverage relative to maximum
    armor = mech.armor.get_armor_percent()
    # Check for explosive stuff that can disable the mech
    exp = (i.gear.get_ammo_exp_bv(mech.engine) +
           i.gear.get_weapon_exp_bv(mech.engine))
    if exp < 0:
        e_str = "EXP"
    else:
        e_str = ""
    # Check for a stealth system
    sth = mech.get_stealth()
    if sth:
        s_str = "STH"
    else:
        s_str = ""
    # Armor points
    arm_p = mech.armor.total.arm
    max_p = mech.armor.total.max
    # Armor weight
    wgt = mech.armor.get_weight()
    # BF armor
    batt_f = BattleForce(mech, i)
    bf_a = batt_f.get_armor()
    short = mech.armor.short

    return (name_str, weight, batt_val, arm_p, max_p, armor, wgt, short,
            bf_a, e_str, s_str)


def handle_armor_list(file_list, select_l, header_l):
    """
    armor_list output

    In the form of name, weight, BV, points/max, Armor%, armor tonnage,
    armor type, battleforce armor value, Explosive, Stealth,
    sorted by armor points, descending
    """
    # Build list
    unit_list = create_unit_list(file_list, select_l,
                                 create_armor_list_item, 0)

    # Sort by armor points
    unit_list.sort(key=itemgetter(3), reverse=True)

    # Print output
    print_armor_list(header_l, unit_list)


## Speed listing

def create_speed_list_item(mech, i, var):
    """
    Compile info used by print_speed_list()
    """
    name_str = mech.name + " " + mech.model + i.get_name()
    batt_val = mech.get_bv(i)
    weight = mech.weight
    walk = mech.get_walk()
    run = mech.get_run()
    jump = i.get_jump()
    spd = max(walk, jump)
    if mech.type == "BM":
        enh = mech.enhancement.get_type()
    else:
        enh = ""
    mod = mech.get_move_target_modifier(i)
    batt_f = BattleForce(mech, i)
    bf_str = batt_f.get_move()
    osf = mech.get_off_speed_factor(i, False)
    sup = ""
    if i.gear.supercharger.supercharger:
        sup = "SupC"
    eng_s = mech.engine.short

    return (name_str, weight, batt_val, spd, walk, run, jump, enh, eng_s, mod,
            bf_str, osf, sup)


def handle_speed_list(file_list, select_l, header_l):
    """
    speed_list output

    In the form of name, weight, BV, speed, myomer enhancement, target mod,
    battleforce string
    sorted by speed, descending
    """
    # Build list
    unit_list = create_unit_list(file_list, select_l,
                                 create_speed_list_item, 0)

    # Sort by jump, speed
    unit_list.sort(key=itemgetter(6), reverse=True)
    unit_list.sort(key=itemgetter(3), reverse=True)

    # Print output
    print_speed_list(header_l, unit_list)


## Electronics listing

def create_electronics_list_item(mech, i, var):
    """
    Compile info used by print_electronics_list()
    """
    name_str = mech.name + " " + mech.model + i.get_name()
    batt_val = mech.get_bv(i)
    weight = mech.weight
    walk = mech.get_walk()
    run = mech.get_run()
    jump = i.get_jump()
    spd = max(walk, jump)

    ecm = "---"
    if ("ECM" in i.specials or "AECM" in i.specials or "WAT" in i.specials):
        ecm = "ECM"
    bap = "---"
    if ("WAT" in i.specials or "BH" in i.specials or "PRB" in i.specials or
        "LPRB" in i.specials):
        bap = "BAP"
    tag = "---"
    if ("TAG" in i.specials or "LTAG" in i.specials):
        tag = "TAG"
    narc = "----"
    if ("SNARC" in i.specials or "INARC" in i.specials):
        narc = "NARC"
    c3s = "---"
    if ("C3S" in i.specials or "C3BSM" in i.specials):
        c3s = "C3S"
    c3m = "---"
    if ("C3M" in i.specials or "C3BSM" in i.specials):
        c3m = "C3M"
    c3i = "---"
    if ("C3I" in i.specials):
        c3i = "C3I"

    return (name_str, weight, batt_val, spd, walk, run, jump, ecm, bap, tag,
            narc, c3s, c3m, c3i)


def handle_electronics_list(file_list, select_l, header_l):
    """
    electronics_list output

    In the form of name, weight, BV, speed, myomer enhancement, target mod,
    battleforce string
    sorted by speed, descending
    """
    # Build list
    unit_list = create_unit_list(file_list, select_l,
                                 create_electronics_list_item, 0)

    # Sort by jump, speed
    unit_list.sort(key=itemgetter(6), reverse=True)
    unit_list.sort(key=itemgetter(3), reverse=True)

    # Print output
    print_electronics_list(header_l, unit_list)


## Weapons listing


def create_weapon_list_item(mech, i, var):
    """
    Compile info used by print_weapon_list()
    """
    name_str = mech.name + " " + mech.model + i.get_name()
    batt_val = mech.get_bv(i)
    weight = mech.weight

    walk = mech.get_walk()
    jump = i.get_jump()
    mov = str(walk)
    if jump > 0:
        mov += "j"

    l_str = ""
    l_str = i.gear.weaponlist.all_summary()

    return (name_str, weight, batt_val, mov, l_str)


def handle_weapon_list(file_list, select_l, header_l):
    """
    weapon_list output

    In the form of name, weight, BV, Movement, weapon details
    sorted by BV, descending
    """
    # Build list
    unit_list = create_unit_list(file_list, select_l,
                                 create_weapon_list_item, 0)

    # Sort by BV
    unit_list.sort(key=itemgetter(2), reverse=True)

    # Print output
    print_weapon_list("List of All Weapons", header_l, unit_list)


def create_main_weapon_list_item(mech, i, var):
    """
    Compile info used by print_main_weapon_list()
    """
    name_str = mech.name + " " + mech.model + i.get_name()
    batt_val = mech.get_bv(i)
    weight = mech.weight

    walk = mech.get_walk()
    jump = i.get_jump()
    mov = str(walk)
    if jump > 0:
        mov += "j"

    l_str = ""
    l_str = i.gear.weaponlist.main_summary()

    # No big main weapon
    if l_str == "":
        return False

    return (name_str, weight, batt_val, mov, l_str)


def handle_main_weapon_list(file_list, select_l, header_l):
    """
    main_weapon_list output

    In the form of name, weight, BV, Movement, weapon details
    sorted by BV, descending
    """
    # Build list
    unit_list = create_unit_list(file_list, select_l,
                                 create_main_weapon_list_item, 0)

    # Sort by BV
    unit_list.sort(key=itemgetter(2), reverse=True)

    # Print output
    print_weapon_list("List of 'Main' Weapons", header_l, unit_list)


## Timeline listing

def create_timeline_list_item(mech, i, var):
    """
    Compile info used by print_timeline_list()
    """
    name_str = mech.name + " " + mech.model + i.get_name()
    batt_val = mech.get_bv(i)
    weight = mech.weight
    year = mech.get_year(i)

    walk = mech.get_walk()
    jump = i.get_jump()
    mov = str(walk)
    if jump > 0:
        mov += "j"

    e_short = mech.engine.short
    a_short = mech.armor.short
    s_short = mech.structure.short
    l_str = ""
    l_str = i.gear.weaponlist.all_summary()

    return (name_str, weight, e_short, year, mov, s_short, a_short, l_str)


def handle_timeline_list(file_list, select_l, header_l):
    """
    timeline_list output

    In the form of year, name, weight, BV, Movement, structure, armor,
    weapon details
    sorted by BV, descending
    """
    # Build list
    unit_list = create_unit_list(file_list, select_l,
                                 create_timeline_list_item, 0)

    # Sort by year
    unit_list.sort(key=itemgetter(3))

    # Print output
    print_timeline_list(header_l, unit_list)


## LRM tubes listing

def create_missile_list_item(mech, i, var):
    """
    Compile info used by print_missile_list()

    Requirements:
    - Have lrm tubes
    """
    name_str = mech.name + " " + mech.model + i.get_name()
    batt_val = mech.get_bv(i)
    weight = mech.weight
    lrm = i.gear.weaponlist.lrms

    # No lrm tubes
    if lrm == 0:
        return False

    if i.artemis4 == "TRUE":
        art = "AIV"
    elif i.artemis5 == "TRUE":
        art = "AV"
    else:
        art = ""
    walk = mech.get_walk()
    jump = i.get_jump()
    mov = str(walk)
    if jump > 0:
        mov += "j"

    l_str = ""
    (l_str, dam, heat) = i.gear.weaponlist.list_summary(LRM_LIST, 18)

    l_heat = str(heat) + "/" + str(i.get_sink())

    # Ignore heat for combat vehicles
    if mech.type == "CV":
        l_heat = "---"

    return (name_str, weight, batt_val, lrm, art, l_heat, mov, l_str)


def handle_missile_list(file_list, select_l, header_l):
    """
    missile_list output

    In the form of name, weight, BV, LRM tubes, Artemis, Heat, Movement,
    launcher details
    sorted by LRM tubes, descending
    """
    # Build list
    unit_list = create_unit_list(file_list, select_l,
                                 create_missile_list_item, 0)

    # Sort by tubes
    unit_list.sort(key=itemgetter(3), reverse=True)

    # Print output
    print_missile_list(header_l, unit_list)


## SRM tubes listing

def create_srm_list_item(mech, i, var):
    """
    Compile info used by print_srm_list()

    Requirements:
    - Have srm tubes
    """
    name_str = mech.name + " " + mech.model + i.get_name()
    batt_val = mech.get_bv(i)
    weight = mech.weight
    srm = i.gear.weaponlist.count_srms()

    # No srm tubes
    if srm == 0:
        return False

    if i.artemis4 == "TRUE":
        art = "AIV"
    elif i.artemis5 == "TRUE":
        art = "AV"
    else:
        art = ""
    walk = mech.get_walk()
    jump = i.get_jump()
    mov = str(walk)
    if jump > 0:
        mov += "j"

    heat = 0
    l_str = ""
    (l_str, dam, heat) = i.gear.weaponlist.list_summary(SRM_LIST, 6)

    l_heat = str(heat) + "/" + str(i.get_sink())

    # Ignore heat for combat vehicles
    if mech.type == "CV":
        l_heat = "---"

    return (name_str, weight, batt_val, srm, art, l_heat, mov, l_str)


def handle_srm_list(file_list, select_l, header_l):
    """
    srm_list output

    In the form of name, weight, BV, SRM tubes, Artemis, Heat, Movement,
    launcher details
    sorted by SRM tubes, descending
    """
    # Build list
    unit_list = create_unit_list(file_list, select_l, create_srm_list_item, 0)

    # Sort by tubes
    unit_list.sort(key=itemgetter(3), reverse=True)

    # Print output
    print_srm_list(header_l, unit_list)


## Autocannon listing

def create_autocannon_list_item(mech, i, var):
    """
    Compile info used by print_autocannon_list()

    Requirements:
    - Have special ammo using AC
    """
    name_str = mech.name + " " + mech.model + i.get_name()
    batt_val = mech.get_bv(i)
    weight = mech.weight

    # No AC
    if not i.gear.weaponlist.has_ac():
        return False

    if i.gear.tarcomp > 0:
        tarcomp = "TC"
    else:
        tarcomp = ""
    walk = mech.get_walk()
    jump = i.get_jump()
    mov = str(walk)
    if jump > 0:
        mov += "j"

    dam = 0
    heat = 0
    l_str = ""
    (l_str, dam, heat) = i.gear.weaponlist.list_summary(AC_LIST, 9)

    l_heat = str(heat) + "/" + str(i.get_sink())

    # Ignore heat for combat vehicles
    if mech.type == "CV":
        l_heat = "---"

    return (name_str, weight, batt_val, dam, tarcomp, l_heat, mov, l_str)


def handle_autocannon_list(file_list, select_l, header_l):
    """
    autocannon_list output

    In the form of name, weight, BV, damage, tarcomp, Heat, Movement,
    weapon details
    sorted by damage, descending
    """
    # Build list
    unit_list = create_unit_list(file_list, select_l,
                                 create_autocannon_list_item, 0)

    # Sort by tubes
    unit_list.sort(key=itemgetter(3), reverse=True)

    # Print output
    print_autocannon_list(header_l, unit_list)


### Standard listing ###

def create_std_list_item(mech, i, rnge):
    """
    Compile info in a format used by several listings
    """
    name_str = mech.name + " " + mech.model + i.get_name()
    batt_val = mech.get_bv(i)
    weight = mech.weight
    walk = mech.get_walk()
    jump = i.get_jump()
    mov = str(walk)
    if jump > 0:
        mov += "j"

    dam = 0
    heat = 0
    l_str = ""
    (l_str, dam, heat) = i.gear.weaponlist.std_summary(rnge)
    arm_p = mech.armor.total.arm

    l_heat = str(int(heat)) + "/" + str(i.get_sink())
    # Ignore heat for combat vehicles
    if mech.type == "CV":
        l_heat = "---"

    # Ignore mechs that has no damage at this range
    if dam == 0:
        return False

    return (name_str, weight, batt_val, dam, l_heat, mov, arm_p, l_str)


## Juggernaut listing

def print_juggernaut_list(file_list, select_l, header_l):
    """
    juggernaut_list output

    In the form of name, weight, BV, damage, heat, movement, weapon details
    sorted by damage, descending
    """
    # Add juggernaut selector
    # - At least 30 damage at range 6
    # - BF armor at least 5
    arm = 135  # Minimum armor
    dam = 30  # Minimum damage
    rng = 6  # Selected range
    select_l.append(lambda x, y: (x.armor.total.arm >= arm))
    header_l.append(("with at least armor %d" % arm))
    select_l.append(lambda x, y: (y.gear.weaponlist.count_damage(rng) >= dam))
    header_l.append(("with at least damage %d at range %d" % (dam, rng)))
#    select_l.append(lambda x, y: (x.is_juggernaut(y)))

    # Build list
    unit_list = create_unit_list(file_list, select_l,
                                 create_std_list_item, rng)

    # Sort by damage
    unit_list.sort(key=itemgetter(3), reverse=True)

    print_std_list("List of 'Juggernauts' (Alpha)", header_l, unit_list)

## Sniper listing


def print_snipe_list(file_list, select_l, header_l):
    """
    snipe_list output

    In the form of name, weight, BV, damage, heat, movement, weapon details
    sorted by damage, descending
    """
    # Add sniper selector
    # - At least 10 damage at range 18
    # - At least one non-missile long-range weapon
    dam = 10  # Minimum damage
    rng = 18  # Selected range
    select_l.append(lambda x, y: (y.gear.weaponlist.count_damage(rng) >= dam))
    header_l.append(("with at least damage %d at range %d" % (dam, rng)))
    select_l.append(lambda x, y: (y.gear.weaponlist.snipe == True))
    header_l.append("with at least one non-missile long-range weapon")
#    select_l.append(lambda x, y: (x.is_sniper(y)))

    # Build list
    unit_list = create_unit_list(file_list, select_l,
                                 create_std_list_item, rng)

    # Sort by damage
    unit_list.sort(key=itemgetter(3), reverse=True)

    print_std_list("List of 'Snipers' (Alpha)", header_l, unit_list)

## Range listing


def print_range_list(file_list, select_l, header_l, rng):
    """
    range_list output

    In the form of name, weight, BV, damage, heat, movement, weapon details
    sorted by damage, descending
    """
    # Build list
    unit_list = create_unit_list(file_list, select_l,
                                 create_std_list_item, rng)

    # Sort by damage
    unit_list.sort(key=itemgetter(3), reverse=True)

    print_std_list(("List of Damage at Range %d" % (rng)),
                   header_l, unit_list)

## Striker listing


def print_striker_list(file_list, select_l, header_l):
    """
    striker_list output

    In the form of name, weight, BV, damage, heat, movement, weapon details
    sorted by damage, descending
    """
    # Add striker selector
    # - Walk 5 or Jump 5
    # - At least 15 damage at range 3
    spd = 5  # Minimum speed
    dam = 15  # Minimum damage
    rng = 3  # Selected range
    select_l.append(lambda x, y: (max(x.get_walk(), y.get_jump()) >= spd))
    header_l.append("with at least speed %d" % spd)
    select_l.append(lambda x, y: (y.gear.weaponlist.count_damage(rng) >= dam))
    header_l.append(("with at least damage %d at range %d" % (dam, rng)))
#    select_l.append(lambda x, y: (x.is_striker(y)))

    # Build list
    unit_list = create_unit_list(file_list, select_l,
                                 create_std_list_item, rng)

    # Sort by damage
    unit_list.sort(key=itemgetter(3), reverse=True)

    print_std_list("List of 'Strikers' (Alpha)", header_l, unit_list)

## Skirmisher listing


def print_skirmisher_list(file_list, select_l, header_l):
    """
    skirmisher_list output

    In the form of name, weight, BV, damage, heat, movement, weapon details
    sorted by damage, descending
    """
    # Add skirimisher selector
    # - Walk 5 or Jump 5
    # - At least 1 damage at range 18
    # - BF armor value at least 3
    spd = 5  # Minimum speed
    arm = 75  # Minimum armor
    dam = 1  # Minimum damage
    rng = 18  # Selected range
    select_l.append(lambda x, y: (max(x.get_walk(), y.get_jump()) >= spd))
    header_l.append("with at least speed %d" % spd)
    select_l.append(lambda x, y: (x.armor.total.arm >= arm))
    header_l.append(("with at least armor %d" % arm))
    select_l.append(lambda x, y: (y.gear.weaponlist.count_damage(rng) >= dam))
    header_l.append(("with at least damage %d at range %d" % (dam, rng)))
#    select_l.append(lambda x, y: (x.is_skirmisher(y)))

    # Build list
    unit_list = create_unit_list(file_list, select_l,
                                 create_std_list_item, rng)

    # Sort by damage
    unit_list.sort(key=itemgetter(3), reverse=True)

    print_std_list("List of 'Skirmishers' (Alpha)", header_l, unit_list)

## Brawler listing


def print_brawler_list(file_list, select_l, header_l):
    """
    brawler_list output

    In the form of name, weight, BV, damage, heat, movement, weapon details
    sorted by damage, descending
    """
    # Add brawler selector
    # - Walk 4 or Jump 4
    # - At least 10 damage at range 15
    # - BF armor value at least 4
    # - Do more damage at range 15 than range 18
    spd = 4  # Minimum speed
    arm = 105  # Minimum armor
    dam = 10  # Minimum damage
    rng = 15  # Selected range
    select_l.append(lambda x, y: (max(x.get_walk(), y.get_jump()) >= spd))
    header_l.append("with at least speed %d" % spd)
    select_l.append(lambda x, y: (x.armor.total.arm >= arm))
    header_l.append(("with at least armor %d" % arm))
    select_l.append(lambda x, y: (y.gear.weaponlist.count_damage(rng) >= dam))
    header_l.append(("with at least damage %d at range %d" % (dam, rng)))
    select_l.append(lambda x, y: ((y.gear.weaponlist.count_damage(rng) >
                                   y.gear.weaponlist.count_damage(rng + 3))))
    header_l.append(("does more damage at range %d than range %d" %
                     (rng, rng + 3)))
#    select_l.append(lambda x, y: (x.is_brawler(y)))

    # Build list
    unit_list = create_unit_list(file_list, select_l,
                                 create_std_list_item, rng)

    # Sort by damage
    unit_list.sort(key=itemgetter(3), reverse=True)

    print_std_list("List of 'Brawlers' (Alpha)", header_l, unit_list)

## Scout listing


def print_scout_list(file_list, select_l, header_l):
    """
    scout_list output

    In the form of name, weight, BV, damage, heat, movement, weapon details
    sorted by damage, descending
    """
    # Add scout selector
    # - Walk 6 or Jump 6
    spd = 6  # Minimum speed
    rng = 3  # Selected range
    select_l.append(lambda x, y: (max(x.get_walk(), y.get_jump()) >= spd))
    header_l.append("with at least speed %d" % spd)
#    select_l.append(lambda x, y: (x.is_scout(y)))

    # Build list
    unit_list = create_unit_list(file_list, select_l,
                                 create_std_list_item, rng)

    # Sort by damage
    unit_list.sort(key=itemgetter(3), reverse=True)

    print_std_list("List of 'Scouts' (Alpha)", header_l, unit_list)

## Missile Boat listing


def print_missile_boat_list(file_list, select_l, header_l):
    """
    missile_boat_list output

    In the form of name, weight, BV, damage, heat, movement, weapon details
    sorted by damage, descending
    """
    # Add missile boat selector
    # - At least 20 lrm tubes
    # - No non-missile long-range weapons
    lrms = 20  # LRM tubes
    rng = 21  # Selected range
    select_l.append(lambda x, y: (y.gear.weaponlist.lrms >= lrms))
    header_l.append(("with at least %d lrm tubes" % lrms))
    select_l.append(lambda x, y: (y.gear.weaponlist.snipe == False))
    header_l.append("with no non-missile long-range weapon")
#    select_l.append(lambda x, y: (x.is_missile_boat(y)))

    # Build list
    unit_list = create_unit_list(file_list, select_l,
                                 create_std_list_item, rng)

    # Sort by damage
    unit_list.sort(key=itemgetter(3), reverse=True)

    print_std_list("List of 'Missile Boats' (Alpha)", header_l, unit_list)


## Head-capper listing

def create_headcap_list_item(mech, i, var):
    """
    Compile info used by print_headcap_list()
    """
    name_str = mech.name + " " + mech.model + i.get_name()
    batt_val = mech.get_bv(i)
    weight = mech.weight
#    l_heat = str(i.gear.l_heat) + "/" + str(i.get_sink())
    walk = mech.get_walk()
    jump = i.get_jump()
    mov = str(walk)
    if jump > 0:
        mov += "j"

    l_str = ""
    cap = 0
    # List of headcapper names and shorthand
    # Missing: iHLL
    # We will ignore the Bombast laser due to its inaccuracy
    capper_list = [["(IS) Autocannon/20", "ac20:"],
                   ["(IS) LB 20-X AC", "lb20:"],
                   ["(IS) Ultra AC/20", "uac20:"],
                   ["(IS) Gauss Rifle", "gr:"],
                   ["(IS) Heavy Gauss Rifle", "hgr:"],
                   ["(IS) Heavy PPC", "hppc:"],
                   ["(CL) LB 20-X AC", "clb20:"],
                   ["(CL) Ultra AC/20", "cuac20:"],
                   ["(CL) Gauss Rifle", "cgr:"],
                   ["(CL) Heavy Large Laser", "hll:"],
                   ["(CL) ER PPC", "ceppc:"],
                   # Advanced Weapons
                   ["(IS) Improved Heavy Gauss Rifle", "ihgr:"],
                   ["(IS) Binary Laser Cannon", "bl:"],
                   ["(IS) Heavy PPC + PPC Capacitor", "h+cap:"],
                   ["(IS) PPC + PPC Capacitor", "ppc+cap:"],
                   ["(IS) ER PPC + PPC Capacitor", "er+cap:"],
                   ["(IS) Snub-Nose PPC + PPC Capacitor", "sn+cap:"],
                   ["(IS) Thunderbolt-15", "tb15:"],
                   ["(IS) Thunderbolt-20", "tb20:"]]

    for weap in i.gear.weaponlist.list.itervalues():
        for capper in capper_list:
            if (weap.name == capper[0] and weap.count > 0):
                l_str += weap.get_short_count() + " "
                cap += weap.count

    # Armor coverage relative to maximum
    armor = mech.armor.get_armor_percent()

    # Targeting Computer
    tarcomp = ""
    if (i.gear.tarcomp > 0):
        tarcomp = "X"

    return (name_str, weight, batt_val, cap, mov, armor, tarcomp, l_str)


def handle_headcap_list(file_list, select_l, header_l):
    """
    headcap_list output

    In the form of name, weight, BV, Headcappers, Movement, Armor, Tarcomp
    weapon details
    sorted by number of headcappers, descending
    """
    # Build list
    unit_list = create_unit_list(file_list, select_l,
                                 create_headcap_list_item, 0)

    # Sort by speed
    unit_list.sort(key=itemgetter(3), reverse=True)

    # Print output
    print_headcap_list(header_l, unit_list)


## Battle-force listing

def create_battle_force_list_item(mech, i, var):
    """
    Compile info used by print_battle_force_list()
    """
    name_str = mech.name + " " + mech.model + i.get_name()
    batt_f = BattleForce(mech, i)
    batt_val = batt_f.get_point_value()
    weight = batt_f.get_weight_class()
    mov = batt_f.get_move()
    armor = batt_f.get_armor()

    return (name_str, weight, batt_val, mov, armor)


def handle_battle_force_list(file_list, select_l, header_l):
    """
    battle_force_list output

    In the form of name, weight, BV, Headcappers, Movement, Armor, Tarcomp
    weapon details
    sorted by number of headcappers, descending
    """
    # Build list
    unit_list = create_unit_list(file_list, select_l,
                                 create_battle_force_list_item, 0)

    # Sort by points
    unit_list.sort(key=itemgetter(2), reverse=True)

    # Print output
    print_battle_force_list(header_l, unit_list)


## Damage/range listing

def create_damage_range_list_item(mech, i, var):
    """
    Compile info used by print_damage_range_list()
    """
    name_str = mech.name + " " + mech.model + i.get_name()
    batt_val = mech.get_bv(i)
    weight = mech.weight

    dam3 = i.gear.weaponlist.count_damage(3)
    dam6 = i.gear.weaponlist.count_damage(6)
    dam9 = i.gear.weaponlist.count_damage(9)
    dam12 = i.gear.weaponlist.count_damage(12)
    dam15 = i.gear.weaponlist.count_damage(15)
    dam18 = i.gear.weaponlist.count_damage(18)
    dam21 = i.gear.weaponlist.count_damage(21)
    dam24 = i.gear.weaponlist.count_damage(24)

    return (name_str, weight, batt_val, dam3, dam6, dam9, dam12, dam15, dam18,
            dam21, dam24)


def handle_damage_range_list(file_list, select_l, header_l):
    """
    range_list output

    In the form of name, weight, BV, damage
    sorted by damage, descending
    """
    # Build list
    unit_list = create_unit_list(file_list, select_l,
                                 create_damage_range_list_item, 0)

    # Sort by speed
    unit_list.sort(key=itemgetter(3), reverse=True)

    # Print output
    print_damage_range_list(header_l, unit_list)


## Mech type listing

def create_type_list_item(mech, i, var):
    """
    Compile info used by print_type_list()
    """
    name_str = mech.name + " " + mech.model + i.get_name()
    batt_val = mech.get_bv(i)
    weight = mech.weight
    m_type = Type(mech, i)

    warn = "!!"

    sco = "-"
    if m_type.is_scout():
        sco = "X"
        warn = ""
    stri = "-"
    if m_type.is_striker():
        stri = "X"
        warn = ""
    skir = "-"
    if m_type.is_skirmisher():
        skir = "X"
        warn = ""
    brw = "-"
    if m_type.is_brawler():
        brw = "X"
        warn = ""
    mis = "-"
    if m_type.is_missile_boat():
        mis = "X"
        warn = ""
    snp = "-"
    if m_type.is_sniper():
        snp = "X"
        warn = ""
    jug = "-"
    if m_type.is_juggernaut():
        jug = "X"
        warn = ""

    return (name_str, weight, batt_val, sco, stri, skir, brw, mis, snp, jug,
            warn)


def handle_type_list(file_list, select_l, header_l):
    """
    type_list output

    In the form of name, weight, BV, damage
    sorted by damage, descending
    """
    # Build list
    unit_list = create_unit_list(file_list, select_l, create_type_list_item, 0)

    # Sort by speed
    # unit_list.sort(key=itemgetter(3), reverse=True)

    # Print output
    print_type_list(header_l, unit_list)


## Cost listing

def create_cost_list_item(mech, i, var):
    """
    Compile info used by print_cost_list()
    """
    name_str = mech.name + " " + mech.model + i.get_name()
    batt_val = mech.get_bv(i)
    weight = mech.weight
    cost = mech.calculate_cost(i)
    cost_ssw = i.cost
    cost_diff = cost_ssw - cost

    return (name_str, weight, batt_val, cost, cost_ssw, cost_diff)


def handle_cost_list(file_list, select_l, header_l):
    """
    cost_list output

    In the form of name, weight, BV, cost
    sorted by cost, descending
    """
    # Build list
    unit_list = create_unit_list(file_list, select_l, create_cost_list_item, 0)

    # Sort by cost
    unit_list.sort(key=itemgetter(3), reverse=True)

    # Print output
    print_cost_list(header_l, unit_list)


## Weight listing


def create_weight_list_item(mech, i, var):
    """
    Compile info used by print_weight_list()
    """
    name_str = mech.name + " " + mech.model + i.get_name()
#    batt_val = mech.get_bv(i)
    weight = mech.weight
    s_w = mech.structure.get_weight()
    e_w = mech.engine.get_weight()
    # Add gyro for mechs
    if mech.type == "BM":
        e_w += mech.gyro.get_weight()
        e_w += mech.enhancement.get_weight()
    # Add lift/dive equipment & rotors for combat vehicles
    elif mech.type == "CV":
        e_w += mech.lift.get_weight()
    a_w = mech.armor.get_weight()
    # Cockpits and other controls
    c_w = 0
    if mech.type == "BM":
        c_w = mech.cockpit.get_weight()
    elif mech.type == "CV":
        c_w = mech.control.get_weight()
    j_w = i.jjets.get_weight() + i.partw.get_weight() + i.jumpb.get_weight()
    h_w = i.heatsinks.get_weight() + i.power_amp.get_weight()
    t_w = i.gear.tur_weight
    g_w = (i.gear.get_weight() + i.btrap.get_weight() +
           i.aes_ra.get_weight() + i.aes_la.get_weight())
    rest = weight - s_w - e_w - a_w - c_w - j_w - h_w - t_w - g_w
    if rest == 0:
        r_str = ""
    else:
        r_str = str(rest)

    return (name_str, weight, s_w, e_w, a_w, c_w, j_w, h_w, t_w, g_w, r_str)


def handle_weight_list(file_list, select_l, header_l):
    """
    weight_list output

    In the form of name, weight, BV, cost
    sorted by cost, descending
    """
    # Build list
    unit_list = create_unit_list(file_list, select_l,
                                 create_weight_list_item, 0)

    # Separate out mechs where the weight does not add up right, and put them
    # at the bottom
    unit_list.sort(key=itemgetter(10))

    # Print output
    print_weight_list(header_l, unit_list)


## Default listing

def create_def_list_item(mech, i, var):
    """
    Compile info used by print_default()
    """
    name_str = mech.name + " " + mech.model + i.get_name()
    batt_val = mech.get_bv(i)
    weight = mech.weight
    source = i.source
    prod_era = conv_era(i.get_prod_era())
    rules = conv_rules(mech.get_rules_level(i), 0)
    year = mech.get_year(i)
    return (name_str, weight, batt_val, source, rules, prod_era, year)


def handle_default(file_list, select_l, header_l):
    """
    Default output format

    In the form of name, weight, BV, source, era
    Intended to conform to the MUL format
    """
    # Build list
    unit_list = create_unit_list(file_list, select_l, create_def_list_item, 0)

    # Print output
    print_default(header_l, unit_list)


##################################
##### Define argument parser #####
##################################

def parse_arg():
    """
    Defines and parses command-line arguments
    """
    ### Handle arguments ###

    # Create parser
    parser = argparse.ArgumentParser(description='List mech summaries.')
    # Input argument
    parser.add_argument('-f', action='append', help='list of .ssw files')
    # Output type selection arguments
    parser.add_argument('-b', action='store_const', help='BV/ton list output',
                        dest='output', const='b')
    parser.add_argument('-bv', action='store_const', help='BV list output',
                        dest='output', const='bv')
    parser.add_argument('-a', action='store_const', help='Armor list output',
                        dest='output', const='a')
    parser.add_argument('-s', action='store_const', help='Speed list output',
                        dest='output', const='s')
    parser.add_argument('-l', action='store_const', help='LRM list output',
                        dest='output', const='l')
    parser.add_argument('-sn', action='store_const', help='Snipe list output',
                        dest='output', const='sn')
    parser.add_argument('-cap', action='store_const',
                        help='Headcap list output',
                        dest='output', const='cap')
    parser.add_argument('-dr', action='store_const',
                        help='Print damage over range list output',
                        dest='output', const='dr')
    parser.add_argument('-str', action='store_const',
                        help='Striker list output',
                        dest='output', const='str')
    parser.add_argument('-skir', action='store_const',
                        help='Skirmisher list output',
                        dest='output', const='skir')
    parser.add_argument('-brwl', action='store_const',
                        help='Brawler list output',
                        dest='output', const='brwl')
    parser.add_argument('-scout', action='store_const',
                        help='Scout list output',
                        dest='output', const='scout')
    parser.add_argument('-mb', action='store_const',
                        help='Missile Boat list output',
                        dest='output', const='mb')
    parser.add_argument('-jug', action='store_const',
                        help='Juggernaut list output',
                        dest='output', const='jug')
    parser.add_argument('-typ', action='store_const',
                        help='Mech type list output',
                        dest='output', const='typ')
    parser.add_argument('-ac', action='store_const',
                        help='Autocannon list output',
                        dest='output', const='ac')
    parser.add_argument('-srm', action='store_const',
                        help='SRM list output',
                        dest='output', const='srm')
    parser.add_argument('-w', action='store_const', help='Weapon list output',
                        dest='output', const='w')
    parser.add_argument('-mw', action='store_const', help='Weapon list output',
                        dest='output', const='mw')
    parser.add_argument('-tl', action='store_const', help='Timeline output',
                        dest='output', const='tl')
    parser.add_argument('-bf', action='store_const',
                        help='Battle Force list output',
                        dest='output', const='bf')
    parser.add_argument('-r', action='store', default=0, type=int,
                        help='Range <d> damage list output',)
    parser.add_argument('-cost', action='store_const',
                        help='Cost list output',
                        dest='output', const='cost')
    parser.add_argument('-weight', action='store_const',
                        help='Weight list output',
                        dest='output', const='weight')
    parser.add_argument('-elec', action='store_const',
                        help='Electronics list output',
                        dest='output', const='elec')
    # Filter arguments
    parser.add_argument('-tag', action='store_true',
                        help='Select units with TAG')
    parser.add_argument('-c3s', action='store_true',
                        help='Select units with C3 Slave')
    parser.add_argument('-c3m', action='store_true',
                        help='Select units with C3 Master')
    parser.add_argument('-c3i', action='store_true',
                        help='Select units with C3i')
    parser.add_argument('-narc', action='store_true',
                        help='Select units with Narc')
    parser.add_argument('-ecm', action='store_true',
                        help='Select units with ECM')
    parser.add_argument('-probe', action='store_true',
                        help='Select units with Active Probe')
    parser.add_argument('-taser', action='store_true',
                        help='Select units with Taser')
    parser.add_argument('-i', action='store_true',
                        help='Select Inner Sphere tech units')
    parser.add_argument('-cl', action='store_true',
                        help='Select Clan tech units')
    parser.add_argument('-cc', action='store_true',
                        help='Select units with Command Console')
    parser.add_argument('-e', action='store', default=99, type=int,
                        help='Select units up to era <n>')
    parser.add_argument('-y', action='store', default=0, type=int,
                        help='Select units up to year <n>')
    parser.add_argument('-se', action='store', default=0, type=int,
                        help='Select units with speed <n>')
    parser.add_argument('-sf', action='store', default=0, type=int,
                        help='Select units with at least speed <n>')
    parser.add_argument('-lrm', action='store', default=0, type=int,
                        help='Select units with at least <n> lrms')
    parser.add_argument('-npr', action='store_true',
                        help='Select non-Primitive units')
    parser.add_argument('-wgt', action='store', default=0, type=int,
                        help='Select units of weight <n>')
    parser.add_argument('-rule', action='store', default=99, type=int,
                        help='Select units with highest rules level <n>')
    parser.add_argument('-af', action='store', default=0, type=int,
                        help='Select units with at least armor points <n>')
    parser.add_argument('-vtol', action='store_true',
                        help='Select VTOL units')
    parser.add_argument('-j', action='store_true',
                        help='Select jumping units')
    parser.add_argument('-light', action='store_true',
                        help='Select light units')
    parser.add_argument('-medium', action='store_true',
                        help='Select medium units')
    parser.add_argument('-heavy', action='store_true',
                        help='Select heavy units')
    parser.add_argument('-assault', action='store_true',
                        help='Select assault units')
    # Default: one filename
    parser.add_argument('file', nargs='*')

    return parser.parse_args()


###########################
##### Build file list #####
###########################

def create_file_list(args):
    """
    Builds the list of input files from the argument list.
    """
    d_string = ""
    file_list = []

    # We have a single file name
    if args.file:
        file_list = args.file
    # Default case, we supplied a list with -f option
    else:
        for file_n in args.f:
            f_handle = open(file_n)
            file_list_raw = f_handle.readlines()
            f_handle.close()
            # Strip out trailing newlines
            for file_name in file_list_raw:
                fname = file_name.strip()
                # Ignore empty lines
                if fname == "":
                    continue
                # Ignore comments
                if fname[0] == '#':
                    # We have a command
                    if fname[1] == '!':
                        # Change working directory
                        if fname[2:4] == "cd":
                            d_string = fname[5:]
                            #work_dir = os.getcwdu()
                            #os.chdir(work_dir + "/" + d_string)
                            continue
                    else:
                        continue
                if d_string != "":
                    file_list.append(d_string + "/" + fname)
                else:
                    file_list.append(fname)

    # Remove duplicates
    file_list = list(set(file_list))

    return file_list


###########################
##### Build file list #####
###########################

def create_selector_list(args):
    """
    Builds select lists from arguments
    """
    # Create lists
    select = lambda x, y: True
    select_l = []
    select_l.append(select)
    header_l = []

    # TAG
    if args.tag:
        select_l.append(lambda x, y: ("TAG" in y.specials or
                                      "LTAG" in y.specials))
        header_l.append("with TAG")
    # C3 Slave
    if args.c3s:
        select_l.append(lambda x, y: ("C3S" in y.specials or
                                      "C3BSS" in y.specials))
        header_l.append("with C3 Slave")
    # C3 Master
    if args.c3m:
        select_l.append(lambda x, y: ("C3M" in y.specials or
                                      "C3BSM" in y.specials))
        header_l.append("with C3 Master")
    # C3i
    if args.c3i:
        select_l.append(lambda x, y: "C3I" in y.specials)
        header_l.append("with C3i")
    # Narc
    if args.narc:
        select_l.append(lambda x, y: ("SNARC" in y.specials or
                                      "INARC" in y.specials))
        header_l.append("with Narc")
    # ECM
    if args.ecm:
        select_l.append(lambda x, y: ("ECM" in y.specials or
                                      "AECM" in y.specials or
                                      "WAT" in y.specials))
        header_l.append("with ECM")
    # Active Probe
    if args.probe:
        select_l.append(lambda x, y: ("PRB" in y.specials or
                                      "BH" in y.specials or
                                      "LPRB" in y.specials or
                                      "WAT" in y.specials))
        header_l.append("with Active Probe")
    # Taser
    if args.taser:
        select_l.append(lambda x, y: "MTAS" in y.specials)
        header_l.append("with Battlemech Taser")
    # Inner Sphere
    if args.i:
        select_l.append(lambda x, y: (x.techbase == "Inner Sphere" and
                                      not y.mixed))
        header_l.append("Inner Sphere-tech")
    # Clan
    if args.cl:
        select_l.append(lambda x, y: (x.techbase == "Clan" and not y.mixed))
        header_l.append("Clan-tech")
    # Command Console
    if args.cc:
        select_l.append(lambda x, y: x.cockpit.console == "TRUE")
        header_l.append("with Command Console")
    # Era
    if args.e < 99:
        era = args.e
        select_l.append(lambda x, y: (y.get_prod_era() <= era))
        header_l.append(("available at era %s" % conv_era(era)))
    # Year
    if args.y > 0:
        select_l.append(lambda x, y: (x.get_year(y) <= args.y))
        header_l.append(("available at year %d" % args.y))
    # Speed
    if args.se > 0:
        spd = args.se
        select_l.append(lambda x, y: (max(x.get_walk(), y.get_jump()) == spd))
        header_l.append(("with speed %d" % spd))
    # Speed
    if args.sf > 0:
        spd = args.sf
        select_l.append(lambda x, y: (max(x.get_walk(), y.get_jump()) >= spd))
        header_l.append(("with at least speed %d" % spd))
    # Jumping
    if args.j:
        select_l.append(lambda x, y: (y.get_jump() > 0))
        header_l.append("can jump")
    # Armor
    if args.af > 0:
        select_l.append(lambda x, y: (x.armor.total.arm >= args.af))
        header_l.append(("with at least armor %d" % args.af))
    # LRMs
    if args.lrm > 0:
        lrm = args.lrm
        select_l.append(lambda x, y: (y.gear.weaponlist.lrms >= lrm))
        header_l.append(("with at least %d lrm tubes" % lrm))
    # non-primitive
    if args.npr:
        select_l.append(lambda x, y:
                            x.engine.etype != "Primitive Fusion Engine")
        header_l.append("Non-primitive")
    # Weight
    if args.wgt > 0:
        select_l.append(lambda x, y: (x.weight == args.wgt))
        header_l.append(("of weight %d" % args.wgt))
    # Rules level
    if args.rule < 99:
        select_l.append(lambda x, y: (x.get_rules_level(y) <= args.rule))
        header_l.append(("with highest rules level %s" % conv_rules(args.rule,
                                                                    1)))
    # VTOL
    if args.vtol:
        select_l.append(lambda x, y: (x.type == "CV" and x.mot_type == "VTOL"))
        header_l.append("VTOL")
    # Light
    if args.light:
        select_l.append(lambda x, y: (x.weight < 40))
        header_l.append("of light weight")
    # Medium
    if args.medium:
        select_l.append(lambda x, y: (x.weight >= 40 and x.weight < 60))
        header_l.append("of medium weight")
    # Heavy
    if args.heavy:
        select_l.append(lambda x, y: (x.weight >= 60 and x.weight < 80))
        header_l.append("of heavy weight")
    # Assault
    if args.assault:
        select_l.append(lambda x, y: (x.weight >= 80))
        header_l.append("of assault weight")

    return (select_l, header_l)


####################################
##### Main program starts here #####
####################################

def main():
    """
    main() function for summary.py. Prints out a summary of units
    according to the command-line switches.
    """

    ### Parse arguments ###
    args = parse_arg()

    ### Create file_list ###

    file_list = create_file_list(args)

    ### Activate selectors ###

    (select_l, header_l) = create_selector_list(args)

    ### Process output ###

    arg_calls = {
        'b': handle_bvt_list,
        'bv': handle_bv_list,
        'a': handle_armor_list,
        's': handle_speed_list,
        'elec': handle_electronics_list,
        'w': handle_weapon_list,
        'mw': handle_main_weapon_list,
        'tl': handle_timeline_list,
        # Special ammo users
        'l': handle_missile_list,
        'srm': handle_srm_list,
        'ac': handle_autocannon_list,
        # Mech types
        'sn': print_snipe_list,
        'str': print_striker_list,
        'skir': print_skirmisher_list,
        'brwl': print_brawler_list,
        'jug': print_juggernaut_list,
        'mb': print_missile_boat_list,
        'scout': print_scout_list,
        'typ': handle_type_list,
        # Misc
        'cap': handle_headcap_list,
        'bf': handle_battle_force_list,
        'dr': handle_damage_range_list,
        'cost': handle_cost_list,
        'weight': handle_weight_list,
        }

    # Special case, damage at range <d>
    if args.r > 0:
        print_range_list(file_list, select_l, header_l, args.r)
    # Otherwise use dictionary lookup
    elif args.output:
        arg_calls[args.output](file_list, select_l, header_l)
    else:
        handle_default(file_list, select_l, header_l)

if __name__ == "__main__":
    main()
