The index plan
--------------
In order to index the CSV, we want to take two fields from each row, title
and description, and turn them into suitable terms. For straightforward
textual search we don't need document values.

Because we're dealing with free text, and because we know the whole dataset
is in English, we can use stemming so that for instance searching for
"sundial" and "sundials" will both match the same documents. This way
people don't need to worry too much about exactly which words to use in
their query.

Finally, we want a way of separating the two fields. In Xapian this is done
using `term prefixes`, basically by putting short strings at the beginning
of terms to indicate which field the term indexes. As well as prefixed
terms, we also want to generate unprefixed terms, so that as well as
searching within fields you can also search for text in any field.

There are some conventional prefixes used, which is helpful if you ever need to
interoperate with omega (a web-based search engine) or other compatible
systems. From this, we'll use 'S' to prefix title (it stands for 'subject'), and
for description we'll use 'XD'. A full list of conventional prefixes is given at
the top of the `omega documentation on termprefixes`_.

.. _omega documentation on termprefixes: https://xapian.org/docs/omega/termprefixes

When you're indexing multiple fields like this, the term positions used for
each field when indexed unprefixed need to be kept apart. Say you have a
title of "The Saints", and description "Don't like rabbits? Keep reading."
If you index those fields without a gap, the phrase search "Saints don't
like rabbits" will match, where it really shouldn't. Usually a gap of 100
between each field is enough.

To write to a database, we use the WritableDatabase class, which allows us
to create, update or overwrite a database.

To create terms, we use Xapian's TermGenerator, a built-in class to make
turning free text into terms easier. It will split into words, apply
stemming, and then add term prefixes as needed. It can also take care of
term positions, including the gap between different fields.
