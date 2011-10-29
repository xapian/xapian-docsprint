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
using `term prefixes`, basically by putting short strings at the beginning
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

Let's write some code
---------------------

We need some code here. code/python/index1.py has it.

Verifying the index using delve
-------------------------------

Xapian comes with a handy utility called `delve` which can be used to inspect a database, so let's look at the one you just built. If you just run ``delve db``, you'll get an overview: how many documents, average term length, and some other statistics::

    $ delve db
    UUID = 4ab88abe-4fd1-42b5-9eeb-4c705d42dac7
    number of documents = 99
    average document length = 100.495
    document length lower bound = 33
    document length upper bound = 251
    highest document id ever used = 99
    has positional information = true

You can also look at an individual document, using Xapian's docid (``-d`` means output document data as well)::

    $ delve -r 1 -d db
    Data for record #1:
    {"MEASUREMENTS": "", "DESCRIPTION": "Ansonia Sunwatch (pocket compass dial)", "PLACE_MADE": "New York county, New York state, United States", "id_NUMBER": "1974-100", "WHOLE_PART": "WHOLE", "TITLE": "Ansonia Sunwatch (pocket compass dial)", "DATE_MADE": "1922-1939", "COLLECTION": "SCM - Time Measurement", "ITEM_NAME": "Pocket horizontal sundial", "MATERIALS": "", "MAKER": "Ansonia Clock Co."}
    Term List for record #1: Q1974-100 Sansonia Scompass Sdial Spocket Ssunwatch XDansonia XDcompass XDdial XDpocket XDsunwatch ZSansonia ZScompass ZSdial ZSpocket ZSsunwatch ZXDansonia ZXDcompass ZXDdial ZXDpocket ZXDsunwatch Zansonia Zcompass Zdial Zpocket Zsunwatch ansonia compass dial pocket sunwatch

You can also go the other way, starting with a term and finding both statistics and which documents it indexes::

    $ delve -t Scompass db
    Posting List for term `Scompass' (termfreq 5, collfreq 5, wdf_max 5): 1 26 28 29 70

This means you can look documents up by identifier::

    $ delve -t Q1974-100 db
    Posting List for term `Q1974-100' (termfreq 1, collfreq 1, wdf_max 1): 1

``delve`` is frequently useful if you aren't getting the behaviour you
expect from a search system, to check that the database contains the
documents and terms you expect.

