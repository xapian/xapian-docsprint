Values
======

`Values` are in a sense a more flexible version of terms. Each document can
have a set of values associated with it, which hold pieces of data which
can be useful during a search. These pieces of data could be things such as
keys which you want to be able to sort the results on, numeric values used for range searches, or numbers to be
used to affect the weight calculated for documents during the search.

It is important to keep the amount of data stored in the values to a
minimum, since the values for a large number of documents may be read
during the search, and unused information will thus slow the search down.
Developers are often tempted to use the value slots to hold information
which should really be stored in the document's data area; don't succumb to
this temptation.

.. todo:: discuss how to serialise numbers into values so they can be used for range searches, and possibly a few other types of things that might be stored.
