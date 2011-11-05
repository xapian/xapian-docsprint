#!/usr/bin/env python

import json
import sys
import xapian
from parsecsv import parse_csv_file


def delete(dbpath, identifiers):
    # Open the database we're going to be deleting from.
    db = xapian.WritableDatabase(dbpath, xapian.DB_CREATE_OR_OPEN)

    for identifiers in identifiers:
        idterm = u'Q' + identifiers
        db.delete_document(idterm)


delete(dbpath = sys.argv[1], identifiers=sys.argv[2:])
