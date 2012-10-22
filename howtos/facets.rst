.. Copyright (C) 2007,2010,2011 Olly Betts
.. Copyright (C) 2009 Lemur Consulting Ltd
.. Copyright (C) 2011 Richard Boulton
.. Copyright (C) 2011 Justin Finkelstein
.. Copyright (C) 2011 James Aylett

======
Facets
======

Xapian provides functionality which allows you to dynamically generate
complete lists of values which feature in matching documents. For example,
colour, manufacturer, size values are good candidates for faceting.

There are numerous potential uses this can be put to, but a common one is
to offer the user the ability to narrow down their search by filtering it
to only include documents with a particular value of a particular category.
This is often referred to as `faceted search`.


Implementation
==============
Faceting works against information stored in document value slots [link to
value slots] and, when executed, provides a list of the unique values for
that slot together with a count of the number of times each value occurs.


Indexing
--------

No additional work is needed to implement faceted searching, except to
ensure that the values you wish to use in facets are stored as
document values.

.. xapianexample:: index_facets
    :start-after: Start of example code.
    :end-before: End of example code.

Here we're using two value slots: 0 contains the collection, and 1
contains the name of whoever made the object. We know from the
documentation of the dataset that both from fixed and curated lists,
so we don't have to worry about normalising the values before using
them as facets. Let's run that to build a dataset with document values
suitable for faceting::

    $ python code/python/index_facets.py data/muscat.csv db


Querying
--------

.. todo:: explain what goes on here, ie why we use a MatchSpy

To add a spy you need to create a new `Xapian::ValueCountMatchSpy` object,
stating which value slot the spy is to operate on and add this to the
`Xapian::Enquire` as follows:

.. xapianexample:: search_facets
    :start-after: Start of example code.
    :end-before: End of example code.

Here we're faceting on value slot 1, which is the object maker. After
you get the MSet, you can ask the spy for the facets it found,
including the frequency. Note that although we're generally only
showing ten matches, we use a parameter to `get_mset` called
`checkatleast`, so that the entire dataset is considered and the facet
frequencies are correct. See `Limitations`_ for some discussion of the
implications of this. Here's the output::

    $ python code/python/search_facets.py db clock
    1: #044 Two-dial clock by the Self-Winding Clock Co; as used on the
    2: #096 Clock with Hipp pendulum (an electric driven clock with Hipp
    3: #012 Assembled and unassembled EXA electric clock kit
    4: #098 'Pond' electric clock movement (no dial)
    5: #005 "Ever Ready" ceiling clock
    6: #039 Electric clock of the Bain type
    7: #061 Van der Plancke master clock
    8: #064 Morse electrical clock, dial mechanism
    9: #052 Reconstruction of Dondi's Astronomical Clock, 1974
    10: #057 Electric clock by Alexander Bain, in case
    Facet: Bain, Alexander; count: 3
    Facet: Bloxam, J. M.; count: 1
    Facet: Braun (maker); count: 1
    Facet: British Horo-Electric Ltd. (maker); count: 1
    Facet: British Vacuum Cleaner and Engineering Co. Ltd., Magneto Time division (maker); count: 1
    Facet: EXA; count: 1
    Facet: Ever Ready Co. (maker); count: 2
    Facet: Ferranti Ltd.; count: 1
    Facet: Galilei, Galileo, 1564-1642; Galilei, Vincenzio, 1606-1649; count: 1
    Facet: Harrison, John (maker); count: 1
    Facet: Hipp, M.; count: 1
    Facet: La Précision Cie; count: 1
    Facet: Lund, J.; count: 1
    Facet: Morse, J. S.; count: 1
    Facet: Self Winding Clock Company; count: 1
    Facet: Self-Winding Clock Co. (maker); count: 1
    Facet: Synchronome Co. Ltd. (maker); count: 2
    Facet: Thwaites and Reed Ltd.; count: 1
    Facet: Thwaites and Reed Ltd. (maker); count: 1
    Facet: Viviani, Vincenzo; count: 1
    Facet: Vulliamy, Benjamin, 1747-1811; count: 1
    Facet: Whitefriars Glass Ltd. (maker); count: 1
    INFO:xapian.search:'clock'[0:10] = 44 96 12 98 5 39 61 64 52 57

Note that the spy will give you facets in alphabetical order, not in
order of frequency; if you want to show the most frequent first you
should use the `top_values` iterator (`begin_top_values` in C++ and
some other languages).

If you want to work with multiple facets, you can register multiple
`ValueCountMatchSpy` objects before running `get_mset`, although each
additional one will have some performance impact.

Restricting by Facets
---------------------
If you're using the facets to offer the user choices for narrowing down
their search results, you then need to be able to apply a suitable filter.

For a single value, you could use `Xapian::Query::OP_VALUE_RANGE` with the
same start and end, or `Xapian::MatchDecider`, but it's probably most
efficient to also index the categories as suitably prefixed boolean terms
and use those for filtering.


Limitations
===========

The accuracy of Xapian's faceting capability is determined by the number
of records that are examined by Xapian whilst it is searching. You can
control this number by specifying the `checkatleast` value of `get_mset`;
however it is important to be aware that increasing this number may have an
effect on overall query performance.


In Development
==============
Some additional features currently in development may benefit users of
facets. These are:

    * Multiple values in slots: this will allow you to have a single value slot
      (e.g. colour) which contains multiple values (e.g. red, blue).  This will
      also allow you to create a facet by colour which is aware of these
      multiple values, giving counts for both red and blue.

    * Bucketing: this provides a means to group together numeric facets, so that
      a single facet can contain a range of values (e.g. price ranges).
