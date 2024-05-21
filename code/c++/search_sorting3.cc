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
    class DistanceKeyMaker : public Xapian::KeyMaker {
	string operator()(const Xapian::Document& doc) const override {
            // we want to return a sortable string which represents
            // the distance from Washington, DC to the middle of this
            // state.
	    const string& latlon = doc.get_value(4);
	    size_t comma = latlon.find(',');
            double lat = atof(latlon.c_str());
            double lon = atof(latlon.c_str() + comma + 1);
	    pair<double, double> coords = make_pair(lat, lon);
            pair<double, double> washington = make_pair(38.012, -77.037);
	    double distance = distance_between_coords(coords, washington);
            return Xapian::sortable_serialise(distance);
	}
    };
    DistanceKeyMaker distance_keymaker;
    enquire.set_sort_by_key_then_relevance(&distance_keymaker, false);
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
	     << population << '\n';
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
