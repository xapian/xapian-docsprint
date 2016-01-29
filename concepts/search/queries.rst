Queries
-------

Queries within Xapian are the mechanism by which documents are searched for
within a database. They can be a simple search for text-based terms or
a search based on the values assigned to documents, which can be combined
using a number of different methods to produce more complex queries.

Simple Queries
~~~~~~~~~~~~~~

The most basic query is a search for a single textual term. This will find
all documents in the database which have that term assigned to them. For
example, a search might be for the term "wood".

Queries can also be used to match values assigned to documents by applying
a *value operator* to a particular value slot.

When a query is executed, the result is a list of documents that match the
query, together with a weight for each which indicates how good a match for
the query that particular document is.

Logical Operators
~~~~~~~~~~~~~~~~~

Each query produces a list of documents with a weight according to how good
a match each document is for that query. These queries can then be combined
to produce a more complex tree-like query structure, with the operators
acting as branches within the tree.

The most basic operators are the logical operators: OR, AND and AND_NOT
- these match documents in the following way:

* :xapian-just-constant:`OP_OR` - matches documents which match query A
  *or* B (or both)
* :xapian-just-constant:`OP_AND` - matches documents which match both
  query A *and* B
* :xapian-just-constant:`OP_AND_NOT` - matches documents which match
  query A but *not* B

Each operator produces a weight for each document it matches, which
depends on the weight of one or both subqueries in the following way:

* :xapian-just-constant:`OP_OR` - matches documents with the sum of
  weights from A and B
* :xapian-just-constant:`OP_AND` - matches documents with the sum of
  weights from A and B
* :xapian-just-constant:`OP_AND_NOT` - matches documents with the weight
  from A only

Maybe
~~~~~

In addition to the basic logical operators, there is an additional logical
operator :xapian-just-constant:`OP_AND_MAYBE` which matches any document
which matches A (whether or not B matches).  If only B matches, then
:xapian-just-constant:`OP_AND_MAYBE` doesn't match.  For this operator, the
weight is the sum of the matching subqueries, so:

1. Documents which match A and B match with the weight of A+B
2. Documents which match A only match with weight of A

This allows you to state that you require some terms (A) and that other
terms (B) are useful but not required.

Filtering
~~~~~~~~~

A query can be filtered by another query.  There are two ways to apply
a filter to a query depending whether you want to include or exclude
documents:

* :xapian-just-constant:`OP_FILTER` - matches documents which match both
  subqueries, but the weight is only taken from the left subquery (in
  other respects it acts like :xapian-just-constant:`OP_AND`)
* :xapian-just-constant:`OP_AND_NOT` - matches documents which match the
  left subquery but don't match the right hand one (with weights coming
  from the left subquery)

Value ranges
~~~~~~~~~~~~

When using document values, there are three relevant operators:

* :xapian-just-constant:`OP_VALUE_LE` - matches documents where the given
  value is less than or equal a fixed value
* :xapian-just-constant:`OP_VALUE_GE` - matches documents where the given
  value is greater than or equal to a fixed value
* :xapian-just-constant:`OP_VALUE_RANGE` - matches documents where the
  given value is within the given fixed range (including both
  endpoints)

Note that when using these operators, they decide whether to include or
exclude documents only and do not affect the weight of a document.

Near and Phrase
~~~~~~~~~~~~~~~

Two additional operators that are commonly used are *NEAR*, which finds
terms within 10 words of each other in the current document, behaving like
:xapian-just-constant:`OP_AND` with regard to weights, so that:

* Documents which match A within 10 words of B are matched, with weight
  of A+B

The phrase operator allows for searching for a specific phrase and returns
only matches where all terms appear in the document, in the correct order,
giving a weight of the sum of each term. For example:

* Documents which match A followed by B followed by C gives a weight of
  A+B+C

Additional operators
~~~~~~~~~~~~~~~~~~~~

Xapian also provides additional operators which can be used to provide more
flexibility than the operators above. For more details of these, see the
`Xapian API documentation <https://xapian.org/docs/apidoc/html/classXapian_1_1Query.html#a7e7b6b8ad0c915c2364578dfaaf6100b>`_.

There are also a pair of predefined query objects which can provide handy:
:ref:`MatchAll <match-all>` matches all the documents in the database, and
MatchNothing matches none of them.
