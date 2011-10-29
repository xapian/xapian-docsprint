#!/usr/bin/env python

import csv
import json
import sys
import xapian

def index(datapath, dbpath):
    """Index a set of data.

    :param datapath The path to the file containing the incoming data.
    :param dbpath The path to the database to index to.

    This will create the database if it doesn't already exist.

    """

    # Create or open the database we're going to be writing to. 
    db = xapian.WritableDatabase(dbpath, xapian.DB_CREATE_OR_OPEN)
    termgenerator = xapian.TermGenerator()
    termgenerator.set_stemmer(xapian.Stem("en"))

    for fields in parse_csv_file(datapath):
        # fields is a dictionary keyed by field name.  We're just going to use
        # the id_NUMBER, TITLE and DESCRIPTION fields to start with.
        doc = xapian.Document()

        termgenerator.set_document(doc)
        termgenerator.index_text(fields['TITLE'], 'S')
        termgenerator.index_text(fields['DESCRIPTION'], 'XD')

        termgenerator.index_text(fields['TITLE'])
        termgenerator.increase_termpos()
        termgenerator.index_text(fields['DESCRIPTION'])

        doc.set_data(json.dumps(fields))
        db.add(doc)

def parse_csv_file(datapath):
    """Parse a CSV file, yielding dictionaries of the fields.

    """
    fd = open(datapath)
    reader = csv.reader(fd)

    # Read the first 
    titles = reader.next()
    for row in reader:
        yield dict(zip(titles, row))
    fd.close()


if __name__ == '__main__':
    datapath = sys.argv[1]
    dbpath = sys.argv[2]
    index(datapath, dbpath)
