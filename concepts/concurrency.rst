===========
Concurrency
===========

---------
Threading
---------

Xapian does not provide explicit support for multi-threading, though it
can be used in a multi-threaded program if you are aware of the details
described below.

Xapian doesn't maintain any global state, so you can safely use Xapian in a
multi-threaded program provided you don't share objects between threads.
In practice this restriction is often not a problem - each thread can
create its own :xapian-class:`Database` object, and everything will work
fine.

If you really want to access the same Xapian object from multiple threads,
then you need to ensure that it won't ever be accessed concurrently (if you
don't ensure this bad things are likely to happen - for example crashes
or even data corruption).  One way to prevent concurrent access is to
require that a thread gets an exclusive lock on a mutex while the access is
made.

Xapian doesn't include thread locking code to avoid imposing an overhead
when it isn't needed.  And in practice the caller can often lock over
several operations, which wouldn't work if the locking code was in
Xapian itself.

Be aware that some Xapian objects will keep internal references to others
- for example, if you call :xapian-method:`Database::get_document()`, the
resulting :xapian-class:`Document` object will keep a reference to the
:xapian-class:`Database` object, and so you can't safely use the
:xapian-class:`Database` object in one thread at the same time as using the
:xapian-class:`Document` object in another.
