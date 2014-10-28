Building the search
-------------------

Now we have our database populated with some values, it is time for
the code to search the database and display some results.

We want to take some text from the user, and search for it in the
database; to do that we need to convert it into a Xapian Query, which
you will recall is a tree made up of terms (which in this case will be
the stemmed forms of words in the text from the user), and operations
such as AND, OR and so forth.

There are many ways to go from the user's text to a Query, but the
most simple of these is to use the QueryParser. We then pass the Query
to an Enquire object, which also needs setting up with a database, and
is where you'd set various other options that affect how the query is
run (such as sorting, for instance) which we won't address here.

.. xapianexample:: search1

A full copy of this code is available in :xapian-code-example:`^`.
