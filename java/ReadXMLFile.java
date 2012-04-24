
import java.io.File;

public class ReadXMLFile {

	public static void main (String argv[]) {

		try {
			File fXmlFile = new File("../../../Master_List_new/Assault/Atlas AS7-D.ssw");
			Mech Atlas = new Mech(fXmlFile);

		} catch (Exception e) {
			e.printStackTrace();
		}
	}
}

