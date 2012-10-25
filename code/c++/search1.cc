#include <xapian.h>

#include <cstdio>
#include <iomanip>
#include <iostream>
#include <string>

using namespace std;

static string
get_field(const string & data, size_t field)
{
    size_t start = 0;
    while (true) {
	size_t end = data.find('\n', start);
	if (field == 0)
	    return string(data, start, end - start);
	start = end;
	if (start != string::npos) ++start;
	--field;
    }
}

// Start of example code.
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

    // And print out something about each match.
    Xapian::MSet mset = enquire.get_mset(offset, pagesize);

    clog << "'" << querystring << "'[" << offset << ":" << offset + pagesize
	 << "] =";
    for (Xapian::MSetIterator m = mset.begin(); m != mset.end(); ++m) {
	Xapian::docid did = *m;
	cout << m.get_rank() + 1 << ": #" << setfill('0') << setw(3) << did
	     << ' ';

	const string & data = m.get_document().get_data();
	cout << get_field(data, 1) << endl;
	// Log the document id.
	clog << ' ' << did;
    }
    clog << endl;
}
// End of example code.

int main(int argc, char** argv) {
    if (argc < 3) {
	cerr << "Syntax: " << argv[0] << " DBPATH QUERYTERM[...]" << endl;
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
