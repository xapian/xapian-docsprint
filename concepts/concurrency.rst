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
- for example, if you call :xapian-method:`Database::get-document()`, the
resulting :xapian-class:`Document` object will keep a reference to the
:xapian-class:`Database` object, and so it isn't safe to use them in different
threads concurrently.

If you want to access a Xapian object, from multiple threads then you
need to ensure that it won't be accessed concurrently - for example, by
using a mutex.  If you fail to do this, bad things are likely to happen -
for example crashes or even data corruption.  
