Query Parser
------------

To make searching databases simpler, Xapian provides a `QueryParser` class
which converts a human readable query string into a Xapian Query object,
for example::

    apple AND a NEAR word OR "a phrase" NOT (too difficult) +eh

The above example shows how some of the basic modifiers are interpreted by
the QueryParser; the operators it supports follow the operators described
earlier, for example:

* ``apple AND pear`` matches documents where both terms are present
* ``apple OR pear`` matches documents where either term (or both) are
  present
* ``apple NOT pear`` matches documents where ``apple`` is present and
  ``pear`` is not

Term Generation
~~~~~~~~~~~~~~~

The QueryParser uses an internal process to convert the query string into terms.
This is similar to the process used by the :doc:`TermGenerator
<../indexing/termgenerator>`, which can be used at index time to convert a
string into terms.  It is often easiest to use QueryParser and
:doc:`TermGenerator <../indexing/termgenerator>` on the same database.

.. todo: link TermGenerator to the termgenerator page

.. todo: stemming and Z prefix discussion

Operators
~~~~~~~~~

As well as the basic logical operators, QueryParser supports the additional
operators discussed earlier and introduces some new ones, for example::

    apple NEAR dessert
    president "united states"
    "race condition" -horse
    +recipe +apple pie cake dessert

The NEAR and phrase support behaves in the same way as described earlier;
the new features are the + and - operators, which select documents based on
the presence or absence of specified terms, for example::

    "race condition" -horse

Matches all documents with the phrase ``"race condition"`` but not ``horse``; and::

    +recipe +apple pie cake desert

Which matches all documents which have the terms ``recipe`` and ``apple``; then
all documents with these terms are weighted according to the weight of the
additional terms.

One thing to note is that the behaviour of the +/- operators vary depending
on the default operator used and the above examples assume that
:xapian-just-constant:`OP_OR` is used.

Bracketed Expressions
~~~~~~~~~~~~~~~~~~~~~

When queries contain both OR and AND operators, AND takes precedence.
To change the precedence of parts of the query, brackets can be used.
For example, with the query::

    apple OR pear AND dessert

The query parser will interpret this query as::

    apple OR (pear AND dessert)

So to change the precedence and make the dessert a requirement, you would
write the query initially as::

    (apple OR pear) AND dessert

Stop words
~~~~~~~~~~

Xapian also supports a `stop word` list, which allows you to specify words
which should be removed from a query before processing. This list can
be overridden within user search, so stop words can still be searched for
if desired, for example if a stop word list contained 'the' and a search
was for::

    +the +document

Then the search would find relevant documents which contained both 'the'
and 'document'.  Also, when searching for phrases, stop words do not apply,
for example here we will retrieve documents with the exact phrase including
'the'::

    "the green space"

Searching with Prefixes
~~~~~~~~~~~~~~~~~~~~~~~

When a database is populated using prefixed terms (for example, title,
author) it is possible to tell the QueryParser that these fields can be
searched for using a human-readable prefix; for example::

    author:"william shakespeare" title:juliet

Ranges
~~~~~~

The QueryParser also supports range searches on document values, matching
documents which have values within a given range. There are several types
of range processors available, but the two discussed here are `Date`_ and
`Number`_, which require that values are serialised as they are indexed.

To use a range, additional programming is required to tell the QueryParser
what format a range is specified in and which value is to be searched for
matches within that range. This then gives rise to the ability to specify
ranges as:

.. code-block:: none

    $10..50
    5..10kg
    01/01/1970..01/03/1970
    size:3..7

When date ranges are configured (as a `DateRangeProcessor`_), you can
configure which format dates are to be interpreted as (i.e. month-day-year)
or otherwise.

.. _Date:
.. _DateRangeProcessor: https://xapian.org/docs/apidoc/html/classXapian_1_1DateRangeProcessor.html

.. _Number:
.. _NumericRangeProcessor: https://xapian.org/docs/apidoc/html/classXapian_1_1NumberRangeProcessor.html

Wildcards
~~~~~~~~~

It is also possible to use wildcards to match any number of trailing
characters within a term; for example:

    ``wild*`` matches ``wild, wildcard, wildcat, wilderness``

This feature is disabled by default; to enable it, see 'Parser Flags'
below.  It also requires a database to be set on the QueryParser (so
that it can find the list of terms to expand the wildcard to).

By default the wildcard will expand to as many terms as there are with
the specified prefix.  This can cause performance problems, so you can limit
the number of terms a wildcard will expand to by calling
:xapian-method:`QueryParser::set_max_wildcard_expansion()`.  If this limit
would be exceeded then an exception will be thrown.  The exception may
be thrown by the QueryParser, or later when Enquire handles the query.

Searching for Partially Entered Queries
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The QueryParser also supports performing a search with a query which has
only been partially entered. This is intended for use with "incremental
search" systems, which don't wait for the user to finish typing their
search before displaying an initial set of results. For example, in such
a system a user would enter a search, and the system would display a new
set of results after each letter, or whenever the user pauses for a
short period of time (or some other similar strategy).

The problem with this kind of search is that the last word in a
partially entered query often has no semantic relation to the completed
word. For example, a search for "dynamic cat" would return a quite
different set of results to a search for "dynamic categorisation". This
results in the set of results displayed flicking rapidly as each new
character is entered. A much smoother result can be obtained if the
final word is treated as having an implicit terminating wildcard, so
that it matches all words starting with the entered characters - thus,
as each letter is entered, the set of results displayed narrows down to
the desired subject.

A similar effect could be obtained simply by enabling the wildcard
matching option, and appending a "\*" character to each query string.
However, this would be confused by searches which ended with punctuation
or other characters.

This feature is disabled by default - pass
:xapian-just-constant:`FLAG_PARTIAL` flag in the flags argument of
:xapian-method:`QueryParser::parse_query(query_string, flags)` to enable it,
and tell the QueryParser which database to expand wildcards from using
the :xapian-method:`QueryParser::set_database(database)` method.

Default Operator
~~~~~~~~~~~~~~~~

When the QueryParser receives a query, it joins together its component
queries using a `default operator`_ which defaults to
:xapian-just-constant:`OP_OR` but can be modified at run time.

.. _default operator: https://xapian.org/docs/apidoc/html/classXapian_1_1QueryParser.html#a2efe48be88c4872afec4bc963f417ea5

Parser Flags
~~~~~~~~~~~~
The operation of the QueryParser can be altered through the use of flags,
combined with the bitwise OR operator; these flags include:

* :xapian-just-constant:`FLAG_BOOLEAN`: enables support for AND, OR, etc and bracketed
  expressions
* :xapian-just-constant:`FLAG_PHRASE`: enables support for phrase expressions
* :xapian-just-constant:`FLAG_LOVEHATE`: enables support for `+` and `-` operators
* :xapian-just-constant:`FLAG_BOOLEAN_ANY_CASE`: enables support for lower/mixed case boolean
  operators
* :xapian-just-constant:`FLAG_WILDCARD`: enables support for wildcards

You can find more information about the available flags in the
`API documentation
<https://xapian.org/docs/apidoc/html/classXapian_1_1QueryParser.html#ae96a58a8de9d219ca3214a5a66e0407e>`_.

By default, the QueryParser enables :xapian-just-constant:`FLAG_BOOLEAN`,
:xapian-just-constant:`FLAG_PHRASE` and :xapian-just-constant:`FLAG_LOVEHATE`.
