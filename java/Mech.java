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
	short weight;
	String motive;
	InternalStructure structure;
	Cockpit cockpit;
	Armor armor;

	Mech(File fXmlFile) {
		try {
			DocumentBuilderFactory dbFactory = DocumentBuilderFactory.newInstance();
			DocumentBuilder dBuilder = dbFactory.newDocumentBuilder();
			Document doc = dBuilder.parse(fXmlFile);
			doc.getDocumentElement().normalize();

			System.out.println("Root element :" + doc.getDocumentElement().getNodeName());
			// Extract base information
			name = doc.getDocumentElement().getAttribute("name");
			model = doc.getDocumentElement().getAttribute("model");
			weight = (short)Integer.parseInt(doc.getDocumentElement().getAttribute("tons"));

			System.out.println(name + " " + model);
			System.out.println("Mech weight : " + weight);

			// Internal Structure
			NodeList nList = doc.getElementsByTagName("structure");
			System.out.println("-----------------------");

			for (int temp = 0; temp < nList.getLength(); temp++) {

				Node nNode = nList.item(temp);
				
				Element el = (Element)nNode;

				structure = new InternalStructure(el, weight);
			}

			// Cockpit
			nList = doc.getElementsByTagName("cockpit");
			System.out.println("-----------------------");

			for (int temp = 0; temp < nList.getLength(); temp++) {

				Node nNode = nList.item(temp);
				
				Element el = (Element)nNode;

				cockpit = new Cockpit(el);
			}

			// Armor
			nList = doc.getElementsByTagName("armor");
			System.out.println("-----------------------");

			for (int temp = 0; temp < nList.getLength(); temp++) {

				Node nNode = nList.item(temp);
				
				Element el = (Element)nNode;

				armor = new Armor(el);
			}
		} catch (Exception e) {
			e.printStackTrace();
		}

	}
}
