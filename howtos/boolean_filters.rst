How to filter search results
============================

.. todo:: point out that lowercasing by TermGenerator or similar will
.. prevent unexpected matching of prefixes terms by "real" words in
.. the source data

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
    :start-after: Start of new indexing code
    :end-before: End of new indexing code

A full copy of the indexer with this updated code is available in
``code/python/index_filters.py``.

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

Suppose that the interface we want to provide allows users to type a free text
search into one form input, but also has a set of checkboxes for different
possible materials.  We want to return documents which match the text search
entered, but only if they also contain one of the materials for which the
checkbox is selected.

To build a query which performs this task, we can take the Query object
returned by the query parser, and combine it with a manually built Query
representing the checkboxes which are selected, using the ``OP_FILTER``
operator.  If multiple checkboxes are selected, we need to combine the Query
objects for each checkbox with an ``OP_OR`` operator.

An arbitrarily complex Query tree can be built using queries returned from the
QueryParser and manually constructed Query objects, which allows very flexible
filtering of the results from parsed queries.

.. literalinclude:: /code/python/search_filters.py
    :start-after: Start of example code
    :end-before: End of example code

A full copy of the this updated search code is available in
``code/python/search_filters.py``.  With this, we could perform a search for
documents matching "clock", and filter the results to return only those with a
value of ``"steel (metal)"`` as one of the semicolon separated values in the
materials field::

    $ python code/python/search_filters.py db clock 'steel (metal)'
    1: #012 Assembled and unassembled EXA electric clock kit
    2: #098 'Pond' electric clock movement (no dial)
    3: #052 Reconstruction of Dondi's Astronomical Clock, 1974
    4: #059 Electrically operated clock controller
    5: #024 Regulator Clock with Gravity Escapement
    6: #097 Bain's subsidiary electric clock
    7: #009 Copy  of a Dwerrihouse skeleton clock with coup-perdu escape
    8: #091 Pendulum clock designed by Galileo in 1642 and made by his son in 1649, model.
    INFO:xapian.search:'clock'.material(['steel (metal)'])[0:10] = 12 98 52 59 24 97 9 91


Using the query parser
----------------------

The previous section shows how to write code to filter the results of a query
programatically.  This can be very flexible, but sometimes you want users to be
able to specify filters themselves, within the text query that they enter.

You can do this using the ``QueryParser.add_boolean_prefix()`` method.  This
lets you tell the query parser about a field to use for filtering, and the
prefix that terms have been stored in for that term.  For our materials search,
we just need to a add a single line to the search code:

.. literalinclude:: /code/python/search_filters2.py
    :start-after: Start of example code
    :end-before: End of example code
    :emphasize-lines: 21-26

Users can then perform a filtered search by preceding a word or phrase with
"material:", similar to the syntax supported for this sort of thing by many web
search engines::

    $ python code/python/search_filters2.py db 'clock material:"steel (metal)"'
    1: #012 Assembled and unassembled EXA electric clock kit
    2: #098 'Pond' electric clock movement (no dial)
    3: #052 Reconstruction of Dondi's Astronomical Clock, 1974
    4: #059 Electrically operated clock controller
    5: #024 Regulator Clock with Gravity Escapement
    6: #097 Bain's subsidiary electric clock
    7: #009 Copy  of a Dwerrihouse skeleton clock with coup-perdu escape
    8: #091 Pendulum clock designed by Galileo in 1642 and made by his son in 1649, model.
    INFO:xapian.search:'clock material:"steel (metal)"'[0:10] = 12 98 52 59 24 97 9 91

What to supply to the query parser
----------------------------------

Often, developers seem to be tempted to apply filters to a query by modifying
the query supplied by a user (eg, by adding things like ``material:steel`` to
the end of it).  This is generally a bad idea, because the query parser
contains various heuristics to handle input from users; it is very hard to
modify the input to a query parser to reliably add a filter to the parsed
query.

The rule is that the query parser should be supplied with direct user input,
and if you want to apply extra filters to the query, you should apply them to
the output of the query parser.

In later sections, we'll see how to tell the query parser about other types of
searches that users might enter (for example, range searches).  In each of
these cases, it is also possible to perform such searches and restrictions
without using the query parser; the query parser just allows the user of the
search system to perform such restrictions in the query string.
