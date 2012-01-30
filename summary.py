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
Prints out a one-line summary of a mech
"""

import argparse
from xml.dom import minidom
from operator import itemgetter
from mech import Mech
from weapons import LAUNCHER_LIST

#############################
##### Utility functions #####
#############################

def conv_era(era):
    """
    Convert era to string
    """
    conv = {
        0 : "AoW",
        1 : "SL",
        2 : "SW-E",
        3 : "SW-L",
        4 : "Clan",
        5 : "CW",
        6 : "Jihad",
        7 : "Rep",
        8 : "DA"
        }
    return conv[era]
    

def load_mech(file_name):
    """
    Load mech from file

    Takes a file name as argument, returns a mech object
    """
    # Read file
    fsock = open(file_name)
    xmldoc = minidom.parse(fsock)
    fsock.close()

    # Get mech
    return Mech(xmldoc)


def create_header(header_l):
    """
    Construct filter header
    """
    # Start with Mechs
    header = "Mechs "

    # Add specific filter description(s)
    for h_item in header_l:
        header += h_item
        header += ", "

    # Clean up end
    header = header[:-2] + ":"

    return header


def armor_letter(percent):
    """
    ANS Kamas P81's armor granding system
    """
    if percent < 50:
        return "F"
    elif percent <= 60:
        return "D"
    elif percent <= 75:
        return "C"
    elif percent <= 90:
        return "B"
    else:
        return "A"

###############################
##### Mech entry creation #####
###############################

def create_mech_list(file_list, select_l, creator):
    """
    Create a list of mechs

    file_list is the list of files containing mech info
    select is the selection criteria
    creator specifies which items should be included
    Note that item 0 is always supposed to be the name,
    item 1 is supposed to be Weight, and item 2 is supposed to be BV
    """
    mech_list = []
    # Loop over input
    for i in file_list:
        # Load mech from file
        mech = load_mech(i)

        # Construct data
        if mech.omni == "TRUE":
            for i in mech.loads:
                sel = True
                # Go through the list of selections
                for select in select_l:
                    if select(mech, i) and sel:
                        sel = True
                    else:
                        sel = False
                if sel:
                    item = creator(mech, i)
                    if item:
                        mech_list.append(item)
        else:
            sel = True
            # Go through the list of selections
            for select in select_l:
                if select(mech, mech.load) and sel:
                    sel = True
                else:
                    sel = False
            if sel:
                # Creator returns false if the entry is rejected
                item = creator(mech, mech.load)
                if item:
                    mech_list.append(item)

    # Default: Sort by weight, name
    mech_list.sort(key=itemgetter(0))
    mech_list.sort(key=itemgetter(1))

    return mech_list


###################################
##### Output format functions #####
###################################

# When constructing a list function, always set
# first item as name
# second item as weight
# third item as BV

## BV listings, two different sorting methods

def create_bv_list_item(mech, i):
    """
    Compile info used by print_BV_list()
    """
    name_str = mech.name + " " + mech.model + i.get_name()
    batt_val = mech.get_bv(i)
    weight = mech.weight
    bv_ton = float(batt_val)/float(weight)
    bv_def = mech.def_bv(i, False)
    bv_off = mech.off_bv(i, False)
    cockp = ""
    if mech.cockpit.type == "Small Cockpit":
        cockp = "SML"
    return (name_str, weight, batt_val, bv_ton, bv_def, bv_off, cockp)

def print_bvt_list(file_list, select_l, header):
    """
    BV_list output

    In the form of name, weight, BV, BV/weight, def BV, off BV, small cockpit?
    sorted by BV/weight, descending
    """

    # Build list
    mech_list = create_mech_list(file_list, select_l, create_bv_list_item)

    # Sort by BV/ton
    mech_list.sort(key=itemgetter(3), reverse=True)

    # Print output
    print header
    header2 = "Name                          "
    header2 += "Tons BV    BV/Wt | defBV   offBV   cpit"
    print header2
    for i in mech_list:
        print ("%-30s %3d %4d  %5.2f | %7.2f %7.2f %s" %
               (i[0], i[1], i[2], i[3], i[4], i[5], i[6]))


def print_bv_list(file_list, select_l, header):
    """
    BV_list output

    In the form of name, weight, BV, BV/weight, def BV, off BV, small cockpit?
    sorted by BV/weight, descending
    """

    # Build list
    mech_list = create_mech_list(file_list, select_l, create_bv_list_item)

    # Sort by BV
    mech_list.sort(key=itemgetter(2), reverse=True)

    # Print output
    print header
    header2 = "Name                          "
    header2 += "Tons BV    BV/Wt | defBV   offBV   cpit"
    print header2
    for i in mech_list:
        print ("%-30s %3d %4d  %5.2f | %7.2f %7.2f %s" %
               (i[0], i[1], i[2], i[3], i[4], i[5], i[6]))


## Armor listing

def create_armor_list_item(mech, i):
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
    bf_a = mech.armor.get_bf_value()

    return (name_str, weight, batt_val, armor, e_str, s_str, arm_p, max_p,
            wgt, bf_a)

def print_armor_list(file_list, select_l, header):
    """
    armor_list output

    In the form of name, weight, BV, Armor%, Explosive, Stealth, points/max,
    armor tonnage, battleforce armor value
    sorted by armor%, descending
    """
    # Build list
    mech_list = create_mech_list(file_list, select_l, create_armor_list_item)

    # Sort by armor%
    mech_list.sort(key=itemgetter(3), reverse=True)

    # Print output
    print header
    header2 = "Name                          "
    header2 += "Tons BV   Armr Exp Sth | Points  Tons  BF"
    print header2
    for i in mech_list:
        print ("%-30s %3d %4d %3.0f%% %3s %3s | %3d/%3d %4.1ft %2d" % 
               (i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9]))


## Speed listing

def create_speed_list_item(mech, i):
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
    enh = mech.enhancement.get_type()
    mod = mech.get_move_target_modifier(i)
    bf_str = mech.get_bf_move(i)

    return (name_str, weight, batt_val, spd, walk, run, jump, enh, mod, bf_str)

def print_speed_list(file_list, select_l, header):
    """
    speed_list output

    In the form of name, weight, BV, speed, myomer enhancement, target mod,
    battleforce string
    sorted by speed, descending
    """
    # Build list
    mech_list = create_mech_list(file_list, select_l, create_speed_list_item)

    # Sort by speed
    mech_list.sort(key=itemgetter(3), reverse=True)

    # Print output
    print header
    print "Name                          Tons BV    Speed   Enh  Mod BF"
    for i in mech_list:
        print ("%-30s %3d %4d %2d/%2d/%2d %-4s %d   %s" % 
               (i[0], i[1], i[2], i[4], i[5], i[6], i[7], i[8], i[9]))

## LRM tubes listing

def create_missile_list_item(mech, i):
    """
    Compile info used by print_missile_list()

    Requirements:
    - Have lrm tubes
    """
    name_str = mech.name + " " + mech.model + i.get_name()
    batt_val = mech.get_bv(i)
    weight = mech.weight
    lrm = i.gear.lrms

    # No lrm tubes
    if lrm == 0:
        return False

    l_heat = str(i.gear.l_heat) + "/" + str(i.get_sink())
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
    for weap in i.gear.weaponlist.list:
        for launcher in LAUNCHER_LIST:
            if (weap.name == launcher[0] and weap.count > 0):
#                l_str += launcher[1] + str(weap.count) + "/"
#                l_str += str(weap.get_ammo_per_weapon()) + " "
                l_str += weap.get_short_count() + " "
               
    return (name_str, weight, batt_val, lrm, art, l_heat, mov, l_str)

def print_missile_list(file_list, select_l, header):
    """
    missile_list output

    In the form of name, weight, BV, LRM tubes, Artemis, Heat, Movement,
    launcher details
    sorted by LRM tubes, descending
    """
    # Build list
    mech_list = create_mech_list(file_list, select_l, create_missile_list_item)

    # Sort by tubes
    mech_list.sort(key=itemgetter(3), reverse=True)

    # Print output
    print header
    header2 = "Name                          "
    header2 += "Tons BV   LRM Art Heat  Mov Lnchrs/turns of fire"
    print header2
    for i in mech_list:
        print ("%-30s %3d %4d %3d %-3s %-5s %-3s %s" %
               (i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7]))


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

    arm = mech.armor.get_bf_value()

    dam = 0
    heat = 0
    l_str = ""

    for weap in i.gear.weaponlist.list:
        if (weap.get_range() >= rnge and weap.count > 0):
            l_str += weap.get_short_count() + " "
            dam += weap.get_damage(rnge) * weap.count
            heat += weap.get_heat() * weap.count

    l_heat = str(heat) + "/" + str(i.get_sink())

    return (name_str, weight, batt_val, dam, l_heat, mov, l_str)


def create_juggernaut_list_item(mech, i):
    """
    Compile info used by print_juggernaut_list()

    Requirements:
    - At least 30 damage at range 9
    - BF armor at least 5
    """
    if mech.is_juggernaut(i):
        return create_std_list_item(mech, i, 9)
    else:
        return False
    

def print_juggernaut_list(file_list, select_l, header):
    """
    juggernaut_list output

    In the form of name, weight, BV, damage, heat, movement, weapon details
    sorted by damage, descending
    """
    # Build list
    mech_list = create_mech_list(file_list, select_l,
                                 create_juggernaut_list_item)

    # Sort by speed
    mech_list.sort(key=itemgetter(3), reverse=True)

    # Print output
    print header
    header2 = "Name                          "
    header2 += "Tons BV   Dam Heat  Mov Wpns/turns of fire"
    print header2
    for i in mech_list:
        print ("%-30s %3d %4d %3d %-5s %-3s %s" %
               (i[0], i[1], i[2], i[3], i[4], i[5], i[6]))



## Sniper listing

def create_snipe_list_item(mech, i):
    """
    Compile info used by print_snipe_list()

    Requirements:
    - At least 10 damage at range 18
    """
    if mech.is_sniper(i):
        return create_std_list_item(mech, i, 18)
    else:
        return False

def print_snipe_list(file_list, select_l, header):
    """
    snipe_list output

    In the form of name, weight, BV, damage, heat, movement, weapon details
    sorted by damage, descending
    """
    # Build list
    mech_list = create_mech_list(file_list, select_l, create_snipe_list_item)

    # Sort by speed
    mech_list.sort(key=itemgetter(3), reverse=True)

    # Print output
    print header
    header2 = "Name                          "
    header2 += "Tons BV   Dam Heat  Mov Wpns/turns of fire"
    print header2
    for i in mech_list:
        print ("%-30s %3d %4d %3d %-5s %-3s %s" %
               (i[0], i[1], i[2], i[3], i[4], i[5], i[6]))


## Striker listing

def create_striker_list_item(mech, i):
    """
    Compile info used by print_striker_list()

    Requirements:
    - Walk 6 or Jump 5
    - At least 10 damage at range 3
    """
    if mech.is_striker(i):
        return create_std_list_item(mech, i, 3)
    else:
        return False

def print_striker_list(file_list, select_l, header):
    """
    striker_list output

    In the form of name, weight, BV, damage, heat, movement, weapon details
    sorted by damage, descending
    """
    # Build list
    mech_list = create_mech_list(file_list, select_l, create_striker_list_item)

    # Sort by speed
    mech_list.sort(key=itemgetter(3), reverse=True)

    # Print output
    print header
    header2 = "Name                          "
    header2 += "Tons BV   Dam Heat  Mov Wpns/turns of fire"
    print header2
    for i in mech_list:
        print ("%-30s %3d %4d %3d %-5s %-3s %s" %
               (i[0], i[1], i[2], i[3], i[4], i[5], i[6]))


## Skirmisher listing

def create_skirmisher_list_item(mech, i):
    """
    Compile info used by print_skirmisher_list()

    Requirements:
    - Walk 5 or Jump 4
    - At least 5 damage at range 15
    - BF armor value at least 4
    """
    if mech.is_skirmisher(i):
        return create_std_list_item(mech, i, 15)
    else:
        return False

def print_skirmisher_list(file_list, select_l, header):
    """
    skirmisher_list output

    In the form of name, weight, BV, damage, heat, movement, weapon details
    sorted by damage, descending
    """
    # Build list
    mech_list = create_mech_list(file_list, select_l,
                                 create_skirmisher_list_item)

    # Sort by speed
    mech_list.sort(key=itemgetter(3), reverse=True)

    # Print output
    print header
    header2 = "Name                          "
    header2 += "Tons BV   Dam Heat  Mov Wpns/turns of fire"
    print header2
    for i in mech_list:
        print ("%-30s %3d %4d %3d %-5s %-3s %s" %
               (i[0], i[1], i[2], i[3], i[4], i[5], i[6]))


## Head-capper listing

def create_headcap_list_item(mech, i):
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
    # Missing: iHGR, iHLL, PPC + Cap, HPPC + CAP, ERPPC + Cap
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
                   ["(IS) Binary Laser Cannon", "bl:"],
                   ["(IS) Snub-Nose PPC + PPC Capacitor", "sn+cap:"],
                   ["(IS) Thunderbolt-15", "tb15:"],
                   ["(IS) Thunderbolt-20", "tb20:"]]

    for weap in i.gear.weaponlist.list:
        for capper in capper_list:
            if (weap.name == capper[0] and weap.count > 0):
#                if weap.useammo > 0:
#                    l_str += capper[1] + str(weap.count) + "/"
#                    l_str += str(weap.get_ammo_per_weapon()) + " "
#                else:
#                    l_str += capper[1] + str(weap.count) + " "
                l_str += weap.get_short_count() + " "
                cap += weap.count

    # Armor coverage relative to maximum
    armor = mech.armor.get_armor_percent()

    # Targeting Computer
    tarcomp = ""
    if (i.gear.tarcomp > 0):
        tarcomp = "X"

    return (name_str, weight, batt_val, cap, mov, armor, tarcomp, l_str)

def print_headcap_list(file_list, select_l, header):
    """
    headcap_list output

    In the form of name, weight, BV, Headcappers, Movement, Armor, Tarcomp
    weapon details
    sorted by number of headcappers, descending
    """
    # Build list
    mech_list = create_mech_list(file_list, select_l, create_headcap_list_item)

    # Sort by speed
    mech_list.sort(key=itemgetter(3), reverse=True)

    # Print output
    print header
    header2 = "Name                          "
    header2 += "Tons BV   Cap Mov Armr TC Weapons/turns of fire"
    print header2
    for i in mech_list:
        if i[3] > 0:
            print ("%-30s %3d %4d %3d %-3s %3.0f%% %-2s %s" %
                   (i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7]))


## Damage/range listing

def create_range_list_item(mech, i):
    """
    Compile info used by print_range_list()
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

