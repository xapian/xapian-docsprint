Using external identifiers with Xapian
======================================

Often the documents which you're indexing with Xapian will already have
unique ids which you want to be able to use to reindex an updated version
of an existing document, or delete an expired document from the Xapian
index. There are two ways of approaching this.

One is to use a one-to-one mapping between your identifiers and Xapian
docids. This will work if your identifiers positive integers and they all
fit within 32 bits (under about 4 billion).

The other is to use a special term containing your identifier, which will
work for any type of identifier, of any size. Typically you will prefix
this, by convention with 'Q', so it can't be confused with other
terms. Terms have a limit of 245 bytes, so longer identifiers will need to
be split into multiple terms (perhaps 'Q1...', 'Q2...' and so on).

For more information on both techniques, see our FAQ on this:
<http://trac.xapian.org/wiki/FAQ/UniqueIds>.
