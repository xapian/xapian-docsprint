How to filter search results
============================

In our earlier discussion of building an index of museum catalog data, we
showed how to index text from the title and description fields with
separate prefixes, allowing searches to be performed across just one of
those fields.  This is a simple type of fielded search, but often some
fields in a document won't contain unconstrained text; for example, they
may contain only a few specific values or identifiers.  We often wish to
use such fields to restrict the results to only those matching a particular
value, rather than treating them as unstructured "free text".

In the museum catalog, the ``MATERIALS`` field is an example of a field
which contains text from a restricted vocabulary.  This text can be thought
of as an identifier, rather than text which needs to be parsed.  In fact,
for many records this field contains several identifiers for materials in
the object, separated by semicolons.

Indexing
--------

When indexing such fields, we don't want to perform stemming, though we may
well want to convert the identifiers to lowercase if case is not significant.
We also don't expect the number of times a term from these fields occurs in a
document to be significant (we only expect it to occur 0 or 1 times), so we
don't need to store "within document frequency" information.  A field like
this, which we're using to restrict the results returned from a search rather
than as part of the weighted search, is referred to as a `boolean term`.

We can therefore just add the identifiers to the ``Document`` directly,
after splitting on semicolons, using the ``add_boolean_term()`` method.

.. literalinclude:: /code/python/index_filters.py
    :emphasize-lines: 10-14
    :start-after: termgenerator.set_document(doc)
    :end-before: we use the identifier to ensure each object ends up

If we check the resulting index with delve, we will see that documents for
which there was a value in the ``MATERIALS`` field now contain terms with the
``XM`` prefix (output snipped to show the relevant lines)::

    $ delve -r 3 -1 db
    Term List for record #3:
    ...
    XDwooden
    XMglass
    XMmounted
    XMsand
    XMtimer
    XMwood
    ZSabbot
    ...

Searching
---------

.. todo:: How to search using manually built Query objects.

Using the query parser
----------------------

.. todo:: How to search using the query parser.

