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

Queries can also be used to match values assigned to documents, either by 
an exact match, a numeric range or by applying a *value operator* against
the value.

When queries are executed, documents that match that query are returned 
together with a weight which indicates how good a match for that query a 
particular document is. 

Logical Operators
~~~~~~~~~~~~~~~~~
Each query produces a list of documents with a weight according to how good
a match each document is for that query. These queries can then be combined
to produce a more complex tree-like query structure, with the operators
acting as branches within the tree.

The most basic operators are the logical operators: OR, AND and AND_NOT. 
These operators process documents which match certain queries (A and B), 
which have a weight assigned for each match. As documents pass through each
operator branch, their weight is adjusted according to the type of branch,
for example:

	* OP_OR - passes documents which match query A *or* B (or both)
	* OP_AND - passes documents which match both query A *and* B
	* OP_AND_NOT - passes documents which match query A but *not* B

The weights of the documents are adjusted as follows:

	* OP_OR - passes documents with the sum of weights from A and B
	* OP_AND - passes documents with the sum of weights from A and B
	* OP_AND_NOT - passes documents with the weight from A only

Maybe
~~~~~
In addition to the basic logical operators, there is an additional logical
operator *OP_AND_MAYBE* which can be used to give a document which matches
A or (A and B). When this operator is used, the document weight is
adjusted so that:

	1. Documents which match A and B are passed, with weight of A+B
	2. Documents which match A only are passed, with weight of A
	3. Documents which match B only are not passed
	
This allows you to state that you require some terms (A) and that other 
terms (B) are useful but not required.

Filtering
~~~~~~~~~
There are two ways to apply filters to queries: using document values or
using a filter query (i.e. where a document matches a query or not).

When using document values, there are three relevant operators:

	* OP_VALUE_LE - passes documents where the given value is less than or 
	  equal a fixed value
	* OP_VALUE_GE - passes documents where the given value is greater than 
	  or equal to a fixed value
	* OP_VALUE_RANGE - passes documents where the given value is within the
	  given fixed range (including both endpoints)

Note that when using these operators, they decide whether to include or
exclude documents only and do not affect the weight of a document.

Another way to filter documents is by using the OP_FILTER operand, which
behaves like OP_AND, but passes only the weight from match (A):

	* Documents which match A and B are passed, with weight of A
	
Near and Phrase
~~~~~~~~~~~~~~~
Two additional operators that are commonly used are *NEAR*, which finds 
terms within 10 words of each other in the current document, behaving like
OP_AND with regard to weights, so that:

	* Documents which match A within 10 words of B are passed, with weight 
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
full Xapian documentation at http://xapian.org/.
