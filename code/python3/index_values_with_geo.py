#!/usr/bin/env python

import json
from support import parse_states
import sys
import xapian

def index(datapath, dbpath):
    # Create or open the database we're going to be writing to.
    db = xapian.WritableDatabase(dbpath, xapian.DB_CREATE_OR_OPEN)

    # Set up a TermGenerator that we'll use in indexing.
    termgenerator = xapian.TermGenerator()
    termgenerator.set_stemmer(xapian.Stem("en"))

    for fields in parse_states(datapath):
        # 'fields' is a dictionary mapping from field name to value.
        # Pick out the fields we're going to index.
        name = fields.get('name', u'')
        description = fields.get('description', u'')
        motto = fields.get('motto', u'')
        admitted = fields.get('admitted', None)
        population = fields.get('population', None)
        order = fields.get('order', u'')

        # We make a document and tell the term generator to use this.
        doc = xapian.Document()
        termgenerator.set_document(doc)

        # index each field with a suitable prefix
        termgenerator.index_text(name, 1, 'S')
        termgenerator.index_text(description, 1, 'XD')
        termgenerator.index_text(motto, 1, 'XM')

        # Index fields without prefixes for general search.
        termgenerator.index_text(name)
        termgenerator.increase_termpos()
        termgenerator.index_text(description)
        termgenerator.increase_termpos()
        termgenerator.index_text(motto)

        # Add document values.
        if admitted is not None:
            doc.add_value(1, xapian.sortable_serialise(int(admitted[:4])))
            doc.add_value(2, admitted) # YYYYMMDD
        if population is not None:
            doc.add_value(3, xapian.sortable_serialise(int(population)))
### Start of example code.
        midlat = fields['midlat']
        midlon = fields['midlon']
        if midlat and midlon:
            doc.add_value(4, "%f,%f" % (float(midlat), float(midlon)))
### End of example code.

        # Store all the fields for display purposes.
        doc.set_data(json.dumps(fields))

        # We use the order to ensure each object ends up in the
        # database only once no matter how many times we run the
        # indexer.
        idterm = u"Q" + order
        doc.add_boolean_term(idterm)
        db.replace_document(idterm, doc)

if len(sys.argv) != 3:
    print("Usage: %s DATAPATH DBPATH" % sys.argv[0])
    sys.exit(1)

index(datapath = sys.argv[1], dbpath = sys.argv[2])
