#include <xapian.h>

#include <cstdlib>
#include <fstream>
#include <iostream>
#include <vector>
#include <string>
#include <cstring>

using namespace std;

static bool
csv_parse_line(ifstream & csv, vector<string> & fields)
{
    fields.resize(0);

    char line[4096];
    if (!csv.getline(line, sizeof(line)))
	return false;

    // If the input has \r\n line endings, drop the \r.
    size_t len = strlen(line);
    if (len && line[len - 1] == '\r') line[len - 1] = '\0';

    bool in_quotes = false;
    string field;

    const unsigned END_OF_FIELD = 0x100;
    for (Xapian::Utf8Iterator i(line); i != Xapian::Utf8Iterator(); ++i) {
	unsigned ch = *i;

	if (!in_quotes) {
	    // If not already in double quotes, '"' starts quoting and
	    // ',' starts a new field.
	    if (ch == '"') {
		in_quotes = true;
		continue;
	    }
	    if (ch == ',')
		ch = END_OF_FIELD;
	} else if (ch == '"') {
	    // In double quotes, '"' either ends double quotes, or
	    // if followed by another '"', means a literal '"'.
	    if (++i == Xapian::Utf8Iterator()) {
		ch = END_OF_FIELD;
	    } else {
		ch = *i;
		if (ch != '"') {
		    in_quotes = false;
		    if (ch == ',')
			ch = END_OF_FIELD;
		}
	    }
	}

	if (ch == END_OF_FIELD) {
	    fields.push_back(field);
	    field.resize(0);
	    if (i == Xapian::Utf8Iterator())
		break;
	    continue;
	}

	field += ch;
    }
    return true;
}

// Start of example code.
void index(const string & datapath, const string & dbpath)
{
    // Hardcode field offsets for simplicity.
    const size_t FIELD_ID_NUMBER = 0;
    const size_t FIELD_TITLE = 2;
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
    if (fields.at(FIELD_ID_NUMBER) != "id_NUMBER" ||
	fields.at(FIELD_TITLE) != "TITLE" ||
	fields.at(FIELD_DESCRIPTION) != "DESCRIPTION") {
	// The CSV format doesn't match what we expect.
	cerr << "CSV format has changed!" << endl;
	exit(1);
    }
    
    while (csv_parse_line(csv, fields)) {
        // 'fields' is a vector mapping from field number to value.
	// We look up fields with the 'at' method so we get an exception
	// if that field isn't set.
	//
        // We're just going to use DESCRIPTION, TITLE and id_NUMBER.
        const string & description = fields.at(FIELD_DESCRIPTION);
        const string & title = fields.at(FIELD_TITLE);
        const string & identifier = fields.at(FIELD_ID_NUMBER);

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
	cerr << "Syntax: " << argv[0] << " DATAPATH DBPATH" << endl;
	return 1;
    }
    index(argv[1], argv[2]);
}
