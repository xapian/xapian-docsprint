package code.java;

import org.xapian.Database;
import org.xapian.Document;
import org.xapian.Enquire;
import org.xapian.MSet;
import org.xapian.MSetIterator;
import org.xapian.Query;
import org.xapian.QueryParser;
import org.xapian.Stem;

public class search1 {

    // Command line args - dbpath querystring
    public static void main(String[] args) {
        if (args.length < 2) {
            System.out.println("Insufficient number of arguments (should be dbpath querystring)");
            return;
        }
        search(args[0], args[1]);
    }

    public static void search(String dbpath, String queryString) {
        search(dbpath, queryString, 0, 10);
    }

    // Start of example code.
    public static void search(String dbpath, String queryString, int offset, int pagesize) {
        // offset - defines starting point within result set
        // pagesize - defines number of records to retrieve

        // Open the databse we're going to search.
        Database db = new Database(dbpath);

        // Set up a QueryParser with a stemmer and suitable prefixes
        QueryParser queryParser = new QueryParser();
        queryParser.setStemmer(new Stem("en"));
        queryParser.setStemmingStrategy(QueryParser.stem_strategy.STEM_SOME);
        // Start of prefix configuration.
        queryParser.addPrefix("title", "S");
        queryParser.addPrefix("description", "XD");
        // End of prefix configuration.

        // And parse the query
        Query query = queryParser.parseQuery(queryString);

        // Use an Enquire object on the database to run the query
        Enquire enquire = new Enquire(db);
        enquire.setQuery(query);

        // And print out something about each match
        MSet mset = enquire.getMSet(offset, pagesize);
        MSetIterator msetIterator = mset.begin();

        while (msetIterator.hasNext())
        {
            long rank = msetIterator.getRank();
            long docID = msetIterator.getDocId();
            Document doc = db.getDocument(docID);

            System.out.printf("%i: #%3.3i %s%n", rank+1, docID, doc.getValue(0))
            msetIterator.next();
        }

        System.out.printf("'%s'[%i:%i] = ", queryString, offset, offset+pagesize);
        msetIterator = mset.begin();
        while (msetIterator.hasNext())
        {
            System.out.printf("%i", msetIterator.getDocId());
            msetIterator.next();
            if (msetIterator.hasNext()) {
                System.out.print(" ");
            }
        }
        System.out.print("\n");
    }
    // End of example code.
}
