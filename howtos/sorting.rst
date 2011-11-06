.. Copyright (C) 2007,2009,2011 Olly Betts
.. Copyright (C) 2011 Justin Finkelstein
.. Copyright (C) 2011 James Aylett


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
- for details, see the :ref:`document on weighting schemes and
  document scoring <weighting_scheme>` for details.

Sorting by Value
----------------

You can order documents by comparing a specified document value.  Note that the
comparison used compares the byte values in the value (i.e. it's a string sort
ignoring locale), so ``1`` < ``10`` < ``2``.  If you want to encode the value
such that it sorts numerically, use ``Xapian::sortable_serialise()`` to encode
values at index time - this works equally well on integers and floating point
values::

    Xapian::Document doc;
    doc.add_value(0, Xapian::sortable_serialise(price));

There are three methods which are used to specify how the value is used to
sort, depending if/how you want relevance used in the ordering:

 * ``Enquire::set_sort_by_value()`` specifies the relevance doesn't affect the
   ordering at all.
 * ``Enquire::set_sort_by_value_then_relevance()`` specifies that relevance is
   used for ordering any groups of documents for which the value is the same.
 * ``Enquire::set_sort_by_relevance_then_value()`` specifies that documents are
   ordered by relevance, and the value is only used to order groups of documents
   with identical relevance values (note: the weight has to be exactly the same
   for values to determine the order, so this method isn't very useful when
   using BM25 with the default parameters, as that will rarely give identical
   scores to different documents).

We'll use the states dataset to demonstrate this, and the code from
dealing with dates in the :ref:`range queries <range_queries>` HOWTO::

    $ python code/python/index_ranges2.py states.csv statesdb

This has three document values: slot 1 has the year of admission to
the union, slot 2 the full date (as "YYYYMMDD"), and slot 3 the latest
population estimate. So if we want to sort by year of entry to the
union and then within that by relevance, we want to add the following
before we call `get_mset`:

.. literalinclude:: /code/python/search_sorting.py
    :start-after: Start of example code.
    :end-before: End of example code.

The final parameter is `False` for ascending order, `True` for
descending. We can then run sorted searches like this::

    $ python code/python/search_sorting.py statesdb spanish
    1: #019 State of Texas December 29, 1845 (28th)
            Population 25,145,561 (2010 Census) [ 5 ]
    2: #004 State of Montana November 8, 1889 (41st)
            Population 989,415 (2010)
    INFO:xapian.search:'spanish'[0:10] = 19 4


Generated Sort Keys
-------------------

To allow more elaborate sorting schemes, Xapian allows you to provide a
functor object subclassed from ``Xapian::KeyMaker`` which generates a sort
key for each matching document which is under consideration.  This is
called at most once for each document, and then the generated sort keys are
ordered by comparing byte values (i.e. with a string sort ignoring locale).

Sorting by Multiple Values
~~~~~~~~~~~~~~~~~~~~~~~~~~

There's a standard subclass ``Xapian::MultiValueKeyMaker`` which allows
sorting on more than one document value (so the first document value
specified determines the order; amongst groups of documents where that's
the same, the second document value determines the order, and so on).

We'll use this to change our sorted search above to order by year of
entry to the union and then by decreasing population.

.. literalinclude:: /code/python/search_sorting2.py
    :start-after: Start of example code.
    :end-before: End of example code.

As with the `Enquire` methods, `add_value` has a second parameter that
controls whether it uses an ascending or descending sort. So now we
can run a search with a more complex sort::

    $ python code/python/search_sorting2.py statesdb/ State
    1: #040 Commonwealth of Pennsylvania December 12, 1787 (2nd)
            Population 12,702,379(2010.) [ 2 ]
    2: #043 State of New Jersey December 18, 1787 (3rd)
            Population 8,791,894 (2010 Census) [ 4 ]
    3: #049 State of Delaware December 7, 1787 (1st)
            Population 897,934
    4: #041 State of New York July 26, 1788 (11th)
            Population 19,378,102 (2010 Census) [ 3 ]
    5: #038 Commonwealth of Virginia June 25, 1788 (10th)
            Population 8,001,024
    6: #050 State of Maryland April 28, 1788 (7th)
            Population 5,773,552 (2010) [ 3 ] 5,296,486 (2000)
    7: #036 State of South Carolina May 23, 1788 (8th)
            Population 4,625,384 (2010 census) [ 1 ]
    8: #045 State of New Hampshire June 21, 1788 (9th)
            Population 1,316,470 (2010 census) [ 1 ] 1,235,786 (2000)
    9: #034 State of Georgia January 2, 1788 (4th)
            Population (2010) 9,687,653 [ 1 ]
    10: #048 State of Connecticut January 9, 1788 (5th)
            Population (2010) 3,574,097 [ 7 ]
    INFO:xapian.search:'State'[0:10] = 40 43 49 41 38 50 36 45 34 48


Other Uses for Generated Keys
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``Xapian::KeyMaker`` can also be subclassed to sort based on a calculation.
For example, "sort by geographical distance", where a subclass could take
the latitude and longitude of the user's location, and coordinates of the
document from a value slot, and sort results so that those closest to the
user are ranked highest.

For this, we're going to want the geographical coordinates of each
state stored in a value. We can use the approximate middle of the
state for this purpose, which are calculated for us when parsing the
`states.csv` file:

.. literalinclude:: /code/python/index_values_with_geo.py
    :start-after: Start of example code.
    :end-before: End of example code.

We don't have to sort on these, so we've just put them both into one
slot that we can easily read them out from again. Now we need a
KeyMaker; let's have it return a key that sorts by distance from
Washington, DC.

.. literalinclude:: /code/python/search_sorting3.py
    :start-after: Start of example code.
    :end-before: End of example code.

And running it is as simple as before::

    python code/python/search_sorting3.py statesdb/ State
    1: #050 State of Maryland 17880428
            Population 5773552
    2: #040 Commonwealth of Pennsylvania 17871212
            Population 12702379
    3: #049 State of Delaware 17871207
            Population 897934
    4: #041 State of New York 17880726
            Population 19378102
    5: #043 State of New Jersey 17871218
            Population 8791894
    6: #037 State of North Carolina 17891121
            Population 9535483
    7: #039 State of West Virginia 18630620
            Population 1859815
    8: #036 State of South Carolina 17880523
            Population 4625384
    9: #048 State of Connecticut 17880109
            Population 3574097
    10: #038 Commonwealth of Virginia 17880625
            Population 8001024
    INFO:xapian.search:'State'[0:10] = 50 40 49 41 43 37 39 36 48 38
