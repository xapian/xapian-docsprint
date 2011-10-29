Ranked matches
==============

When you run a Query using Xapian, what you get is a list of _ranked_
_matches_.

Each match is a Xapian Document which satisfies the Query, with a
_weight_, and the list is ordered by decreasing weight, the weight
being an indicator of how good a match that Document is for the query
that was run: a higher weight means a better match. The _rank_ of each
match is simply the position in the list of all matches, starting from
0.

The actual weight is calculated by a _weight scheme_; Xapian comes
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
for 10 matches, the second page starting at 11 for 10 matches, and so
on.

A page of matches in Xapian is called an MSet (for "match set").
