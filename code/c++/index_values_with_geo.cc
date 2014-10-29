#include <xapian.h>
#include <cstdlib>
#include <fstream>
#include <iostream>
#include <vector>
#include <list>
#include <string>
#include <cstring>
#include <sstream> 

using namespace std;

string NumberToString ( int Number )
{
	stringstream ss;
	ss << Number;
	return ss.str();
}

const string
numbers_from_string( string &  str) {
 	list<int> numbers;
	string temp = " ";
	stringstream ss;
	ss<<str;
	int maxnum = -1;

	while(!ss.eof()) {
		ss>>temp;
    	try
    	{
    		int currnum = std::atoi(temp.c_str());
      		if( currnum > maxnum ) {
      			maxnum = currnum;
      		}  
    	}
    	catch(std::exception& e)
    	{
        	ss >> str; // keep iterating
    	}
	}

	return NumberToString(maxnum);
}

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
	    if (++i == Xapian::Utf8Iterator())
		break;
	    ch = *i;
	    if (ch != '"') {
		in_quotes = false;
		if (ch == ',')
		    ch = END_OF_FIELD;
	    }
	}

	if (ch == END_OF_FIELD) {
	    fields.push_back(field);
	    field.resize(0);
	    continue;
	}

	field += ch;
    }
    fields.push_back(field);
    return true;
}

void index(const string & datapath, const string & dbpath)
{
    // Hardcode field offsets for simplicity.
    const size_t FIELD_NAME = 0;
    const size_t FIELD_DESCRIPTION = 7;
    const size_t FIELD_MOTTO = 6;
    const size_t FIELD_ADMITTED = 2;
    const size_t FIELD_POPULATION = 3;
    const size_t FIELD_ORDER = 1;
    const size_t FIELD_LATITUDE = 4;
    const size_t FIELD_LONGIUDE = 5;


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
	fields.at(FIELD_MOTTO) != "motto" ||
	fields.at(FIELD_DESCRIPTION) != "description" ||
	fields.at(FIELD_ADMITTED) != "admitted" || 
	fields.at(FIELD_POPULATION) != "population" || 
	fields.at(FIELD_ORDER) != "order" ||
	fields.at(FIELD_LATITUDE) != "latitude" || 
	fields.at(FIELD_LONGIUDE) != "longitude") {
		// The CSV format doesn't match what we expect.
		cerr << "CSV format has changed!" << endl;
		exit(1);
    }

    while (csv_parse_line(csv, fields)) {
	// 'fields' is a vector mapping from field number to value.
	// We look up fields with the 'at' method so we get an exception
	// if that field isn't set
	const string & name = fields.at(FIELD_NAME);
    const string & description = fields.at(FIELD_DESCRIPTION);
    const string & motto = fields.at(FIELD_MOTTO);
    const string & admitted = fields.at(FIELD_ADMITTED);
    const string & population = fields.at(FIELD_POPULATION);
    const string & order = fields.at(FIELD_ORDER);
	const string & latitude = fields.at(FIELD_LATITUDE);
    const string & longitude = fields.at(FIELD_LONGIUDE);
	// We make a document and tell the term generator to use this.

	Xapian::Document doc;
	termgenerator.set_document(doc);

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


	// Store all the fields for display purposes.
	doc.set_data(name + "\n" + "\n" + description +"\n"+motto);

	/* Start of example code.
    # parse the two values we need*/
    string & admitted_ = fields.at(FIELD_ADMITTED);
    doc.add_value(1,  Xapian::sortable_serialise(atoi(admitted_.c_str())));
    doc.add_value(2, admitted_);
    string & population_ = fields.at(FIELD_POPULATION);
    doc.add_value(3, Xapian::sortable_serialise(atoi(population_.c_str())));
	// End of example code.
    string geoloc = latitude+","+longitude;
    doc.add_value(4,geoloc);

	// We use the identifier to ensure each object ends up in the
	// database only once no matter how many times we run the
	// indexer.
	string idterm = "Q" + order;
	doc.add_boolean_term(idterm);
	db.replace_document(idterm, doc);
    }
}

int main(int argc, char** argv) {
    if (argc != 3) {
	cerr << "Syntax: " << argv[0] << " DATAPATH DBPATH" << endl;
	return 1;
    }
    index(argv[1], argv[2]);
}



