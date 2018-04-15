/** @file search_letor.cc
 */
/* Copyright (C) 2004,2005,2006,2007,2008,2009,2010,2015 Olly Betts
 * Copyright (C) 2011 Parth Gupta
 * Copyright (C) 2016 Ayush Tomar
 *
 * This program is free software; you can redistribute it and/or
 * modify it under the terms of the GNU General Public License as
 * published by the Free Software Foundation; either version 2 of the
 * License, or (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301
 * USA
 */
#include <xapian-letor.h>

#include <iostream>
#include <sstream>
#include <string>

using namespace std;

static void show_usage()
{
    cout << "Usage: search_letor --db=DBPATH MODEL_METADATA_KEY QUERY\n";
}

// Start of example code
void rank_letor(string db_path, string model_key, string query_)
{
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
    Xapian::Query query_no_prefix = parser.parse_query(query_,
						       parser.FLAG_DEFAULT);
    // query with title as default prefix
    Xapian::Query query_default_prefix = parser.parse_query(query_,
							    parser.FLAG_DEFAULT,
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

    // Re-rank the existing mset using the letor model.
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
	return 1;
    }
    string db_path = argv[1];
    string model_key = argv[2];
    string query = argv[3];
    rank_letor(db_path, model_key, query);
    return 0;
}
