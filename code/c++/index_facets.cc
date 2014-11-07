#include <xapian.h>

#include <cstdlib>
#include <fstream>
#include <iostream>
#include <string>
#include <vector>

#include "support.h"

using namespace std;

// Start of example code.
void index(const string & datapath, const string & dbpath)
{
    // Hardcode field offsets for simplicity.
    const size_t FIELD_ID_NUMBER = 0;
    const size_t FIELD_TITLE = 2;
    const size_t FIELD_MAKER = 3;
    const size_t FIELD_DESCRIPTION = 8;
    const size_t FIELD_COLLECTION = 10;

    // Create or open the database we're going to be writing to.
    Xapian::WritableDatabase db(dbpath, Xapian::DB_CREATE_OR_OPEN);

    // Set up a TermGenerator that we'll use in indexing.
    Xapian::TermGenerator termgenerator;
    termgenerator.set_stemmer(Xapian::Stem("en"));

    ifstream csv(datapath.c_str());
    vector<string> fields;
    csv_parse_line(csv, fields);

    // Check the CSV header line matches our hard-code offsets.
    if (fields.at(FIELD_ID_NUMBER) != "id_NUMBER" ||
	fields.at(FIELD_TITLE) != "TITLE" ||
	fields.at(FIELD_DESCRIPTION) != "DESCRIPTION" ||
	fields.at(FIELD_COLLECTION) != "COLLECTION" ||
	fields.at(FIELD_MAKER) != "MAKER") {
	// The CSV format doesn't match what we expect.
	cerr << "CSV format has changed!" << endl;
	exit(1);
    }

    while (csv_parse_line(csv, fields)) {
	// 'fields' is a vector mapping from field number to value.
	// We look up fields with the 'at' method so we get an exception
	// if that field isn't set.
	const string & description = fields.at(FIELD_DESCRIPTION);
	const string & title = fields.at(FIELD_TITLE);
	const string & identifier = fields.at(FIELD_ID_NUMBER);
	const string & collection = fields.at(FIELD_COLLECTION);
	const string & maker = fields.at(FIELD_MAKER);

	// We make a document and tell the term generator to use this.
	Xapian::Document doc;
	termgenerator.set_document(doc);

	// Index each field with a suitable prefix.
	termgenerator.index_text(title, 1, "S");
	termgenerator.index_text(description, 1, "XD");

	// Index fields without prefixes for general search.
	termgenerator.index_text(title);
	termgenerator.increase_termpos();
	termgenerator.index_text(description);

	// Add the collection as a value in slot 0.
	doc.add_value(0, collection);

	// Add the maker as a value in slot 1.
	doc.add_value(1, maker);

	// Store all the fields for display purposes.
	doc.set_data(identifier + "\n" + title + "\n" + description);

	// We use the identifier to ensure each object ends up in the
	// database only once no matter how many times we run the
	// indexer.
	string idterm = "Q" + identifier;
	doc.add_boolean_term(idterm);
	db.replace_document(idterm, doc);
    }
}
// End of example code.

int main(int argc, char** argv) {
    if (argc != 3) {
	cerr << "Usage: " << argv[0] << " DATAPATH DBPATH" << endl;
	return 1;
    }
    index(argv[1], argv[2]);
}
