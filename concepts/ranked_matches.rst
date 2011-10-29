Ranked matches

When you run a search using Xapian, what you get is a list of _ranked_
_matches_. Each match is a Xapian Document, with a _weight_, and the
list is ordered by decreasing weight. The rank of each match is simply
the position in the list of all matches, starting from 0.

Rather than having to run through the entire list of matches from the
beginning, you actually ask for a sub-range of the entire list of
matches, from an offset and extending for a given number of
matches. Many search applications will provide the user with a way of
"paging" through the matches, so the first page might be starting at 0
for 10 matches, the second page starting at 11 for 10 matches, and so
on.

A page of matches in Xapian is called an MSet (for "match set").
