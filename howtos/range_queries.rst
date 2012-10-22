.. Copyright (C) 2011 James Aylett

Range queries
=============

.. todo:: check valueranges.rst to see if anything else needs moving across

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
*value range processors*, subclasses of :xapian-class:`ValueRangeProcessor`.
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

We can check this has created document values using `delve`::

    $ delve -V0 db
    Value 0 for each document: 5:?? 10:?F 11:?? 12:?P 15:? 19:?t 20:?? 21:? 24:?: 25:?? 26:?? 27:?X 29:?D 30: 31:?@ 33:?` 34:?0 35:?? 36:? 37:?? 38:?( 39:?T 42:?2 45:?@ 46:?P 50:?? 51:?P 52:̡ 54:è 55:?? 56:?P 59:?` 61:?( 62:?@ 64:?? 66:?? 67:?` 68:?D33333@ 69:? 70:?? 71:˨ 72:? 73:??fffff? 74:??fffff? 75:?$?????? 76:¿33333@ 77:?>33333@ 78:?? 79:? 80:?P 81:?@ 84:?? 86:?~ 87:?? 88:?(?????? 89:??33333@ 90:??33333@ 91:?| 93:?( 94:?` 97:?? 98:?h 100:? 101:?V 102:??

All the '?' characters are because `delve` doesn't know to run
`sortable_unserialise` to turn the strings back into numbers.

Searching with ranges
---------------------

All we need to do once we've got the document values in place is to
tell the QueryParser about them. The simplest value range processor is
:xapian-class:`StringValueRangeProcessor`, but here we need two
:xapian-class:`NumberValueRangeProcessor` instances.

To distinguish between the two different ranges, we'll require that
dimensions must be specified with the suffix 'mm', but years are just
numbers. For this to work, we have to tell QueryParser about the value
range with a suffix first:

.. xapianexample:: search_ranges
    :start-after: and add in value range processors
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
`ValueRangeProcessor` that tripped up:

.. xapianrunexample:: search_ranges
    :args: db 1000mm..


Handling dates
--------------

To restrict to a date range, we need to decide how to both store the
date in a document value, and how we want users to input the date
range in their query. :xapian-class:`DateValueRangeProcessor`, which is part of
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
slot 2. We'll look at just the date ones for now, and come back to the
others in a minute.

There isn't any new code in this indexer that's specific to Xapian,
although there's a fair amount of work to turn the data from Wikipedia
into the forms we need. We use the indexer in the same way as previous
ones:

.. xapianrunexample:: index_ranges2
    :args: data/states.csv statesdb

With this done, we can change the set of value range processors we
give to the QueryParser.

.. xapianexample:: search_ranges2
    :marker: date example code

The :xapian-class:`DateValueRangeProcessor` is working on value slot 2, with an
"epoch" of 1860 (so two digit years will be considered as starting at
1860 and going forward as far 1959). The second parameter is whether
it should prefer US style dates or not; since we're looking at US
states, we've gone for US dates. The :xapian-class:`NumberValueRangeProcessor`
is as we saw before.

This enables us to search for any state that talks about the Spanish
in its description:

.. xapianrunexample:: search_ranges2
    :args: statesdb spanish

or for all states admitted in the 19th century:

.. xapianrunexample:: search_ranges2
    :args: statesdb 1800.1899

That uses the :xapian-class:`NumberValueRangeProcessor` on value slot 1, as in
our previous example. Let's be more specific and ask for only those
between November 8th 1889, when Montana became part of the Union, and
July 10th 1890, when Wyoming joined:

.. xapianrunexample:: search_ranges2
    :args: statesdb 11/08/1889..07/10/1890

That uses the :xapian-class:`DateValueRangeProcessor` on value slot 2; it can't
cope with year ranges, which is why we indexed to both slots 1 and 2.

Writing your own ValueRangeProcessor
------------------------------------

We haven't yet done anything with population. What we want is
something that behaves like :xapian-class:`NumberValueRangeProcessor`, but knows
what reason possible values are. If we insert it *before* the
:xapian-class:`NumberValueRangeProcessor` on slot 1 (year), it can pick up
anything that should be treated as a population, and let everything else be
treated as a year range.

To do this, we need to know how a :xapian-class:`ValueRangeProcessor` gets
called by the QueryParser. What happens is that each processor in turn is
passed the start and end of the range. If it doesn't understand the range, it
should return :xapian-constant:`Xapian::BAD_VALUENO`.  If it *does* understand
the range, it should return the value number to use with
:xapian-constant:`Xapian::Query::OP_VALUE_RANGE` and if it wants to, it can
modify the start and end values (to convert them to the correct format for
the string comparison which :xapian-constant:`OP_VALUE_RANGE` uses).

What we're going to do is to write a custom :xapian-class:`ValueRangeProcessor`
that accepts numbers in the range 500,000 to 50,000,000; these can't
possibly be years in our data set, and encompass the full range of
populations. If either number is outside that range, we will return
:xapian-constant:`Xapian::BAD_VALUENO` and the QueryParser will move on.

.. xapianexample:: search_ranges2
    :marker: custom VRP code

Most of the work is in `__call__` (python's equivalent of `operator()`
in C++), which gets called with the two strings at either end of the
range in the query string; either but not both can be the empty
string, which indicates an open-ended range. In python this method
should return a tuple of the value slot and the two strings modified
so they can be used for :xapian-just-constant:`OP_VALUE_RANGE`. Rather than
re-implement :xapian-class:`NumberValueRangeProcessor`, we wrap it to do the
serialisation (due to the way python interacts with the API it's currently not
possible to subclass it successfully here).

Value range processors are called in the order they're added, so our
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

Performance limitations
-----------------------

Without other terms in a query, a :xapian-class:`ValueRangeProcessor` will cause
a value operation to be performed across the whole database, which means
loading all the values in a given slot. On a small database, this
isn't a problem, but for a large one it can have performance
implications: you may end up with very slow queries.

.. todo:: the above paragraph isn't entirely inaccurate; the processor is
	  unweighted, so if there's no other query, and the docid ordering is
	  don't care or ascending, then the search can terminate early.  If the
	  VRP isn't matching many documents, that could still be slow, but
	  might not be.  If it's not matching any documents, it might be fast
	  because the bounds on stored values may show that it can't match
	  anything.  Oh, it's all quite complicated really.  It would be nice
	  to explain how this is done somewhere, but probably not here.

If combined with a suitable term-based query (such as an `OP_AND`
query over one or more terms), this performance impact will be less
because the range operation will only have to run over the potential
matches, which are reduced from the entire database by the term-based
query.

If, as well as using document values, you also convert groups of those
values into terms, you can provide those term-based queries even when
your users are only interested in a pure range search. For instance,
consider the population information. If you divide the range of
populations into a number of subranges, you can allocate a term to
describe each. We'll use a prefix of `XP` (for "population") here.

+------------------+------+
| Population range | Term |
+==================+======+
| 0 - 10 million   | XP0  |
+------------------+------+
| 10 - 20 million  | XP1  |
+------------------+------+
| 20 - 30 million  | XP2  |
+------------------+------+
| 30 - 40 million  | XP3  |
+------------------+------+

Then you can use a custom :xapian-class:`ValueRangeProcessor` to both generate
the relevant information for QueryParser to construct an
:xapian-just-constant:`OP_VALUE_RANGE` query and to record which subranges we're
interested in. For instance, if the user asks for '..15000000', your processor
can remember that and later spit out an additional
:xapian-just-constant:`OP_AND` query with terms `XP0` and `XP1`, that can be
combined with the query generated by the QueryParser using
:xapian-just-constant:`OP_FILTER`.

.. todo:: actually, you can't safely combine the query with an external filter,
	  because other bits of the query might be higher level.  For example,
	  a query of '1790..1799 OR york' couldn't have the filter applied to
	  the generated query because it shouldn't be applied to the "york"
	  part.

.. todo:: possibly implementing this example would help make it more clear.
