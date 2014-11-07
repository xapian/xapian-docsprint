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
    # and add in value range processors
    # Start of custom VRP code
    class PopulationValueRangeProcessor(xapian.ValueRangeProcessor):
        def __init__(self, value, low, high):
            super(PopulationValueRangeProcessor, self).__init__()
            self.nvrp = xapian.NumberValueRangeProcessor(value)
            self.low = low
            self.high = high

        def __call__(self, begin, end):
            if begin != u"":
                try:
                    _begin = int(begin)
                    if _begin < self.low or _begin > self.high:
                        raise ValueError()
                except:
                    return (xapian.BAD_VALUENO, begin, end)
            if end != u"":
                try:
                    _end = int(end)
                    if _end < self.low or _end > self.high:
                        raise ValueError()
                except:
                    return (xapian.BAD_VALUENO, begin, end)
            return self.nvrp(begin, end)
    queryparser.add_valuerangeprocessor(
        PopulationValueRangeProcessor(3, 500000, 50000000)
        )
    # End of custom VRP code
    # Start of date example code
    queryparser.add_valuerangeprocessor(
        xapian.DateValueRangeProcessor(2, True, 1860)
    )
    queryparser.add_valuerangeprocessor(
        xapian.NumberValueRangeProcessor(1, '')
    )
    # End of date example code
    # And parse the query
    query = queryparser.parse_query(querystring)

    # Use an Enquire object on the database to run the query
    enquire = xapian.Enquire(db)
    enquire.set_query(query)

    # And print out something about each match
    matches = []
    for match in enquire.get_mset(offset, pagesize):
        fields = json.loads(match.document.get_data())
        population = support.format_numeral(fields.get('population', 0))
        date = support.format_date(fields.get('admitted'))

        print u"""\
%(rank)i: #%(docid)3.3i %(name)s %(date)s
        Population %(pop)s""" % {
            'rank': match.rank + 1,
            'docid': match.docid,
            'name': fields.get('name', u''),
            'date': date,
            'pop': population,
            'lat': fields.get('latitude', u''),
            'lon': fields.get('longitude', u''),
            }
        matches.append(match.docid)

    # Finally, make sure we log the query and displayed results
    support.log_matches(querystring, offset, pagesize, matches)
### End of example code.

if len(sys.argv) < 3:
    print "Usage: %s DBPATH QUERYTERM..." % sys.argv[0]
    sys.exit(1)

logging.basicConfig(level=logging.INFO)
search(dbpath = sys.argv[1], querystring = " ".join(sys.argv[2:]))
