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
    :args: data/ch-objects.csv db

We can check this has created document values using `xapian-delve`:

.. code-block:: none

    $ xapian-delve -VS0 db
    Value 0 for each document: 1:668 2:441 3:291 4:162 5:426 6:300 7:123 8:546 9:590 10:549 11:428 12:541 13:537 14:269 17:300 18:102 19:560 20:281 21:369 22:473 23:462 24:207 25:474 26:388 27:236 28:150 29:380 30:319 31:278 32:144 33:284 34:405 35:213 36:375 37:578 38:502 39:448 40:162 41:539 42:289 43:442 44:147 46:263 47:161 48:219 49:337 50:208 51:163 52:232 53:108 54:224 55:229 56:225 57:457.2 58:238 59:245 60:559 61:215 62:251 63:176 64:457.2 65:153 66:130 67:130 68:154 69:165.1 70:131 71:222.3 72:115 73:458 74:420 75:982 76:580 77:535 78:985 79:980 80:1091 81:860 82:859 83:873 84:291 85:545 86:498 87:870 88:943 89:956 90:1095 91:1095 92:1020 93:262 94:138 95:404.8 96:250 97:396 98:418 99:411 100:420

Note the use of ``S`` after ``-V`` which tells `xapian-delve` to use
:xapian-just-method:`sortable_unserialise` to turn the strings back into
numbers (this is supported since Xapian 1.4.6).

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
modifies the output to show the measurements and date-made fields as
well as the title.

We can now restrict across dimensions using queries like '..120mm'
(everything at most 120mm in its longest dimension), and across years
using '1400..1500':

.. xapianrunexample:: search_ranges
    :args: db ..120mm

.. xapianrunexample:: search_ranges
    :args: db 1400..1500

You can of course combine this with 'normal' search terms, such as all
cartoons before the 19th century:

.. xapianrunexample:: search_ranges
    :args: db cartoon ..1799

and even combining both ranges at once, such as all large objects from the 19th century:

.. xapianrunexample:: search_ranges
    :args: db 500..mm 1800..1899

If you're using Xapian 1.4.31 or newer you can use the more natural syntax
*500mm..* instead of the slightly awkward *500..mm*.

The rule here is that when :xapian-constant:`RP_REPEATED` is used, an empty range
bound doesn't need a prefix so long as it's specified on the other bound.

If you get the rules wrong, the QueryParser will raise a
`QueryParserError`, which in production code you could catch and
either signal to the user or perhaps try the query again without the
`RangeProcessor` that tripped up.


Handling dates
--------------

To restrict to a date range, we need to decide how to both store the
date in a document value, and how we want users to input the date
range in their query. Xapian comes with :xapian-class:`DateRangeProcessor`,
which requires dates to be stored in a value slot as a string in the form
'YYYYMMDD', and can take dates in most commonly used formats.  The
month/day/year format commonly used in the US can be ambiguous with
the day/month/year format commonly used in much of the rest of the world
so :xapian-class:`DateRangeProcessor` provides a flag to control how to
interpret ambiguous cases.

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
1860 and going forward as far 1959). The second parameter specifies flags;
since we're looking at US states, we've gone for setting the flag which
resolves ambiguous cases as US-format dates. The
:xapian-class:`NumberRangeProcessor` is as we saw before, which means that it
can't cope with two digit years.

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
what reasonable population values are. If we insert it *before* the
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
range in the query string; either (but not both) can be the empty
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
