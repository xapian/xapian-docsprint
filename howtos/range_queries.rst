Range queries
=============

.. todo:: Write about how to do range queries.  Discuss how to index numeric
	  values using sortable_serialise(), and probably discuss how to index
	  dates as YYYYMMDD, too, since that's a common scheme.  Discuss
	  ValueRangeProcessor use with query parsers.  Maybe discuss
	  performance issues (ie, range searches can be slow because they have
	  to run through all potential matches) - lead on to a discussion of
	  speeding up range searches with terms covering parts of the range.

.. todo:: Start from valueranges.rst.

I'm only interested in the 1980s
--------------------------------

In the museums dataset we used in our earlier examples, there is a
field `DATE_MADE` that tells us when the object in question was made,
so one of the natural things people might want to do is to only search
for objects made in a particular time period. Suppose we want to
extend our original system to allow that, we're going to have to do a
number of things.

1. Parse the field from the data set to turn it into something
consistent; at the moment it includes years, year ranges
("1671-1700"), approximate years ("c. 1936") and commentary ("patented
1885", or "1642-1649 (original); 1883 (model)"). Additionally, some
records have no information about when the object was made.

2. Store that information in the Xapian database.

3. Provide a way during search of specifying a date range to constrain
to.

If we look through the other fields in the data set, there are more
that could be useful for range queries: we could extract the longest
dimension from `MEASUREMENTS` to enable people to restrict to only
very large or very small objects, for instance.

We'll see how to perform range searches across both those dimensions,
and then we'll look at how to cope with full dates rather than just
years.


How Xapian supports range queries
---------------------------------

If you think back to when we introduced the query concepts behind
Xapian, you'll remember that one group of query operators is
responsible for handling *value ranges*: `OP_VALUE_LE`, `OP_VALUE_GE`
and `OP_VALUE_RANGE`. So we'll be tackling range queries by using
document values, and constructing queries using these operators to
restrict matches suitably.

Since we want to expose this functionality generally to users, we want
them to be able to type in a query that will include one or more range
restrictions; the QueryParser contains support for doing this, using
*value range processors*, subclasses of `ValueRangeProcessor`. Xapian
comes with some standard ones itself, or you can write your own.

Since document values are stored as strings in Xapian, we need a way
of storing numbers as well. For this, Xapian provides a fair of
utility functions: `sortable_serialise` and `sortable_unserialise`
convert between floating point numbers (strictly, each is a `double`)
and a string that will sort in the same way and so can be compared
easily.

Creating the document values
----------------------------

We need a new version of our indexer. This one is
`code/python/index_ranges.py`, and creates document values from both
`MEASUREMENTS` and `DATE_MADE`. We'll put the largest dimension in
value slot 0 (fortunately the data is stored in millimetres and
kilograms, so we can cheat a little and assume that dimensions will
always be larger than weights), and a year taken from date made into
value slot 1 (we choose the first year we can parse, since it can
contain such a variety of date formats).

.. literalinclude:: /code/python/index_ranges.py

We can check this has create document values using `delve`:

    $ delve -V0 db
    Value 0 for each document: 5:?? 10:?F 11:?? 12:?P 15:? 19:?t 20:?? 21:? 24:?: 25:?? 26:?? 27:?X 29:?D 30: 31:?@ 33:?` 34:?0 35:?? 36:? 37:?? 38:?( 39:?T 42:?2 45:?@ 46:?P 50:?? 51:?P 52:̡ 54:è 55:?? 56:?P 59:?` 61:?( 62:?@ 64:?? 66:?? 67:?` 68:?D33333@ 69:? 70:?? 71:˨ 72:? 73:??fffff? 74:??fffff? 75:?$?????? 76:¿33333@ 77:?>33333@ 78:?? 79:? 80:?P 81:?@ 84:?? 86:?~ 87:?? 88:?(?????? 89:??33333@ 90:??33333@ 91:?| 93:?( 94:?` 97:?? 98:?h 100:? 101:?V 102:??

All the '?' characters are because `delve` doesn't know to run
`sortable_unserialise` to turn the strings back into numbers.

Searching with ranges
---------------------

All we need to do once we've got the document values in place is to
tell the QueryParser about them. The simplest value range processor is
`StringValueRangeProcessor`, but here we need two
`NumberValueRangeProcessor` instances.

To distinguish between the two different ranges, we'll require that
dimensions must be specified with the suffix 'mm', but years are just
numbers. For this to work, we have to tell QueryParser about the value
range with a suffix first::


    queryparser.add_valuerangeprocessor(
        xapian.NumberValueRangeProcessor(0, 'mm', False)
    )
    queryparser.add_valuerangeprocessor(
        xapian.NumberValueRangeProcessor(1, '')
    )

The first call has a final parameter of `False` to say that 'mm' is a
suffix (the default is for it to be a prefix). When using the empty
string, as in the second call, it doesn't matter whether you say it's
a suffix or prefix, so it's convenient to skip that parameter.


This is implemented in `code/python/search_ranges.py`, which also
modifies the output to show the measurements and date made fields as
well as the title.

We can now restrict across dimensions using queries like '..50mm'
(everything at most 50mm in its longest dimension), and across years
using '1980..1989'::

    $ python code/python/search_ranges.py db ..50mm
    1: #031 (1588) overall diameter: 50 mm
            Portable universal equinoctial sundial, in brass, signed "A
    2: #073 (1701-1721) overall: 15 mm x 44.45 mm, weight: 0.055kg
            Universal pocket sundial
    3: #074 (1596) overall: 13 mm x 44.45 mm x 44.45 mm, weight: 0.095kg
            Sundial, made as a locket, gilt metal, part silver
    INFO:xapian.search:'..50mm'[0:10] = 31 73 74

    $ python code/python/search_ranges.py db 1980..1989
    1: #050 (1984) overall: 105 mm x 75 mm x 57 mm,
            Quartz Analogue "no battery" wristwatch by Pulsar Quartz (CA
    2: #051 (1984) overall: 85 mm x 65 mm x 38 mm,
            Analogue quartz clock with voice controlled alarm by Braun,
    INFO:xapian.search:'1980..1989'[0:10] = 50 51

You can of course combine this with 'normal' search terms, such as all
clocks made from 1960 onwards::

    $ python code/python/search_ranges.py db clock 1960..
    1: #052 (1974) clock: 1185 x 780 mm, 122 kg; rewind unit: 460 x 640 x 350 mm
            Reconstruction of Dondi's Astronomical Clock, 1974
    2: #051 (1984) overall: 85 mm x 65 mm x 38 mm,
            Analogue quartz clock with voice controlled alarm by Braun,
    3: #102 (1973) overall: 380 mm x 300 mm x 192 mm, weight: 6.45kg
            Copy  of a Dwerrihouse skeleton clock with coup-perdu escape
    INFO:xapian.search:'clock 1960..'[0:10] = 52 51 102

and even combining both ranges at once, such as all large objects from the 19th century::

    $ python code/python/search_ranges.py db 1000..mm 1800..1899
    1: #024 (1845-1855) overall: 1850 mm x 350 mm x 250 mm
            Regulator Clock with Gravity Escapement
    INFO:xapian.search:'1000..mm 1800..1899'[0:10] = 24

Note the slightly awkward syntax *1000..mm*. The suffix must always go
on the end of the entire range; it may also go on the beginning (so
you can do *1000mm..mm*). Similarly, you can have *100mm..200mm* or
*100..200mm* but not *100mm..200*. These rules are reversed for
prefixes.

If you get the rules wrong, the QueryParser will raise a
`QueryParserError`, which in production code you could catch and
either signal to the user or perhaps try the query again without the
`ValueRangeProcessor` that tripped up::

    $ python code/python/search_ranges.py db 1000mm..
    Traceback (most recent call last):
      File "code/python/search_ranges.py", line 59, in <module>
        search(dbpath = sys.argv[1], querystring = " ".join(sys.argv[2:]))
      File "code/python/search_ranges.py", line 29, in search
        query = queryparser.parse_query(querystring)
    xapian.QueryParserError: Unknown range operation


Handling dates
--------------

TODO: write this

Writing your own ValueRangeProcessor
------------------------------------

TODO: write this
