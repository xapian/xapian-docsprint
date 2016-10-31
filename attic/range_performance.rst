Performance of Value Ranges
===========================

If combined with a suitable term-based query (such as an `OP_AND`
query over one or more terms), this performance impact will be less
because the range operation will only have to run over the potential
matches, which are reduced from the entire database by the term-based
query.

If, as well as using document values, you also convert groups of those
values into terms, you can provide those term-based queries even when
your users are only interested in a pure range search. For instance,
consider the population information. If you divide the range of
populations into a number of subranges, you can allocate a term to
describe each. We'll use a prefix of `XP` (for "population") here.

+------------------+------+
| Population range | Term |
+==================+======+
| 0 - 10 million   | XP0  |
+------------------+------+
| 10 - 20 million  | XP1  |
+------------------+------+
| 20 - 30 million  | XP2  |
+------------------+------+
| 30 - 40 million  | XP3  |
+------------------+------+

Then you can use a custom :xapian-class:`RangeProcessor` to produce a
query which uses :xapian-just-constant:`OP_VALUE_RANGE` to match the
range exactly, but first limits the number of documents that this
needs to consider use the filter terms above.  For instance, if the user asks
for '..15000000', you can use :xapian-just-constant:`OP_FILTER` to limit
the value range subquery to only considering documents matching a
:xapian-just-constant:`OP_AND` subquery with terms `XP0` and `XP1`.

.. todo:: possibly implementing this example would help make it more clear.

.. todo:: Now ticket #663 <https://trac.xapian.org/ticket/663> is done and
          we have RangeProcessor, we can move this to advanced and the range
          queries howto should point here.
