Running a Search
----------------
To search the database we've built, you just run our simple search engine:

.. xapianrunexample:: index1
    :silent:
    :args: data/ch-objects.csv db

.. xapianrunexample:: search1
    :args: db sketch

These results show that 4 documents match our search for the term
'sketch', providing the document ID (such as #003) and title for each.
If you want to search for multiple words, just chain them together on
the command line:

.. xapianrunexample:: search1
    :args: db sketch cotton

You'll notice that all of the results from the first time come back
the second time also, with additional ones (which match 'cotton' but
not 'sketch'), because by default QueryParser will use the OR operator
to combine the different search terms. Also, because #075 contains
both 'sketch' and 'cotton', it now ranks highest of all the matches.
