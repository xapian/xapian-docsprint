#!/usr/bin/env python

import sys
import xapian

### Start of example code.
def delete(dbpath, identifiers):
    # Open the database we're going to be deleting from.
    db = xapian.WritableDatabase(dbpath, xapian.DB_OPEN)

    for identifier in identifiers:
        idterm = u'Q' + identifier
        db.delete_document(idterm)
### End of example code.

delete(dbpath = sys.argv[1], identifiers=sys.argv[2:])
