
"""Support code for the python examples."""

import csv
from datetime import date, datetime
import math
import re


def log_matches(querystring, offset, pagesize, matches):
    print(
        "'%s'[%i:%i] = %s" % (
            querystring,
            offset,
            offset + pagesize,
            ' '.join(str(docid) for docid in matches),
        )
    )


def parse_csv_file(datapath, charset='utf8'):
    """Parse a CSV file.

    Assumes the first row has field names.

    Yields a dict keyed by field name for the remaining rows.

    """
    with open(datapath) as fd:
        reader = csv.DictReader(fd)
        for row in reader:
            yield row


def numbers_from_string(s):
    """Find all numbers in a string."""
    return [float(n) for n in re.findall(r'[\d.]*\d[\d.]*', s)]


def distance_between_coords(latlon1, latlon2):
    # For simplicity we treat these as planar coordinates and use
    # Pythagoras. Note that you should really use something like
    # Haversine; there's an implementation in Xapian's geo support.
    return math.sqrt(
        math.pow(latlon2[0] - latlon1[0], 2) +
        math.pow(latlon2[1] - latlon1[1], 2)
        )


def parse_states(datapath):
    """Parser for the states.csv data file.

    This is a generator, returning dicts with data parsed from the row.

    """
    for fields in parse_csv_file(datapath, 'utf-8'):
        # 'fields' is a dictionary mapping from field name to value.

        # We use 'order' as our unique identifier so check it's there.
        order = fields.get('order', None)
        if order is None:
            print("Couldn't process", fields)
            continue

        yield fields


def format_numeral(numeral, sep=','):
    if numeral and isinstance(numeral, int):
        _numeral = []
        numeral = str(numeral)
        for i, j in enumerate(reversed(numeral)):
            if i > 0 and i % 3 == 0 and i != len(numeral):
                _numeral.append(',')
            _numeral.append(j)
        return ''.join(reversed(_numeral))
    elif numeral == 0:
        return numeral

    raise ValueError("Numeral must be an int type to format")


def format_date(datestr):
    if datestr:
        _date = datetime.strptime(datestr, '%Y%m%d')
        # Python 2 date objects don't allow years before 1900, so we have to
        # build an object for a support year and the correct month to get the
        # month name.
        wtf_date = date(2000, _date.month, 01)
        return '%s %s, %s' % (wtf_date.strftime('%B'), _date.day, _date.year)

    raise ValueError("Could not parse date to format 'YYYYMMDD'")
