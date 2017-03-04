/* Support code for Java examples */
package code.java;

import java.util.ArrayList;

public class support {
	// Returns an ArrayList of the parsed CSV line
	public static ArrayList<String> parseCsvLine(String csvLine) {
		ArrayList<String> words = new ArrayList<String>();
		boolean insideQuote = false, endEarly = false;
		int start = 0, end = 0;
		for (int i = 0; i < csvLine.length()-1; i++) {
			if(csvLine.charAt(i) == ',' && !insideQuote) {
				if (endEarly) {
					words.add(csvLine.substring(start,i-1).replace("\"\"","\""));
					endEarly = false;
				} else {
					words.add(csvLine.substring(start,i));
				}

				if(csvLine.charAt(i+1) == '"') {
					start = i + 2;
					i++;
					endEarly = true;
					insideQuote = true;
				} else {
					start = i + 1;
				}
			} else if (csvLine.charAt(i) == '"') {
				insideQuote = !insideQuote;
			}
		}
		words.add(csvLine.substring(start));
		return words;
	}
}
