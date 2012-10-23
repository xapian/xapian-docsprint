#!/usr/bin/env python

import json
import logging
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
    # Start of example code.
    keymaker = xapian.MultiValueKeyMaker()
    keymaker.add_value(1, False)
    keymaker.add_value(3, True)
    enquire.set_sort_by_key_then_relevance(keymaker, False)
    # End of example code.

    # And print out something about each match
    matches = []
    for index, match in enumerate(enquire.get_mset(offset, pagesize)):
        fields = json.loads(match.document.get_data())
        print u"%(rank)i: #%(docid)3.3i %(name)s %(date)s\n        Population %(pop)s" % {
            'rank': offset + index + 1,
            'docid': match.docid,
            'name': fields.get('name', u''),
            'date': support.format_date(fields.get('admitted', u'')),
            'pop': support.format_numeral(fields.get('population', 0)),
            'lat': fields.get('latitude', u''),
            'lon': fields.get('longitude', u''),
            }
        matches.append(match.docid)

    # Finally, make sure we log the query and displayed results
    support.log_matches(querystring, offset, pagesize, matches)
### End of example code.

logging.basicConfig(level=logging.INFO)
search(dbpath = sys.argv[1], querystring = " ".join(sys.argv[2:]))
