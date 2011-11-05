Facets
======

Xapian provides functionality which allows you to dynamically generate 
complete lists of values which feature in matching documents. For example,
colour, manufacturer, size values are good candidates for faceting.

There are numerous potential uses this can be put to, but a common one is 
to offer the user the ability to narrow down their search by filtering it 
to only include documents with a particular value of a particular category. 
This is often referred to as `faceted search`.

Limitations
===========
The accuracy of Xapian's faceting capability is determined by the number
of records that are examined by Xapian whilst it is searching. You can 
control this number by specifying the `checkatleast` value of `get_mset`; 
however it is important to be aware that increasing this number may have an
effect on overall query performance.


Implementation
==============
Faceting works against information stored in document value slots [link to
value slots] and, when executed, provides a list of the unique values for
that slot together with a count of the number of times each value occurs. 

Indexing
--------
No additional work is needed to implement faceted searching, except to 
ensure that the values you wish to use in facets are stored in value slots.

Querying
--------
To add a spy you need to create a new `XapianValueCountMatchSpy` object,
stating which value slot the spy is to operate on and add this to the 
`XapianEnquire` as follows::

.. literalinclude:: /code/python/index_facets.py		
	
The results of the spy can then be output in the same way as the matches
are displayed: by looping through the output::

.. literalinclude:: /code/python/index_facets.py		

Restricting by Facets
---------------------
If you're using the facets to offer the user choices for narrowing down 
their search results, you then need to be able to apply a suitable filter.

For a single value, you could use `Xapian::Query::OP_VALUE_RANGE` with the 
same start and end, or `Xapian::MatchDecider`, but it's probably most 
efficient to also index the categories as suitably prefixed boolean terms 
and use those for filtering.


In Development
==============
Some additional features currently in development may benefit users of 
facets. These are:

	* Values in slots: this will allow you to have a single value slot 
		(e.g. colour) which contains multiple values (e.g. red, blue). 
		This will also allow you to create a facet by colour which is aware
		of these multiple values, giving counts for both red and blue.
		
		
	* Bucketing: this provides a means to group togethernumeric facets, so
	that a single facet can contain a range of values (e.g. price ranges).