def print_range_list(file_list, select_l, header):
    """
    range_list output

    In the form of name, weight, BV, damage
    sorted by damage, descending
    """
    # Build list
    mech_list = create_mech_list(file_list, select_l, create_range_list_item)

    # Sort by speed
    mech_list.sort(key=itemgetter(3), reverse=True)

    # Print output
    print header
    header2 = "Name                          "
    header2 += "Tons BV    D3  D6  D9 D12 D15 D18 D21 D24"
    print header2
    for i in mech_list:
        print ("%-30s %3d %4d %3d %3d %3d %3d %3d %3d %3d %3d" %
               (i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9],
                i[10]))




## Mech type listing

def create_type_list_item(mech, i):
    """
    Compile info used by print_type_list()
    """
    name_str = mech.name + " " + mech.model + i.get_name()
    batt_val = mech.get_bv(i)
    weight = mech.weight

    warn = "!!"

    sco = "-"
    if mech.is_scout(i):
        sco = "X"
        warn = ""
    stri = "-"
    if mech.is_striker(i):
        stri = "X"
        warn = ""
    skir = "-"
    if mech.is_skirmisher(i):
        skir = "X"
        warn = ""
    brw = "-"
    mis = "-"
    snp = "-"
    if mech.is_sniper(i):
        snp = "X"
        warn = ""
    jug = "-"
    if mech.is_juggernaut(i):
        jug = "X"
        warn = ""

    return (name_str, weight, batt_val, sco, stri, skir, brw, mis, snp, jug,
            warn)

