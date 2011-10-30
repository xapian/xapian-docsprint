Ranked matches
==============

When you run a Query using Xapian, what you get is a list of `ranked`
`matches`.

Each match is a Xapian Document which satisfies the Query, with a
`weight`, and the list is ordered by decreasing weight, the weight
being an indicator of how good a match that Document is for the query
that was run: a higher weight means a better match. The `rank` of each
match is simply the position in the list of all matches, starting from
0.  Some other search systems use the word "score" instead of weight.

The actual weight is calculated by a `weighting scheme`; Xapian comes
with a few different ones or you can write your own, although often
the default is fine. (It uses a scheme called BM25, which takes into
account things like how common a matching term is in a matching
document compared to in the entire database, and the lengths of
different matching documents.)

Rather than having to run through the entire list of matches from the
beginning, you actually ask for a sub-range of the entire list of
matches, from an offset and extending for a given number of
matches. Many search applications will provide the user with a way of
"paging" through the matches, so the first page might be starting at 0
for 10 matches, the second page starting at 10 for 10 matches, and so
on.

A page of matches in Xapian is called an MSet (for "match set").

Alternative sort orders
-----------------------

Sometimes, rather than getting results sorted by `weight`, it would be more
useful to get them in some other order.  For example, it might be desirable
to get results in order of the values stored in a date field.

To do this, you first need to store the information used for the sort in a
value slot, as described in the indexing documentation.  You can then tell
Xapian at search time to sort by the value in that slot.  It is also
possible to sort by the values in several slots (e.g., to sort items which
have the same value in a particular slot by the value in a secondary slot).

Finally, it is possible to ask Xapian to return the documents in order of
the Xapian document ID numbers.
