.. _search-limitations:

=======================
Search-time Limitations
=======================

Document ID Range
-----------------

When searching over multiple database at once, the document ids from each
database are interleaved to produce the document ids in the combined
database, so the 32-bit document id size can hit well before you reach four
billion documents - for example, if you're searching one large database and
31 small ones, you'll reach the limit of document id size on the combined
database when the largest database reaches document id 2\ :sup:`27` (about
134 million).

Also, there may be gaps in the range of used document ids, either because
you've deleted documents, or because you're explicitly setting them to
match an external system.

Positional Queries
------------------

Currently :xapian-just-constant:`OP_PHRASE` and :xapian-just-constant:`OP_NEAR`
don't really support non-term subqueries, though simple cases get rearranged
(so for example, ``A PHRASE (B OR C)`` becomes ``(A PHRASE B) OR (A PHRASE
C)``).

Queries which use positional information (:xapian-just-constant:`OP_PHRASE` and
:xapian-just-constant:`OP_NEAR`) can be significantly slower to process.  The
way these are implemented is to find documents which have all the necessary
terms in, and then to check if the terms fulfil the positional requirements, so
if a lot of documents contain the required terms but not in the right places, a
lot more work is required than for just doing an AND query.  This will be
improved in a future release.

Collapsing
----------

You can't perform more than one collapse operation during a search.

Concurrently Open Databases
---------------------------

If you try to search many databases concurrently, you may hit the
per-process file-descriptor limit - each chert database uses between 3 and
7 fds depending which tables are present, and a process can only open a
certain number (on Linux, the default is usually 1024, so that limits you
to a few hundred concurrently open databases).  You can `raise the
per-process limit <https://wiki.debian.org/Limits>`_ on some Unix-like
platforms, though you may need to be root to do so; if you're doing this
from a service (for instance if you're using a :doc:`remote backend
</advanced/remote>`) then you may need to do this `via a limit stanza
for upstart <http://upstart.ubuntu.com/wiki/Stanzas#limit>`_, or `the
LimitNOFILE= option for systemd
<https://www.freedesktop.org/software/systemd/man/systemd.exec.html#LimitCPU=>`_.

You can also address this issue (and spread the search load) by using the
remote backend to search databases on a cluster of machines - the remote
backend only uses one fd per database on the client machine.
