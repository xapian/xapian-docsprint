
"""Support code for the python examples."""

import csv
from datetime import datetime
import math


def parse_csv_file(datapath, charset='iso-8859-1'):
    """Parse a CSV file.

    Assumes the first row has field names.

    Yields a dict keyed by field name for the remaining rows.

    """
    with open(datapath) as fd:
        reader = csv.DictReader(fd)
        for row in reader:
            yield row


def numbers_from_string(string_):
    """Find all numbers in a string.

    """
    numbers = []
    sub_char = ''
    for char_ in string_:
        char_ = char_.decode(errors='ignore').strip()
        if char_ and (char_.isdigit() or char_ == u'.'):
            sub_char += char_
        elif sub_char:
            numbers.append(float(sub_char))
            sub_char = ''
    return numbers


def middle_coord(text):
    """Get the middle coordinate from a coordinate range.

    The input is in the form <start> to <end> with both extents being in
    degrees and minutes as N/S/W/E. S and W thus need to be negated as we only
    care about N/E.

    """
    def tuple_to_float(numbers):
        divisor = 1
        result = 0
        for num in numbers:
            result += float(num) / divisor
            divisor = divisor * 60
        return result

    if text is None:
        return None
    pieces = text.split(' to ', 1)
    start, end = map(numbers_from_string, pieces)
    start = tuple_to_float(start)
    end = tuple_to_float(end)
    if pieces[0][-1] in ('S', 'W'):
        start = -start
    if pieces[1][-1] in ('S', 'W'):
        end = -end
    return (start + end) / 2


def distance_between_coords(latlon1, latlon2):
    # For simplicity we treat these as planar coordinates and use
    # Pythagoras. Note that you should really use something like
    # Haversine; there's an implementation in Xapian's geo support,
    # although this is still on a branch.
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
        admitted = fields.get('admitted', None)
        if admitted is None:
            print "Couldn't process", fields
            continue

        # Date (order) -- we use the order as our identifier

        pieces = admitted.split('(', 1)
        admitted = pieces[0].strip()
        try:
            admitted = datetime.strptime(admitted, "%B %d, %Y")
        except ValueError, e:
            print e
            print "couldn't parse admitted '%s'" % admitted
            admitted = None
        fields['admitted'] = "%s%s%s" % (
            admitted.year, admitted.month, str(admitted.day).zfill(2))

        order = pieces[1]
        if order[-1] == ')':
            order = order[:-1]
        if order[-2:] in ('st', 'nd', 'rd', 'th'):
            order = order[:-2]
        order.strip()
        fields['order'] = order

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
        fields['population'] = population

        fields['midlat'] = middle_coord(fields.get('latitude', None))
        fields['midlon'] = middle_coord(fields.get('longitude', None))

        yield fields
