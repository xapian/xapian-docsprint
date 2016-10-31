Range queries
=============

.. contents:: Table of contents

I'm only interested in the 1980s
--------------------------------

In the museums dataset we used in our earlier examples, there is a
field `DATE_MADE` that tells us when the object in question was made,
so one of the natural things people might want to do is to only search
for objects made in a particular time period. Suppose we want to
extend our original system to allow that, we're going to have to do a
number of things.

 1. Parse the field from the data set to turn it into something consistent;
    at the moment it includes years, year ranges ("1671-1700"), approximate
    years ("c. 1936") and commentary ("patented 1885", or "1642-1649
    (original); 1883 (model)"). Additionally, some records have no
    information about when the object was made.
 2. Store that information in the Xapian database.
 3. Provide a way during search of specifying a date range to constrain to.

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
responsible for handling *value ranges*: :xapian-just-constant:`OP_VALUE_LE`,
:xapian-just-constant:`OP_VALUE_GE` and :xapian-just-constant:`OP_VALUE_RANGE`.
So we'll be tackling range queries by using document values, and constructing
queries using these operators to restrict matches suitably.

Since we want to expose this functionality generally to users, we want
them to be able to type in a query that will include one or more range
restrictions; the QueryParser contains support for doing this, using
*range processors*, subclasses of :xapian-class:`RangeProcessor`.
Xapian comes with some standard ones itself, or you can write your own.

Since document values are stored as strings in Xapian, and the
operators provided perform string comparisons, we need a way of
converting numbers to strings to store them. For this, Xapian provides
a pair of utility functions: `sortable_serialise` and
`sortable_unserialise`, which convert between floating point numbers
(strictly, each works with a `double`) and a string that will sort in
the same way and so can be compared easily.

Creating the document values
----------------------------

We need a new version of our indexer. This one is
:xapian-basename-code-example:`index_ranges`, and creates document values from both
`MEASUREMENTS` and `DATE_MADE`. We'll put the largest dimension in
value slot 0 (fortunately the data is stored in millimetres and
kilograms, so we can cheat a little and assume that dimensions will
always be larger than weights), and a year taken from `DATE_MADE` into
value slot 1 (we choose the first year we can parse, since it can
contain such a variety of date formats).

.. xapianexample:: index_ranges

We run this like so:

.. xapianrunexample:: index_ranges
    :cleanfirst: db
    :args: data/100-objects-v1.csv db

We can check this has created document values using `xapian-delve`:

.. code-block:: none

    $ xapian-delve -V0 db | cat -v
    Value 0 for each document: 5:M-@M-@ 8:M-HV 9:M-EM-p 10:M-MF 11:M-AM-0 12:M-AP 15:M-8^P 19:M-Dt 20:M-GM-P 21:M-E 24:M-O: 25:M-BM-@ 26:M-AM-  27:M-BX 29:M-DD 30:M-BM-^P 31:M-6@ 33:M-;` 34:M-A0 35:M-LM-l 36:M-C^P 37:M-9M-p 38:M-A( 39:M-FT 42:M-H2 45:M-N@ 46:M-AP 50:M-:M-^P 51:M-9P 52:M-LM-! 54:M-CM-( 55:M-9M-P 56:M-@P 59:M-D` 61:M-A( 62:M-;@ 64:M-:M-^P 66:M-AM-H 67:M-8` 68:M-@D33333@ 69:M-D^P 70:M-@M-H 71:M-KM-( 72:M-8^P 73:M-5M-^NfffffM-^@ 74:M-5M-^NfffffM-^@ 75:M-C$M-LM-LM-LM-LM-LM-@ 76:M-BM-?33333@ 77:M-C>33333@ 78:M-;M-^@ 79:M-E^T 80:M-9P 81:M-A@ 84:M-9M-t 86:M-L~ 87:M-BM-@ 88:M-9(M-LM-LM-LM-LM-LM-@ 89:M-:M-?33333@ 90:M-8M-C33333@ 91:M-E| 93:M-A( 94:M-@` 97:M-EM-\ 98:M-Bh 100:M-9^P

All the odd characters are because `xapian-delve` doesn't know to run
`sortable_unserialise` to turn the strings back into numbers.

Searching with ranges
---------------------

All we need to do once we've got the document values in place is to
tell the QueryParser about them. The simplest range processor is
:xapian-class:`RangeProcessor` itself, but here we need two
:xapian-class:`NumberRangeProcessor` instances.

To distinguish between the two different ranges, we'll require that
dimensions must be specified with the suffix 'mm', but years are just
numbers. For this to work, we have to tell QueryParser about the value
range with a suffix first:

.. xapianexample:: search_ranges
    :start-after: and add in range processors
    :end-before: And parse the query

The first call has a final parameter of `False` to say that 'mm' is a
suffix (the default is for it to be a prefix). When using the empty
string, as in the second call, it doesn't matter whether you say it's
a suffix or prefix, so it's convenient to skip that parameter.


This is implemented in :xapian-basename-code-example:`^`, which also
modifies the output to show the measurements and date made fields as
well as the title.

We can now restrict across dimensions using queries like '..50mm'
(everything at most 50mm in its longest dimension), and across years
using '1980..1989':

.. xapianrunexample:: search_ranges
    :args: db ..50mm

.. xapianrunexample:: search_ranges
    :args: db 1980..1989

You can of course combine this with 'normal' search terms, such as all
clocks made from 1960 onwards:

.. xapianrunexample:: search_ranges
    :args: db clock 1960..

and even combining both ranges at once, such as all large objects from the 19th century:

.. xapianrunexample:: search_ranges
    :args: db 1000..mm 1800..1899

Note the slightly awkward syntax *1000..mm*. The suffix must always go
on the end of the entire range; it may also go on the beginning (so
you can do *1000mm..mm*). Similarly, you can have *100mm..200mm* or
*100..200mm* but not *100mm..200*. These rules are reversed for
prefixes.

If you get the rules wrong, the QueryParser will raise a
`QueryParserError`, which in production code you could catch and
either signal to the user or perhaps try the query again without the
`RangeProcessor` that tripped up:

.. xapianrunexample:: search_ranges
    :args: db 1000mm..
    :shouldfail: 1


Handling dates
--------------

To restrict to a date range, we need to decide how to both store the
date in a document value, and how we want users to input the date
range in their query. :xapian-class:`DateRangeProcessor`, which is part of
Xapian, works by storing the date as a string in the form 'YYYYMMDD',
and can take dates in either US style (month/day/year) or European
style (day/month/year).

To show how this works, we're going to need to use a different dataset, because
the museums data only gives years the objects were made in; we've built one
using data on the fifty US states, taken from Wikipedia infoboxes on 5th
November 2011 and then tidied up a small amount. The CSV file is
:xapian-basename-example:`data/states.csv`, and the code that did most of the
work is :xapian-basename-code-example:`from_wikipedia`, using a
list of Wikipedia page titles in
:xapian-basename-example:`data/us_states_on_wikipedia`. The CSV is licensed as
Creative Commons Attribution-Share Alike 3.0, as per Wikipedia.

We need a new indexer for this as well, which is
:xapian-basename-code-example:`index_ranges2`. It stores two numbers using
`sortable_serialise`: year of admission in value slot 1 and population
in slot 3. It also stores the date of admission as 'YYYYMMDD' in
slot 2.  Here's the code which does this:

.. xapianexample:: index_ranges2

We'll look at just the date ones for now, and come back to the
others in a minute.

We use the indexer in the same way as previous ones:

.. xapianrunexample:: index_ranges2
    :cleanfirst: statesdb
    :args: data/states.csv statesdb

With this done, we can change the set of value range processors we
give to the QueryParser.

.. xapianexample:: search_ranges2
    :marker: date example code

The :xapian-class:`DateRangeProcessor` is working on value slot 2, with an
"epoch" of 1860 (so two digit years will be considered as starting at
1860 and going forward as far 1959). The second parameter is whether
it should prefer US style dates or not; since we're looking at US
states, we've gone for US dates. The :xapian-class:`NumberRangeProcessor`
is as we saw before, which means that it can't cope with two digit years.

This enables us to search for any state that talks about the Spanish
in its description:

.. xapianrunexample:: search_ranges2
    :args: statesdb spanish

or for all states admitted in the 19th century:

.. xapianrunexample:: search_ranges2
    :args: statesdb 1800..1899

That uses the :xapian-class:`NumberRangeProcessor` on value slot 1, as in
our previous example. Let's be more specific and ask for only those
between November 8th 1889, when Montana became part of the Union, and
July 10th 1890, when Wyoming joined:

.. xapianrunexample:: search_ranges2
    :args: statesdb 11/08/1889..07/10/1890

That uses the :xapian-class:`DateRangeProcessor` on value slot 2; it can't
cope with year ranges, which is why we indexed to both slots 1 and 2.

Writing your own RangeProcessor
-------------------------------

We haven't yet done anything with population. What we want is
something that behaves like :xapian-class:`NumberRangeProcessor`, but knows
what reason possible values are. If we insert it *before* the
:xapian-class:`NumberRangeProcessor` on slot 1 (year), it can pick up
anything that should be treated as a population, and let everything else be
treated as a year range.

To do this, we need to know how a :xapian-class:`RangeProcessor` gets
called by the QueryParser. What happens is that each processor in turn is
passed the start and end of the range. If it doesn't understand the range, it
should return :xapian-constant:`BAD_VALUENO`.  If it *does* understand
the range, it should return the value number to use with
:xapian-constant:`Query::OP_VALUE_RANGE` and if it wants to, it can
modify the start and end values (to convert them to the correct format for
the string comparison which :xapian-constant:`OP_VALUE_RANGE` uses).

What we're going to do is to write a custom :xapian-class:`RangeProcessor`
that accepts numbers in the range 500,000 to 50,000,000; these can't
possibly be years in our data set, and encompass the full range of
populations. If either number is outside that range, we will return
:xapian-constant:`BAD_VALUENO` and the QueryParser will move on.

.. xapianexample:: search_ranges2
    :marker: custom RP code

Most of the work is in `__call__` (python's equivalent of `operator()`
in C++), which gets called with the two strings at either end of the
range in the query string; either but not both can be the empty
string, which indicates an open-ended range.  This method returns a
:xapian-class:`Query` object - if the object doesn't want to handle
the range, then this should use operator :xapian-just-constant:`OP_INVALID`.
it doesn't want to handle it; otherwise this query is the range that
is matched - typically using :xapian-just-constant:`OP_VALUE_RANGE`, but
arbitrary :xapian-class:`Query` objects are supported.

Rather than re-implement :xapian-class:`NumberRangeProcessor`, we wrap it to do
the serialisation (due to the way python interacts with the API it's currently
not possible to subclass it successfully here).

.. todo: Is the above paragraph still correct?

Range processors are called in the order they're added, so our
custom one gets a chance to look at all ranges, but will only 'claim'
ranges which use integer numbers within the 500 thousand to 50 million
range.

We can then search for states by population, such as all over 10
million:

.. xapianrunexample:: search_ranges2
    :args: statesdb 10000000..

Or all that joined the union in the 1780s and have a population now over 10 million:

.. xapianrunexample:: search_ranges2
    :args: statesdb 1780..1789 10000000..

With a little more work, we could support ranges such as '..5m' to
mean up to 5 million, or '..750k' for up to 750 thousand.

Similarly, it would be possible to use the same approach to create a custom
:xapian-class:`RangeProcessor` that could restrict to a range of years, and
cope with two digit years, as our :xapian-class:`DateRangeProcessor` did for
full dates.

Performance limitations
-----------------------

Without other terms in a query, a :xapian-class:`RangeProcessor` can cause
a value operation to be performed across the whole database, which means
loading all the values in a given slot. On a small database, this
isn't a problem, but for a large one it can have performance
implications: you may end up with very slow queries.
