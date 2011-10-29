
Databases
=========

Pretty much all Xapian operations revolve around a Xapian database.  Before
performing a search, details of the documents being searched need to be put
into the database; the search process then refers to the database to determine
the best matches for a given query.  The process of putting documents into the
database is usually referred to as indexing.

The main information stored in a database is a mapping from all the words in
the documents to the list of documents those words occurred in, together with
various statistics about these occurrences. It may also store the full text, or
extracts, from the documents, so that result summaries can be displayed.
Databases can also contain additional data such as tables for spelling
correction and synonym expansion; users can even store arbitrary key-value
pairs in part of the database.

Xapian databases store data in custom formats which allow searches to be
performed extremely quickly; Xapian does not use a relational database as its
datastore.  There are several database backends; the main backend in the 1.2
release series of Xapian is called the "Chert" backend.  This stores
information in the filesystem (under a given path).  If you're familiar with
data storage structures, you might be interested to know that this backend uses
a B+-tree structure with copy-on-write, but don't worry if that doesn't mean
anything to you!

Most backend formats (and certainly the main backend format for each release)
will allow updates to be grouped into transactions, and will allow at least
some old versions of the database to be searched while new ones are being
written.

As well as the main backend, there is a "remote" database backend which allows
the database to be located on a different machine and accessed via a custom TCP
protocol.

It is possible to perform searches across multiple databases at once; Xapian
will handle merging the results together appropriately.


Documents
=========


Terms
=====


Uniqueness
==========


Values
======


Index limitations
=================
