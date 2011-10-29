Search-time Limitations
=======================

Document ID Range
-----------------

When searching over multiple database at once, the document ids from each
database are interleaved to produce the document ids in the combined database,
so the 32-bit document id size can hit well before you reach four billion
documents - for example, if you're searching one large database and 31 small
ones, you'll reach the limit of document id size on the combined database
when the largest database reaches document id 2\ :sup:`27` (about 134 million).

Also, there may be gaps in the range of used document ids, either because
you've deleted documents, or because you're explicitly setting them to match
an external system.

Collapsing
----------

You can't perform more than one collapse operation during a search.

Positional Queries
------------------

Queries which use positional information (``OP_PHRASE`` and ``OP_NEAR``)
can be significantly slower to process.  <FIXME: explain why>

Currently ``OP_PHRASE`` and ``OP_NEAR`` don't really support non-term
subqueries, though simple cases get rearranged (so ``A PHRASE (B OR C)``
becomes ``(A PHRASE B) OR (A PHRASE C)``).
