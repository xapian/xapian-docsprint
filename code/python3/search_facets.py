#!/usr/bin/env python

import json
import sys
import xapian
import support

def search(dbpath, querystring, offset=0, pagesize=10):
    # offset - defines starting point within result set
    # pagesize - defines number of records to retrieve

    # Open the database we're going to search.
    db = xapian.Database(dbpath)

    # Set up a QueryParser with a stemmer and suitable prefixes
    queryparser = xapian.QueryParser()
    queryparser.set_stemmer(xapian.Stem("en"))
    queryparser.set_stemming_strategy(queryparser.STEM_SOME)
    queryparser.add_prefix("title", "S")
    queryparser.add_prefix("description", "XD")

    # And parse the query
    query = queryparser.parse_query(querystring)

    # Use an Enquire object on the database to run the query
    enquire = xapian.Enquire(db)
    enquire.set_query(query)

    # And print out something about each match
    matches = []

### Start of example code.
    # Set up a spy to inspect the MAKER value at slot 1
    spy = xapian.ValueCountMatchSpy(1)
    enquire.add_matchspy(spy)

    for match in enquire.get_mset(offset, pagesize, 100):
        fields = json.loads(match.document.get_data().decode('utf8'))
        print(u"%(rank)i: #%(docid)3.3i %(title)s" % {
            'rank': match.rank + 1,
            'docid': match.docid,
            'title': fields.get('TITLE', u''),
            })
        matches.append(match.docid)

    # Fetch and display the spy values
    for facet in spy.values():
        print("Facet: %(term)s; count: %(count)i" % {
            'term' : facet.term.decode('utf-8'),
            'count' : facet.termfreq
        })

    # Finally, make sure we log the query and displayed results
    support.log_matches(querystring, offset, pagesize, matches)
### End of example code.

if len(sys.argv) < 3:
    print("Usage: %s DBPATH QUERYTERM..." % sys.argv[0])
    sys.exit(1)

search(dbpath = sys.argv[1], querystring = " ".join(sys.argv[2:]))
