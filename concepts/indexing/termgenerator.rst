Term Generator
==============

Rather than force all users to write their own code to process text into terms
for indexing, Xapian provides a :xapian-class:`TermGenerator` class.  This parses
chunks of text, producing appropriate terms, and adds them to a document.

The :xapian-class:`TermGenerator` can be configured to perform stemming (and
stopwording) when generating terms.  It can optionally store information about
the positions of words within the text, and can apply field-specific prefixes
to the generated terms to allow searches to be restricted to specific
fields.  It can also add additional information to the database for use
when performing spelling correction.

If you're using the :xapian-class:`TermGenerator` to process text in this way,
you will probably want to use the :doc:`QueryParser <../search/queryparser>`
(described later) when performing searches.