def print_type_list(file_list, select_l, header):
    """
    type_list output

    In the form of name, weight, BV, damage
    sorted by damage, descending
    """
    # Build list
    mech_list = create_mech_list(file_list, select_l, create_type_list_item)

    # Sort by speed
    mech_list.sort(key=itemgetter(3), reverse=True)

    # Print output
    print header
    header2 = "Name                          "
    header2 += "Tons BV    SCT STR SKR BRW MIS SNP JUG WARN"
    print header2
    for i in mech_list:
        print ("%-30s %3d %4d  %c   %c   %c   %c   %c   %c   %c  %s" %
               (i[0], i[1], i[2], i[3], i[4], i[5], i[6], i[7], i[8], i[9],
                i[10]))




## Default listing

def create_def_list_item(mech, i):
    """
    Compile info used by print_default()
    """
    name_str = mech.name + " " + mech.model + i.get_name()
    batt_val = mech.get_bv(i)
    weight = mech.weight
    source = i.source
    prod_era = conv_era(i.get_prod_era())
    return (name_str, weight, batt_val, source, prod_era)


def print_default(file_list, select_l, header):
    """
    Default output format

    In the form of name, weight, BV, source, era
    Intended to conform to the MUL format
    """
    # Build list
    mech_list = create_mech_list(file_list, select_l, create_def_list_item)

    # Print output
    print header
    print "Name                          Tons BV   Source   Era"
    for i in mech_list:
        print ("%-30s %3d %4d %-8s %s" % (i[0], i[1], i[2], i[3], i[4]))


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
                        dest = 'output', const = 'b')
    parser.add_argument('-bv', action='store_const', help='BV list output',
                        dest = 'output', const = 'bv')
    parser.add_argument('-a', action='store_const', help='Armor list output',
                        dest = 'output', const = 'a')
    parser.add_argument('-s', action='store_const', help='Speed list output',
                        dest = 'output', const = 's')
    parser.add_argument('-l', action='store_const', help='LRM list output',
                        dest = 'output', const = 'l')
    parser.add_argument('-sn', action='store_const', help='Snipe list output',
                        dest = 'output', const = 'sn')
    parser.add_argument('-cap', action='store_const',
                        help='Headcap list output',
                        dest = 'output', const = 'cap')
    parser.add_argument('-r', action='store_const', help='Range list output',
                        dest = 'output', const = 'r')
    parser.add_argument('-str', action='store_const',
                        help='Striker list output',
                        dest = 'output', const = 'str')
    parser.add_argument('-skir', action='store_const',
                        help='Skirmisher list output',
                        dest = 'output', const = 'skir')
    parser.add_argument('-jug', action='store_const',
                        help='Juggernaut list output',
                        dest = 'output', const = 'jug')
    parser.add_argument('-typ', action='store_const',
                        help='Mech type list output',
                        dest = 'output', const = 'typ')
    # Filter arguments
    parser.add_argument('-t', action='store_true', help='Select mechs with TAG')
    parser.add_argument('-c', action='store_true',
                        help='Select mechs with C3 Slave')
    parser.add_argument('-cm', action='store_true',
                        help='Select mechs with C3 Master')
    parser.add_argument('-ci', action='store_true',
                        help='Select mechs with C3i')
    parser.add_argument('-n', action='store_true',
                        help='Select mechs with Narc')
    parser.add_argument('-i', action='store_true',
                        help='Select Inner Sphere tech mechs')
    parser.add_argument('-cl', action='store_true',
                        help='Select Clan tech mechs')
    parser.add_argument('-cc', action='store_true',
                        help='Select mechs with Command Console')
    parser.add_argument('-e', action='store', default = 99, type=int,
                        help='Select mechs up to era <n>')
    parser.add_argument('-sf', action='store', default = 0, type=int,
                        help='Select mechs with at least speed <n>')
    parser.add_argument('-lrm', action='store', default = 0, type=int,
                        help='Select mechs with at least <n> lrms')
    parser.add_argument('-npr', action='store_true',
                        help='Select non-Primitive mechs')
    parser.add_argument('-wgt', action='store', default = 0, type=int,
                        help='Select mechs of weight <n>')
    # Default: one filename
    parser.add_argument('file', nargs='*')

    return parser.parse_args()


