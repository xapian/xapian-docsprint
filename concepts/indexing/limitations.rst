.. _index-limitations:

=================
Index limitations
=================

There are a few limitations on the data which can be stored in an index;
these rarely get in the way, and are generally easy to work around if they
do, but it's worth knowing about them.

Term length
-----------

Terms are limited to 245 bytes in length (at least with the "glass" and
"chert" backends), but each zero byte in a term is currently internally encoded
as two bytes, so the limit is less for a term which contains zero bytes.
It's rarely useful to have longer terms, but one situation where it can be
is if you're using something like a URL as an ID term; `there is some
discussion of this as one of our FAQs
<https://trac.xapian.org/wiki/FAQ/UniqueIds>`_.

Document data length
--------------------

The document data has a length limit which depends on the blocksize and
some other factors, but with the default block size of 8KB, the document
data length limit will be somewhere over 100MB.

Document value length
---------------------

Document values are limited in length to a similar length to document
data, but for performance reasons you probably wouldn't want to store
document values longer than a few tens of bytes, as reading multiple
100MB+ values during the match would be rather slow.

Document ID
-----------

Document IDs are (currently) 32-bit by default which limits you to
2\ :sup:`32`-1 (nearly 4.3 billion) documents in a database.  Document IDs for
deleted documents aren't reused for when automatically assigning a new document
ID, so this limit also includes documents you've deleted.  You can effectively
reclaim such no-longer-used document IDs by compacting the database.

If you configure xapian-core with `--enable-64bit-docid` then 64-bit docids
will be used instead.  You may well also want to make termcounts 64-bit
with `--enabl-64bit-termcount`.  Note that these options change type sizes and
hence the ABI of the library.

B-tree block number
-------------------

The B-trees use a 32-bit unsigned block count.  The default blocksize is
8KB which limits you to 32TB tables.  You can increase the blocksize if
this is a problem, but it's best to do it before you create the database as
otherwise you need to use xapian-compact to make a compacted copy of the
database with the new blocksize, and that will take a while for such a
large database.  The maximum blocksize currently allowed is 64K, which
limits you to 256TB tables.

OS file size
------------

Any operating or filing system limit on file size obviously applies to
Xapian.  On modern platforms, you're unlikely to hit these limits (e.g. on
Linux, `ext4`_ allows files up to 16TB and filesystems up to 1EB, while `btrfs`_
allows files and filesystems up to 16EB (figures from Wikipedia).

.. _ext4: https://en.wikipedia.org/wiki/Ext4

.. _btrfs: https://en.wikipedia.org/wiki/Btrfs

Total document length limit
---------------------------
Glass stores the total length (i.e. number of terms) of all the documents
in a database so it can calculate the average document length.  This is
currently stored as an unsigned 64-bit quantity so you're almost certain
to hit another limit first.
