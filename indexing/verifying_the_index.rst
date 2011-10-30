Verifying the index using delve
-------------------------------

Xapian comes with a handy utility called `delve` which can be used to 
inspect a database, so let's look at the one you just built. If you just 
run ``delve db``, you'll get an overview: how many documents, average term 
length, and some other statistics::

    $ delve db
    UUID = 1820ef0a-055b-4946-ae73-67aa4ef5c226
    number of documents = 100
    average document length = 78.18
    document length lower bound = 25
    document length upper bound = 153
    highest document id ever used = 100
    has positional information = true

You can also look at an individual document, using Xapian's docid (``-d`` 
means output document data as well)::

    $ delve -r 1 -d db		# output has been reformatted
    Data for record #1:
    {
     "MEASUREMENTS": "", 
     "DESCRIPTION": "Ansonia Sunwatch (pocket compass dial)", 
     "PLACE_MADE": "New York county, New York state, United States", 
	 "id_NUMBER": "1974-100", 
	 "WHOLE_PART": "WHOLE", 
	 "TITLE": "Ansonia Sunwatch (pocket compass dial)", 
	 "DATE_MADE": "1922-1939", 
	 "COLLECTION": "SCM - Time Measurement", 
	 "ITEM_NAME": "Pocket horizontal sundial", 
	 "MATERIALS": "", 
	 "MAKER": "Ansonia Clock Co."
	}
    Term List for record #1: Q1974-100 Sansonia Scompass Sdial Spocket 
    Ssunwatch XDansonia XDcompass XDdial XDpocket XDsunwatch ZSansonia 
    ZScompass ZSdial ZSpocket ZSsunwatch ZXDansonia ZXDcompass ZXDdial 
    ZXDpocket ZXDsunwatch Zansonia Zcompass Zdial Zpocket Zsunwatch 
    ansonia compass dial pocket sunwatch

You can also go the other way, starting with a term and finding both 
statistics and which documents it indexes::

    $ delve -t Sattitude db
    Posting List for term `Sattitude' (termfreq 3, collfreq 3, wdf_max 3): 
    64 65 97

This means you can look documents up by identifier::

    $ delve -t Q1974-100 db
    Posting List for term `Q1974-100' (termfreq 1, collfreq 1, wdf_max 1): 
    1

``delve`` is frequently useful if you aren't getting the behaviour you
expect from a search system, to check that the database contains the
documents and terms you expect.
