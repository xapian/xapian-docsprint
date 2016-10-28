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

.. note::

   Since :ref:`term prefixes <term-prefixes>`
   start with an uppercase letter or letters, and
   the :doc:`term generator </concepts/indexing/termgenerator>`
   lowercases words in order to build
   terms, there's no chance of the boolean terms we're generating here matching
   against "real" words from the source data.

We can therefore just add the identifiers to the :xapian-class:`Document`
directly, after splitting on semicolons, using the
:xapian-just-method:`add_boolean_term()` method.

.. xapianexample:: index_filters
    :marker: new indexing code

A full copy of the indexer with this updated code is available in
:xapian-code-example:`^`.

We run this like so:

.. xapianrunexample:: index_filters
    :cleanfirst: db
    :args: data/100-objects-v1.csv db

If we check the resulting index with xapian-delve, we will see that documents for
which there was a value in the ``MATERIALS`` field now contain terms with the
``XM`` prefix (output snipped to show the relevant lines):

.. code-block:: sh

    $ xapian-delve -r 3 -1 db
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
representing the checkboxes which are selected, using the
:xapian-just-constant:`OP_FILTER` operator.  If multiple checkboxes are
selected, we need to combine the Query objects for each checkbox with an
:xapian-just-constant:`OP_OR` operator.

An arbitrarily complex Query tree can be built using queries returned from the
QueryParser and manually constructed Query objects, which allows very flexible
filtering of the results from parsed queries.

.. xapianexample:: search_filters

A full copy of the this updated search code is available in
:xapian-basename-code-example:`^`.  With this, we could perform a search for
documents matching "clock", and filter the results to return only those with a
value of ``"steel (metal)"`` as one of the semicolon separated values in the
materials field:

.. xapianrunexample:: search_filters
    :args: db clock 'steel (metal)'

Using the query parser
----------------------

The previous section shows how to write code to filter the results of a query
programmatically.  This can be very flexible, but sometimes you want users to be
able to specify filters themselves, within the text query that they enter.

You can do this using the ``QueryParser.add_boolean_prefix()`` method.  This
lets you tell the query parser about a field to use for filtering, and the
prefix that terms have been stored in for that term.  For our materials search,
we just need to a add a single line to the search code:

.. xapianexample:: search_filters2
    :emphasize-lines: 21-26

Users can then perform a filtered search by preceding a word or phrase with
"material:", similar to the syntax supported for this sort of thing by many web
search engines:

.. xapianrunexample:: search_filters2
    :args: db 'clock material:"steel (metal)"'

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