####################################
##### Main program starts here #####
####################################

def main():
    """
    main() function for summary.py. Prints out a summary of mechs
    according to the command-line switches.
    """
    # Parse arguments
    args = parse_arg()

    # Create lists
    file_list = []
    select = lambda x, y: True
    select_l = []
    select_l.append(select)
    header_l = []

    ### Create file_list ###

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
                    continue
                file_list.append(fname)

    ### Activate selectors ###

    # TAG
    if args.t:
        select_l.append(lambda x, y: y.gear.has_tag)
        header_l.append("with TAG")
    # C3 Slave
    if args.c:
        select_l.append(lambda x, y: y.gear.has_c3)
        header_l.append("with C3 Slave")
    # C3 Master
    if args.cm:
        select_l.append(lambda x, y: y.gear.has_c3m)
        header_l.append("with C3 Master")
    # C3i
    if args.ci:
        select_l.append(lambda x, y: y.gear.has_c3i)
        header_l.append("with C3i")
    # Narc
    if args.n:
        select_l.append(lambda x, y: y.gear.has_narc)
        header_l.append("with Narc")
    # Inner Sphere
    if args.i:
        select_l.append(lambda x, y: x.techbase == "Inner Sphere")
        header_l.append("Inner Sphere-tech")
    # Clan
    if args.cl:
        select_l.append(lambda x, y: x.techbase == "Clan")
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
    # Speed
    if args.sf > 0:
        spd = args.sf
        select_l.append(lambda x, y: (max(x.get_walk(), y.get_jump()) >= spd))
        header_l.append(("with at least speed %d" % spd))
    # LRMs
    if args.lrm > 0:
        lrm = args.lrm
        select_l.append(lambda x, y: (y.gear.lrms >= lrm))
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

    ### Process output ###

    # Construct header
    header = create_header(header_l)

    if args.output == 'b':
        print_bvt_list(file_list, select_l, header)
    elif args.output == 'bv':
        print_bv_list(file_list, select_l, header)
    elif args.output == 'a':
        print_armor_list(file_list, select_l, header)
    elif args.output == 's':
        print_speed_list(file_list, select_l, header)
    elif args.output == 'l':
        print_missile_list(file_list, select_l, header)
    elif args.output == 'sn':
        print_snipe_list(file_list, select_l, header)
    elif args.output == 'cap':
        print_headcap_list(file_list, select_l, header)
    elif args.output == 'r':
        print_range_list(file_list, select_l, header)
    elif args.output == 'str':
        print_striker_list(file_list, select_l, header)
    elif args.output == 'skir':
        print_skirmisher_list(file_list, select_l, header)
    elif args.output == 'jug':
        print_juggernaut_list(file_list, select_l, header)
    elif args.output == 'typ':
        print_type_list(file_list, select_l, header)
    else:
        print_default(file_list, select_l, header)

if __name__ == "__main__":
    main()
