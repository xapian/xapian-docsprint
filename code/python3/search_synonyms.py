#!/usr/bin/env python

import json
import sys
import xapian
import support

def search(dbpath, querystring, offset=0, pagesize=10):
    # offset - defines starting point within result set
    # pagesize - defines number of records to retrieve

    # Open the database we're going to search.
    db = xapian.WritableDatabase(dbpath)

    # Start of adding synonyms
    db.add_synonym("time", "calendar")
    # End of adding synonyms

    # Set up a QueryParser with a stemmer and suitable prefixes
    queryparser = xapian.QueryParser()
    queryparser.set_stemmer(xapian.Stem("en"))
    queryparser.set_stemming_strategy(queryparser.STEM_SOME)
    queryparser.add_prefix("title", "S")
    queryparser.add_prefix("description", "XD")

    # Start of set database
    queryparser.set_database(db)
    # End of set database

    # And parse the query
    query = queryparser.parse_query(querystring, queryparser.FLAG_SYNONYM)

    # Use an Enquire object on the database to run the query
    enquire = xapian.Enquire(db)
    enquire.set_query(query)

    # And print out something about each match
    matches = []
    for match in enquire.get_mset(offset, pagesize):
        fields = json.loads(match.document.get_data().decode('utf8'))
        print(u"%(rank)i: #%(docid)3.3i %(title)s" % {
            'rank': match.rank + 1,
            'docid': match.docid,
            'title': fields.get('TITLE', u''),
            })
        matches.append(match.docid)

    # Finally, make sure we log the query and displayed results
    support.log_matches(querystring, offset, pagesize, matches)

if len(sys.argv) < 3:
    print("Usage: %s DBPATH QUERYTERM..." % sys.argv[0])
    sys.exit(1)

search(dbpath = sys.argv[1], querystring = " ".join(sys.argv[2:]))
