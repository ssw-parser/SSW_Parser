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

import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.DocumentBuilder;
import org.w3c.dom.Document;
import org.w3c.dom.NodeList;
import org.w3c.dom.Node;
import org.w3c.dom.Element;
import java.io.File;

public class Mech {
	String name;
	String model;
	String omni;
	short weight;
	int batt_val;
	double cost;
	byte prod_era;
	String motive;
	InternalStructure structure;
	Engine engine;
	Cockpit cockpit;
	Armor armor;

	Mech(File fXmlFile) {
		try {
			DocumentBuilderFactory dbFactory = DocumentBuilderFactory.newInstance();
			DocumentBuilder dBuilder = dbFactory.newDocumentBuilder();
			Document doc = dBuilder.parse(fXmlFile);
			doc.getDocumentElement().normalize();

			// Extract base information
			name = doc.getDocumentElement().getAttribute("name");
			model = doc.getDocumentElement().getAttribute("model");
			omni = doc.getDocumentElement().getAttribute("omnimech");
			weight = (short)Integer.parseInt(doc.getDocumentElement().getAttribute("tons"));

			batt_val = Integer.parseInt(Util.getChildData(doc, "battle_value"));
			cost = Double.parseDouble(Util.getChildData(doc, "cost"));
			prod_era = (byte)Integer.parseInt(Util.getChildData(doc, "productionera"));
			motive = Util.getChildData(doc, "motive_type");

			System.out.println(name + " " + model);
			System.out.println("Omnimech : " + omni);
			System.out.println("Mech weight : " + weight);
			System.out.println("Battle Value : " + batt_val);
			System.out.println("Cost : " + cost);
			System.out.println("Production Era : " + prod_era);
			System.out.println("Motive type : " + motive);

			// Internal Structure
			System.out.println("-----------------------");

				
			Element el = Util.getChild(doc, "structure");

			structure = new InternalStructure(el, weight);

			// Engine
			System.out.println("-----------------------");

				
			el = Util.getChild(doc, "engine");

			engine = new Engine(el);

			// Cockpit
			System.out.println("-----------------------");

			el = Util.getChild(doc, "cockpit");

			cockpit = new Cockpit(el);

			// Armor
			System.out.println("-----------------------");

			el = Util.getChild(doc, "armor");
			
			armor = new Armor(el);

		} catch (Exception e) {
			e.printStackTrace();
		}

	}
}
