.. Original content was taken from xapian-core/docs/facets.rst with
.. a copyright statement of:
.. Copyright (C) 2007,2010,2011 Olly Betts
.. Copyright (C) 2009 Lemur Consulting Ltd
.. Copyright (C) 2011 Richard Boulton

======
Facets
======

.. contents:: Table of contents

Xapian provides functionality which allows you to dynamically generate
complete lists of values which feature in matching documents. For example,
colour, manufacturer, size values are good candidates for faceting.

There are numerous potential uses this can be put to, but a common one is
to offer the user the ability to narrow down their search by filtering it
to only include documents with a particular value of a particular category.
This is often referred to as `faceted search`.

.. todo:: string and numeric facets
.. todo:: grouping
.. todo:: selecting which facets to show

Implementation
==============
Faceting works against information stored in :doc:`document value slots
</concepts/indexing/values>`
and, when executed, provides a list of the unique values for
that slot together with a count of the number of times each value occurs.

Indexing
--------

No additional work is needed to implement faceted searching, except to
ensure that the values you wish to use in facets are stored as
document values.

.. xapianexample:: index_facets

Here we're using two value slots: 0 contains the collection, and 1
contains the name of whoever made the object. We know from the
documentation of the dataset that both from fixed and curated lists,
so we don't have to worry about normalising the values before using
them as facets. Let's run that to build a dataset with document values
suitable for faceting:

.. xapianrunexample:: index_facets
    :cleanfirst: db
    :args: data/100-objects-v1.csv db

Querying
--------

To query, Xapian uses the concept of spies to observe
slots of matched documents during a search.

The procedure works in three steps: first, you create a spy
(instance of :xapian-class:`ValueCountMatchSpy`)
for each slot you want the facets; second, you bind each spy to the
:xapian-class:`Enquire` using :xapian-just-method:`add_matchspy(spy)`;
third, after the search was performed, you retrieve the results that
each spy observed. This is an example of how this is done:

.. xapianexample:: search_facets

Here we're faceting on value slot 1, which is the object maker. After
you get the MSet, you can ask the spy for the facets it found,
including the frequency. Note that although we're generally only
showing ten matches, we use a parameter to :xapian-just-method:`get_mset()`
called `checkatleast`, so that the entire dataset is considered and the facet
frequencies are correct. See `Limitations`_ for some discussion of the
implications of this. Here's the output:

.. xapianrunexample:: search_facets
    :args: db clock

Note that the spy will give you facets in alphabetical order, not in
order of frequency; if you want to show the most frequent first you
should use the `top_values` iterator (:xapian-just-method:`begin_top_values()`
in C++ and some other languages).

If you want to work with multiple facets, you can register multiple
:xapian-class:`ValueCountMatchSpy` objects before running
:xapian-just-method:`get_mset()`, although each additional one will have some
performance impact.

Restricting by Facets
---------------------

If you're using the facets to offer the user choices for narrowing down
their search results, you then need to be able to apply a suitable filter.

For a single value, you could use :xapian-constant:`Query::OP_VALUE_RANGE` with
the same start and end, or :xapian-class:`MatchDecider`, but it's probably most
efficient to also index the categories as suitably prefixed boolean terms
and use those for filtering.


Limitations
===========

The accuracy of Xapian's faceting capability is determined by the number
of records that are examined by Xapian whilst it is searching. You can
control this number by specifying the `checkatleast` parameter to
:xapian-just-method:`get_mset()`; however it is important to be aware that
increasing this number may have an effect on overall query performance,
although a typical sized database is unlikely to see adverse effects.


In Development
==============
Some additional features currently in development may benefit users of
facets. These are:

* Multiple values in slots: this will allow you to have a single value slot
  (e.g. colour) which contains multiple values (e.g. red, blue).  This will
  also allow you to create a facet by colour which is aware of these
  multiple values, giving counts for both red and blue.

.. TODO:: This is misleading - it's already possibly to dead with a facet
  with multiple values like this.  We should document how rather than
  seeming to imply you can't currently.

* Bucketing: this provides a means to group together numeric facets, so that
  a single facet can contain a range of values (e.g. price ranges).
