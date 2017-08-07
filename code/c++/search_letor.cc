#include <xapian-letor.h>

#include <iostream>
#include <sstream>
#include <string>

using namespace std;

static void show_usage()
{
    cout << "Usage: rank_letor --db=DIRECTORY MODEL_METADATA_KEY QUERY\n";
}

// Start of example code.
// Stopwords:
static const char * sw[] = {
    "a", "about", "an", "and", "are", "as", "at",
    "be", "by",
    "en",
    "for", "from",
    "how",
    "i", "in", "is", "it",
    "of", "on", "or",
    "that", "the", "this", "to",
    "was", "what", "when", "where", "which", "who", "why", "will", "with"
};

void rank_letor(string db_path, string model_key, string query_)
{
    Xapian::SimpleStopper mystopper(sw, sw + sizeof(sw) / sizeof(sw[0]));
    Xapian::Stem stemmer("english");
    Xapian::doccount msize = 10;
    Xapian::QueryParser parser;
    parser.add_prefix("title", "S");
    parser.add_prefix("subject", "S");
    Xapian::Database db(db_path);
    parser.set_database(db);
    parser.set_default_op(Xapian::Query::OP_OR);
    parser.set_stemmer(stemmer);
    parser.set_stemming_strategy(Xapian::QueryParser::STEM_SOME);
    parser.set_stopper(&mystopper);
    Xapian::Query query_no_prefix = parser.parse_query(query_,
						       parser.FLAG_DEFAULT|
						       parser.FLAG_SPELLING_CORRECTION);
    // query with title as default prefix
    Xapian::Query query_default_prefix = parser.parse_query(query_,
							    parser.FLAG_DEFAULT|
							    parser.FLAG_SPELLING_CORRECTION,
							    "S");
    // Combine queries
    Xapian::Query query = Xapian::Query(Xapian::Query::OP_OR, query_no_prefix,
					query_default_prefix);
    Xapian::Enquire enquire(db);
    enquire.set_query(query);
    Xapian::MSet mset = enquire.get_mset(0, msize);

    cout << "Docids before re-ranking by LTR model:" << endl;
    for (Xapian::MSetIterator i = mset.begin(); i != mset.end(); ++i) {
	Xapian::Document doc = i.get_document();
	string data = doc.get_data();
	cout << *i << ": [" << i.get_weight() << "]\n" << data << "\n";
    }

    // Initialise Ranker object with ListNETRanker instance, db path and query.
    // See Ranker documentation for available Ranker subclass options.
    Xapian::ListNETRanker ranker;
    ranker.set_database_path(db_path);
    ranker.set_query(query);

    // Get vector of re-ranked docids
    ranker.rank(mset, model_key);

    cout << "Docids after re-ranking by LTR model:\n" << endl;

    for (Xapian::MSetIterator i = mset.begin(); i != mset.end(); ++i) {
	Xapian::Document doc = i.get_document();
	string data = doc.get_data();
	cout << *i << ": [" << i.get_weight() << "]\n" << data << "\n";
    }
}
// End of example code.

int main(int argc, char** argv)
{
    if (argc != 4) {
	show_usage();
	return 0;
    }
    string db_path = argv[1];
    string model_key = argv[2];
    string query = argv[3];
    rank_letor(db_path, model_key, query);
    return 0;
}
