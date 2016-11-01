Using identifiers with Xapian
=============================

Every document stored in a Xapian database has a unique positive integer
id, either assigned automatically or manually.

Often the documents which you're indexing with Xapian will already have
unique ids, and you'll want to be able to use these to reindex an updated
version of an existing document, or delete an expired document from the
Xapian index. There are two ways of approaching this.

One is to use a one-to-one mapping between your identifiers and Xapian
docids. This will work if your identifiers are positive integers and they
all fit within 32 bits (under about 4 billion), or if they are 64-bit
and you configure xapian-core with `--enable-64bit-docid`.

The other is to use a special term containing your identifier, which will
work for any type of identifier.  Typically you will prefix this (by
convention with 'Q') to avoid collisions with other terms.  Terms have a
limited length (245 bytes in glass and chert), so if your unique identifiers
are really long you'll need to do something more complicated.

For more information on both techniques, `see our FAQ on this`_.

.. _see our FAQ on this: https://trac.xapian.org/wiki/FAQ/UniqueIds
