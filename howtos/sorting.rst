Sorting
=======

By default, Xapian orders search results by decreasing relevance score.
However, it also allows results to be ordered by other criteria, or
a mixture of other criteria and relevance score.

If two or more results compare equal by the sorting criteria, then their 
order is decided by their document ids in ascending order; if required, 
this can be changed by using the function `XapianEnquire::set_docid`.

It is also possible to change the way that the ranking is calculated; for
details on this, see the [link to ranking doc] document.

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
   with identical relevance values
   
NOTE: The relevance values used to for these calculations are based on the
default BM25 weighting for each document, which rarely assigns identical 
scores to different documents so you may find that relevance_then_value 
does not behave as expected.

Sorting by Multiple Values
--------------------------
To allow more elaborate sorting schemes, Xapian allows you to provide a functor
object subclassed from ``Xapian::KeyMaker`` which generates a sort key for each
matching document which is under consideration.  This is called at most once
for each document, and then the generated sort keys are ordered by comparing
byte values (i.e. with a string sort ignoring locale).

There's a standard subclass ``Xapian::MultiValueKeyMaker`` which allows sorting
on more than one document value (so the first document value specified
determines the order except among groups which have the same value, when
the second document value specified is used, and so on).

``Xapian::KeyMaker`` can also be subclassed to offer features such as "sort by
geographical distance".  A subclass could take a coordinate pair - e.g.
(latitude, longitude) - for the user's location and sort results using
coordinates stored in a document value so that the nearest results ranked
highest.
