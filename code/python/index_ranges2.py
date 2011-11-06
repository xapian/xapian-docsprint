#!/usr/bin/env python

import json
import time
import datetime
import sys
import xapian
from parsecsv import parse_csv_file

def numbers_from_string(s):
    """Find all numbers in a string."""
    numbers = []
    in_number = False
    while len(s) > 0:
        next_in_number = (s[0].isdigit() or s[0]=='.')
        if next_in_number != in_number:
            in_number = not in_number
            if in_number:
                numbers.append(s[0])
        else:
            if in_number:
                numbers[-1] = numbers[-1] + s[0]
        s = s[1:]
    # fix up leading or trailing '.'
    for index, number in enumerate(numbers):
        if number[0]=='.':
            number = '0.' + number[1:]
        if number[-1]=='.':
            number += '0'
        numbers[index] = float(number)
    return numbers


def index(datapath, dbpath):
    # Create or open the database we're going to be writing to.
    db = xapian.WritableDatabase(dbpath, xapian.DB_CREATE_OR_OPEN)

    # Set up a TermGenerator that we'll use in indexing.
    termgenerator = xapian.TermGenerator()
    termgenerator.set_stemmer(xapian.Stem("en"))

    for fields in parse_csv_file(datapath, 'utf-8'):
        # 'fields' is a dictionary mapping from field name to value.
        admitted = fields.get('admitted', None)
        if admitted is None:
            print "Couldn't process", fields
            continue
        else:
            # Date (order) -- we use the order as our identifier
            pieces = admitted.split('(', 1)
            admitted = pieces[0]
            admitted.strip()
            try:
                admitted = time.strptime(
                    admitted,
                    "%B %d, %Y ",
                    )
                # now a struct_time, convert to YYYYMMDD
                admitted = "%4.4i%2.2i%2.2i" % (
                    admitted[0],
                    admitted[1],
                    admitted[2],
                    )
            except ValueError:
                print "couldn't parse admitted '%s'" % admitted
                admitted = None

            order = pieces[1]
            if order[-1] == ')':
                order = order[:-1]
            if order[-2:] in ('st', 'nd', 'rd', 'th'):
                order = order[:-2]
            order.strip()
        population = fields.get('population', None)
        if population is not None:
            # Population-comma-formatted (comment) extra
            pieces = population.split('(', 1)
            population = pieces[0].replace(',', '')
            population.strip()
            try:
                population = int(population)
            except ValueError:
                population = None
        
        # Note that the following code isn't used in explaining
        # range queries at all. I thought I was going to use it,
        # but ended up not bothering. It may prove useful in
        # explaining geosearch at some point in the future.
        def middle_coord(text):
            """
            In the form <start> to <end> with both extents being in
            degrees and minutes as N/S/W/E. S and W thus need to be
            negated as we only care about N/E.
            """
            if text is None:
                return None
            pieces = text.split(' to ', 1)
            #print "coords", pieces
            start, end = map(numbers_from_string, pieces)
            def tuple_to_float(numbers):
                divisor = 1
                result = 0
                while len(numbers) > 0:
                    result += float(numbers[0]) / divisor
                    numbers = numbers[1:]
                    divisor = divisor * 60
                return result
            start = tuple_to_float(start)
            end = tuple_to_float(end)
            if pieces[0][-1] in ('S', 'W'):
                start = -start
            if pieces[1][-1] in ('S', 'W'):
                end = -end
            return (start + end) / 2
        midlat = middle_coord(fields.get('latitude', None))
        midlon = middle_coord(fields.get('longitude', None))

        # We make a document and tell the term generator to use this.
        doc = xapian.Document()
        termgenerator.set_document(doc)

        # Index each field with a suitable prefix.
        name = fields.get('name', u'')
        description = fields.get('description', u'')
        motto = fields.get('motto', u'')
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

        # Store all the fields for display purposes.
        doc.set_data(json.dumps(fields))

        # add document values
        if admitted is not None:
            doc.add_value(1, xapian.sortable_serialise(int(admitted[:4])))
            doc.add_value(2, admitted) # YYYYMMDD
        if population is not None:
            doc.add_value(3, xapian.sortable_serialise(population))

        # we use the identifier to ensure each object ends up
        # in the database only once no matter how many times
        # we run the indexer
        idterm = u"Q" + order
        doc.add_boolean_term(idterm)
        db.replace_document(idterm, doc)

index(datapath = sys.argv[1], dbpath = sys.argv[2])
