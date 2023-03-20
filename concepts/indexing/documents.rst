Documents
=========

A document in Xapian is simply an item which is returned by a search.  When
building a new search system, a key thing to decide is what the documents
in your system are going to be.  There's often an obvious choice here, but
in many cases there are alternatives.  For example, for a search over a
website, it seems natural to have one document for each page of the site.
However, you could instead choose to use one document for each paragraph of
each page, or to group pages together into subjects and have one document
for each subject.

Documents are identified in a database by a unique positive integer id,
known as the `document ID`.  Currently this is a 32-bit quantity by
default (you can configure xapian-core with ``--enable-64bit-docid``
to get 64-bit docids).

Documents have three components: `data`, `terms` and `values`.  We'll
discuss terms and data first - values are useful for some more advanced
search types.

Document Data
-------------

The `document data` is an arbitrary binary blob of data associated with the
document.  Xapian treats this as completely opaque, and does nothing with
this data other than storing it in the database (compressed with zlib if it
is compressible) and returning it when requested.

It can be used to hold a reference to the document elsewhere (such as the
primary key in an external database table), or could be used to store the
full text of the document.

Generally you use the document data to store any information you need in order
to display the resulting document to the user (or to whatever process consumes
the results of searches).  Xapian doesn't enforce a serialisation scheme for
putting structured information into the document data, so you can use whatever
is most appropriate for your application.

Protocol buffers are often a good choice - there's support for them for most
programming languages, they use a compact representation which doesn't
explicitly store the field names, and you can add new fields without
invalidating existing encoded data.

Some other possible options are a simple scheme using newlines to separate
``name=value`` entries (like Omega uses), JSON, XML, or a language-specific
serialisation such as ``pickle`` in Python.

.. todo:: Talk about the importance of batching changes where feasible
