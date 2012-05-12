
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

public class Engine implements Item {
	short rating;
	String type;
	int tech_base;

	Engine(Element eElement) {
		rating = (short)Integer.parseInt(eElement.getAttribute("rating"));
		tech_base = Integer.parseInt(eElement.getAttribute("techbase"));

		NodeList childnl = eElement.getChildNodes();
		Node child = childnl.item(0);

		type = child.getNodeValue();
		System.out.println("Engine Type : " + type);
		System.out.println("Engine Rating : " + rating);
		System.out.println("Tech Base : " + tech_base);
	}

	public byte get_rules_level()
	{
		byte r_level;

		if (type == "Fusion Engine")
			r_level = INTRO_TECH;
		else if (type == "XL Engine")
			r_level = TOURNAMENT_LEGAL;
		else if (type == "Light Fusion Engine")
			r_level = TOURNAMENT_LEGAL;
		else if (type == "Compact Fusion Engine")
			r_level = TOURNAMENT_LEGAL;
		else if (type == "XXL Engine")
			r_level = EXPERIMENTAL;
		else if (type == "Primitive Fusion Engine")
			r_level = PRIMITIVE;
		else
			{
				System.out.println("Unknown Engine:" + type);
				System.exit(-1);
				return -1;
			}			
		// Large engines are advanced

		if (rating > 400 && r_level < ADVANCED)
			r_level = ADVANCED;

		return r_level;
	}

	public double get_weight()
	{
		double weight = 0.0;

		// if (type == "Standard Cockpit")
		// 	weight = 3.0;
		// else if (type == "Small Cockpit")
		// 	weight = 2.0;
		// else if (type == "Torso-Mounted Cockpit")
		// 	weight = 4.0;
		// else if (type == "Primitive Cockpit")
		// 	weight = 5.0;
		// else
		// 	{
		// 		System.out.println("Unknown cockpit:" + type);
		// 		System.exit(-1);
		// 		weight = 0.0;
		// 	}			

		// // Command Console
		// if (console == "TRUE")
		// 	weight += 3.0;

		return weight;
	}

	public long get_cost()
	{
		long cost = 0;

		// if (type == "Standard Cockpit")
		// 	cost = 200000;
		// else if (type == "Small Cockpit")
		// 	cost = 175000;
		// else if (type == "Torso-Mounted Cockpit")
		// 	cost = 750000;
		// else if (type == "Primitive Cockpit")
		// 	cost = 100000;
		// else
		// 	{
		// 		System.out.println("Unknown cockpit:" + type);
		// 		System.exit(-1);
		// 		cost = 0;
		// 	}			

		// // Command Console
		// if (console == "TRUE")
		// 	cost += 750000;

		return cost;
	}
}


