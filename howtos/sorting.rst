.. Original content was taken from xapian-core/docs/sorting.rst with
.. a copyright statement of:
.. Copyright (C) 2007,2009,2011 Olly Betts


Sorting
=======

By default, Xapian orders search results by decreasing relevance score.
However, it also allows results to be ordered by other criteria, or
a combination of other criteria and relevance score.

If two or more results compare equal by the sorting criteria, then their
order is decided by their document ids.  By default, the document ids sort
in ascending order (so a lower document id is "better"), but descending
order can be chosen using ``enquire.set_docid_order(enquire.DESCENDING);``.
If you have no preference, you can tell Xapian to use whatever order is
most efficient using ``enquire.set_docid_order(enquire.DONT_CARE);``.

It is also possible to change the way that the relevance scores are calculated
- for details, see the :doc:`document on weighting schemes and scoring
<weighting_scheme>` for details.

Sorting by Value
----------------

You can order documents by comparing a specified document value.  Note that the
comparison used compares the byte values in the value (i.e. it's a string sort
ignoring locale), so ``1`` < ``10`` < ``2``.  If you want to encode the value
such that it sorts numerically, use :xapian-just-method:`sortable_serialise()` to encode
values at index time - this works equally well on integers and floating point
values:

.. xapiancodesnippet:: c++

    Xapian::Document doc;
    doc.add_value(0, Xapian::sortable_serialise(price));

.. xapiancodesnippet:: php

    $doc->add_value(0, Xapian::sortable_serialise($price));

.. xapiancodesnippet:: python

    doc.add_value(0, xapian.sortable_serialise(price))

There are three methods which are used to specify how the value is used to
sort, depending if/how you want relevance used in the ordering:

* :xapian-method:`Enquire::set_sort_by_value()` specifies the relevance doesn't affect the
  ordering at all.
* :xapian-method:`Enquire::set_sort_by_value_then_relevance()` specifies that relevance is
  used for ordering any groups of documents for which the value is the same.
* :xapian-method:`Enquire::set_sort_by_relevance_then_value()` specifies that documents are
  ordered by relevance, and the value is only used to order groups of documents
  with identical relevance values (note: the weight has to be exactly the same
  for values to determine the order, so this method isn't very useful when
  using BM25 with the default parameters, as that will rarely give identical
  scores to different documents).

We'll use the states dataset to demonstrate this, and the code from
dealing with dates in the :doc:`range queries <range_queries>` HOWTO:

.. xapianrunexample:: index_ranges2
    :cleanfirst: statesdb
    :args: data/states.csv statesdb

This has three document values: slot 1 has the year of admission to
the union, slot 2 the full date (as "YYYYMMDD"), and slot 3 the latest
population estimate. So if we want to sort by year of entry to the
union and then within that by relevance, we want to add the following
before we call `get_mset`:

.. xapianexample:: search_sorting

The final parameter is :xapian-literal:`false` for ascending order,
:xapian-literal:`true` for descending.  We can then run sorted searches like
this:

.. xapianrunexample:: search_sorting
    :args: statesdb spanish


Generated Sort Keys
-------------------

To allow more elaborate sorting schemes, Xapian allows you to provide a
functor object subclassed from :xapian-class:`KeyMaker` which generates a sort
key for each matching document which is under consideration.  This is
called at most once for each document, and then the generated sort keys are
ordered by comparing byte values (i.e. with a string sort ignoring locale).

Sorting by Multiple Values
~~~~~~~~~~~~~~~~~~~~~~~~~~

There's a standard subclass :xapian-class:`MultiValueKeyMaker` which allows
sorting on more than one document value (so the first document value
specified determines the order; amongst groups of documents where that's
the same, the second document value determines the order, and so on).

We'll use this to change our sorted search above to order by year of
entry to the union and then by decreasing population.

.. xapianexample:: search_sorting2

As with the `Enquire` methods, `add_value` has a second parameter that
controls whether it uses an ascending or descending sort. So now we
can run a search with a more complex sort:

.. xapianrunexample:: search_sorting2
    :args: statesdb State

Other Uses for Generated Keys
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:xapian-class:`KeyMaker` can also be subclassed to sort based on a calculation.
For example, "sort by geographical distance", where a subclass could take
the latitude and longitude of the user's location, and coordinates of the
document from a value slot, and sort results so that those closest to the
user are ranked highest.

For this, we're going to want the geographical coordinates of each
state stored in a value. We can use the approximate middle of the
state for this purpose, which is calculated for us when parsing the
`states.csv` file:

.. xapianexample:: index_values_with_geo

We don't have to sort on these, so we've just put them both into one
slot that we can easily read them out from again:

.. xapianrunexample:: index_values_with_geo
    :cleanfirst: statesdb
    :args: data/states.csv statesdb

Now we need a KeyMaker; let's have it return a key that sorts by distance from
Washington, DC.

.. xapianexample:: search_sorting3

And running it is as simple as before:

.. xapianrunexample:: search_sorting3
    :args: statesdb State
