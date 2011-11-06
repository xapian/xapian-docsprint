
"""Support code for the python examples."""

import csv
import time

def parse_csv_file(datapath, charset='iso-8859-1'):
    """Parse a CSV file.

    Assumes the first row has field names.

    Yields a dict keyed by field name for each other row.

    """
    fd = open(datapath)
    reader = csv.reader(fd)
    titles = reader.next()
    for row in reader:
        yield dict(zip(titles, map(lambda x: x.decode(charset), row)))
    fd.close()


def numbers_from_string(s):
    """Find all numbers in a string.
    
    """
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


def middle_coord(text):
    """Get the middle coordinate from a coordinate range.

    The input is in the form <start> to <end> with both extents being in
    degrees and minutes as N/S/W/E. S and W thus need to be negated as we only
    care about N/E.

    """
    if text is None:
        return None
    pieces = text.split(' to ', 1)
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
        fields['admitted'] = admitted

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
