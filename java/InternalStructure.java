
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

public class InternalStructure implements Item {
	String type;
	int tech_base;
	short wgt;

	InternalStructure(Element sElement, short weight) {
		type = getTagValue("type", sElement);
		tech_base = Integer.parseInt(sElement.getAttribute("techbase"));
		wgt = weight;
		System.out.println("Internal Structure Type : " + type);
		System.out.println("Tech Base : " + tech_base);
	}

	public byte get_rules_level()
	{
		if (type == "Standard Structure")
			return INTRO_TECH;
		else if (type == "Endo-Steel")
			return TOURNAMENT_LEGAL;
		else if (type == "Composite Structure")
			return ADVANCED;
		else if (type == "Reinforced Structure")
			return ADVANCED;
		else if (type == "Endo-Composite")
			return ADVANCED;
		else if (type == "Primitive Structure")
			return PRIMITIVE;
		else
			{
				System.out.println("Unknown structure:" + type);
				System.exit(-1);
				return -1;
			}			
	}

	public double get_weight()
	{
		double weight, factor;

		if (type == "Standard Structure")
			factor = 0.1;
		else if (type == "Endo-Steel")
			factor = 0.05;
		else if (type == "Composite Structure")
			factor = 0.05;
		else if (type == "Reinforced Structure")
			factor = 0.2;
		else if (type == "Endo-Composite")
			factor = 0.075;
		else if (type == "Primitive Structure")
			factor = 0.1;
		else
			{
				System.out.println("Unknown structure:" + type);
				System.exit(-1);
				factor = 0.0;
			}			

		weight = wgt * factor;
		weight = ceil_05(weight);
		return weight;
	}

	public long get_cost()
	{
		long factor;

		if (type == "Standard Structure")
			factor = 400;
		else if (type == "Endo-Steel")
			factor = 1600;
		else if (type == "Composite Structure")
			factor = 1600;
		else if (type == "Reinforced Structure")
			factor = 6400;
		else if (type == "Endo-Composite")
			factor = 3200;
		else if (type == "Primitive Structure")
			factor = 400;
		else
			{
				System.out.println("Unknown structure:" + type);
				System.exit(-1);
				factor = 0;
			}			

		return factor * wgt;
	}

	private double ceil_05(double value)
	{
		value *= 2.0;
		value = Math.ceil(value);
		value /= 2.0;
		return value;
	}

	private static String getTagValue(String sTag, Element eElement) {
		NodeList nlList = eElement.getElementsByTagName(sTag).item(0).getChildNodes();

		Node nValue = nlList.item(0);

		return nValue.getNodeValue();
	}

}


