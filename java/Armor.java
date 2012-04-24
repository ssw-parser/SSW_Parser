
/*
 *    SSW-file parser: Prints mech summaries
 *    Copyright (C) 2012  Christer Nyfält
 *
 *    This program is free software; you can redistribute it and/or modify
 *    it under the terms of the GNU General Public License as published by
 *    the Free Software Foundation; either version 2 of the License, or
 *    (at your option) any later version.
 *
 *    This program is distributed in the hope that it will be useful,
 *    but WITHOUT ANY WARRANTY; without even the implied warranty of
 *    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *    GNU General Public License for more details.
 *
 *    You should have received a copy of the GNU General Public License along
 *    with this program; if not, write to the Free Software Foundation, Inc.,
 *    51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
 */

import org.w3c.dom.NodeList;
import org.w3c.dom.Node;
import org.w3c.dom.Element;

public class Armor {
	String type;
	int tech_base;
	int hd;
	int ct;
	int ctr;
	int lt;
	int ltr;
	int rt;
	int rtr;
	int la;
	int ra;
	int ll;
	int rl;
	int total;

	Armor(Element aElement) {
		type = getTagValue("type", aElement);
		tech_base = Integer.parseInt(aElement.getAttribute("techbase"));
		hd = Integer.parseInt(getTagValue("hd", aElement));
		ct = Integer.parseInt(getTagValue("ct", aElement));
		ctr = Integer.parseInt(getTagValue("ctr", aElement));
		lt = Integer.parseInt(getTagValue("lt", aElement));
		ltr = Integer.parseInt(getTagValue("ltr", aElement));
		rt = Integer.parseInt(getTagValue("rt", aElement));
		rtr = Integer.parseInt(getTagValue("rtr", aElement));
		la = Integer.parseInt(getTagValue("la", aElement));
		ra = Integer.parseInt(getTagValue("ra", aElement));
		ll = Integer.parseInt(getTagValue("ll", aElement));
		rl = Integer.parseInt(getTagValue("rl", aElement));
		total = hd + ct + ctr + lt + ltr + rt + rtr + la + ra + ll + rl;
		System.out.println("Armor Type : " + type);
		System.out.println("Tech Base : " + tech_base);
		System.out.println("Head              : " + hd);
		System.out.println("Center Torso      : " + ct);
		System.out.println("Center Torso Rear : " + ctr);
		System.out.println("Left Torso        : " + lt);
		System.out.println("Left Torso Rear   : " + ltr);
		System.out.println("Right Torso       : " + rt);
		System.out.println("Right Torso Rear  : " + rtr);
		System.out.println("Left Arm          : " + la);
		System.out.println("Right Arm         : " + ra);
		System.out.println("Left Leg          : " + ll);
		System.out.println("Right Leg         : " + rl);
		System.out.println("Total Armor       : " + total);
	}

	private static String getTagValue(String sTag, Element eElement) {
		NodeList nlList = eElement.getElementsByTagName(sTag).item(0).getChildNodes();

		Node nValue = (Node) nlList.item(0);

		return nValue.getNodeValue();
	}

}


