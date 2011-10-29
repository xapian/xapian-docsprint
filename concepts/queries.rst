Queries
-------

Queries within Xapian are the mechanism by which documents are searched for 
within its database. They can be a single search for text-based terms or 
a search based on the values assigned to documents, which can be combined
using a number of different methods to produce more complex queries.

Simple Queries
~~~~~~~~~~~~~~
The most basic query is a search for a single textual term. This will find 
all documents in the database which have that term assigned to them. For 
example, a search might be for the term "wood".

Queries can also be used to match values assigned to documents, either as
a direct comparison (equals) match or a numerical range, such as a date
range.

Building on these, you can create queries which find documents based on the
values that a document posseses - either as a simple match or as a range.
Operators (i.e. OR, AND, etc) can be used to combine these simple queries
into more complex patterns.

Filters
~~~~~~~
It is also possible to filter the results of a query by using a special
operator, *OP_FILTER*, which takes a query (containing a requirement to 
match a term, value or value range) and processes the results of all of 
the other queries combined with the filter query, so that this returns
only those results which match the filter.

