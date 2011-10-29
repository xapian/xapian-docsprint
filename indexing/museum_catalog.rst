Building a museum catalogue
===========================

We're going to build a simple search system based on museum catalogue data released under a Creative Commons license (By-NC-SA) by the Science Museum in London, UK.

http://api.sciencemuseum.org.uk/documentation/collections/

To make things easier, we've extracted just the first 100 objects and provide them as a gzipped CSV file.

What data is there?
-------------------

Each row in the CSV file is an object from the catalogue, and has a number of fields. There are:

ID_NUMBER:
    a unique identifier
ITEM_NAME:
    a simple name, often from an established thesaurus
TITLE:
    a short caption
MAKER:
    the name of who made the object
DATE_MADE:
    when the object was made, which may be a range, approximate date or unknown
PLACE_MADE:
    where the object was made
MATERIALS:
    what the object is made of
MEASUREMENTS:
    the dimensions of the object
DESCRIPTION
    a description of the object
COLLECTION:
    the collection the object came from (eg: Science Museum - Space Technology)

There are obviously a number of different types of data here: free text,
identifiers, dates, places (which could be geocoded to geo coordinates),
and dimensions. Additionally, COLLECTION and MAKER both come from a list of
possible values.

What do people want to search for?
----------------------------------

We can think of a large number of different things that people might want
to find from our catalogue. For instance, they may want to find objects
that were created in Nantes, or after 1812, or by Hurd-Brown Ltd. They may
want to find everything made of brass, or not containing wood, or more than
a metre in length. They may care only about objects in the National Railway
Museum, or in their Railway Heraldry collection, or everything not in the
Railway Heraldry collection. And of course they may want to look up objects
that have certain words or phrases in the title or description - "free text
search", one of the most common uses of search today.

In order to support all of this we'll need to use many of the features of
Xapian, but to get started we'll just look at one: free text search of the
title and description.

In later sections of this guide (if we ever write them), and in guides to
do specific things (if we ever convert them) we'll use the same data and
build on the system we create here.

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
using _term prefixes_, basically by putting short strings at the beginning
of terms to indicate which field the term indexes. As well as prefixed
terms, we also want to generate unprefixed terms, so that as well as
searching within fields you can also search for text in any field.

There are some conventional prefixes used, which is helpful if you ever
need to interoperate with omega (a web-based search engine) or other
compatible systems. From this, we'll use 'S' to prefix title (it stands for
'subject'), and for description we'll use 'XD'.

When you're indexing multiple fields like this, the term positions used for
each field when indexed unprefixed need to be kept apart. Say you have a
title of "The Saints", and description "Don't like rabbits? Keep reading."
If you index those fields without a gap, the phrase search "Saints don't
like rabbits" will match, where it really shoudn't. Usually a gap of 100
between each field is enough.

To create terms, we use Xapian's TermGenerator, a built-in class to make
turning free text into terms easier. It will split into words, apply
stemming, and then add term prefixes as needed. It can also take care of
term positions, including the gap between different fields.
