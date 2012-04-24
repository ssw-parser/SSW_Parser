
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
	}

	private static String getTagValue(String sTag, Element eElement) {
		NodeList nlList = eElement.getElementsByTagName(sTag).item(0).getChildNodes();

		Node nValue = (Node) nlList.item(0);

		return nValue.getNodeValue();
	}

}


