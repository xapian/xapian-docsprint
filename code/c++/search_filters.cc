#include <xapian.h>

#include <cstdio>
#include <iomanip>
#include <iostream>
#include <string>
#include <vector>

#include "support.h"

using namespace std;

static void
search(const string & dbpath, const string & querystring,
       char * materials[],
       Xapian::doccount offset = 0, Xapian::doccount pagesize = 10)
{
    // offset - defines starting point within result set.
    // pagesize - defines number of records to retrieve.

    // Open the database we're going to search.
    Xapian::Database db(dbpath);

// Start of example code.
    // Set up a QueryParser with a stemmer and suitable prefixes.
    Xapian::QueryParser queryparser;
    queryparser.set_stemmer(Xapian::Stem("en"));
    queryparser.set_stemming_strategy(queryparser.STEM_SOME);
    queryparser.add_prefix("title", "S");
    queryparser.add_prefix("description", "XD");

    // And parse the query.
    Xapian::Query query = queryparser.parse_query(querystring);

    if (materials[0] != NULL) {
	// Filter the results to ones which contain at least one of the
	// materials.

	// Build a query for each material value
	vector<Xapian::Query> material_queries;
	while (*materials) {
	    string material("XM");
	    material += Xapian::Unicode::tolower(*materials);
	    material_queries.push_back(Xapian::Query(material));
	    ++materials;
	}

	// Combine these queries with an OR operator
	Xapian::Query material_query(Xapian::Query::OP_OR,
				     material_queries.begin(),
				     material_queries.end());

	// Use the material query to filter the main query
	query = Xapian::Query(Xapian::Query::OP_FILTER, query, material_query);
    }
// End of example code.

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
	cerr << "Usage: " << argv[0] << " DBPATH QUERY [MATERIALS...]" << endl;
	return 1;
    }
    const char * dbpath = argv[1];

    string querystring = argv[2];

    search(dbpath, querystring, argv + 3);
}
