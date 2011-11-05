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
        # We're just going to use id_NUMBER, TITLE and DESCRIPTION
        description = fields.get('DESCRIPTION', u'')
        title = fields.get('TITLE', u'')
        identifier = fields.get('id_NUMBER', u'')

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

        ### Start of new indexing code.
        # index the MATERIALS field, splitting on semicolons
        for material in fields.get('MATERIALS', u'').split(';'):
            material = material.strip()
            if material != '':
                doc.add_boolean_term('XM' + material)
        ### End of new indexing code.

        # store all the fields for display purposes
        doc.set_data(json.dumps(fields))

        # we use the identifier to ensure each object ends up
        # in the database only once no matter how many times
        # we run the indexer
        idterm = u"Q" + identifier
        doc.add_term(idterm)
        db.replace_document(idterm, doc)


index(datapath = sys.argv[1], dbpath = sys.argv[2])
