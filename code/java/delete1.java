package code.java;

import org.xapian.WritableDatabase;
import org.xapian.XapianConstants;

public class delete1 {

    // Command line args - dbpath identifiers...
    public static void main(String[] args) {
        if (args.length < 2) {
            System.out.println("Insufficient number of arguments (should be dbpath identifiers...)");
            return;
        }
        // Splitting the array to obtain an array of identifiers
        String[] identifierArgs = new String[args.length - 1];
        System.arraycopy(args, 1, identifierArgs, 0, identifierArgs.length);
        deleteDocs(args[0], identifierArgs);
    }

    // Start of example code.
    public static void deleteDocs(String dbpath, String[] identifierArgs) {
        // Open the database we're going to be deleting from.
        WritableDatabase db = new WritableDatabase(dbpath, XapianConstants.DB_OPEN);

        for (String identifierArg : identifierArgs) {
            String idterm = "Q" + identifierArg;
            db.deleteDocument(idterm);
        }

        // Commit to delete documents from disk
        db.commit();
    }
    // End of example code.
}
