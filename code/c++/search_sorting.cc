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
    Xapian::Database db(dbpath);

    // Set up a QueryParser with a stemmer and suitable prefixes.
    Xapian::QueryParser queryparser;
    queryparser.set_stemmer(Xapian::Stem("en"));
    queryparser.set_stemming_strategy(queryparser.STEM_SOME);
    queryparser.add_prefix("title", "S");
    queryparser.add_prefix("description", "XD");

    // And parse the query.
    Xapian::Query query = queryparser.parse_query(querystring);

    // Use an Enquire object on the database to run the query.
    Xapian::Enquire enquire(db);
    enquire.set_query(query);
    // Start of example code.
    enquire.set_sort_by_value_then_relevance(1, false);
    // End of example code.

    // And print out something about each match.
    Xapian::MSet mset = enquire.get_mset(offset, pagesize);

    clog << "'" << querystring << "'[" << offset << ":" << offset + pagesize
	 << "] =";
    for (Xapian::MSetIterator m = mset.begin(); m != mset.end(); ++m) {
	const size_t DOC_FIELD_NAME = 0;
	const size_t DOC_FIELD_DESCRIPTION = 1;
	const size_t DOC_FIELD_MOTTO = 2;
	const size_t DOC_FIELD_ADMITTED = 3;
	const size_t DOC_FIELD_POPULATION = 4;

	Xapian::docid did = *m;
	const string& data = m.get_document().get_data();
	const string& date = format_date(get_field(data, DOC_FIELD_ADMITTED));
	const string& population =
	    format_numeral(get_field(data, DOC_FIELD_POPULATION));

	cout << m.get_rank() + 1 << ": #" << setfill('0') << setw(3) << did
	     << " " << get_field(data, DOC_FIELD_NAME) << " "
	     << date << "\n        Population "
	     << population << endl;
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
