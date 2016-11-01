#!/usr/bin/env python

import json
import sys
import xapian
from support import numbers_from_string, parse_csv_file

def index(datapath, dbpath):
    # Create or open the database we're going to be writing to.
    db = xapian.WritableDatabase(dbpath, xapian.DB_CREATE_OR_OPEN)

    # Set up a TermGenerator that we'll use in indexing.
    termgenerator = xapian.TermGenerator()
    termgenerator.set_stemmer(xapian.Stem("en"))

    for fields in parse_csv_file(datapath):
        # 'fields' is a dictionary mapping from field name to value.
        # Pick out the fields we're going to index.
        description = fields.get('DESCRIPTION', u'')
        title = fields.get('TITLE', u'')
        identifier = fields.get('id_NUMBER', u'')

        # We make a document and tell the term generator to use this.
        doc = xapian.Document()
        termgenerator.set_document(doc)

        # Index each field with a suitable prefix.
        termgenerator.index_text(title, 1, 'S')
        termgenerator.index_text(description, 1, 'XD')

        # Index fields without prefixes for general search.
        termgenerator.index_text(title)
        termgenerator.increase_termpos()
        termgenerator.index_text(description)

        # Store all the fields for display purposes.
        doc.set_data(json.dumps(fields))

### Start of example code.
        # parse the two values we need
        measurements = fields.get('MEASUREMENTS', u'')
        if len(measurements) > 0:
            numbers = numbers_from_string(measurements)
            if len(numbers) > 0:
                doc.add_value(0, xapian.sortable_serialise(max(numbers)))

        date_made = fields.get('DATE_MADE', u'')
        years = numbers_from_string(date_made)
        if len(years) > 0:
            doc.add_value(1, xapian.sortable_serialise(years[0]))
### End of example code.

        # We use the identifier to ensure each object ends up in the
        # database only once no matter how many times we run the
        # indexer.
        idterm = u"Q" + identifier
        doc.add_boolean_term(idterm)
        db.replace_document(idterm, doc)

if len(sys.argv) != 3:
    print("Usage: %s DATAPATH DBPATH" % sys.argv[0])
    sys.exit(1)

index(datapath = sys.argv[1], dbpath = sys.argv[2])
