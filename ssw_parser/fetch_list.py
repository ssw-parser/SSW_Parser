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
fetch_list.py
=============
Fetches faction lists from MUL
"""

import httplib

h = httplib.HTTP('www.masterunitlist.info', 80)
# Get Capellan Confederation (5) list, Jihad Era (14)
h.putrequest('GET', '/Era/FactionEraDetails?EraId=14&FactionId=5')
h.putheader('Host', 'www.masterunitlist.info')
h.putheader('Accept', 'text/html')
h.putheader('Accept', 'text/plain')
h.endheaders()
errcode, errmsg, headers = h.getreply()
print errcode # Should be 200
f = h.getfile()
data = f.read() # Get the raw HTML
f.close()

print data
