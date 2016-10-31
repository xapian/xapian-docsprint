Verifying the index using xapian-delve
--------------------------------------

Xapian comes with a handy utility called `xapian-delve` which can be used to
inspect a database, so let's look at the one you just built. If you just
pass a database path as a parameter you'll get an overview: how many documents,
average term length, and some other statistics:

.. code-block:: none

    $ xapian-delve db
    UUID = 1820ef0a-055b-4946-ae73-67aa4ef5c226
    number of documents = 100
    average document length = 100.58
    document length lower bound = 33
    document length upper bound = 251
    highest document id ever used = 100
    has positional information = true

You can also look at an individual document, using Xapian's docid (``-d``
means output document data as well):

.. code-block:: none

    $ xapian-delve -r 1 -d db       # output has been reformatted
    Data for record #1:
    {
     "MEASUREMENTS": "",
     "DESCRIPTION": "Ansonia Sunwatch (pocket compas dial)",
     "PLACE_MADE": "New York county, New York state, United States",
     "id_NUMBER": "1974-100",
     "WHOLE_PART": "WHOLE",
     "TITLE": "Ansonia Sunwatch (pocket compas dial)",
     "DATE_MADE": "1922-1939",
     "COLLECTION": "SCM - Time Measurement",
     "ITEM_NAME": "Pocket horizontal sundial",
     "MATERIALS": "",
     "MAKER": "Ansonia Clock Co."
    }
    Term List for record #1: Q1974-100 Sansonia Scompas Sdial Spocket
    Ssunwatch XDansonia XDcompass XDdial XDpocket XDsunwatch ZSansonia
    ZScompas ZSdial ZSpocket ZSsunwatch ZXDansonia ZXDcompas ZXDdial
    ZXDpocket ZXDsunwatch Zansonia Zcompass Zdial Zpocket Zsunwatch
    ansonia compass dial pocket sunwatch

You can also go the other way, starting with a term and finding both
statistics and which documents it indexes:

.. code-block:: none

    $ xapian-delve -t Stime db
    Posting List for term `Stime' (termfreq 4, collfreq 4, wdf_max 4):
    41 56 58 65

This means you can look documents up by identifier:

.. code-block:: none

    $ xapian-delve -t Q1974-100 db
    Posting List for term `Q1974-100' (termfreq 1, collfreq 1, wdf_max 1):
    1

``xapian-delve`` is frequently useful if you aren't getting the behaviour you
expect from a search system, to check that the database contains the
documents and terms you expect.
