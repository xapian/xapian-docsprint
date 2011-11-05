.. Copyright (C) 2007,2009,2011 Olly Betts
.. Copyright (C) 2011 Justin Finkelstein

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
- for details, see the [link to ranking doc] document.

.. todo:: write the above referenced document and link it

Sorting by Value
----------------

You can order documents by comparing a specified document value.  Note that the
comparison used compares the byte values in the value (i.e. it's a string sort
ignoring locale), so ``1`` < ``10`` < ``2``.  If you want to encode the value
such that it sorts numerically, use ``Xapian::sortable_serialise()`` to encode
values at index time - this works equally will on integers and floating point
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

Other Uses for Generated Keys
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``Xapian::KeyMaker`` can also be subclassed to sort based on a calculation.
For example, "sort by geographical distance", where a subclass could take
the latitude and longitude of the user's location, and coordinates of the
document from a value slot, and sort results so that those closest to the
user are ranked highest.
