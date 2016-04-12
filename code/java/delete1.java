package code.java;

import org.xapian.WritableDatabase;
import org.xapian.XapianConstants;

public class delete1 {

    // Command line args - dbpath identifiers...
    public static void main(String[] args) {
        if(args.length < 2)
        {
            System.out.println("Insufficient number of arguments (should be dbpath identifiers...)");
            return;
        }
        deleteDocs(args[0], args);
    }

    // Start of example code.
    public static void deleteDocs(String dbpath, String[] identifierArgs) {
        // Open the database we're going to be deleting from.
        WritableDatabase db = new WritableDatabase(dbpath, XapianConstants.DB_OPEN);

        // Identifiers start from index 1
        for(int i = 1; i < identifierArgs.length; i++)
        {
            String idterm = "Q" + identifierArgs[i];
            db.deleteDocument(idterm);
        }

        // Commit to delete documents from disk
        db.commit();
    }
    // End of example code.
}
