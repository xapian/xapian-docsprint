Terms
=====

`Terms` are the basis of most searches in Xapian.  At its simplest, a
search is a process of comparing the terms specified in a query against the
terms in each document, and returning a list of the documents which match
the best.

A term will often be generated for each word in a piece of text, usually
by applying some form of normalisation (it's usual to at least change all
the characters to be lowercase).  There are many useful strategies for
producing terms.

Often the same word will occur multiple times in a piece of text.  Xapian
calls this number the `within document frequency` and stores it in the
database.  It is often used when searching to give documents in which a
term occurs more often a higher weight.

It is also possible to store a set of positions along with each term; this
allows the positions at which words occur to be used when searching, e.g.,
in a phrase query.  These positions are usually stored as word counts
(rather than character or byte counts).

The database also keeps track of a couple of statistics about the frequency
of terms in the database; the `term frequency` is the number of documents
that a particular term occurs in,  and the `collection frequency` is the
total number of times that term occurs (i.e., the sum of the within
document frequencies for the term).

Stemmers
--------

A common form of normalisation is `stemming`.  This process converts
various different forms of words to a single form: for example, converting
a plural (e.g., "birds") and a singular form of a word ("bird") to the same
thing (in this case, both are converted to "bird").

Note that the output of a stemmer is not necessarily a valid word; what is
important is that words with closely related meaning are converted to the
same form, allowing a search to find them.  For example, both the word
"happy" and the word "happiness" are converted to the form "happi", so if a
document contained "happiness", a search for "happy" would find that
document.

The rules applied by a stemmer are dependent on the language of the text;
Xapian includes stemmers for more than a dozen languages (and for some
languages there is a choice of stemmers).
