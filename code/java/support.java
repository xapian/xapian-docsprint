/* Support code for Java examples */

package code.java;
import java.util.ArrayList;

public class support {

	// Returns an ArrayList of the parsed CSV line
	public static ArrayList<String> parseCsvLine(String csvLine) {
		ArrayList<String> words = new ArrayList<String>();
		boolean notInsideComma = true;int start = 0, end = 0;
		for (int i = 0; i < csvLine.length()-1; i++) {
			if(csvLine.charAt(i) == ',' && notInsideComma) {
				words.add(csvLine.substring(start,i));
				start = i + 1;
			} else if (csvLine.charAt(i) == '"') {
				notInsideComma =! notInsideComma;
			}
		}
		words.add(csvLine.substring(start));
		return words;
	}

}
