===========
Concurrency
===========

---------
Threading
---------

Xapian does not provide explicit support for multi-threading to avoid
imposing the overhead of thread locking when it isn't needed.

Xapian doesn't use any global state, so you can safely use Xapian in a
multi-threaded program provided you don't share objects between threads
(and in practice this restriction is often not a problem).

Be aware that some Xapian objects will keep internal references to others
- for example, if you call ``Xapian::Database::get_document()``, the
resulting ``Xapian::Document`` object will keep a reference to the
``Xapian::Database`` object, and so it isn't safe to use them in different
threads concurrently.

If you want to access a Xapian object, from multiple threads then you
need to ensure that it won't be accessed concurrently - for example, by
using a mutex.  If you fail to do this, bad things are likely to happen -
for example crashes or even data corruption.  

-------------------------------
Multiple readers, single writer
-------------------------------

Most Xapian backends provide `multi-version concurrency`.  This allows only
a single writer to exist for each database at any given time, but allows
multiple readers to exist concurrently (in addition to the writer).

When a database is opened for reading, a fixed snapshot of the database is
referenced by the reader.  Updates which are made to the database will not
be visible to the reader unless it calls ``Xapian::Database::reopen()``.

Current Xapian backends have a limitation to their `multi version
concurrency` implementation - specifically, at most two versions can exist
concurrently.  So reader will be able to access its snapshot of the
database without limitations when only one change has been made and
committed by the writer, but after the writer has made two changes, readers
will receive a `Xapian::DatabaseModifiedError` if they attempt to access a
part of the database which has changed.  In this situation, the
reader may be updated to the latest version using the `reopen()`
method.

Locking
=======

With the disk-based Xapian backends, when a database is opened for writing,
a lock is obtained on the database to ensure that no further writers are
opened concurrently.  This lock will be released when the database writer
is closed (or automatically if the writer process dies).

One unusual feature of Xapian's locking mechanism (at least on POSIX
operating systems) is that Xapian forks a subprocess to hold the lock,
rather than holding it in the main process.  This is to avoid the lock
being accidentally released due to the slightly unhelpful semantics of
fcntl locks.
