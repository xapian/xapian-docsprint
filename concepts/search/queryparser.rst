Query Parser
------------

To make searching databases simpler, Xapian provides a `QueryParser` class
which converts a human readable query string into a Xapian Query object,
for example:

	apple AND a NEAR word OR "a phrase" NOT (too difficult) +eh

The above example shows how some of the basic modifiers are interpreted by
the QueryParser; the operators it supports follow the operators described
earlier, for example:

	* 'apple AND pear' matches documents where both terms are present
	* 'apple OR pear' matches documents where either term (or both) are 
	  present
	* 'apple NOT pear' matches documents where apple is present and pear is
	  not

Term Generation
~~~~~~~~~~~~~~~

The QueryParser uses an internal process to convert the query string into 
terms.  This is similar to the procses used by the TermGenerator, which
can be used at index time to convert a string into terms.  It is often 
easiest to use QueryParser and TermGenerator on the same database.

.. todo: link TermGenerator to the termgenerator page

Wildcards
~~~~~~~~~

It is also possible to use wildcards to match any number of trailing 
characters within a term; for example:

	'wild*' matches wild, wildcard, wildcat, wilderness, etc
	
This feature is disabled by default; to enable it, see 'Enabling Features'
below.

Bracketed Expressions
~~~~~~~~~~~~~~~~~~~~~

When queries contain both OR and AND operators, AND takes precedence.
To change the precedence of parts of the query, brackets can be used.
For example, with the query:

	apple OR pear AND dessert
	
The query parser will interpret this query as:

	apple OR (pear AND dessert)
	
So to change the precedence and make the dessert a requirement, you would
write the query initially as:

	(apple OR pear) AND dessert

Default Operator
~~~~~~~~~~~~~~~~

When the QueryParser receives a query, it joins together its component
queries using a `default operator` which defaults to OP_OR but can be 
modified at run time.

Additional operators
~~~~~~~~~~~~~~~~~~~~

As well as the basic logical operators, QueryParser supports the additional
operators discussed earlier and introduces some new ones, for example:

	apple NEAR dessert
	president "united states"
	"race condition" -horse
	+recipe +apple pie cake dessert

The NEAR and phrase support behaves in the same way as described earlier; 
the new features are the + and - operators, which select documents based on
the presence or absence of specified terms, for example:

	"race condition" -horse

Matches all documents with the phrase "race condition" but not horse; and:

	+recipe +apple pie cake desert
	
Which matches all documents which have the terms 'recipe' and 'apple'; then
all documents with these terms are weighted according to the weight of the
additional terms. 

One thing to note is that the behaviour of the +/- operators vary depending
on the default operator used and the above examples assume that OP_OR is 
used. 

Searching with Prefixes
~~~~~~~~~~~~~~~~~~~~~~~

When a database is populated using prefixed terms (for example, title, 
author) it is possible to tell the QueryParser that these fields can be 
searched for using a human-readable prefix; for example:

	author:"william shakespeare" title:juliet
	
Ranges
~~~~~~

The QueryParser also supports range searches on document values, matching
documents which have values within a given range. There are several types
of range processors available, but the two discussed here are Date and 
Number, which require that values are serialised as they are indexed.

To use a range, additional programming is required to tell the QueryParser
what format a range is specified in and which value is to be searched for
matches within that range. This then gives rise to the ability to specify
ranges as:

	$10..50
	5..10kg
	01/01/1970..01/03/1970
	size:3..7
	
When date ranges are configured (as a `DateValueRangeProcessor`), you can
configure which format dates are to be interpreted as (i.e. month-day-year)
or otherwise.

Stop words
~~~~~~~~~~

Xapian also supports a `stop word` list, which allows you to specify words
which should be removed from a query before processing. This stop list can
be overridden within user search, so stop words can still be searched for
if desired, for example if a stop word list contained 'the' and a search
was for:

	+the +document
	
Then the search would find relevant documents which contained both 'the' 
and 'document'.  Also, when searching for phrases, stop words do not apply,
for example:

	"the green space" retrieves documents with this exact phrase
	
Parser Flags
~~~~~~~~~~~~
The operation of the QueryParser can be altered through the use of flags,
combined with a bitwise OR operator; these flags include:

	* FLAG_BOOLEAN: enables support for AND, OR, etc and bracketed 
	  expressions
	* FLAG_PHRASE: enables support for phrase expressions
	* FLAG_LOVEHATE: enabled support for +/- operators
	* FLAG_BOOLEAN_ANY_CASE: enables support for lower/mixed case boolean 
	  operators
	* FLAG_WILDCARD: enables support for wildcards
	
By default, the QueryParser enables FLAG_BOOLEAN, FLAG_PHRASE and 
FLAG_LOVEHATE.
