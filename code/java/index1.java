package code.java;

import java.io.File;
import java.io.FileNotFoundException;
import java.util.Scanner;
import java.util.ArrayList;
import java.util.logging.Level;
import java.util.logging.Logger;
import org.xapian.Document;
import org.xapian.Stem;
import org.xapian.TermGenerator;
import org.xapian.WritableDatabase;
import org.xapian.XapianConstants;
import org.xapian.XapianJNI;

import code.java.support;

public class index1 {

    // Command line args - datapath dbpath
    public static void main(String[] args) {
        if (args.length < 2) {
            System.out.println("Insufficient number of arguments (should be datapath dbpath)");
            return;
        }
        index(args[0], args[1]);
    }

    // Start of example code.
    public static void index(String datapath, String dbpath) {
        // Create or open the database we're going to be writing to.
        WritableDatabase db = new WritableDatabase(dbpath, XapianConstants.DB_CREATE_OR_OPEN);
        // Set up a TermGenerator that we'll use in indexing.
        TermGenerator termGenerator = new TermGenerator();
        termGenerator.setStemmer(new Stem("en"));

        // Parsing the CSV input file
        Scanner csvScanner = null;

        try {
            File csv = new File(datapath);
            csvScanner = new Scanner(csv);
        } catch (FileNotFoundException ex) {
            Logger.getLogger(index1.class.getName()).log(Level.SEVERE, null, ex);
        }

        // Ignoring first line (contains descriptors)
        csvScanner.nextLine();

        while (csvScanner.hasNextLine()) {
            String currentLine = csvScanner.nextLine();

            /* Parsing each line for identifier, title, and description */
            ArrayList<String> parsedCSV = support.parseCsvLine(currentLine);
            // Identifier is the first comma seperated value (according to CSV file)
            String identifier = parsedCSV.get(0);

            // Title is third comma seperated value
            String title = parsedCSV.get(2);

            // Description is ninth comma sperated value
            String description = parsedCSV.get(8);

            /* Finished Parsing line */

            // We make a document and tell the term generator to use this.
            Document doc = new Document();
            termGenerator.setDocument(doc);

            // Index each field with a suitable prefix.
            termGenerator.indexText(title, 1, "S");
            termGenerator.indexText(description, 1, "XD");

            // Index fields without prefixes for general search.
            termGenerator.indexText(title);
            termGenerator.increaseTermpos();
            termGenerator.indexText(description);

            // Store all fields for display purposes
            doc.setData(currentLine);
            doc.addValue(0, title);

            // We use the identifier to ensure each object ends up in the
            // database only once no matter how many times we run the
            // indexer.
            String idterm = "Q"+identifier;
            doc.addBooleanTerm(idterm);
            db.replaceDocument(idterm, doc);
        }

        // Commit to write documents to disk
        db.commit();
        csvScanner.close();
    }
    // End of example code.

}
