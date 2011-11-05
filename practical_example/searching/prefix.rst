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
in the search query relate to those in the index::

    queryparser.add_prefix("title", "S")
    queryparser.add_prefix("description", "XD")

This allows us to perform a search based on either field, for example::

	python search1.py db title:sunwatch
	1: #001 Ansonia Sunwatch (pocket compas dial)
	INFO:xapian.search:'title:sunwatch'[0:10] = 1

We can also combine prefixes with of the logical operators to perform more
complex queries::

	$ python search1.py db description:"silver case" AND title:sundial
	1: #055 Silver altitude sundial in leather case
	2: #073 Universal pocket sundial
	3: #084 Magnetic sundial in brass case
	4: #074 Sundial, made as a locket, gilt metal, part silver
	INFO:xapian.search:'description:silver case AND title:sundial'[0:10] = 55 73 84 74
