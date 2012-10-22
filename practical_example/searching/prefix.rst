Searching separate fields
-------------------------

When we built our index, we used prefixes to separate the terms generated from
the title and description fields.  This allows us to perform searches which are
restricted to the text in just one of those fields, by searching only terms
with the desired prefix.

When using the Query Parser, it is possible to restrict your search to
certain prefixed terms (e.g. title, or description). These can be searched
for either by using a search prefix (which can correlate to an indexing
prefix) or as a general text document.

To set up a search prefix, the QueryParser needs to be told which prefixes
in the search query relate to those in the index:


.. todo:: This example should really be pulled directly from the code. There
          seems to be a bug with line number limiting somewhere in the literal
          include directive.

.. code-block:: python

    queryparser.add_prefix("title", "S")
    queryparser.add_prefix("description", "XD")

This allows us to perform a search based on either field, for example:

.. xapianrunexample:: search1
    :args: db title:sunwatch

We can also combine prefixes with the logical operators to perform more
complex queries (note that we need to escape quotes or else the shell
will eat them):

.. xapianrunexample:: search1
    :args: db description:\"leather case\" AND title:sundial
