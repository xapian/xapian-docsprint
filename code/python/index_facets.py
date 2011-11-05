#!/usr/bin/env python

import json
import sys
import xapian
from parsecsv import parse_csv_file


def index(datapath, dbpath):
    # Create or open the database we're going to be writing to. 
    db = xapian.WritableDatabase(dbpath, xapian.DB_CREATE_OR_OPEN)

    # Set up a TermGenerator that we'll use in indexing
    termgenerator = xapian.TermGenerator()
    termgenerator.set_stemmer(xapian.Stem("en"))

    for fields in parse_csv_file(datapath):
        # fields is a dictionary mapping from field name to value.
        # We're going to use id_NUMBER, TITLE, DESCRIPTION and COLLECTION
        description = fields.get('DESCRIPTION', u'')
        title = fields.get('TITLE', u'')
        identifier = fields.get('id_NUMBER', u'')
        collection = fields.get('COLLECTION', u'')
        maker = fields.get('MAKER', u'')

        # we make a document and tell the term generator to use this
        doc = xapian.Document()
        termgenerator.set_document(doc)

        # index each field with a suitable prefix
        termgenerator.index_text(title, 1, 'S')
        termgenerator.index_text(description, 1, 'XD')

        # index fields without prefixes for general search
        termgenerator.index_text(title)
        termgenerator.increase_termpos()
        termgenerator.index_text(description)
        
        # add the collection as a value in slot 0
        doc.add_value(0, collection)
        
        # add the maker as a value in slot 1
        doc.add_value(1, maker)

        # store all the fields for display purposes
        doc.set_data(json.dumps(fields))

        # we use the identifier to ensure each object ends up
        # in the database only once no matter how many times
        # we run the indexer
        idterm = u"Q" + identifier
        doc.add_term(idterm)
        db.replace_document(idterm, doc)


index(datapath = sys.argv[1], dbpath = sys.argv[2])
