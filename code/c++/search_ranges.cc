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
    // and add in range processors
    Xapian::NumberRangeProcessor size_vrp(0, "mm", Xapian::RP_SUFFIX);
    queryparser.add_rangeprocessor(&size_vrp);
    Xapian::NumberRangeProcessor date_vrp(1);
    queryparser.add_rangeprocessor(&date_vrp);

    // And parse the query.
    Xapian::Query query = queryparser.parse_query(querystring);

    // Use an Enquire object on the database to run the query.
    Xapian::Enquire enquire(db);
    enquire.set_query(query);

    // And print out something about each match.
    Xapian::MSet mset = enquire.get_mset(offset, pagesize);

    clog << "'" << querystring << "'[" << offset << ":" << offset + pagesize
	 << "] =";
    for (Xapian::MSetIterator m = mset.begin(); m != mset.end(); ++m) {
	Xapian::docid did = *m;
	cout << m.get_rank() + 1 << ": #" << setfill('0') << setw(3) << did;

	const size_t DOC_FIELD_TITLE = 1;
	const size_t DOC_FIELD_DATE_MADE = 3;
	const size_t DOC_FIELD_MEASUREMENTS = 4;
	const string & data = m.get_document().get_data();
	cout << " (" << get_field(data, DOC_FIELD_DATE_MADE) << ") "
	     << get_field(data, DOC_FIELD_MEASUREMENTS) << "\n        "
	     << get_field(data, DOC_FIELD_TITLE) << '\n';
	// Log the document id.
	clog << ' ' << did;
    }
    clog << '\n';
}

int main(int argc, char** argv) {
    if (argc < 3) {
	cerr << "Usage: " << argv[0] << " DBPATH QUERYTERM...\n";
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
