Index limitations
=================

.. FIXME: add more and fill out those already here a little more

Document IDs are (currently) 32-bit which limits you to 2\ :sup:`32`-1
(nearly 4.3 billion) documents in a database.  Document IDs for deleted
documents aren't reused for when automatically assigning a new document ID,
so this limit also includes documents you've deleted.  You can effectively
reclaim such no-longer-used document IDs by compacting the database.

The B-trees use a 32-bit unsigned block count.  The default blocksize is
8KB which limits you to 32TB tables.  You can increase the blocksize if
this is a problem, but it's best to do it before you create the database as
otherwise you need to use xapian-compact to make a compacted copy of the
database with the new blocksize, and that will take a while for such a
large database.  The maximum blocksize currently allowed is 64K, which
limits you to 256TB tables.

Any operating or filing system limit on file size obviously applies to
Xapian.  On modern platforms, you're unlikely to hit these limits (e.g. on
Linux, ext4 allows files up to 16TB and filesystems up to 1EB, while btrfs
allows files and filesystems up to 16EB (figures from Wikipedia).

Chert stores the total length (i.e. number of terms) of all the documents
in a database so it can calculate the average document length.  This is
currently stored as an unsigned 64-bit quantity so you're almost certain
to hit another limit first.
