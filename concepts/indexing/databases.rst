Databases
=========

Pretty much all Xapian operations revolve around a Xapian database.  Before
searches can be performed, details of the documents to be searched need to
be put into a database; the search process then refers to the database to
efficiently determine the best matches for a given query.  The process of
putting documents into the database is usually referred to as *indexing*.

The main information stored in a database is a mapping from each term to a
list of all the documents it occurs in, together with various statistics
about these occurrences.  It may also store the full text, or extracts,
from the documents, so that result summaries can be displayed.  Databases
can also contain additional data for spelling correction and synonym
expansion, and developers can even store arbitrary key-value pairs in part
of the database.

Xapian databases store data in custom formats which allow searches to be
performed extremely quickly; Xapian does not use a relational database as
its datastore.  There are several database backends; the main backend in
the 1.2 release series of Xapian is called the *Chert* backend.  This
stores information in the filesystem (under a given path).  If you're
familiar with data storage structures, you might be interested to know that
this backend uses a copy-on-write B+-tree structure, but don't worry if
that doesn't mean anything to you!

Most backend formats (and certainly the main backend format for each release)
will allow updates to be grouped into transactions, and will allow at least some
old versions of the database to be searched while new ones are being written.
Currently, all the backends only support a single writer existing at a given
time; attempting to open another writer on the same database will throw
``Xapian::DatabaseLockError`` to indicate that it wasn't possible to acquire a
lock.  Multiple concurrent readers are supported (in addition to the writer).

When a database is opened for reading, a fixed snapshot of the database is
referenced by the reader, (essentially `Multi-Version Concurrency Control`_).
Updates which are made to the database will not be visible to the reader unless
it calls ``Xapian::Database::reopen()``.

.. _Multi-Version Concurrency Control: http://en.wikipedia.org/wiki/Multiversion_concurrency_control

Currently Xapian's disk based backends have a limitation to their *multi-version
concurrency* implementation - specifically, at most two versions can exist
concurrently.  Therefore a reader will be able to access its snapshot of the
database without limitations when only one change has been made and committed by
the writer, but after the writer has made two changes, readers will receive a
``Xapian::DatabaseModifiedError`` if they attempt to access a part of the database
which has changed.  In this situation, the reader can be updated to the latest
version using the ``Xapian::Database::reopen()`` method.

With the disk-based Xapian backends, when a database is opened for writing,
a lock is obtained on the database to ensure that no further writers are
opened concurrently.  This lock will be released when the database writer
is closed (or automatically if the writer process dies).

One unusual feature of Xapian's locking mechanism (at least on POSIX
operating systems) is that Xapian forks a subprocess to hold the lock,
rather than holding it in the main process.  This is to avoid the lock
being accidentally released due to the slightly unhelpful semantics of
fcntl locks.

There's also a *remote* database backend which allows the database to be
located on a different machine and accessed via a custom network protocol.

It is possible to perform searches across multiple databases at once, and
Xapian will handle merging the results together appropriately.  This
feature can be combined with remote databases to handle datasets which are
too large for a single machine, by performing searches across multiple
remote databases.

Xapian also has special support for replicating databases to multiple
machines, such that only the parts of the database which have been modified
are copied; this can be useful for redundancy and load-balancing purposes.

Xapian also supports a simple text file format for listing the locations of
a set of databases (either on the local file system, or remote databases).
Such files are called *stub-databases*, and can be used to point to a
database when the physical database location may vary; for example, because
a new database is being built nightly, and is named according to the date
on which it was built.
