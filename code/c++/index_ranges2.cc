#include <xapian.h>

#include <cstdlib>
#include <fstream>
#include <iostream>
#include <string>
#include <vector>

#include "support.h"

using namespace std;

void index(const string & datapath, const string & dbpath)
{
    // Hardcode field offsets for simplicity.
    const size_t FIELD_NAME = 0;
    const size_t FIELD_ADMITTED = 2;
    const size_t FIELD_ORDER = 3;
    const size_t FIELD_POPULATION = 4;
    const size_t FIELD_MOTTO = 7;
    const size_t FIELD_DESCRIPTION = 8;

    // Create or open the database we're going to be writing to.
    Xapian::WritableDatabase db(dbpath, Xapian::DB_CREATE_OR_OPEN);

    // Set up a TermGenerator that we'll use in indexing.
    Xapian::TermGenerator termgenerator;
    termgenerator.set_stemmer(Xapian::Stem("en"));

    ifstream csv(datapath.c_str());
    vector<string> fields;
    csv_parse_line(csv, fields);

    // Check the CSV header line matches our hard-code offsets.
    if (fields.at(FIELD_NAME) != "name" ||
	fields.at(FIELD_ADMITTED) != "admitted" ||
	fields.at(FIELD_ORDER) != "order" ||
	fields.at(FIELD_POPULATION) != "population" ||
	fields.at(FIELD_MOTTO) != "motto" ||
	fields.at(FIELD_DESCRIPTION) != "description") {
	// The CSV format doesn't match what we expect.
	cerr << "CSV format has changed!" << endl;
	exit(1);
    }

    while (csv_parse_line(csv, fields)) {
	// 'fields' is a vector mapping from field number to value.
	// We look up fields with the 'at' method so we get an exception
	// if that field isn't set.
	const string & name = fields.at(FIELD_NAME);
	const string & description = fields.at(FIELD_DESCRIPTION);
	const string & motto = fields.at(FIELD_MOTTO);
	const string & admitted = fields.at(FIELD_ADMITTED);
	const string & population = fields.at(FIELD_POPULATION);
	const string & order = fields.at(FIELD_ORDER);

	// We make a document and tell the term generator to use this.
	Xapian::Document doc;
	termgenerator.set_document(doc);

// Start of example code.
	// Index each field with a suitable prefix.
	termgenerator.index_text(name, 1, "S");
	termgenerator.index_text(description, 1, "XD");
	termgenerator.index_text(motto, 1, "XM");

	// Index fields without prefixes for general search.
	termgenerator.index_text(name);
	termgenerator.increase_termpos();
	termgenerator.index_text(description);
	termgenerator.increase_termpos();
	termgenerator.index_text(motto);

	// Add document values.
	if (!admitted.empty()) {
	    doc.add_value(1, Xapian::sortable_serialise(atoi(admitted.substr(0, 4).c_str())));
	    doc.add_value(2, admitted); // YYYYMMDD
	}
	if (!population.empty()) {
	    doc.add_value(3, Xapian::sortable_serialise(atoi(population.c_str())));
	}
// End of example code.

	// Store all the fields for display purposes.
	doc.set_data(name + "\n" + description + "\n" + motto + "\n" +
		     admitted + "\n" + population + "\n" + order);

	// We use the order to ensure each object ends up in the
	// database only once no matter how many times we run the
	// indexer.
	string idterm = "Q" + order;
	doc.add_boolean_term(idterm);
	db.replace_document(idterm, doc);
    }
}

int main(int argc, char** argv) {
    if (argc != 3) {
	cerr << "Usage: " << argv[0] << " DATAPATH DBPATH" << endl;
	return 1;
    }
    index(argv[1], argv[2]);
}
