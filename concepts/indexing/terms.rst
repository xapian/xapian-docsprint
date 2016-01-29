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
database.  It is often useful when searching to give documents in which a
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
Xapian includes `stemmers for more than a dozen languages <https://xapian.org/docs/apidoc/html/classXapian_1_1Stem.html>`_
(and for some languages there is a choice of stemmers), built using the
`Snowball language <http://snowballstem.org/>`_. We'd like to add
stemmers for more languages - see the Snowball site for information on how
to contribute.

.. _term-prefixes:

Fields and term prefixes
------------------------

It's common to think of a document as consisting, rather than just a single
quantity of text, of a number of *fields*, each of which itself is made up
of terms. These could be actual fields from a structured document, such as
the title, or they could be metadata such as colour of fruit
(so you could search for only red fruit). The first allows normal free text
searching, but constrained to a particular field -- perhaps you want to
search for all documents whose author is called "Sam"; the second can be used
for :doc:`filtering documents </howtos/boolean_filters>`, a technique
referred to as *boolean filtering* (and hence those prefixed terms are called
*boolean terms*).

Xapian supports a convention for representing fields in the database by
mapping each field to a *term prefix*, which are one or more capital letters;
this is to avoid confusion
(which could adversely affect search results) with normal terms generated
from words, which are lowercased by the :doc:`/concepts/indexing/termgenerator`.
(If you need a capital letter after the prefix of your term, you can separate
it from the prefix using a colon ':'.)

When using the :doc:`/concepts/search/queryparser`, you can map from "human
understandable" prefixes (which act as field names) in the query to the term
prefixes used in the database, and you can specify a default prefix to control
any parts of the query that don't specify a field.
You can map one field name to multiple term prefixes, so if you want to search
across multiple fields by default, instead of setting a default prefix you can
map an empty field name to several term prefixes.

Xapian has `conventions for term prefixes
<https://xapian.org/docs/omega/termprefixes.html>`_ used for common fields,
which originally came from Omega. For instance, 'A' is used for author, 'S'
for subject/title, and so forth.
