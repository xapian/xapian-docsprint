Terms
=====

`Terms` are the basic unit of information retrieval used by Xapian.  At its
simplest, a search is a process of matching terms specified in a query
against terms in a document, and returning the best matches. A term will
often be generated for each word in a piece of text, possibly by applying
some form of normalisation, but this isn't required, and
there is a very wide range of useful strategies for producing terms.

In a piece of text, it is common for an individual word to occur multiple
times.  To represent this, a document stores a "within document frequency"
along with each term, indicating the number of times the term occurred in a
document; this is often used when searching to give documents in which a
term occurs more often a higher weight.

It is also possible to store a set of positions along with each term; this
allows the positions at which the words occured to be used when searching,
eg, in a phrase query.  It is usual for the positions used here to be a
word count (rather than a character or byte count).

Stemmers
--------

A common form of normalisation is `stemming`.  This process converts
various different forms of words to a single form: for example, converting
a plural (eg, "birds") and a singular form of a word ("bird") to the same
thing (in this case, both are converted to "bird").

Note that the output of a stemmer is not necessarily a valid word; what is
important is that words with closely related meaning are converted to the
same form, allowing a search to find them.  For example, both the word
"happy" and the word "happiness" are converted to the form "happi", so if a
document contained "happiness", a search for "happy" would find that
document.

The rules applied by a stemmer are dependent on the language of the text;
Xapian includes stemmers for a variety of languages.
