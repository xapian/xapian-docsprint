Iterate through all documents
=============================

Sometimes you want to access all the documents in a Xapian database.  This can actually be done in two ways:

.. _match-all:

MatchAll Queries
----------------

The `Xapian::Query::MatchAll` query is a special static query which will match all documents in the database.
If you run this query on its own, with appropriate start and end parameters, you could retrieve all the documents.
However be aware that even if you paged through the result sets, when you try to access a page deep in the result
set a lot of processing and memory will be used even if the page is small, so running a plain `MatchAll` query is
rarely a good idea.

However, this method *is* appropriate if you're constructing a complicated query, and one of the components of that
query should be all the documents.  In particular, since Xapian doesn't support a unary `NOT` operator, if you want to
run a "pure NOT" query to retrieve all documents which do not contain a given term, this can be only be done using a
`MatchAll` query and the binary `NOT` operator.

.. todo: Need an example here, and probably some rewording of the previous paragraph.

.. note: MatchAll queries can also be created by constructing a query with an empty term: the MatchAll class is
.. syntactic sugar for this, and avoids you needing to create an instance of a query for this.

Iterating through all documents
-------------------------------

If you do need access to all the documents in the database, it is better to use a "posting list iterator".
Such an iterator, which returns all documents in the database, can be created using::

    Xapian::Database::postlist_begin("")

In Xapian, a postlist is a list of the documents in which a term exists.  Here, we're again using the special
"empty" term, which implicitly matches all documents, to get an iterator over all documents.

The iterator can be dereferenced to get the document IDs; to get the actual documents, the
:xapian-method:`Database::get_document()` method should be used.

.. todo: Need an example here, and probably some rewording.
