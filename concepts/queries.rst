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

The most basic operators are the logical operators: OR, AND and AND_NOT; in
these examples each takes two queries (A and B) as arguments. Remembering 
this, the effect of these operators can be described as follows:

	* OP_OR - returns documents which match query A *or* B (or both)
	* OP_AND - returns documents which match both query A *and* B
	* OP_AND_NOT - returns documents which match query A but *not* B


----
All operators control the weight of the documents which are passed 


Xapian supports a wide range of operators, the most common of which are 
normally applied to the results of two queries (A and B), for example:



When applying logical operators, the resulting list of documents will have 
a weight according to the logical rule applied by that operator; for 
example: 

	* OR - documents will have the weight of the first match
	* AND - documents will have the combined weight of both documents

Filtering Operators
~~~~~~~~~~~~~~~~~~~
In addition to the logical operators, there are those which apply filtering
to the results:

	* OP_FILTER - finds all documents which match both query A and B, but
uses only the weights from query A
	* OP_AND_MAYBE - finds all documents which match query A and uses their
weights. If a document also matches query B, its weight is also added to
the resulting document.


