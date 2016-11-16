#include <xapian.h>

#include <cstdio>
#include <iomanip>
#include <iostream>
#include <string>

#include "support.h"

using namespace std;

static void
search(const string & dbpath, const string & querystring,
       Xapian::doccount offset = 0, Xapian::doccount pagesize = 10)
{
    // offset - defines starting point within result set.
    // pagesize - defines number of records to retrieve.

    // Open the database we're going to search.
    Xapian::WritableDatabase db(dbpath);

    // Start of adding synonyms
    db.add_synonym("time", "calendar");
    // End of adding synonyms

    // Set up a QueryParser with a stemmer and suitable prefixes.
    Xapian::QueryParser queryparser;
    queryparser.set_stemmer(Xapian::Stem("en"));
    queryparser.set_stemming_strategy(queryparser.STEM_SOME);
    queryparser.add_prefix("title", "S");
    queryparser.add_prefix("description", "XD");

    // Start of set database
    queryparser.set_database(db);
    // End of set database

    // And parse the query.
    Xapian::Query query = queryparser.parse_query(querystring,
						  queryparser.FLAG_DEFAULT |
						  queryparser.FLAG_SYNONYM);

    // Use an Enquire object on the database to run the query.
    Xapian::Enquire enquire(db);
    enquire.set_query(query);

    // And print out something about each match.
    Xapian::MSet mset = enquire.get_mset(offset, pagesize);

    clog << "'" << querystring << "'[" << offset << ":" << offset + pagesize
	 << "] =";
    for (Xapian::MSetIterator m = mset.begin(); m != mset.end(); ++m) {
	Xapian::docid did = *m;
	cout << m.get_rank() + 1 << ": #" << setfill('0') << setw(3) << did
	     << ' ';

	const size_t DOC_FIELD_TITLE = 1;
	const string & data = m.get_document().get_data();
	cout << get_field(data, DOC_FIELD_TITLE) << endl;
	// Log the document id.
	clog << ' ' << did;
    }
    clog << endl;
}

int main(int argc, char** argv) {
    if (argc < 3) {
	cerr << "Usage: " << argv[0] << " DBPATH QUERYTERM..." << endl;
	return 1;
    }
    const char * dbpath = argv[1];

    // Join the rest of the arguments with spaces to make the query string.
    string querystring;
    for (argv += 2; *argv; ++argv) {
	if (!querystring.empty()) querystring += ' ';
	querystring += *argv;
    }

    search(dbpath, querystring);
}
