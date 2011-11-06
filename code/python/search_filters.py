#!/usr/bin/env python

import json
import logging
import sys
import xapian

def search(dbpath, querystring, materials, offset=0, pagesize=10):
    # offset - defines starting point within result set
    # pagesize - defines number of records to retrieve

    # Open the database we're going to search.
    db = xapian.Database(dbpath)

### Start of example code.
    # Set up a QueryParser with a stemmer and suitable prefixes
    queryparser = xapian.QueryParser()
    queryparser.set_stemmer(xapian.Stem("en"))
    queryparser.add_prefix("title", "S")
    queryparser.add_prefix("description", "XD")

    # And parse the query
    query = queryparser.parse_query(querystring)

    if len(materials) > 0:
        # Filter the results to ones which contain at least one of the
        # materials.

        # Build a query for each material value
        material_queries = [
            xapian.Query('XM' + material.lower())
            for material in materials
        ]

        # Combine these queries with an OR operator
        material_query = xapian.Query(xapian.Query.OP_OR, material_queries)

        # Use the material query to filter the main query
        query = xapian.Query(xapian.Query.OP_FILTER, query, material_query)
### End of example code.

    # Use an Enquire object on the database to run the query
    enquire = xapian.Enquire(db)
    enquire.set_query(query)

    # And print out something about each match
    matches = []
    for index, match in enumerate(enquire.get_mset(offset, pagesize)):
        fields = json.loads(match.document.get_data())
        print u"%(rank)i: #%(docid)3.3i %(title)s" % {
            'rank': offset + index + 1,
            'docid': match.docid,
            'title': fields.get('TITLE', u''),
            }
        matches.append(match.docid)

    # Finally, make sure we log the query and displayed results
    logger = logging.getLogger("xapian.search")
    logger.info(
        "'%s'.material(%s)[%i:%i] = %s",
        querystring,
        materials,
        offset,
        offset + pagesize,
        ' '.join([str(docid) for docid in matches]),
        )

logging.basicConfig(level=logging.INFO)
search(dbpath = sys.argv[1], querystring = sys.argv[2],
       materials = sys.argv[3:])
